// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'queue.dart';

// ignore_for_file: type=lint
class $PendingCommandsTable extends PendingCommands
    with TableInfo<$PendingCommandsTable, PendingCommand> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $PendingCommandsTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _accountMeta = const VerificationMeta(
    'account',
  );
  @override
  late final GeneratedColumn<String> account = GeneratedColumn<String>(
    'account',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _commandKeyMeta = const VerificationMeta(
    'commandKey',
  );
  @override
  late final GeneratedColumn<String> commandKey = GeneratedColumn<String>(
    'command_key',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _actionMeta = const VerificationMeta('action');
  @override
  late final GeneratedColumn<String> action = GeneratedColumn<String>(
    'action',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _payloadMeta = const VerificationMeta(
    'payload',
  );
  @override
  late final GeneratedColumn<String> payload = GeneratedColumn<String>(
    'payload',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _expectedVersionMeta = const VerificationMeta(
    'expectedVersion',
  );
  @override
  late final GeneratedColumn<int> expectedVersion = GeneratedColumn<int>(
    'expected_version',
    aliasedName,
    false,
    type: DriftSqlType.int,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _stateMeta = const VerificationMeta('state');
  @override
  late final GeneratedColumn<String> state = GeneratedColumn<String>(
    'state',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: false,
    defaultValue: const Constant('PENDING'),
  );
  static const VerificationMeta _reasonMeta = const VerificationMeta('reason');
  @override
  late final GeneratedColumn<String> reason = GeneratedColumn<String>(
    'reason',
    aliasedName,
    true,
    type: DriftSqlType.string,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _acceptedVersionMeta = const VerificationMeta(
    'acceptedVersion',
  );
  @override
  late final GeneratedColumn<int> acceptedVersion = GeneratedColumn<int>(
    'accepted_version',
    aliasedName,
    true,
    type: DriftSqlType.int,
    requiredDuringInsert: false,
  );
  @override
  List<GeneratedColumn> get $columns => [
    account,
    commandKey,
    action,
    payload,
    expectedVersion,
    state,
    reason,
    acceptedVersion,
  ];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'pending_commands';
  @override
  VerificationContext validateIntegrity(
    Insertable<PendingCommand> instance, {
    bool isInserting = false,
  }) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('account')) {
      context.handle(
        _accountMeta,
        account.isAcceptableOrUnknown(data['account']!, _accountMeta),
      );
    } else if (isInserting) {
      context.missing(_accountMeta);
    }
    if (data.containsKey('command_key')) {
      context.handle(
        _commandKeyMeta,
        commandKey.isAcceptableOrUnknown(data['command_key']!, _commandKeyMeta),
      );
    } else if (isInserting) {
      context.missing(_commandKeyMeta);
    }
    if (data.containsKey('action')) {
      context.handle(
        _actionMeta,
        action.isAcceptableOrUnknown(data['action']!, _actionMeta),
      );
    } else if (isInserting) {
      context.missing(_actionMeta);
    }
    if (data.containsKey('payload')) {
      context.handle(
        _payloadMeta,
        payload.isAcceptableOrUnknown(data['payload']!, _payloadMeta),
      );
    } else if (isInserting) {
      context.missing(_payloadMeta);
    }
    if (data.containsKey('expected_version')) {
      context.handle(
        _expectedVersionMeta,
        expectedVersion.isAcceptableOrUnknown(
          data['expected_version']!,
          _expectedVersionMeta,
        ),
      );
    } else if (isInserting) {
      context.missing(_expectedVersionMeta);
    }
    if (data.containsKey('state')) {
      context.handle(
        _stateMeta,
        state.isAcceptableOrUnknown(data['state']!, _stateMeta),
      );
    }
    if (data.containsKey('reason')) {
      context.handle(
        _reasonMeta,
        reason.isAcceptableOrUnknown(data['reason']!, _reasonMeta),
      );
    }
    if (data.containsKey('accepted_version')) {
      context.handle(
        _acceptedVersionMeta,
        acceptedVersion.isAcceptableOrUnknown(
          data['accepted_version']!,
          _acceptedVersionMeta,
        ),
      );
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {account, commandKey};
  @override
  PendingCommand map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return PendingCommand(
      account: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}account'],
      )!,
      commandKey: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}command_key'],
      )!,
      action: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}action'],
      )!,
      payload: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}payload'],
      )!,
      expectedVersion: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}expected_version'],
      )!,
      state: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}state'],
      )!,
      reason: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}reason'],
      ),
      acceptedVersion: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}accepted_version'],
      ),
    );
  }

  @override
  $PendingCommandsTable createAlias(String alias) {
    return $PendingCommandsTable(attachedDatabase, alias);
  }
}

class PendingCommand extends DataClass implements Insertable<PendingCommand> {
  final String account;
  final String commandKey;
  final String action;
  final String payload;
  final int expectedVersion;
  final String state;
  final String? reason;
  final int? acceptedVersion;
  const PendingCommand({
    required this.account,
    required this.commandKey,
    required this.action,
    required this.payload,
    required this.expectedVersion,
    required this.state,
    this.reason,
    this.acceptedVersion,
  });
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['account'] = Variable<String>(account);
    map['command_key'] = Variable<String>(commandKey);
    map['action'] = Variable<String>(action);
    map['payload'] = Variable<String>(payload);
    map['expected_version'] = Variable<int>(expectedVersion);
    map['state'] = Variable<String>(state);
    if (!nullToAbsent || reason != null) {
      map['reason'] = Variable<String>(reason);
    }
    if (!nullToAbsent || acceptedVersion != null) {
      map['accepted_version'] = Variable<int>(acceptedVersion);
    }
    return map;
  }

  PendingCommandsCompanion toCompanion(bool nullToAbsent) {
    return PendingCommandsCompanion(
      account: Value(account),
      commandKey: Value(commandKey),
      action: Value(action),
      payload: Value(payload),
      expectedVersion: Value(expectedVersion),
      state: Value(state),
      reason: reason == null && nullToAbsent
          ? const Value.absent()
          : Value(reason),
      acceptedVersion: acceptedVersion == null && nullToAbsent
          ? const Value.absent()
          : Value(acceptedVersion),
    );
  }

  factory PendingCommand.fromJson(
    Map<String, dynamic> json, {
    ValueSerializer? serializer,
  }) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return PendingCommand(
      account: serializer.fromJson<String>(json['account']),
      commandKey: serializer.fromJson<String>(json['commandKey']),
      action: serializer.fromJson<String>(json['action']),
      payload: serializer.fromJson<String>(json['payload']),
      expectedVersion: serializer.fromJson<int>(json['expectedVersion']),
      state: serializer.fromJson<String>(json['state']),
      reason: serializer.fromJson<String?>(json['reason']),
      acceptedVersion: serializer.fromJson<int?>(json['acceptedVersion']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'account': serializer.toJson<String>(account),
      'commandKey': serializer.toJson<String>(commandKey),
      'action': serializer.toJson<String>(action),
      'payload': serializer.toJson<String>(payload),
      'expectedVersion': serializer.toJson<int>(expectedVersion),
      'state': serializer.toJson<String>(state),
      'reason': serializer.toJson<String?>(reason),
      'acceptedVersion': serializer.toJson<int?>(acceptedVersion),
    };
  }

  PendingCommand copyWith({
    String? account,
    String? commandKey,
    String? action,
    String? payload,
    int? expectedVersion,
    String? state,
    Value<String?> reason = const Value.absent(),
    Value<int?> acceptedVersion = const Value.absent(),
  }) => PendingCommand(
    account: account ?? this.account,
    commandKey: commandKey ?? this.commandKey,
    action: action ?? this.action,
    payload: payload ?? this.payload,
    expectedVersion: expectedVersion ?? this.expectedVersion,
    state: state ?? this.state,
    reason: reason.present ? reason.value : this.reason,
    acceptedVersion: acceptedVersion.present
        ? acceptedVersion.value
        : this.acceptedVersion,
  );
  PendingCommand copyWithCompanion(PendingCommandsCompanion data) {
    return PendingCommand(
      account: data.account.present ? data.account.value : this.account,
      commandKey: data.commandKey.present
          ? data.commandKey.value
          : this.commandKey,
      action: data.action.present ? data.action.value : this.action,
      payload: data.payload.present ? data.payload.value : this.payload,
      expectedVersion: data.expectedVersion.present
          ? data.expectedVersion.value
          : this.expectedVersion,
      state: data.state.present ? data.state.value : this.state,
      reason: data.reason.present ? data.reason.value : this.reason,
      acceptedVersion: data.acceptedVersion.present
          ? data.acceptedVersion.value
          : this.acceptedVersion,
    );
  }

  @override
  String toString() {
    return (StringBuffer('PendingCommand(')
          ..write('account: $account, ')
          ..write('commandKey: $commandKey, ')
          ..write('action: $action, ')
          ..write('payload: $payload, ')
          ..write('expectedVersion: $expectedVersion, ')
          ..write('state: $state, ')
          ..write('reason: $reason, ')
          ..write('acceptedVersion: $acceptedVersion')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode => Object.hash(
    account,
    commandKey,
    action,
    payload,
    expectedVersion,
    state,
    reason,
    acceptedVersion,
  );
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is PendingCommand &&
          other.account == this.account &&
          other.commandKey == this.commandKey &&
          other.action == this.action &&
          other.payload == this.payload &&
          other.expectedVersion == this.expectedVersion &&
          other.state == this.state &&
          other.reason == this.reason &&
          other.acceptedVersion == this.acceptedVersion);
}

class PendingCommandsCompanion extends UpdateCompanion<PendingCommand> {
  final Value<String> account;
  final Value<String> commandKey;
  final Value<String> action;
  final Value<String> payload;
  final Value<int> expectedVersion;
  final Value<String> state;
  final Value<String?> reason;
  final Value<int?> acceptedVersion;
  final Value<int> rowid;
  const PendingCommandsCompanion({
    this.account = const Value.absent(),
    this.commandKey = const Value.absent(),
    this.action = const Value.absent(),
    this.payload = const Value.absent(),
    this.expectedVersion = const Value.absent(),
    this.state = const Value.absent(),
    this.reason = const Value.absent(),
    this.acceptedVersion = const Value.absent(),
    this.rowid = const Value.absent(),
  });
  PendingCommandsCompanion.insert({
    required String account,
    required String commandKey,
    required String action,
    required String payload,
    required int expectedVersion,
    this.state = const Value.absent(),
    this.reason = const Value.absent(),
    this.acceptedVersion = const Value.absent(),
    this.rowid = const Value.absent(),
  }) : account = Value(account),
       commandKey = Value(commandKey),
       action = Value(action),
       payload = Value(payload),
       expectedVersion = Value(expectedVersion);
  static Insertable<PendingCommand> custom({
    Expression<String>? account,
    Expression<String>? commandKey,
    Expression<String>? action,
    Expression<String>? payload,
    Expression<int>? expectedVersion,
    Expression<String>? state,
    Expression<String>? reason,
    Expression<int>? acceptedVersion,
    Expression<int>? rowid,
  }) {
    return RawValuesInsertable({
      if (account != null) 'account': account,
      if (commandKey != null) 'command_key': commandKey,
      if (action != null) 'action': action,
      if (payload != null) 'payload': payload,
      if (expectedVersion != null) 'expected_version': expectedVersion,
      if (state != null) 'state': state,
      if (reason != null) 'reason': reason,
      if (acceptedVersion != null) 'accepted_version': acceptedVersion,
      if (rowid != null) 'rowid': rowid,
    });
  }

  PendingCommandsCompanion copyWith({
    Value<String>? account,
    Value<String>? commandKey,
    Value<String>? action,
    Value<String>? payload,
    Value<int>? expectedVersion,
    Value<String>? state,
    Value<String?>? reason,
    Value<int?>? acceptedVersion,
    Value<int>? rowid,
  }) {
    return PendingCommandsCompanion(
      account: account ?? this.account,
      commandKey: commandKey ?? this.commandKey,
      action: action ?? this.action,
      payload: payload ?? this.payload,
      expectedVersion: expectedVersion ?? this.expectedVersion,
      state: state ?? this.state,
      reason: reason ?? this.reason,
      acceptedVersion: acceptedVersion ?? this.acceptedVersion,
      rowid: rowid ?? this.rowid,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (account.present) {
      map['account'] = Variable<String>(account.value);
    }
    if (commandKey.present) {
      map['command_key'] = Variable<String>(commandKey.value);
    }
    if (action.present) {
      map['action'] = Variable<String>(action.value);
    }
    if (payload.present) {
      map['payload'] = Variable<String>(payload.value);
    }
    if (expectedVersion.present) {
      map['expected_version'] = Variable<int>(expectedVersion.value);
    }
    if (state.present) {
      map['state'] = Variable<String>(state.value);
    }
    if (reason.present) {
      map['reason'] = Variable<String>(reason.value);
    }
    if (acceptedVersion.present) {
      map['accepted_version'] = Variable<int>(acceptedVersion.value);
    }
    if (rowid.present) {
      map['rowid'] = Variable<int>(rowid.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('PendingCommandsCompanion(')
          ..write('account: $account, ')
          ..write('commandKey: $commandKey, ')
          ..write('action: $action, ')
          ..write('payload: $payload, ')
          ..write('expectedVersion: $expectedVersion, ')
          ..write('state: $state, ')
          ..write('reason: $reason, ')
          ..write('acceptedVersion: $acceptedVersion, ')
          ..write('rowid: $rowid')
          ..write(')'))
        .toString();
  }
}

abstract class _$ProbeDatabase extends GeneratedDatabase {
  _$ProbeDatabase(QueryExecutor e) : super(e);
  $ProbeDatabaseManager get managers => $ProbeDatabaseManager(this);
  late final $PendingCommandsTable pendingCommands = $PendingCommandsTable(
    this,
  );
  @override
  Iterable<TableInfo<Table, Object?>> get allTables =>
      allSchemaEntities.whereType<TableInfo<Table, Object?>>();
  @override
  List<DatabaseSchemaEntity> get allSchemaEntities => [pendingCommands];
}

typedef $$PendingCommandsTableCreateCompanionBuilder =
    PendingCommandsCompanion Function({
      required String account,
      required String commandKey,
      required String action,
      required String payload,
      required int expectedVersion,
      Value<String> state,
      Value<String?> reason,
      Value<int?> acceptedVersion,
      Value<int> rowid,
    });
typedef $$PendingCommandsTableUpdateCompanionBuilder =
    PendingCommandsCompanion Function({
      Value<String> account,
      Value<String> commandKey,
      Value<String> action,
      Value<String> payload,
      Value<int> expectedVersion,
      Value<String> state,
      Value<String?> reason,
      Value<int?> acceptedVersion,
      Value<int> rowid,
    });

class $$PendingCommandsTableFilterComposer
    extends Composer<_$ProbeDatabase, $PendingCommandsTable> {
  $$PendingCommandsTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<String> get account => $composableBuilder(
    column: $table.account,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get commandKey => $composableBuilder(
    column: $table.commandKey,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get action => $composableBuilder(
    column: $table.action,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get payload => $composableBuilder(
    column: $table.payload,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<int> get expectedVersion => $composableBuilder(
    column: $table.expectedVersion,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get state => $composableBuilder(
    column: $table.state,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get reason => $composableBuilder(
    column: $table.reason,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<int> get acceptedVersion => $composableBuilder(
    column: $table.acceptedVersion,
    builder: (column) => ColumnFilters(column),
  );
}

class $$PendingCommandsTableOrderingComposer
    extends Composer<_$ProbeDatabase, $PendingCommandsTable> {
  $$PendingCommandsTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<String> get account => $composableBuilder(
    column: $table.account,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get commandKey => $composableBuilder(
    column: $table.commandKey,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get action => $composableBuilder(
    column: $table.action,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get payload => $composableBuilder(
    column: $table.payload,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<int> get expectedVersion => $composableBuilder(
    column: $table.expectedVersion,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get state => $composableBuilder(
    column: $table.state,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get reason => $composableBuilder(
    column: $table.reason,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<int> get acceptedVersion => $composableBuilder(
    column: $table.acceptedVersion,
    builder: (column) => ColumnOrderings(column),
  );
}

class $$PendingCommandsTableAnnotationComposer
    extends Composer<_$ProbeDatabase, $PendingCommandsTable> {
  $$PendingCommandsTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<String> get account =>
      $composableBuilder(column: $table.account, builder: (column) => column);

  GeneratedColumn<String> get commandKey => $composableBuilder(
    column: $table.commandKey,
    builder: (column) => column,
  );

  GeneratedColumn<String> get action =>
      $composableBuilder(column: $table.action, builder: (column) => column);

  GeneratedColumn<String> get payload =>
      $composableBuilder(column: $table.payload, builder: (column) => column);

  GeneratedColumn<int> get expectedVersion => $composableBuilder(
    column: $table.expectedVersion,
    builder: (column) => column,
  );

  GeneratedColumn<String> get state =>
      $composableBuilder(column: $table.state, builder: (column) => column);

  GeneratedColumn<String> get reason =>
      $composableBuilder(column: $table.reason, builder: (column) => column);

  GeneratedColumn<int> get acceptedVersion => $composableBuilder(
    column: $table.acceptedVersion,
    builder: (column) => column,
  );
}

class $$PendingCommandsTableTableManager
    extends
        RootTableManager<
          _$ProbeDatabase,
          $PendingCommandsTable,
          PendingCommand,
          $$PendingCommandsTableFilterComposer,
          $$PendingCommandsTableOrderingComposer,
          $$PendingCommandsTableAnnotationComposer,
          $$PendingCommandsTableCreateCompanionBuilder,
          $$PendingCommandsTableUpdateCompanionBuilder,
          (
            PendingCommand,
            BaseReferences<
              _$ProbeDatabase,
              $PendingCommandsTable,
              PendingCommand
            >,
          ),
          PendingCommand,
          PrefetchHooks Function()
        > {
  $$PendingCommandsTableTableManager(
    _$ProbeDatabase db,
    $PendingCommandsTable table,
  ) : super(
        TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$PendingCommandsTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$PendingCommandsTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$PendingCommandsTableAnnotationComposer($db: db, $table: table),
          updateCompanionCallback:
              ({
                Value<String> account = const Value.absent(),
                Value<String> commandKey = const Value.absent(),
                Value<String> action = const Value.absent(),
                Value<String> payload = const Value.absent(),
                Value<int> expectedVersion = const Value.absent(),
                Value<String> state = const Value.absent(),
                Value<String?> reason = const Value.absent(),
                Value<int?> acceptedVersion = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => PendingCommandsCompanion(
                account: account,
                commandKey: commandKey,
                action: action,
                payload: payload,
                expectedVersion: expectedVersion,
                state: state,
                reason: reason,
                acceptedVersion: acceptedVersion,
                rowid: rowid,
              ),
          createCompanionCallback:
              ({
                required String account,
                required String commandKey,
                required String action,
                required String payload,
                required int expectedVersion,
                Value<String> state = const Value.absent(),
                Value<String?> reason = const Value.absent(),
                Value<int?> acceptedVersion = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => PendingCommandsCompanion.insert(
                account: account,
                commandKey: commandKey,
                action: action,
                payload: payload,
                expectedVersion: expectedVersion,
                state: state,
                reason: reason,
                acceptedVersion: acceptedVersion,
                rowid: rowid,
              ),
          withReferenceMapper: (p0) => p0
              .map((e) => (e.readTable(table), BaseReferences(db, table, e)))
              .toList(),
          prefetchHooksCallback: null,
        ),
      );
}

typedef $$PendingCommandsTableProcessedTableManager =
    ProcessedTableManager<
      _$ProbeDatabase,
      $PendingCommandsTable,
      PendingCommand,
      $$PendingCommandsTableFilterComposer,
      $$PendingCommandsTableOrderingComposer,
      $$PendingCommandsTableAnnotationComposer,
      $$PendingCommandsTableCreateCompanionBuilder,
      $$PendingCommandsTableUpdateCompanionBuilder,
      (
        PendingCommand,
        BaseReferences<_$ProbeDatabase, $PendingCommandsTable, PendingCommand>,
      ),
      PendingCommand,
      PrefetchHooks Function()
    >;

class $ProbeDatabaseManager {
  final _$ProbeDatabase _db;
  $ProbeDatabaseManager(this._db);
  $$PendingCommandsTableTableManager get pendingCommands =>
      $$PendingCommandsTableTableManager(_db, _db.pendingCommands);
}
