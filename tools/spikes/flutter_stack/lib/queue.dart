// Synthetic P0 fixture. No network, payment or production authorization.
import 'package:drift/drift.dart' hide JsonKey;
import 'package:freezed_annotation/freezed_annotation.dart';

part 'queue.g.dart';
part 'queue.freezed.dart';

@freezed
sealed class Receipt with _$Receipt {
  const factory Receipt.accepted(int version) = Accepted;
  const factory Receipt.rejected(String reason) = Rejected;
}

class PendingCommands extends Table {
  TextColumn get account => text()();
  TextColumn get commandKey => text()();
  TextColumn get action => text()();
  TextColumn get payload => text()();
  IntColumn get expectedVersion => integer()();
  TextColumn get state => text().withDefault(const Constant('PENDING'))();
  TextColumn get reason => text().nullable()();
  IntColumn get acceptedVersion => integer().nullable()();

  @override
  Set<Column> get primaryKey => {account, commandKey};
}

@DriftDatabase(tables: [PendingCommands])
class ProbeDatabase extends _$ProbeDatabase {
  ProbeDatabase(super.executor);

  @override
  int get schemaVersion => 1;

  // Deliberately narrow allowlist: financial actions cannot enter the queue.
  static const allowed = {'check_in', 'check_out', 'record_pickup'};

  Future<void> enqueue({
    required String account,
    required String key,
    required String action,
    required String payload,
    required int expectedVersion,
  }) async {
    if (!allowed.contains(action) ||
        account.isEmpty ||
        key.isEmpty ||
        expectedVersion < 0) {
      throw ArgumentError('Invalid offline field command');
    }
    await transaction(() async {
      final existing = await command(account, key);
      if (existing != null) {
        if (existing.action != action ||
            existing.payload != payload ||
            existing.expectedVersion != expectedVersion) {
          throw StateError('Idempotency key reused with different command');
        }
        return;
      }
      await into(pendingCommands).insert(
        PendingCommandsCompanion.insert(
          account: account,
          commandKey: key,
          action: action,
          payload: payload,
          expectedVersion: expectedVersion,
        ),
      );
    });
  }

  Future<PendingCommand?> command(String account, String key) =>
      (select(
            pendingCommands,
          )..where((t) => t.account.equals(account) & t.commandKey.equals(key)))
          .getSingleOrNull();

  Future<List<PendingCommand>> pending(String account) => (select(
    pendingCommands,
  )..where((t) => t.account.equals(account) & t.state.equals('PENDING'))).get();

  Future<void> receive(
    String account,
    String key,
    Receipt receipt,
  ) => transaction(() async {
    final existing = await command(account, key);
    if (existing == null) throw StateError('Unknown account-scoped command');
    final nextState = receipt is Accepted ? 'ACKED' : 'REJECTED';
    final nextVersion = receipt is Accepted ? receipt.version : null;
    final nextReason = receipt is Rejected ? receipt.reason : null;
    if (nextVersion != null && nextVersion <= existing.expectedVersion) {
      throw StateError('Receipt does not advance aggregate version');
    }
    if (existing.state != 'PENDING') {
      if (existing.state != nextState ||
          existing.acceptedVersion != nextVersion ||
          existing.reason != nextReason) {
        throw StateError('Conflicting terminal receipt');
      }
      return;
    }
    await (update(pendingCommands)
          ..where((t) => t.account.equals(account) & t.commandKey.equals(key)))
        .write(
          PendingCommandsCompanion(
            state: Value(nextState),
            acceptedVersion: Value(nextVersion),
            reason: Value(nextReason),
          ),
        );
  });

  // Fixture for logout/revocation erasure; production needs reviewed retention rules.
  Future<int> clearAccount(String account) =>
      (delete(pendingCommands)..where((t) => t.account.equals(account))).go();
}
