"""Explicit P0 identity schemas; no server/runtime behavior is implemented here."""

from __future__ import annotations

from copy import deepcopy


def ref(name):
    return {"$ref": f"#/components/schemas/{name}"}


def obj(properties, required=None, **extra):
    return {"type": "object", "additionalProperties": False, "properties": properties,
            "required": list(properties) if required is None else required, **extra}


def text(minimum=1, maximum=200, **extra):
    return {"type": "string", "minLength": minimum, "maxLength": maximum, **extra}


def enum(*values):
    return {"type": "string", "enum": list(values)}


def integer(minimum=0, maximum=2147483647):
    return {"type": "integer", "minimum": minimum, "maximum": maximum}


def nullable(schema):
    return {"anyOf": [schema, {"type": "null"}]}


ID = text(36, 36, format="uuid")
TIME = text(20, 32, format="date-time", pattern=r"Z$")
TOKEN = text(32, 4096, writeOnly=True)
VERSION = integer()
BOOL = {"type": "boolean"}
UUID = "11111111-1111-4111-8111-111111111111"
DEVICE = "22222222-2222-4222-8222-222222222222"
NOW = "2026-09-10T12:00:00Z"
LATER = "2026-09-10T12:05:00Z"
EXAMPLE_TOKEN = "synthetic_example_not_a_real_token_0000000000"


def schemas():
    s = {}
    s["OtpRequest"] = obj({"phone_e164": text(8, 16, pattern=r"^\+[1-9][0-9]{7,14}$"),
                            "device_id": ID, "client_kind": enum("mobile", "web")})
    s["OtpChallenge"] = obj({"challenge_id": ID, "expires_at": TIME, "resend_after": TIME,
                              "delivery_status": enum("accepted"), "code_length": {"const": 6, "type": "integer"}})
    s["OtpVerify"] = obj({"challenge_id": ID, "code": text(6, 6, pattern=r"^[0-9]{6}$", writeOnly=True),
                           "device_id": ID, "client_kind": enum("mobile", "web")})
    s["MobileSession"] = obj({"client_kind": {"const": "mobile", "type": "string"},
                               "access_token": text(32, 4096), "token_type": enum("Bearer"),
                               "access_expires_at": TIME, "refresh_token": text(32, 4096),
                               "refresh_expires_at": TIME, "session_id": ID, "user_id": ID,
                               "profile_complete": BOOL})
    s["WebSession"] = obj({key: deepcopy(value) for key, value in s["MobileSession"]["properties"].items()
                            if key not in {"refresh_token", "refresh_expires_at"}})
    s["WebSession"]["properties"]["client_kind"] = {"const": "web", "type": "string"}
    s["SessionResult"] = {"oneOf": [ref("MobileSession"), ref("WebSession")],
                           "discriminator": {"propertyName": "client_kind"}}
    s["MobileRefresh"] = obj({"client_kind": {"const": "mobile", "type": "string"},
                               "device_id": ID, "refresh_token": TOKEN})
    s["WebRefresh"] = obj({"client_kind": {"const": "web", "type": "string"}, "device_id": ID})
    s["RefreshRequest"] = {"oneOf": [ref("MobileRefresh"), ref("WebRefresh")],
                            "discriminator": {"propertyName": "client_kind"}}
    s["VersionCommand"] = obj({"expected_version": VERSION})
    s["SessionRevocation"] = obj({"session_id": ID, "revoked": {"const": True, "type": "boolean"},
                                   "version": VERSION})
    s["SessionSummary"] = obj({"session_id": ID, "device_id": ID, "platform": enum("ios", "android", "web"),
                                "created_at": TIME, "last_seen_at": TIME, "is_current": BOOL,
                                "revoked_at": nullable(TIME), "version": VERSION})
    s["SessionPage"] = page(ref("SessionSummary"))
    s["StepUpRequest"] = obj({"action": enum("revoke_session", "delete_account", "cancel_deletion",
                                              "change_bank", "approve_payout", "record_payout",
                                              "approve_refund", "grant_role", "remove_payment_method"),
                               "resource_id": ID, "expected_resource_version": VERSION})
    s["StepUpVerify"] = obj({"challenge_id": ID, "code": text(6, 6, pattern=r"^[0-9]{6}$", writeOnly=True)})
    s["StepUpGrant"] = obj({"grant_token": text(32, 4096), "expires_at": TIME,
                             "action": s["StepUpRequest"]["properties"]["action"], "resource_id": ID,
                             "resource_version": VERSION, "single_use": {"const": True, "type": "boolean"}})
    s["UserProfile"] = obj({"id": ID, "first_name": nullable(text(1, 80)), "last_name": nullable(text(1, 80)),
                             "avatar_media_id": nullable(ID), "impact_statement": text(0, 200),
                             "locale": enum("en-IN"), "profile_complete": BOOL,
                             "account_status": enum("ACTIVE", "SUSPENDED", "DELETION_PENDING"),
                             "version": VERSION})
    s["ProfileUpdate"] = obj({"expected_version": VERSION, "first_name": text(1, 80),
                               "last_name": nullable(text(1, 80)), "impact_statement": text(0, 200)},
                              ["expected_version"], minProperties=2)
    s["AvatarUpdate"] = obj({"expected_version": VERSION, "media_id": nullable(ID)})
    s["DeletionRequest"] = obj({"expected_version": VERSION, "reason": enum("no_longer_needed", "privacy", "other"),
                                 "acknowledged_policy_version": text(1, 64)})
    s["DeletionStatus"] = obj({"id": ID, "status": enum("REQUESTED", "PROCESSING", "COMPLETED", "CANCELLED", "NEEDS_REVIEW"),
                                "requested_at": TIME, "cancellable": BOOL, "completed_at": nullable(TIME),
                                "policy_version": text(1, 64), "version": VERSION})
    s["DeviceCreate"] = obj({"device_id": ID, "platform": enum("ios", "android", "web"),
                              "push_token": nullable(text(1, 4096, writeOnly=True)), "app_version": text(1, 40)})
    s["DeviceUpdate"] = obj({"expected_version": VERSION, "push_token": nullable(text(1, 4096, writeOnly=True)),
                              "app_version": text(1, 40)})
    s["DeviceSummary"] = obj({"device_id": ID, "platform": enum("ios", "android", "web"),
                               "push_enabled": BOOL, "app_version": text(1, 40), "last_seen_at": TIME, "version": VERSION})
    s["DevicePage"] = page(ref("DeviceSummary"))
    privacy = {"profile_public": BOOL, "contributions_public": BOOL, "impact_sharing": BOOL}
    s["PrivacyPreferences"] = obj({**privacy, "version": VERSION})
    s["PrivacyUpdate"] = obj({**privacy, "expected_version": VERSION})
    s["NotificationPreference"] = obj({"category": enum("contribution", "tracking", "volunteering", "impact", "account"),
                                        "push_enabled": BOOL, "quiet_hours_enabled": BOOL})
    prefs = {"type": "array", "items": ref("NotificationPreference"), "minItems": 5, "maxItems": 5,
             "allOf": [{"contains": {"type": "object", "properties": {"category": {"const": category}},
                                      "required": ["category"]}, "minContains": 1, "maxContains": 1}
                       for category in ("contribution", "tracking", "volunteering", "impact", "account")]}
    s["NotificationPreferences"] = obj({"categories": prefs, "timezone": enum("Asia/Kolkata"), "version": VERSION})
    s["NotificationPreferencesUpdate"] = obj({"categories": prefs, "expected_version": VERSION})
    s["SelectedLocationUpdate"] = obj({"expected_version": VERSION, "locality_id": ID,
                                        "source": enum("manual", "gps", "saved_address")})
    s["SelectedLocation"] = obj({"locality_id": ID, "label": text(1, 160), "city": text(1, 80),
                                  "in_discovery_area": BOOL, "pickup_serviceability": enum("requires_address_check"),
                                  "version": VERSION})
    s["ConsentDocument"] = obj({"kind": enum("terms", "privacy", "volunteer_sop"), "version": text(1, 64),
                                 "effective_at": TIME, "url": text(1, 2048, format="uri", pattern=r"^https://"),
                                 "sha256": text(64, 64, pattern=r"^[a-f0-9]{64}$")})
    s["ConsentDocuments"] = obj({"items": {"type": "array", "items": ref("ConsentDocument"), "minItems": 1}})
    s["ConsentCreate"] = obj({"kind": s["ConsentDocument"]["properties"]["kind"], "document_version": text(1, 64),
                               "accepted": {"const": True, "type": "boolean"}})
    s["ConsentReceipt"] = obj({"id": ID, "kind": s["ConsentDocument"]["properties"]["kind"],
                                "document_version": text(1, 64), "accepted_at": TIME})
    return s


def page(item):
    return obj({"items": {"type": "array", "items": item, "maxItems": 50},
                "next_cursor": nullable(text(1, 2048)), "has_more": BOOL})


def definitions():
    """operation -> request schema, success code, response schema, domain errors, effects."""
    return {
        "request_otp": ("OtpRequest", "200", "OtpChallenge", ["OTP_RATE_LIMITED"], "Auth challenge + durable SMS intent; no account existence signal."),
        "verify_otp": ("OtpVerify", "200", "SessionResult", ["OTP_INVALID", "OTP_EXPIRED", "OTP_LOCKED"], "Consume challenge once; create/restore user and rotating session."),
        "refresh_session": ("RefreshRequest", "200", "SessionResult", ["REFRESH_INVALID", "REFRESH_REUSED"], "Rotate refresh family atomically; reuse revokes family."),
        "logout_session": ("VersionCommand", "200", "SessionRevocation", [], "Revoke current session; browser clears refresh cookie."),
        "list_sessions": (None, "200", "SessionPage", [], "Read own session summaries; never return token hashes."),
        "revoke_session": ("VersionCommand", "200", "SessionRevocation", [], "Revoke selected owned session with action-bound step-up."),
        "get_current_user": (None, "200", "UserProfile", [], "Read owner profile; role claims are not an editable profile field."),
        "request_step_up": ("StepUpRequest", "200", "OtpChallenge", ["OTP_RATE_LIMITED"], "Bind challenge to authenticated subject/session/action/resource/version."),
        "verify_step_up": ("StepUpVerify", "200", "StepUpGrant", ["OTP_INVALID", "OTP_EXPIRED", "OTP_LOCKED"], "Issue short-lived single-use grant; never accept biometric boolean."),
        "request_account_deletion": ("DeletionRequest", "202", "DeletionStatus", ["CONSENT_VERSION_CHANGED"], "Persist deletion case; retention worker executes reviewed policy."),
        "get_deletion_status": (None, "200", "DeletionStatus", [], "Read current own deletion case, including cancellation eligibility."),
        "cancel_account_deletion": ("VersionCommand", "200", "DeletionStatus", ["DELETION_NOT_CANCELLABLE"], "Cancel only before irreversible phase; preserve case history."),
        "update_profile": ("ProfileUpdate", "200", "UserProfile", [], "Update allowed profile fields; never roles/approval/phone."),
        "set_avatar": ("AvatarUpdate", "200", "UserProfile", ["MEDIA_NOT_READY"], "Use own clean avatar-purpose media or clear reference."),
        "list_devices": (None, "200", "DevicePage", [], "Read owner device metadata, not push credentials."),
        "register_device": ("DeviceCreate", "201", "DeviceSummary", [], "Bind device/push token to current owner; audit owner-safe token reassignment."),
        "rotate_device_token": ("DeviceUpdate", "200", "DeviceSummary", [], "Replace own device delivery token; token never returned in summary."),
        "remove_device": (None, "204", None, [], "Remove owner delivery registration; session revocation is separate."),
        "get_privacy_preferences": (None, "200", "PrivacyPreferences", [], "Read private defaults and current version."),
        "set_privacy_preferences": ("PrivacyUpdate", "200", "PrivacyPreferences", [], "Save consent-sensitive visibility and invalidate relevant cached projections."),
        "get_notification_preferences": (None, "200", "NotificationPreferences", [], "Read channel/category preferences."),
        "set_notification_preferences": ("NotificationPreferencesUpdate", "200", "NotificationPreferences", [], "Validate exactly one of each category; no duplicate category rows."),
        "set_selected_location": ("SelectedLocationUpdate", "200", "SelectedLocation", ["LOCALITY_NOT_FOUND"], "Set discovery locality; never imply pickup serviceability from city selection."),
        "get_current_consent_documents": (None, "200", "ConsentDocuments", [], "Return current published policy versions and integrity metadata."),
        "record_consent": ("ConsentCreate", "201", "ConsentReceipt", ["CONSENT_VERSION_CHANGED"], "Append accepted document revision with server timestamp, not client supplied time."),
    }


def examples():
    profile = {"id": UUID, "first_name": "Example", "last_name": None, "avatar_media_id": None,
               "impact_statement": "", "locale": "en-IN", "profile_complete": True,
               "account_status": "ACTIVE", "version": 1}
    categories = [{"category": category, "push_enabled": True, "quiet_hours_enabled": True}
                  for category in ("contribution", "tracking", "volunteering", "impact", "account")]
    device = {"device_id": DEVICE, "platform": "android", "push_enabled": False,
              "app_version": "0.1.0", "last_seen_at": NOW, "version": 1}
    mobile = {"client_kind": "mobile", "access_token": EXAMPLE_TOKEN, "token_type": "Bearer",
              "access_expires_at": "2026-09-10T12:15:00Z", "refresh_token": EXAMPLE_TOKEN,
              "refresh_expires_at": "2026-10-10T12:00:00Z", "session_id": UUID, "user_id": UUID,
              "profile_complete": True}
    web = {key: value for key, value in mobile.items() if key not in {"refresh_token", "refresh_expires_at"}}
    web["client_kind"] = "web"
    return {
        "OtpRequest": {"phone_e164": "+919000000001", "device_id": DEVICE, "client_kind": "mobile"},
        "OtpChallenge": {"challenge_id": UUID, "expires_at": LATER, "resend_after": "2026-09-10T12:01:00Z", "delivery_status": "accepted", "code_length": 6},
        "OtpVerify": {"challenge_id": UUID, "code": "123456", "device_id": DEVICE, "client_kind": "mobile"},
        "SessionResult": mobile, "MobileSession": mobile, "WebSession": web,
        "RefreshRequest": {"client_kind": "mobile", "device_id": DEVICE, "refresh_token": EXAMPLE_TOKEN},
        "WebRefresh": {"client_kind": "web", "device_id": DEVICE},
        "VersionCommand": {"expected_version": 1},
        "SessionRevocation": {"session_id": UUID, "revoked": True, "version": 2},
        "SessionPage": {"items": [{"session_id": UUID, "device_id": DEVICE, "platform": "android", "created_at": NOW,
                                     "last_seen_at": NOW, "is_current": True, "revoked_at": None, "version": 1}], "next_cursor": None, "has_more": False},
        "StepUpRequest": {"action": "delete_account", "resource_id": UUID, "expected_resource_version": 1},
        "StepUpVerify": {"challenge_id": UUID, "code": "123456"},
        "StepUpGrant": {"grant_token": EXAMPLE_TOKEN, "expires_at": LATER, "action": "delete_account", "resource_id": UUID, "resource_version": 1, "single_use": True},
        "UserProfile": profile, "ProfileUpdate": {"expected_version": 1, "first_name": "Example"},
        "AvatarUpdate": {"expected_version": 1, "media_id": None},
        "DeletionRequest": {"expected_version": 1, "reason": "privacy", "acknowledged_policy_version": "privacy-2026-09"},
        "DeletionStatus": {"id": UUID, "status": "REQUESTED", "requested_at": NOW, "cancellable": True, "completed_at": None,
                           "policy_version": "privacy-2026-09", "version": 1},
        "DeviceCreate": {"device_id": DEVICE, "platform": "android", "push_token": None, "app_version": "0.1.0"},
        "DeviceUpdate": {"expected_version": 1, "push_token": None, "app_version": "0.1.1"}, "DeviceSummary": device,
        "DevicePage": {"items": [device], "next_cursor": None, "has_more": False},
        "PrivacyPreferences": {"profile_public": False, "contributions_public": False, "impact_sharing": False, "version": 1},
        "PrivacyUpdate": {"profile_public": False, "contributions_public": False, "impact_sharing": False, "expected_version": 1},
        "NotificationPreferences": {"categories": categories, "timezone": "Asia/Kolkata", "version": 1},
        "NotificationPreferencesUpdate": {"categories": categories, "expected_version": 1},
        "SelectedLocationUpdate": {"expected_version": 1, "locality_id": UUID, "source": "manual"},
        "SelectedLocation": {"locality_id": UUID, "label": "New Delhi", "city": "Delhi NCR", "in_discovery_area": True,
                             "pickup_serviceability": "requires_address_check", "version": 2},
        "ConsentDocuments": {"items": [{"kind": "privacy", "version": "privacy-2026-09", "effective_at": NOW,
                                         "url": "https://example.invalid/privacy", "sha256": "a" * 64}]},
        "ConsentCreate": {"kind": "privacy", "document_version": "privacy-2026-09", "accepted": True},
        "ConsentReceipt": {"id": UUID, "kind": "privacy", "document_version": "privacy-2026-09", "accepted_at": NOW},
    }
