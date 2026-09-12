// dart format width=80
// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'queue.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;
/// @nodoc
mixin _$Receipt {





@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is Receipt);
}


@override
int get hashCode => runtimeType.hashCode;

@override
String toString() {
  return 'Receipt()';
}


}

/// @nodoc
class $ReceiptCopyWith<$Res>  {
$ReceiptCopyWith(Receipt _, $Res Function(Receipt) __);
}


/// @nodoc


class Accepted implements Receipt {
  const Accepted(this.version);


 final  int version;

/// Create a copy of Receipt
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$AcceptedCopyWith<Accepted> get copyWith => _$AcceptedCopyWithImpl<Accepted>(this, _$identity);



@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is Accepted&&(identical(other.version, version) || other.version == version));
}


@override
int get hashCode => Object.hash(runtimeType,version);

@override
String toString() {
  return 'Receipt.accepted(version: $version)';
}


}

/// @nodoc
abstract mixin class $AcceptedCopyWith<$Res> implements $ReceiptCopyWith<$Res> {
  factory $AcceptedCopyWith(Accepted value, $Res Function(Accepted) _then) = _$AcceptedCopyWithImpl;
@useResult
$Res call({
 int version
});




}
/// @nodoc
class _$AcceptedCopyWithImpl<$Res>
    implements $AcceptedCopyWith<$Res> {
  _$AcceptedCopyWithImpl(this._self, this._then);

  final Accepted _self;
  final $Res Function(Accepted) _then;

/// Create a copy of Receipt
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') $Res call({Object? version = null,}) {
  return _then(Accepted(
null == version ? _self.version : version // ignore: cast_nullable_to_non_nullable
as int,
  ));
}


}

/// @nodoc


class Rejected implements Receipt {
  const Rejected(this.reason);


 final  String reason;

/// Create a copy of Receipt
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$RejectedCopyWith<Rejected> get copyWith => _$RejectedCopyWithImpl<Rejected>(this, _$identity);



@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is Rejected&&(identical(other.reason, reason) || other.reason == reason));
}


@override
int get hashCode => Object.hash(runtimeType,reason);

@override
String toString() {
  return 'Receipt.rejected(reason: $reason)';
}


}

/// @nodoc
abstract mixin class $RejectedCopyWith<$Res> implements $ReceiptCopyWith<$Res> {
  factory $RejectedCopyWith(Rejected value, $Res Function(Rejected) _then) = _$RejectedCopyWithImpl;
@useResult
$Res call({
 String reason
});




}
/// @nodoc
class _$RejectedCopyWithImpl<$Res>
    implements $RejectedCopyWith<$Res> {
  _$RejectedCopyWithImpl(this._self, this._then);

  final Rejected _self;
  final $Res Function(Rejected) _then;

/// Create a copy of Receipt
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') $Res call({Object? reason = null,}) {
  return _then(Rejected(
null == reason ? _self.reason : reason // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}

// dart format on
