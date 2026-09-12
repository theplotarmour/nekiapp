import 'dart:ffi';
import 'dart:io';
import 'package:drift/native.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sqlite3/open.dart';
import 'package:neki_stack_spike/queue.dart';

void main() {
  // Windows system SQLite for this local probe only. Mobile packaging is untested.
  if (Platform.isWindows) {
    open.overrideFor(
      OperatingSystem.windows,
      () => DynamicLibrary.open('winsqlite3.dll'),
    );
  }
  late Directory directory;
  late File file;
  late ProbeDatabase db;
  setUp(() async {
    directory = await Directory.systemTemp.createTemp('neki-stack-');
    file = File('${directory.path}/probe.sqlite');
    db = ProbeDatabase(NativeDatabase(file));
  });
  tearDown(() async {
    await db.close();
    await directory.delete(recursive: true);
  });
  Future<void> enqueue({
    String account = 'account-a',
    String key = 'key-1',
    String action = 'check_in',
    String payload = 'fixture',
  }) => db.enqueue(
    account: account,
    key: key,
    action: action,
    payload: payload,
    expectedVersion: 1,
  );

  test('pending command survives database close and reopen', () async {
    await enqueue();
    await db.close();
    db = ProbeDatabase(NativeDatabase(file));
    expect((await db.pending('account-a')).single.state, 'PENDING');
  });
  test('same key retry persists only one command', () async {
    await Future.wait([enqueue(), enqueue()]);
    expect(await db.pending('account-a'), hasLength(1));
  });
  test(
    'same key with changed payload is rejected without overwriting',
    () async {
      await enqueue();
      await expectLater(enqueue(payload: 'changed'), throwsStateError);
      expect((await db.command('account-a', 'key-1'))!.payload, 'fixture');
    },
  );
  test('financial operations cannot be queued', () async {
    for (final action in [
      'create_contribution',
      'approve_payout',
      'request_refund',
    ]) {
      await expectLater(enqueue(action: action), throwsArgumentError);
    }
    expect(await db.pending('account-a'), isEmpty);
  });
  test(
    'only account-scoped accepted receipt acknowledges the command',
    () async {
      await enqueue();
      await expectLater(
        db.receive('account-b', 'key-1', const Receipt.accepted(2)),
        throwsStateError,
      );
      expect(await db.pending('account-a'), hasLength(1));
      await db.receive('account-a', 'key-1', const Receipt.accepted(2));
      await db.receive('account-a', 'key-1', const Receipt.accepted(2));
      expect(await db.pending('account-a'), isEmpty);
      expect((await db.command('account-a', 'key-1'))!.acceptedVersion, 2);
    },
  );
  test(
    'rejection remains visible and cannot silently become success',
    () async {
      await enqueue();
      await db.receive(
        'account-a',
        'key-1',
        const Receipt.rejected('ASSIGNMENT_REVOKED'),
      );
      expect(
        (await db.command('account-a', 'key-1'))!.reason,
        'ASSIGNMENT_REVOKED',
      );
      await expectLater(
        db.receive('account-a', 'key-1', const Receipt.accepted(2)),
        throwsStateError,
      );
    },
  );
  test('stale accepted version leaves command pending', () async {
    await enqueue();
    await expectLater(
      db.receive('account-a', 'key-1', const Receipt.accepted(1)),
      throwsStateError,
    );
    expect(await db.pending('account-a'), hasLength(1));
  });
  test('account clearing does not erase another account', () async {
    await enqueue();
    await enqueue(account: 'account-b');
    expect(await db.clearAccount('account-a'), 1);
    expect(await db.pending('account-a'), isEmpty);
    expect(await db.pending('account-b'), hasLength(1));
  });
}
