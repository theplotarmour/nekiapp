import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart' show Ref;

part 'search.g.dart';

abstract interface class SearchSource {
  Future<List<String>> find(String account, String query);
  void cancel(String account, String query);
}

@riverpod
SearchSource searchSource(Ref ref) =>
    throw UnimplementedError('Inject a source');

@riverpod
Future<List<String>> scopedSearch(Ref ref, String account, String query) {
  final source = ref.watch(searchSourceProvider);
  ref.onDispose(() => source.cancel(account, query));
  return source.find(account, query);
}
