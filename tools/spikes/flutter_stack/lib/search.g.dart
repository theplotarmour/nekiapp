// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'search.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint, type=warning

@ProviderFor(searchSource)
final searchSourceProvider = SearchSourceProvider._();

final class SearchSourceProvider
    extends $FunctionalProvider<SearchSource, SearchSource, SearchSource>
    with $Provider<SearchSource> {
  SearchSourceProvider._()
    : super(
        from: null,
        argument: null,
        retry: null,
        name: r'searchSourceProvider',
        isAutoDispose: true,
        dependencies: null,
        $allTransitiveDependencies: null,
      );

  @override
  String debugGetCreateSourceHash() => _$searchSourceHash();

  @$internal
  @override
  $ProviderElement<SearchSource> $createElement($ProviderPointer pointer) =>
      $ProviderElement(pointer);

  @override
  SearchSource create(Ref ref) {
    return searchSource(ref);
  }

  /// {@macro riverpod.override_with_value}
  Override overrideWithValue(SearchSource value) {
    return $ProviderOverride(
      origin: this,
      providerOverride: $SyncValueProvider<SearchSource>(value),
    );
  }
}

String _$searchSourceHash() => r'e1967ebb143116d595507302d95c57f1a28a9a40';

@ProviderFor(scopedSearch)
final scopedSearchProvider = ScopedSearchFamily._();

final class ScopedSearchProvider
    extends
        $FunctionalProvider<
          AsyncValue<List<String>>,
          List<String>,
          FutureOr<List<String>>
        >
    with $FutureModifier<List<String>>, $FutureProvider<List<String>> {
  ScopedSearchProvider._({
    required ScopedSearchFamily super.from,
    required (String, String) super.argument,
  }) : super(
         retry: noAutomaticRetry,
         name: r'scopedSearchProvider',
         isAutoDispose: true,
         dependencies: null,
         $allTransitiveDependencies: null,
       );

  @override
  String debugGetCreateSourceHash() => _$scopedSearchHash();

  @override
  String toString() {
    return r'scopedSearchProvider'
        ''
        '$argument';
  }

  @$internal
  @override
  $FutureProviderElement<List<String>> $createElement(
    $ProviderPointer pointer,
  ) => $FutureProviderElement(pointer);

  @override
  FutureOr<List<String>> create(Ref ref) {
    final argument = this.argument as (String, String);
    return scopedSearch(ref, argument.$1, argument.$2);
  }

  @override
  bool operator ==(Object other) {
    return other is ScopedSearchProvider && other.argument == argument;
  }

  @override
  int get hashCode {
    return argument.hashCode;
  }
}

String _$scopedSearchHash() => r'fbf6d65f6e061b0196afe66f2ac546f0f60a5a01';

final class ScopedSearchFamily extends $Family
    with $FunctionalFamilyOverride<FutureOr<List<String>>, (String, String)> {
  ScopedSearchFamily._()
    : super(
        retry: noAutomaticRetry,
        name: r'scopedSearchProvider',
        dependencies: null,
        $allTransitiveDependencies: null,
        isAutoDispose: true,
      );

  ScopedSearchProvider call(String account, String query) =>
      ScopedSearchProvider._(argument: (account, query), from: this);

  @override
  String toString() => r'scopedSearchProvider';
}
