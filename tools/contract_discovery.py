"""Explicit address/geo, catalogue and discovery contract slice."""

from copy import deepcopy

from contract_identity import BOOL, ID, NOW, TIME, UUID, VERSION, enum, integer, nullable, obj, page, ref, text

HTTPS = text(1, 2048, format="uri", pattern=r"^https://")
QUANTITY = text(1, 18, pattern=r"^(0|[1-9][0-9]{0,11})(\.[0-9]{1,2})?$")
SLUG = text(1, 80, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
COORD = obj({"latitude": {"type": "number", "minimum": -90, "maximum": 90},
             "longitude": {"type": "number", "minimum": -180, "maximum": 180}})


def array(item, maximum=100):
    return {"type": "array", "items": item, "maxItems": maximum}


def schemas():
    s = {}
    address = {"label": text(1, 60), "line1": text(1, 200), "line2": nullable(text(1, 200)),
               "landmark": nullable(text(1, 160)), "city": text(1, 80), "state": text(1, 80),
               "pincode": text(6, 6, pattern=r"^[1-9][0-9]{5}$"), "point": COORD, "is_default": BOOL}
    s["AddressCreate"] = obj(address)
    s["AddressUpdate"] = obj({**address, "expected_version": VERSION}, ["expected_version"], minProperties=2)
    s["Address"] = obj({**address, "id": ID, "version": VERSION})
    s["AddressPage"] = page(ref("Address"))
    s["Locality"] = obj({"id": ID, "label": text(1, 160), "city": text(1, 80), "in_discovery_area": BOOL})
    s["LocalityPage"] = page(ref("Locality"))
    s["ReverseLookup"] = obj({"point": COORD})
    s["ServiceabilityQuery"] = obj({"address_id": ID, "mission_id": ID})
    s["ServiceabilityResult"] = obj({"serviceable": BOOL, "reason": enum("available", "outside_zone", "no_capacity", "mission_closed"),
                                      "checked_at": TIME, "zone_revision": text(1, 64),
                                      "reservation_created": {"type": "boolean", "const": False}},
                                     allOf=[{"if": {"properties": {"serviceable": {"const": True}}},
                                             "then": {"properties": {"reason": {"const": "available"}}},
                                             "else": {"properties": {"reason": enum("outside_zone", "no_capacity", "mission_closed")}}}])
    s["AssignedRouteQuery"] = obj({"assignment_version": VERSION})
    s["AssignedRoute"] = obj({"shipment_id": ID, "assignment_version": VERSION, "expires_at": TIME,
                               "polyline": nullable(text(1, 100000)), "distance_m": nullable(integer(0, 10000000)),
                               "duration_seconds": nullable(integer(0, 604800)), "status": enum("available", "unavailable"),
                               "provider_attribution": text(1, 500)})
    category = {"slug": SLUG, "name": text(1, 80), "description": text(0, 1000), "icon_url": HTTPS,
                "color_token": text(1, 60), "sort_order": integer(0, 10000), "is_active": BOOL}
    subcategory = {"category_id": ID, "slug": SLUG, "name": text(1, 80), "description": text(0, 1000), "is_active": BOOL}
    item = {"category_id": ID, "slug": SLUG, "name": text(1, 80), "default_unit": text(1, 30),
            "accepted_conditions": {**array(enum("NEW", "GOOD", "FAIR"), 3), "uniqueItems": True, "minItems": 1}, "is_active": BOOL}
    synonym = {"term": text(1, 100), "category_id": ID, "subcategory_id": nullable(ID)}
    for name, fields in [("Category", category), ("Subcategory", subcategory), ("ItemType", item), ("Synonym", synonym)]:
        s[name] = obj({**fields, "id": ID, "version": VERSION})
        s[name + "Create"] = obj(fields)
        s[name + "Update"] = obj({**fields, "expected_version": VERSION}, ["expected_version"], minProperties=2)
        s[name + "Page"] = page(ref(name))
    s["CatalogueAdminEntry"] = {"oneOf": [obj({"kind": {"type": "string", "const": name.lower()}, "value": ref(name)})
                                                     for name in ("Category", "Subcategory", "ItemType", "Synonym")]}
    s["CatalogueAdminPage"] = page(ref("CatalogueAdminEntry"))
    s["PublicMedia"] = obj({"url": HTTPS, "alt": text(1, 240), "width": integer(1, 10000), "height": integer(1, 10000)})
    s["PublicOrganization"] = obj({"id": ID, "name": text(1, 160), "description": text(0, 4000),
                                    "org_type": enum("NGO", "TRUST", "SOCIETY", "SECTION_8", "COMMUNITY_GROUP", "SCHOOL", "OTHER"), "website": nullable(HTTPS),
                                    "logo": nullable(ref("PublicMedia")), "verification": enum("verified", "expired", "suspended", "not_verified"),
                                    "location_name": text(1, 160), "missions_completed": integer()})
    s["OrganizationPage"] = page(ref("PublicOrganization"))
    s["NeedAvailability"] = {"oneOf": [
        obj({"type": {"type": "string", "const": "MONEY"}, "need_id": ID, "target_paise": integer(1, 9007199254740991),
             "confirmed_paise": integer(0, 9007199254740991), "available_paise": integer(0, 9007199254740991),
             "currency": enum("INR"), "accepting": BOOL}),
        obj({"type": {"type": "string", "const": "ITEM"}, "need_id": ID, "item_type_id": ID, "label": text(1, 120),
             "target_quantity": QUANTITY, "confirmed_quantity": QUANTITY, "available_quantity": QUANTITY,
             "unit": text(1, 30), "accepting": BOOL}),
        obj({"type": {"type": "string", "const": "TIME"}, "need_id": ID, "slots_total": integer(),
             "slots_available": integer(), "accepting": BOOL}),
    ], "discriminator": {"propertyName": "type"}}
    card = {"id": ID, "title": text(1, 90), "summary": text(0, 300), "organization": ref("PublicOrganization"),
            "category_id": ID, "subcategory_id": nullable(ID), "location_name": text(1, 160), "hero": nullable(ref("PublicMedia")),
            "status": enum("PUBLISHED", "FUNDING", "RECRUITING", "ACTIVE", "READY", "IN_PROGRESS", "DELIVERED", "VERIFICATION", "COMPLETED", "PAUSED", "CANCELLED", "FAILED", "EXPIRED", "DISPUTED"),
            "urgency": enum("URGENT", "THIS_WEEK", "FLEXIBLE"), "deadline_at": nullable(TIME),
            "needs": array(ref("NeedAvailability"), 50), "version": VERSION}
    s["MissionCard"] = obj(card)
    s["MissionPage"] = page(ref("MissionCard"))
    s["MissionDetail"] = obj({**card, "story": text(1, 20000), "gallery": array(ref("PublicMedia"), 20),
                               "allow_partial": BOOL, "fee_disclosure": text(1, 500), "proof_requirements_summary": text(1, 1000)})
    s["MissionUpdate"] = obj({"id": ID, "mission_id": ID, "body": text(1, 4000), "media": array(ref("PublicMedia"), 10), "published_at": TIME})
    s["MissionUpdatePage"] = page(ref("MissionUpdate"))
    s["PublicProof"] = obj({"id": ID, "mission_id": ID, "review_label": enum("Verified"),
                             "redacted_media": array(ref("PublicMedia"), 20), "summary": text(1, 1000), "verified_at": TIME})
    s["PublicProofPage"] = page(ref("PublicProof"))
    s["HomeModule"] = {"oneOf": [
        obj({"key": enum("nearby", "urgent", "picks", "weekend", "completed", "highlight"), "status": enum("ready"), "missions": array(ref("MissionCard"), 20), "next_cursor": nullable(text(1, 2048)), "has_more": BOOL}),
        obj({"key": enum("categories"), "status": enum("ready"), "categories": array(ref("Category"), 50), "next_cursor": nullable(text(1, 2048)), "has_more": BOOL}),
        obj({"key": enum("organizations"), "status": enum("ready"), "organizations": array(ref("PublicOrganization"), 20), "next_cursor": nullable(text(1, 2048)), "has_more": BOOL}),
        obj({"key": enum("nearby", "urgent", "picks", "weekend", "completed", "highlight", "categories", "organizations"),
             "status": enum("unavailable", "empty"), "message": text(1, 200)}),
    ]}
    s["PublicHome"] = obj({"locality_id": nullable(ID), "generated_at": TIME, "modules": array(ref("HomeModule"), 8)})
    s["PersonalHome"] = obj({"generated_at": TIME, "active_contributions": array(obj({"id": ID, "mission_id": ID,
                                "title": text(1, 90), "summary_status": enum("pending", "active", "needs_attention"), "version": VERSION}), 20)})
    s["SearchHit"] = {"oneOf": [obj({"kind": enum(kind), "value": ref(name)}) for kind, name in
                                  [("mission", "MissionCard"), ("organization", "PublicOrganization"), ("category", "Category")]]}
    s["SearchPage"] = page(ref("SearchHit"))
    s["Suggestion"] = obj({"text": text(1, 120), "kind": enum("query", "category", "organization"), "target_id": nullable(ID)})
    s["SuggestionPage"] = page(ref("Suggestion"))
    s["DiscoveryFilters"] = obj({"contribution_types": array(enum("MONEY", "ITEM", "TIME"), 3),
                                   "sorts": array(enum("relevance", "nearest", "urgent", "recent"), 4),
                                   "categories": array(ref("Category"), 100), "default_radius_km": integer(1, 50)})
    s["Bookmark"] = obj({"mission_id": ID, "created_at": TIME, "version": VERSION})
    s["BookmarkPage"] = page(obj({"bookmark": ref("Bookmark"), "mission": nullable(ref("MissionCard")),
                                  "availability": enum("available", "unavailable")}))
    s["ShareMetadata"] = obj({"title": text(1, 200), "description": text(1, 500), "canonical_url": HTTPS,
                               "image": nullable(ref("PublicMedia"))})
    return s


def definitions():
    # Exact operations: no fabricated web/app-association or wildcard schemas.
    operations = {
        "list_addresses": (None, "200", "AddressPage", [], "List only current owner's addresses."),
        "create_address": ("AddressCreate", "201", "Address", [], "Bind address to principal; serialize default-address choice."),
        "update_address": ("AddressUpdate", "200", "Address", [], "Update owned address; active shipments retain their reviewed address revision."),
        "delete_address": (None, "204", None, ["ADDRESS_IN_USE"], "Logical removal under retention; do not erase active custody destination."),
        "set_default_address": ("VersionCommand", "200", "Address", [], "Select one default under owner lock."),
        "search_localities": (None, "200", "LocalityPage", [], "Provider-backed locality search; no pickup approval inferred."),
        "reverse_lookup": ("ReverseLookup", "200", "Locality", [], "Scoped coordinate lookup with provider caching/retention limits."),
        "check_serviceability": ("ServiceabilityQuery", "200", "ServiceabilityResult", [], "Check exact owned address and mission zone; creates no reservation."),
        "get_assigned_route": ("AssignedRouteQuery", "200", "AssignedRoute", ["ASSIGNMENT_ACCESS_EXPIRED"], "Current assignment and window only; route data stays private."),
        "list_categories": (None, "200", "CategoryPage", [], "Return active public catalogue entries."),
        "get_category": (None, "200", "Category", [], "Return one active category."),
        "list_subcategories": (None, "200", "SubcategoryPage", [], "Only active children of selected category."),
        "list_item_types": (None, "200", "ItemTypePage", [], "Active accepted-condition metadata; not operational acceptance of offered items."),
        "get_catalogue_admin": (None, "200", "CatalogueAdminPage", [], "Scoped active/inactive catalogue metadata."),
        "list_synonyms": (None, "200", "SynonymPage", [], "Scoped search synonym maintenance view."),
        "remove_synonym": (None, "204", None, [], "Remove synonym mapping; invalidate search configuration."),
        "get_home": (None, "200", "PublicHome", [], "Compose independent public modules; owner activity excluded."),
        "get_personal_home_modules": (None, "200", "PersonalHome", [], "Read private owner activity; no shared-city cache."),
        "list_missions": (None, "200", "MissionPage", [], "Filter visible missions; per-need availability stays independent."),
        "get_mission": (None, "200", "MissionDetail", [], "Public-safe detail, never editor/private review fields."),
        "list_mission_updates": (None, "200", "MissionUpdatePage", [], "Published moderated updates only."),
        "list_public_proof_derivatives": (None, "200", "PublicProofPage", [], "Only consented reviewed redacted public derivatives."),
        "get_public_organization": (None, "200", "PublicOrganization", [], "Public org profile without registration/bank/private documents."),
        "list_organization_missions": (None, "200", "MissionPage", [], "Only public missions of selected organization."),
        "search": (None, "200", "SearchPage", [], "Stable mixed-kind result cursor; client may group visible result types."),
        "suggest_search": (None, "200", "SuggestionPage", [], "Public query/category/org suggestions; no donor-spend ranking."),
        "get_discovery_filters": (None, "200", "DiscoveryFilters", [], "Data-driven filter metadata; city radius is not pickup service area."),
        "list_bookmarks": (None, "200", "BookmarkPage", [], "Owner bookmarks retain unavailable marker for hidden/deleted mission."),
        "save_bookmark": (None, "201", "Bookmark", [], "Idempotent owner/mission bookmark; unique pair."),
        "remove_bookmark": (None, "204", None, [], "Remove owner's bookmark only."),
        "get_mission_share_metadata": (None, "200", "ShareMetadata", [], "Public mission link metadata; no contribution amount/identity."),
        "get_org_share_metadata": (None, "200", "ShareMetadata", [], "Public org link metadata; no bank/doc data."),
    }
    for suffix, schema in [("category", "Category"), ("subcategory", "Subcategory"), ("item_type", "ItemType"), ("synonym", "Synonym")]:
        operations["create_" + suffix] = (schema + "Create", "201", schema, [], "Create scoped catalogue entry; audited configuration change.")
        update_id = "set_synonym" if suffix == "synonym" else "update_" + suffix
        operations[update_id] = (schema + "Update", "200", schema, [], "Versioned catalogue edit; preserve referenced historical labels/revisions.")
    return operations


def parameters():
    def query(name, schema, required=False):
        return {"name": name, "in": "query", "required": required, "schema": schema}
    search = [query("q", text(1, 200), True)]
    filters = [query("category", ID), query("subcategory", ID), query("contribution_type", enum("MONEY", "ITEM", "TIME")),
               query("locality_id", ID), query("radius_km", integer(1, 50)), query("sort", enum("relevance", "nearest", "urgent", "recent")),
               query("verified_only", BOOL), query("urgency", enum("URGENT", "THIS_WEEK", "FLEXIBLE")),
               query("status", enum("PUBLISHED", "FUNDING", "RECRUITING", "ACTIVE", "READY", "IN_PROGRESS", "DELIVERED", "VERIFICATION", "COMPLETED", "PAUSED", "CANCELLED", "FAILED", "EXPIRED", "DISPUTED")),
               query("organization_type", enum("NGO", "TRUST", "SOCIETY", "SECTION_8", "COMMUNITY_GROUP", "SCHOOL", "OTHER")),
               query("lat", COORD["properties"]["latitude"]), query("lng", COORD["properties"]["longitude"]),
               query("min_amount_paise", integer(0, 9007199254740991)), query("max_amount_paise", integer(0, 9007199254740991))]
    return {"search": search + filters, "suggest_search": search, "search_localities": search,
            "list_missions": filters, "list_organization_missions": filters,
            "get_home": [query("locality_id", ID), query("lat", COORD["properties"]["latitude"]), query("lng", COORD["properties"]["longitude"]),
                         query("module", enum("nearby", "urgent", "picks", "weekend", "completed", "highlight", "categories", "organizations")),
                         query("cursor", text(1, 2048)), query("limit", integer(1, 50))],
            "list_item_types": [query("category_id", ID)]}


def examples():
    media = {"url": "https://example.invalid/public/image.webp", "alt": "Consented illustrative mission image", "width": 800, "height": 600}
    category = {"id": UUID, "slug": "education", "name": "Education", "description": "School supplies and learning",
                "icon_url": "https://example.invalid/icons/education.svg", "color_token": "category.education",
                "sort_order": 1, "is_active": True, "version": 1}
    subcategory = {"id": UUID, "category_id": UUID, "slug": "school-supplies", "name": "School supplies", "description": "Supplies", "is_active": True, "version": 1}
    item = {"id": UUID, "category_id": UUID, "slug": "books", "name": "Books", "default_unit": "pcs", "accepted_conditions": ["NEW", "GOOD"], "is_active": True, "version": 1}
    synonym = {"id": UUID, "term": "books", "category_id": UUID, "subcategory_id": None, "version": 1}
    org = {"id": UUID, "name": "Example Delhi Organization", "description": "Synthetic demonstration organization", "logo": None, "org_type": "NGO", "website": None,
           "verification": "verified", "location_name": "Delhi NCR", "missions_completed": 0}
    need = {"type": "MONEY", "need_id": UUID, "target_paise": 100000, "confirmed_paise": 25000, "available_paise": 75000, "currency": "INR", "accepting": True}
    mission = {"id": UUID, "title": "Books for Delhi students", "summary": "Support a quantified school need", "organization": org,
               "category_id": UUID, "subcategory_id": None, "location_name": "New Delhi", "hero": media, "status": "ACTIVE",
               "urgency": "FLEXIBLE", "deadline_at": "2026-10-10T12:00:00Z", "needs": [need,
                   {"type": "ITEM", "need_id": "33333333-3333-4333-8333-333333333333", "item_type_id": UUID,
                    "label": "Books", "target_quantity": "120", "confirmed_quantity": "40", "available_quantity": "80", "unit": "pcs", "accepting": True},
                   {"type": "TIME", "need_id": "44444444-4444-4444-8444-444444444444", "slots_total": 10, "slots_available": 2, "accepting": True}], "version": 1}
    address = {"id": UUID, "label": "Home", "line1": "Example pickup address", "line2": None, "landmark": None,
               "city": "New Delhi", "state": "Delhi", "pincode": "110001", "point": {"latitude": 28.6139, "longitude": 77.209}, "is_default": True, "version": 1}
    locality = {"id": UUID, "label": "New Delhi", "city": "Delhi NCR", "in_discovery_area": True}
    proof = {"id": UUID, "mission_id": UUID, "review_label": "Verified", "redacted_media": [media], "summary": "Synthetic verified proof example", "verified_at": NOW}
    e = {"Address": address, "AddressCreate": {k: v for k, v in address.items() if k not in {"id", "version"}},
         "AddressUpdate": {"expected_version": 1, "label": "Pickup"}, "Locality": locality,
         "ReverseLookup": {"point": address["point"]}, "ServiceabilityQuery": {"address_id": UUID, "mission_id": UUID},
         "ServiceabilityResult": {"serviceable": True, "reason": "available", "checked_at": NOW, "zone_revision": "draft-zone-1", "reservation_created": False},
         "AssignedRouteQuery": {"assignment_version": 1}, "AssignedRoute": {"shipment_id": UUID, "assignment_version": 1, "expires_at": "2026-09-10T12:01:00Z",
             "polyline": None, "distance_m": None, "duration_seconds": None, "status": "unavailable", "provider_attribution": "Provider unavailable"},
         "PublicOrganization": org, "MissionCard": mission, "NeedAvailability": need,
         "MissionDetail": {**mission, "story": "Synthetic example of a quantified need.", "gallery": [], "allow_partial": True,
                           "fee_disclosure": "Gateway fee covered by NEKI", "proof_requirements_summary": "Delivery receipt and reviewed evidence"},
         "MissionUpdate": {"id": UUID, "mission_id": UUID, "body": "Supplies being prepared", "media": [], "published_at": NOW},
         "PublicProof": proof, "PublicHome": {"locality_id": UUID, "generated_at": NOW, "modules": [{"key": "nearby", "status": "ready", "missions": [mission], "next_cursor": None, "has_more": False}]},
         "PersonalHome": {"generated_at": NOW, "active_contributions": [{"id": UUID, "mission_id": UUID, "title": mission["title"], "summary_status": "pending", "version": 1}]},
         "SearchHit": {"kind": "mission", "value": mission}, "Suggestion": {"text": "books", "kind": "query", "target_id": None},
         "DiscoveryFilters": {"contribution_types": ["MONEY", "ITEM", "TIME"], "sorts": ["relevance", "nearest", "urgent", "recent"], "categories": [category], "default_radius_km": 50},
         "Bookmark": {"mission_id": UUID, "created_at": NOW, "version": 1},
         "ShareMetadata": {"title": mission["title"], "description": mission["summary"], "canonical_url": "https://example.invalid/m/example", "image": media}}
    for name, value in [("Category", category), ("Subcategory", subcategory), ("ItemType", item), ("Synonym", synonym)]:
        e[name] = value
        e[name + "Create"] = {k: v for k, v in value.items() if k not in {"id", "version"}}
        e[name + "Update"] = {"expected_version": 1, **e[name + "Create"]}
    e["CatalogueAdminEntry"] = {"kind": "category", "value": category}
    for name, item_name in [("AddressPage", "Address"), ("LocalityPage", "Locality"), ("CategoryPage", "Category"),
                            ("SubcategoryPage", "Subcategory"), ("ItemTypePage", "ItemType"), ("SynonymPage", "Synonym"),
                            ("CatalogueAdminPage", "CatalogueAdminEntry"), ("OrganizationPage", "PublicOrganization"),
                            ("MissionPage", "MissionCard"), ("MissionUpdatePage", "MissionUpdate"), ("PublicProofPage", "PublicProof"),
                            ("SearchPage", "SearchHit"), ("SuggestionPage", "Suggestion")]:
        e[name] = {"items": [deepcopy(e[item_name])], "next_cursor": None, "has_more": False}
    e["BookmarkPage"] = {"items": [{"bookmark": e["Bookmark"], "mission": mission, "availability": "available"}], "next_cursor": None, "has_more": False}
    return e


def negative_cases():
    e = examples()
    cases = []
    for schema, key, value, reason in [
        ("MissionCard", "pickup_address", "private", "public pickup address"),
        ("MissionCard", "donor_user_id", UUID, "public donor identity"),
        ("PublicOrganization", "settlement_bank_ref", "private", "public bank reference"),
        ("PublicProof", "exif_point", {"latitude": 28.6, "longitude": 77.2}, "public capture GPS"),
        ("PublicProof", "review_label", "Under Review", "unreviewed public proof"),
        ("PublicHome", "active_contributions", [], "private module in public Home"),
        ("AddressCreate", "user_id", UUID, "address ownership injection"),
        ("AddressCreate", "pincode", "011000", "invalid pincode"),
        ("ServiceabilityResult", "reservation_created", True, "lookup treated as reservation"),
        ("ServiceabilityResult", "reason", "outside_zone", "contradictory serviceability"),
        ("NeedAvailability", "available_paise", -1, "negative remaining money"),
        ("NeedAvailability", "available_paise", 1.2, "fractional paise"),
        ("NeedAvailability", "currency", "USD", "non-INR need"),
        ("CategoryCreate", "slug", "Bad Slug", "invalid catalogue slug"),
        ("AddressUpdate", "expected_version", -1, "negative address version"),
    ]:
        value_doc = deepcopy(e[schema]); value_doc[key] = value
        cases.append((schema, value_doc, reason))
    cases.append(("ReverseLookup", {"point": {"latitude": 91, "longitude": 77}}, "latitude outside Earth"))
    cases.append(("ReverseLookup", {"point": {"latitude": 28, "longitude": -181}}, "longitude outside Earth"))
    cases.append(("CategoryUpdate", {"expected_version": 1}, "empty category patch"))
    return cases
