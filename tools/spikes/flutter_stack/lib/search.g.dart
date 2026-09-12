// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'search.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

String _$searchSourceHash() => r'e1967ebb143116d595507302d95c57f1a28a9a40';

/// See also [searchSource].
@ProviderFor(searchSource)
final searchSourceProvider = AutoDisposeProvider<SearchSource>.internal(
  searchSource,
  name: r'searchSourceProvider',
  debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
      ? null
      : _$searchSourceHash,
  dependencies: null,
  allTransitiveDependencies: null,
);

@Deprecated('Will be removed in 3.0. Use Ref instead')
// ignore: unused_element
typedef SearchSourceRef = AutoDisposeProviderRef<SearchSource>;
String _$scopedSearchHash() => r'1c544f6dd29719fa843bc9ac61d6b2a779c8e348';

/// Copied from Dart SDK
class _SystemHash {
  _SystemHash._();

  static int combine(int hash, int value) {
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + value);
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + ((0x0007ffff & hash) << 10));
    return hash ^ (hash >> 6);
  }

  static int finish(int hash) {
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + ((0x03ffffff & hash) << 3));
    // ignore: parameter_assignments
    hash = hash ^ (hash >> 11);
    return 0x1fffffff & (hash + ((0x00003fff & hash) << 15));
  }
}

/// See also [scopedSearch].
@ProviderFor(scopedSearch)
const scopedSearchProvider = ScopedSearchFamily();

/// See also [scopedSearch].
class ScopedSearchFamily extends Family<AsyncValue<List<String>>> {
  /// See also [scopedSearch].
  const ScopedSearchFamily();

  /// See also [scopedSearch].
  ScopedSearchProvider call(String account, String query) {
    return ScopedSearchProvider(account, query);
  }

  @override
  ScopedSearchProvider getProviderOverride(
    covariant ScopedSearchProvider provider,
  ) {
    return call(provider.account, provider.query);
  }

  static const Iterable<ProviderOrFamily>? _dependencies = null;

  @override
  Iterable<ProviderOrFamily>? get dependencies => _dependencies;

  static const Iterable<ProviderOrFamily>? _allTransitiveDependencies = null;

  @override
  Iterable<ProviderOrFamily>? get allTransitiveDependencies =>
      _allTransitiveDependencies;

  @override
  String? get name => r'scopedSearchProvider';
}

/// See also [scopedSearch].
class ScopedSearchProvider extends AutoDisposeFutureProvider<List<String>> {
  /// See also [scopedSearch].
  ScopedSearchProvider(String account, String query)
    : this._internal(
        (ref) => scopedSearch(ref as ScopedSearchRef, account, query),
        from: scopedSearchProvider,
        name: r'scopedSearchProvider',
        debugGetCreateSourceHash: const bool.fromEnvironment('dart.vm.product')
            ? null
            : _$scopedSearchHash,
        dependencies: ScopedSearchFamily._dependencies,
        allTransitiveDependencies:
            ScopedSearchFamily._allTransitiveDependencies,
        account: account,
        query: query,
      );

  ScopedSearchProvider._internal(
    super._createNotifier, {
    required super.name,
    required super.dependencies,
    required super.allTransitiveDependencies,
    required super.debugGetCreateSourceHash,
    required super.from,
    required this.account,
    required this.query,
  }) : super.internal();

  final String account;
  final String query;

  @override
  Override overrideWith(
    FutureOr<List<String>> Function(ScopedSearchRef provider) create,
  ) {
    return ProviderOverride(
      origin: this,
      override: ScopedSearchProvider._internal(
        (ref) => create(ref as ScopedSearchRef),
        from: from,
        name: null,
        dependencies: null,
        allTransitiveDependencies: null,
        debugGetCreateSourceHash: null,
        account: account,
        query: query,
      ),
    );
  }

  @override
  AutoDisposeFutureProviderElement<List<String>> createElement() {
    return _ScopedSearchProviderElement(this);
  }

  @override
  bool operator ==(Object other) {
    return other is ScopedSearchProvider &&
        other.account == account &&
        other.query == query;
  }

  @override
  int get hashCode {
    var hash = _SystemHash.combine(0, runtimeType.hashCode);
    hash = _SystemHash.combine(hash, account.hashCode);
    hash = _SystemHash.combine(hash, query.hashCode);

    return _SystemHash.finish(hash);
  }
}

@Deprecated('Will be removed in 3.0. Use Ref instead')
// ignore: unused_element
mixin ScopedSearchRef on AutoDisposeFutureProviderRef<List<String>> {
  /// The parameter `account` of this provider.
  String get account;

  /// The parameter `query` of this provider.
  String get query;
}

class _ScopedSearchProviderElement
    extends AutoDisposeFutureProviderElement<List<String>>
    with ScopedSearchRef {
  _ScopedSearchProviderElement(super.provider);

  @override
  String get account => (origin as ScopedSearchProvider).account;
  @override
  String get query => (origin as ScopedSearchProvider).query;
}

// ignore_for_file: type=lint
// ignore_for_file: subtype_of_sealed_class, invalid_use_of_internal_member, invalid_use_of_visible_for_testing_member, deprecated_member_use_from_same_package
