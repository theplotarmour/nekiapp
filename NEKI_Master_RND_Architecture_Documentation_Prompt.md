# NEKI --- Master R&D, Architecture & Product Documentation Prompt

## Purpose

You are the principal software architect, mobile product engineer,
backend architect, UX systems designer, security engineer, QA lead,
DevOps engineer, and technical researcher for **NEKI --- Humanity,
Delivered.**

Your task is **not** to immediately start coding.

Your first responsibility is to produce an extremely detailed,
implementation-ready documentation system for the NEKI iOS + Android
application and its supporting platform.

The app should deliver the **speed, density, interaction quality,
operational clarity, marketplace structure, tracking experience, and
polish associated with leading quick-commerce/delivery applications such
as Blinkit**, while being an original NEKI product. Do **not** copy
proprietary source code, private APIs, copyrighted assets, trademarks,
or exact proprietary visual designs. Study publicly available patterns
and open-source implementations only, then adapt the underlying
engineering ideas into an original NEKI experience.

The product vision is:

> **NEKI --- Humanity, Delivered.**

Primary promise:

> **Track every contribution. Verify every mission. See every impact.**

Core product thesis:

> NEKI is a marketplace and coordination layer for social impact:
> organizations publish specific missions and needs; individuals,
> volunteers and businesses contribute money, goods, time or skills;
> NEKI coordinates execution, tracking, proof and impact.

The strategic expansion notes describe NEKI as potentially evolving from
a donation platform into a **trust and coordination layer**, with an
NGO/project marketplace, "Give Anything," a "Neki Impact Ledger,"
corporate surplus, employee volunteering, Neki Drives, a corporate/CSR
product and eventually an enterprise operating system for social impact.
Preserve these ideas, but distinguish clearly between current MVP scope,
validated future opportunities, and speculative long-term concepts.

------------------------------------------------------------------------

# 1. NON-NEGOTIABLE WORKING PRINCIPLES

## 1.1 Research before implementation

Do not start by generating a large amount of application code.

First:

1.  Inspect the existing repository.
2.  Identify what is reusable.
3.  Identify the current stack.
4.  Identify technical debt.
5.  Inspect existing assets and generated media.
6.  Research relevant open-source repositories.
7.  Compare architecture approaches.
8.  Document decisions.
9.  Define MVP boundaries.
10. Produce implementation tickets.
11. Only then implement.

Every major architectural decision must have a documented reason.

------------------------------------------------------------------------

## 1.2 Do not blindly copy an open-source repository

Open-source projects are for R&D and adaptation.

For every repository studied:

-   inspect license;
-   inspect architecture;
-   inspect dependency choices;
-   inspect project structure;
-   inspect testing strategy;
-   inspect networking;
-   inspect state management;
-   inspect caching;
-   inspect navigation;
-   inspect UI composition;
-   inspect delivery/tracking logic;
-   identify what is reusable conceptually;
-   identify what should NOT be copied;
-   identify license obligations.

Never paste an entire repository into NEKI merely because it looks
similar.

------------------------------------------------------------------------

## 1.3 NEKI must be original

The goal is:

> **Blinkit-level product quality, not a Blinkit counterfeit.**

Use familiar marketplace patterns where appropriate:

-   location-first discovery;
-   search;
-   category browsing;
-   dense cards;
-   bottom navigation;
-   sticky CTAs;
-   progressive disclosure;
-   fast checkout/contribution;
-   real-time tracking;
-   persistent status;
-   contextual notifications;
-   operational dashboards.

But create an original NEKI design system, information architecture,
terminology, assets, illustrations, animations and brand expression.

------------------------------------------------------------------------

## 1.4 Do not over-engineer prematurely

The initial backend should preferably be a:

> **Modular monolith**

rather than a collection of microservices.

Use clear domain boundaries so services can be extracted later.

Do not introduce:

-   Kubernetes;
-   Kafka;
-   Elasticsearch/OpenSearch;
-   dozens of microservices;
-   complex ML infrastructure;

unless documentation demonstrates a real requirement.

Start simple and design for extraction.

------------------------------------------------------------------------

# 2. SOURCE-OF-TRUTH PRODUCT CONTEXT

The following concepts come from the internal NEKI strategic expansion
notes and must be treated as the current strategic context, not as proof
that every feature is already built.

## 2.1 Individuals can contribute

Potential contribution types:

-   money;
-   books;
-   clothes;
-   food;
-   furniture;
-   electronics;
-   school supplies;
-   time;
-   volunteering;
-   skills.

Core experience:

> "I have this. Who needs it?"

NEKI should eventually match available resources with verified
organizations or communities.

------------------------------------------------------------------------

## 2.2 Organizations

Organizations may publish concrete needs instead of vague donation
requests.

Examples:

-   500 books required;
-   10 laptops required;
-   2,000 meals required;
-   school kit drive;
-   first aid camp;
-   animal shelter support;
-   volunteer requirement;
-   mentorship requirement.

The product should model these as **missions** or **needs**, not simply
NGO profiles.

------------------------------------------------------------------------

## 2.3 Neki Impact Ledger

Every meaningful contribution should eventually have a digital record.

Conceptual example:

``` text
NEKI ID
#NEK48291

Contribution
120 books

Contributor
XYZ Pvt Ltd

Organization
ABC Foundation

Location
Delhi

Beneficiaries
87 students

Delivered
24 Aug 2026

Proof
Photos + acknowledgement

Impact
87 students received educational material
```

The ledger should become a first-class domain object.

Do not fabricate impact numbers.

------------------------------------------------------------------------

## 2.4 Give Anything

Potential flow:

``` text
User selects:
Books

Uploads:
Photo

Quantity:
150

Condition:
Good

Location:
South Delhi

NEKI:
3 organizations currently need what you have.
```

This should be documented as a future/high-value feature even if not
part of MVP.

------------------------------------------------------------------------

## 2.5 Corporate surplus

Potential flow:

``` text
Company
  ↓
NEKI
  ↓
Verified organization/community
  ↓
Pickup
  ↓
Delivery
  ↓
Verification
  ↓
Impact report
```

Potential surplus:

-   laptops;
-   furniture;
-   stationery;
-   uniforms;
-   excess inventory;
-   educational material;
-   food;
-   clothes;
-   infrastructure-related items.

------------------------------------------------------------------------

## 2.6 Employee volunteering

Potential flow:

``` text
Company has 25 employees
        ↓
NEKI finds opportunities
        ↓
Teach English
Career mentoring
Tree plantation
Digital literacy
Financial literacy
        ↓
Attendance
        ↓
Volunteer hours
        ↓
Verified impact
```

------------------------------------------------------------------------

## 2.7 Neki Drives

Campaign-level missions can connect:

-   companies;
-   colleges;
-   schools;
-   individuals;
-   creators;
-   NGOs;
-   communities.

Examples:

-   Neki Back-to-School Drive;
-   Neki Winter Drive;
-   Neki Digital Drive;
-   Neki School Drive;
-   Neki Food Drive;
-   Neki Festival Drive.

The documentation must explain how campaign objects relate to missions.

------------------------------------------------------------------------

## 2.8 Trust layer

NEKI's long-term differentiation should be a trust/coordination layer.

Potential organization verification:

-   registration;
-   applicable tax/charitable status;
-   track record;
-   projects;
-   location;
-   beneficiary information;
-   documentation.

Potential contribution verification:

-   what was given;
-   who received it;
-   when;
-   where;
-   proof.

Potential impact verification:

-   beneficiaries;
-   photos;
-   documents;
-   delivery confirmation;
-   project completion.

Never claim a verification standard that has not actually been
implemented.

------------------------------------------------------------------------

## 2.9 Enterprise / CSR

Long-term corporate dashboard concepts:

``` text
CSR
Budget
Projects
NGOs
Utilization
Impact

Donations
Money
Products
Surplus

Employees
Volunteers
Hours
Activities

Reports
Impact
Beneficiaries
Documentation
Annual reporting support
```

The long-term positioning can become:

> **The operating system for corporate social impact.**

But do not represent NEKI itself as a statutory CSR implementing agency
unless its legal structure and eligibility support that claim.

------------------------------------------------------------------------

# 3. DOCUMENTATION DELIVERABLE

Before major implementation, create a `/docs` system with at least the
following:

``` text
docs/
├── 00-project-overview.md
├── 01-product-requirements.md
├── 02-product-principles.md
├── 03-mvp-scope.md
├── 04-future-roadmap.md
├── 05-user-personas.md
├── 06-user-journeys.md
├── 07-information-architecture.md
├── 08-mobile-ux-specification.md
├── 09-design-system.md
├── 10-animation-system.md
├── 11-accessibility.md
├── 12-architecture.md
├── 13-domain-model.md
├── 14-database-schema.md
├── 15-api-contracts.md
├── 16-realtime-system.md
├── 17-location-and-maps.md
├── 18-payments.md
├── 19-media-and-proof.md
├── 20-notifications.md
├── 21-search-and-discovery.md
├── 22-feed-ranking.md
├── 23-impact-ledger.md
├── 24-verification-and-trust.md
├── 25-organization-platform.md
├── 26-corporate-platform.md
├── 27-admin-operations.md
├── 28-security.md
├── 29-privacy-and-data.md
├── 30-offline-first.md
├── 31-testing-strategy.md
├── 32-performance.md
├── 33-observability.md
├── 34-devops.md
├── 35-ci-cd.md
├── 36-app-store-release.md
├── 37-rnd-open-source-review.md
├── 38-adr/
├── 39-api-examples/
├── 40-state-machines/
├── 41-diagrams/
└── 42-implementation-plan.md
```

------------------------------------------------------------------------

# 4. `00-project-overview.md`

Document:

-   what NEKI is;
-   who it serves;
-   problem;
-   product thesis;
-   brand promise;
-   current business model;
-   current MVP;
-   long-term vision;
-   platform surfaces;
-   constraints;
-   non-goals.

Include a clear distinction:

``` text
NOW
MVP
NEXT
LATER
EXPERIMENTAL
```

Do not mix speculative features with launch requirements.

------------------------------------------------------------------------

# 5. PRODUCT REQUIREMENTS

Create detailed functional requirements.

Every feature must include:

``` text
Feature
Purpose
User
Preconditions
Primary flow
Alternative flows
Error states
Loading states
Empty states
Offline behavior
Permissions
Analytics events
Backend dependencies
Security considerations
Acceptance criteria
Tests
```

Example:

## Mission Contribution

``` text
User opens mission
↓
Reviews requirement
↓
Selects contribution amount/resource
↓
Reviews summary
↓
Confirms
↓
Payment/resource confirmation
↓
Mission contribution created
↓
Receipt
↓
Mission tracking
↓
Impact history
```

Document every state.

------------------------------------------------------------------------

# 6. USER TYPES

At minimum document:

## Contributor

Wants to:

-   discover;
-   contribute;
-   track;
-   see proof;
-   build impact history.

## Volunteer

Wants to:

-   discover opportunities;
-   accept missions;
-   navigate;
-   update status;
-   upload proof;
-   receive verified hours.

## Organization

Wants to:

-   create missions;
-   receive resources;
-   recruit volunteers;
-   coordinate execution;
-   submit proof;
-   see impact.

## Corporate

Wants to:

-   run programs;
-   allocate budgets;
-   coordinate employees;
-   donate surplus;
-   monitor utilization;
-   produce reports.

## Operations/Admin

Wants to:

-   review organizations;
-   review missions;
-   intervene in failed missions;
-   resolve disputes;
-   verify evidence;
-   monitor platform health.

------------------------------------------------------------------------

# 7. MOBILE INFORMATION ARCHITECTURE

Use a fast, marketplace-like architecture.

Suggested primary navigation:

``` text
Home
Missions
Track
Impact
Profile
```

Document whether this remains optimal after research.

Home should include:

-   location;
-   notifications;
-   search;
-   category shortcuts;
-   nearby missions;
-   urgent missions;
-   recommended missions;
-   volunteering;
-   campaigns;
-   recent impact;
-   personalized discovery.

Do not create a giant marketing homepage inside the app.

The app is a product.

------------------------------------------------------------------------

# 8. MISSION AS THE CORE DOMAIN OBJECT

Define Mission in depth.

Suggested attributes:

``` text
id
public_id
organization_id
campaign_id
title
description
category
mission_type
location
service_area
goal_type
target_quantity
fulfilled_quantity
target_amount
raised_amount
volunteer_slots
filled_slots
priority
urgency
status
start_at
deadline_at
created_at
published_at
completed_at
verification_status
proof_status
visibility
```

Also document:

-   mission requirements;
-   contribution types;
-   volunteer requirements;
-   proof requirements;
-   cancellation;
-   expiration;
-   partial completion;
-   recurring missions;
-   campaign membership.

------------------------------------------------------------------------

# 9. STATE MACHINES

Create explicit state diagrams.

## Mission

``` text
DRAFT
↓
PENDING_REVIEW
↓
PUBLISHED
↓
FUNDING / RECRUITING
↓
READY
↓
ASSIGNED
↓
IN_PROGRESS
↓
DELIVERED
↓
VERIFICATION
↓
COMPLETED
```

Include:

``` text
PAUSED
CANCELLED
FAILED
REJECTED
EXPIRED
DISPUTED
```

Document legal transitions.

------------------------------------------------------------------------

# 10. TRACKING STATE MACHINE

For physical/resource missions:

``` text
CREATED
↓
VOLUNTEER_ASSIGNED
↓
PICKUP_READY
↓
PICKED_UP
↓
IN_TRANSIT
↓
ARRIVED
↓
DELIVERED
↓
VERIFIED
```

Every transition must produce an event.

------------------------------------------------------------------------

# 11. EVENT MODEL

Use domain events.

Examples:

``` text
MissionCreated
MissionPublished
MissionContributionCreated
PaymentAuthorized
PaymentCaptured
VolunteerAssigned
PickupStarted
PickupCompleted
DeliveryStarted
DeliveryCompleted
ProofUploaded
VerificationRequested
MissionVerified
MissionCompleted
ImpactRecordCreated
```

Document:

-   producer;
-   payload;
-   consumers;
-   retry policy;
-   idempotency;
-   ordering requirements;
-   dead-letter behavior.

------------------------------------------------------------------------

# 12. MOBILE ARCHITECTURE

Preferred starting point:

**Flutter + Dart**

Architecture:

``` text
Presentation
    ↓
Application / Use Cases
    ↓
Domain
    ↓
Repository Interfaces
    ↓
Data Sources
```

Feature-first organization.

Example:

``` text
features/
  missions/
    data/
    domain/
    presentation/
```

Do not let UI widgets call HTTP directly.

------------------------------------------------------------------------

# 13. STATE MANAGEMENT

Evaluate:

-   Riverpod;
-   BLoC/Cubit;
-   other serious Flutter approaches.

The default recommendation to investigate is **Riverpod**, but document
the reasoning rather than assuming it.

Requirements:

-   predictable state;
-   minimal rebuilds;
-   testability;
-   lifecycle awareness;
-   offline synchronization;
-   realtime streams;
-   optimistic updates where safe.

------------------------------------------------------------------------

# 14. LOCAL DATA

Document what must be cached locally.

Likely:

-   authentication/session state;
-   user profile;
-   location;
-   saved missions;
-   recent missions;
-   active mission state;
-   pending uploads;
-   pending field updates;
-   notification state.

For field operations, design an offline queue:

``` text
LOCAL ACTION
↓
PENDING
↓
UPLOAD
↓
SERVER ACK
↓
SYNCED
```

Handle retries and conflicts.

------------------------------------------------------------------------

# 15. BACKEND ARCHITECTURE

Recommended initial architecture:

``` text
FastAPI
Modular Monolith
```

Domains:

``` text
auth
users
organizations
missions
contributions
payments
volunteers
dispatch
tracking
verification
impact
campaigns
notifications
search
analytics
corporate
admin
```

Document boundaries and extraction criteria.

------------------------------------------------------------------------

# 16. DATABASE

Preferred:

**PostgreSQL + PostGIS**

Document:

-   tables;
-   primary keys;
-   foreign keys;
-   indexes;
-   constraints;
-   enums;
-   soft deletes;
-   audit records;
-   timestamps;
-   geospatial indexes.

Do not store media blobs in PostgreSQL.

------------------------------------------------------------------------

# 17. CACHE / REALTIME

Evaluate:

**Redis**

for:

-   cache;
-   rate limiting;
-   ephemeral location state;
-   queues;
-   pub/sub;
-   realtime coordination.

Use WebSockets where live state genuinely matters.

Document fallback polling.

------------------------------------------------------------------------

# 18. MEDIA / PROOF

Design:

``` text
Flutter
↓
Signed upload URL
↓
Object storage
↓
Image/video processing
↓
CDN
↓
Proof record
```

Document:

-   compression;
-   thumbnails;
-   EXIF handling;
-   privacy;
-   upload retry;
-   malware scanning where appropriate;
-   access control;
-   signed URLs;
-   deletion;
-   retention.

------------------------------------------------------------------------

# 19. LOCATION

Document:

-   foreground permission;
-   background permission;
-   approximate location;
-   precise location;
-   volunteer tracking;
-   organization locations;
-   mission locations;
-   privacy;
-   battery usage;
-   update frequency;
-   geofencing;
-   spoofing considerations.

Never collect continuous location merely because it is technically
possible.

------------------------------------------------------------------------

# 20. MAP UX

Map experiences:

### Nearby missions

### Active volunteer mission

### Contribution delivery

### Organization location

### Campaign geography

Document:

-   marker clustering;
-   route rendering;
-   marker animations;
-   map loading;
-   fallback when map unavailable.

------------------------------------------------------------------------

# 21. SEARCH

Search should support:

``` text
mission
organization
category
location
resource
skill
campaign
```

Example:

> "books near me"

should be able to produce relevant missions.

Document ranking.

------------------------------------------------------------------------

# 22. FEED / DISCOVERY

Create a dedicated feed specification.

Initial ranking can use deterministic signals:

``` text
distance
urgency
freshness
availability
category relevance
organization reliability
completion likelihood
user preference
```

Do not introduce ML before there is sufficient data.

------------------------------------------------------------------------

# 23. CONTRIBUTION / CHECKOUT

The flow should feel extremely fast.

``` text
Mission
↓
Contribution
↓
Amount/resource
↓
Confirmation
↓
Payment
↓
Success
↓
Tracking
```

Handle:

-   payment failure;
-   retry;
-   duplicate payment;
-   abandoned checkout;
-   webhook delay;
-   refund;
-   cancellation;
-   partial mission completion.

Never trust the client as the source of payment truth.

------------------------------------------------------------------------

# 24. TRUST SYSTEM

Document a layered trust model.

### Organization

-   legal/registration checks;
-   applicable documentation;
-   review;
-   history.

### Mission

-   defined need;
-   location;
-   deadline;
-   responsible organization.

### Contribution

-   what;
-   who;
-   when;
-   where.

### Execution

-   volunteer;
-   timestamp;
-   location where appropriate;
-   proof.

### Impact

-   outcome;
-   beneficiary information where legally appropriate;
-   documentation;
-   completion.

Document which checks are automated and which require human review.

------------------------------------------------------------------------

# 25. IMPACT LEDGER

Design this as a permanent domain model.

Potential schema:

``` text
impact_record
----------------
id
public_id
mission_id
contribution_id
organization_id
contributor_id
volunteer_id
resource_type
quantity
location
completed_at
verification_status
proof_bundle_id
impact_summary
created_at
```

Document immutability rules.

If a record must be corrected, create an auditable correction event
rather than silently rewriting history.

Do not claim blockchain is necessary.

------------------------------------------------------------------------

# 26. ORGANIZATION PLATFORM

Document the future organization dashboard.

Sections:

``` text
Overview
Missions
Volunteers
Contributions
Proof
Impact
Campaigns
Reports
Organization Profile
Settings
```

------------------------------------------------------------------------

# 27. CORPORATE PLATFORM

Document:

``` text
Corporate Dashboard
CSR Programs
Budgets
Projects
Organizations
Employee Volunteering
Surplus
Impact
Reports
Users
Permissions
```

Support future multi-user organizations:

``` text
Owner
Admin
CSR Manager
Program Manager
Finance
Viewer
```

------------------------------------------------------------------------

# 28. ADMIN / OPS PLATFORM

This is mandatory for launch.

Build internal tooling for:

-   organization verification;
-   mission moderation;
-   proof review;
-   disputes;
-   refunds;
-   failed missions;
-   volunteer issues;
-   support;
-   fraud signals;
-   platform health.

Do not rely on database edits for normal operations.

------------------------------------------------------------------------

# 29. DESIGN SYSTEM

Create an original NEKI design system inspired by premium consumer
applications.

Document:

### Typography

-   font families;
-   sizes;
-   weights;
-   line heights;
-   letter spacing.

### Colors

Use a restrained, premium light theme.

### Surfaces

-   cards;
-   sheets;
-   navigation;
-   maps;
-   modals.

### Spacing

Use a consistent spacing scale.

### Radius

Document component-specific radii.

### Elevation

Prefer subtle depth rather than excessive shadows.

------------------------------------------------------------------------

# 30. NEKI BRAND

Primary:

# Humanity, Delivered.

Product promise:

> Track every contribution. Verify every mission. See every impact.

Design language should feel:

-   premium;
-   warm;
-   trustworthy;
-   modern;
-   human;
-   calm;
-   highly usable.

Avoid:

-   childish NGO aesthetics;
-   excessive green;
-   generic charity imagery;
-   visual clutter;
-   excessive gradients;
-   excessive glassmorphism;
-   meaningless 3D objects.

------------------------------------------------------------------------

# 31. AI-GENERATED VISUAL ASSETS

If assets are generated with an image-generation system:

Create an asset specification before generation.

For every image:

``` text
asset_id
purpose
aspect_ratio
subject
composition
background
lighting
brand constraints
negative constraints
where used
```

Never let AI-generated imagery imply fabricated real-world beneficiaries
or fabricated proof.

Marketing illustration and actual mission proof must be visually and
technically distinguishable.

------------------------------------------------------------------------

# 32. ANIMATION SYSTEM

Define a restrained motion language.

Animations:

-   page transitions;
-   card interactions;
-   contribution confirmation;
-   mission status;
-   map movement;
-   progress;
-   loading;
-   success;
-   impact reveal.

Document:

``` text
duration
curve
trigger
purpose
reduced-motion fallback
```

No animation should delay core actions.

------------------------------------------------------------------------

# 33. PERFORMANCE TARGETS

Define measurable targets.

Examples to validate during implementation:

-   fast cold start;
-   smooth scrolling;
-   minimal dropped frames;
-   fast home feed;
-   image lazy loading;
-   efficient map rendering;
-   minimal battery consumption;
-   no unnecessary background location;
-   efficient websocket reconnection.

Use profiling instead of subjective claims.

------------------------------------------------------------------------

# 34. ACCESSIBILITY

Document:

-   semantic labels;
-   text scaling;
-   contrast;
-   touch target size;
-   screen readers;
-   reduced motion;
-   keyboard navigation where applicable;
-   color-independent status;
-   accessible maps alternatives.

------------------------------------------------------------------------

# 35. SECURITY

Threat-model:

-   account takeover;
-   payment manipulation;
-   fake missions;
-   fake organizations;
-   fake proof;
-   location spoofing;
-   API abuse;
-   media abuse;
-   privilege escalation;
-   IDOR;
-   replay attacks;
-   webhook forgery;
-   malicious uploads.

Implement:

-   RBAC;
-   server-side authorization;
-   signed uploads;
-   webhook verification;
-   rate limiting;
-   audit logs;
-   secure token storage;
-   secrets management;
-   encryption in transit;
-   least privilege.

------------------------------------------------------------------------

# 36. PRIVACY

Explicitly document:

-   what data is collected;
-   why;
-   retention;
-   deletion;
-   consent;
-   location;
-   photos;
-   beneficiary data;
-   corporate employee data.

Do not expose sensitive beneficiary information in public mission pages.

------------------------------------------------------------------------

# 37. TESTING

Use multiple layers.

## Unit

Domain logic.

## Widget

UI behavior.

## Integration

API + database.

## End-to-end

Critical user journeys.

## Contract tests

Mobile ↔ API.

## Performance

Feed, maps, tracking, uploads.

## Offline

Connection loss/recovery.

## Security

Authorization and abuse cases.

Critical flows:

``` text
Sign up
Browse missions
Search
Open mission
Contribute
Payment success
Payment failure
Volunteer
Accept mission
Location tracking
Upload proof
Complete mission
View impact
```

------------------------------------------------------------------------

# 38. R&D OPEN-SOURCE REPOSITORIES

Study these repositories for architecture and patterns.

Do NOT copy them wholesale.

## A. Riverpod + Clean Architecture

`parrottkim/flutter_riverpod_clean_architecture`

Study:

-   data/domain/presentation separation;
-   Riverpod;
-   Freezed;
-   Dio;
-   Retrofit;
-   repository interfaces.

Repository:

https://github.com/parrottkim/flutter_riverpod_clean_architecture

------------------------------------------------------------------------

## B. Mature Clean Architecture comparison

`guilherme-v/flutter-clean-architecture-example`

Study:

-   feature organization;
-   dependency direction;
-   state-management separation;
-   testing;
-   caching;
-   remote API integration;
-   infinite scrolling.

Repository:

https://github.com/guilherme-v/flutter-clean-architecture-example

------------------------------------------------------------------------

## C. Riverpod production-style example

`Uuttssaavv/flutter-clean-architecture-riverpod`

Study:

-   authentication;
-   pagination;
-   product/search patterns;
-   Riverpod;
-   Freezed;
-   Dio;
-   routing;
-   repository architecture.

Repository:

https://github.com/Uuttssaavv/flutter-clean-architecture-riverpod

------------------------------------------------------------------------

## D. E-commerce architecture

`MohammadFayyad/flutter-ecommerce-app`

Study:

-   product catalog;
-   authentication;
-   cart;
-   checkout;
-   address management;
-   responsive UI;
-   performance patterns;
-   BLoC implementation.

Repository:

https://github.com/MohammadFayyad/flutter-ecommerce-app

------------------------------------------------------------------------

## E. TDD e-commerce architecture

`Sameera-Perera/Flutter-TDD-Clean-Architecture-E-Commerce-App`

Study:

-   TDD;
-   use cases;
-   orders;
-   delivery information;
-   clean architecture;
-   BLoC;
-   backend integration.

Repository:

https://github.com/Sameera-Perera/Flutter-TDD-Clean-Architecture-E-Commerce-App

------------------------------------------------------------------------

## F. Full-featured Flutter commerce example

`mahmoodhamdi/TStore`

Study:

-   authentication;
-   product search;
-   filtering;
-   wishlist;
-   cart;
-   orders;
-   reviews;
-   chat;
-   notifications;
-   clean architecture;
-   large test suite.

Repository:

https://github.com/mahmoodhamdi/TStore

------------------------------------------------------------------------

## G. Delivery tracking

`kforjan/delivery-app`

Study specifically for:

-   GPS;
-   location exchange;
-   delivery tracking;
-   realtime location concepts.

Repository:

https://github.com/kforjan/delivery-app

Do not assume this is production-ready. Treat it as a focused R&D
reference.

------------------------------------------------------------------------

## H. Food delivery / multi-vendor reference

`patriciaperez90/flutter-food-delivery-app-clone`

Study:

-   consumer delivery flow;
-   vendor concepts;
-   rider concepts;
-   order lifecycle;
-   multi-sided architecture.

Important: the repository states that its frontend is open source while
its backend is proprietary. Do not assume backend code is available for
reuse.

Repository:

https://github.com/patriciaperez90/flutter-food-delivery-app-clone

------------------------------------------------------------------------

# 39. REQUIRED R&D COMPARISON TABLE

Create:

`docs/37-rnd-open-source-review.md`

with:

  --------------------------------------------------------------------------------------------------------------------
  Repository   License   Architecture   State   Networking   Offline   Realtime   Tracking   Testing   Useful   Do not
                                                                                                       for NEKI copy
  ------------ --------- -------------- ------- ------------ --------- ---------- ---------- --------- -------- ------

  --------------------------------------------------------------------------------------------------------------------

Actually inspect the repositories before filling this table.

Do not invent findings.

------------------------------------------------------------------------

# 40. REQUIRED ARCHITECTURE DECISION RECORDS

Create ADRs for:

``` text
ADR-001 Flutter
ADR-002 State management
ADR-003 Navigation
ADR-004 Modular monolith
ADR-005 PostgreSQL
ADR-006 PostGIS
ADR-007 Redis
ADR-008 WebSockets
ADR-009 Object storage
ADR-010 Payment provider
ADR-011 Maps provider
ADR-012 Authentication
ADR-013 Offline persistence
ADR-014 Event architecture
ADR-015 Search architecture
ADR-016 Analytics
ADR-017 Observability
ADR-018 Deployment
```

Each ADR:

``` text
Context
Decision
Alternatives
Pros
Cons
Risks
Consequences
Migration path
```

------------------------------------------------------------------------

# 41. API CONTRACT DOCUMENTATION

Define REST endpoints before implementation.

Example:

``` text
POST   /v1/auth/login
GET    /v1/me

GET    /v1/missions
GET    /v1/missions/{id}
POST   /v1/missions/{id}/contributions
POST   /v1/missions/{id}/volunteer
GET    /v1/missions/{id}/tracking

GET    /v1/impact
GET    /v1/impact/{id}

GET    /v1/organizations
GET    /v1/organizations/{id}

POST   /v1/proofs
POST   /v1/missions/{id}/complete

GET    /v1/notifications
```

Do not finalize endpoint names until domain modelling is complete.

Document:

-   request;
-   response;
-   validation;
-   auth;
-   permissions;
-   error codes;
-   pagination;
-   idempotency;
-   rate limits.

Prefer OpenAPI-generated documentation.

------------------------------------------------------------------------

# 42. ERROR MODEL

Create a standard error contract.

Example:

``` json
{
  "error": {
    "code": "MISSION_UNAVAILABLE",
    "message": "This mission is no longer accepting contributions.",
    "request_id": "req_123"
  }
}
```

Mobile should map backend errors into human-readable UX.

------------------------------------------------------------------------

# 43. PAGINATION

Use cursor-based pagination for feeds where appropriate.

Document:

``` text
cursor
limit
next_cursor
has_more
```

Avoid loading hundreds of missions at once.

------------------------------------------------------------------------

# 44. REALTIME FAILURE STRATEGY

WebSocket disconnect:

``` text
Connected
↓
Disconnected
↓
Reconnect with exponential backoff
↓
If unavailable:
fallback polling
↓
Resync latest state
```

Never assume the client received every event.

Server state remains authoritative.

------------------------------------------------------------------------

# 45. IDEMPOTENCY

Important actions must support idempotency.

Examples:

-   payment creation;
-   contribution creation;
-   volunteer acceptance;
-   proof upload;
-   mission completion.

Example:

``` text
Idempotency-Key:
uuid
```

Document server behavior.

------------------------------------------------------------------------

# 46. ANALYTICS

Create an event taxonomy.

Examples:

``` text
app_opened
location_selected
mission_viewed
mission_saved
mission_shared
contribution_started
contribution_completed
contribution_failed
volunteer_started
volunteer_accepted
tracking_opened
proof_uploaded
mission_completed
impact_viewed
organization_viewed
```

Never send sensitive personal data as analytics payloads.

------------------------------------------------------------------------

# 47. BUSINESS METRICS

Instrument:

### Marketplace

-   mission views;
-   contribution conversion;
-   volunteer conversion;
-   fulfillment rate;
-   time-to-fulfillment.

### Trust

-   proof completion;
-   verification completion;
-   dispute rate.

### Retention

-   repeat contribution;
-   repeat volunteer;
-   repeat mission creation.

### B2B

-   organizations onboarded;
-   active organizations;
-   corporate accounts;
-   campaigns;
-   employee volunteers;
-   recurring contracts.

------------------------------------------------------------------------

# 48. IMPLEMENTATION PHASES

## Phase 0 --- Documentation

No major feature coding.

Deliver:

-   architecture;
-   domain model;
-   API;
-   design system;
-   R&D;
-   ADRs.

## Phase 1 --- Foundation

-   Flutter shell;
-   authentication;
-   navigation;
-   theme;
-   networking;
-   backend;
-   database;
-   analytics;
-   error handling.

## Phase 2 --- Marketplace

-   Home;
-   Missions;
-   Search;
-   Mission detail;
-   organization profile.

## Phase 3 --- Contribution

-   contribution flow;
-   payments;
-   receipts;
-   mission progress.

## Phase 4 --- Volunteer

-   discovery;
-   acceptance;
-   active mission;
-   location;
-   status.

## Phase 5 --- Tracking

-   map;
-   realtime state;
-   timeline;
-   notifications.

## Phase 6 --- Proof / Impact

-   proof;
-   verification;
-   impact ledger;
-   impact profile.

## Phase 7 --- Organization

-   organization dashboard;
-   mission creation;
-   volunteer management;
-   proof;
-   reports.

## Phase 8 --- Corporate

-   CSR;
-   employee volunteering;
-   surplus;
-   campaigns;
-   reporting.

------------------------------------------------------------------------

# 49. DEFINITION OF DONE

A feature is not complete because:

> "The screen exists."

It is complete only when:

-   UI implemented;
-   loading state;
-   empty state;
-   error state;
-   offline behavior;
-   accessibility;
-   analytics;
-   backend;
-   authorization;
-   validation;
-   tests;
-   performance reviewed;
-   documentation updated;
-   observability added;
-   security reviewed.

------------------------------------------------------------------------

# 50. AI CODING AGENT RULES

When implementing:

1.  Read the relevant docs first.
2.  Inspect existing code.
3.  Reuse existing infrastructure.
4.  Do not create duplicate abstractions.
5.  Follow ADRs.
6.  Do not invent APIs.
7.  Do not hardcode production secrets.
8.  Do not silently change architecture.
9.  Update documentation when architecture changes.
10. Add tests with meaningful features.
11. Run formatting and static analysis.
12. Run relevant tests.
13. Check mobile performance.
14. Check iOS and Android behavior.
15. Report assumptions.

If a requirement is ambiguous:

-   identify the ambiguity;
-   choose the safest reversible implementation;
-   document the assumption.

------------------------------------------------------------------------

# 51. ANTI-PATTERNS

Do NOT:

-   put API calls directly in widgets;
-   put business logic in UI;
-   use global mutable state everywhere;
-   duplicate models;
-   hardcode mission data in screens;
-   trust client payment state;
-   trust client authorization;
-   store media in PostgreSQL;
-   permanently store precise location without justification;
-   create microservices prematurely;
-   introduce Kafka prematurely;
-   introduce Kubernetes prematurely;
-   create fake impact metrics;
-   fake verification badges;
-   hardcode secrets;
-   copy proprietary apps;
-   copy open-source projects without license review;
-   build decorative features before core flows work.

------------------------------------------------------------------------

# 52. FINAL REQUIRED OUTPUT

Before implementation, produce:

``` text
1. Complete documentation tree
2. Product requirements
3. MVP definition
4. User journeys
5. Information architecture
6. Mobile UX specification
7. Design system
8. Domain model
9. Database schema
10. API specification
11. State machines
12. Realtime architecture
13. Offline architecture
14. Trust architecture
15. Impact Ledger design
16. Organization platform
17. Corporate platform
18. Admin platform
19. Security threat model
20. Privacy model
21. Testing strategy
22. Performance strategy
23. Observability strategy
24. DevOps strategy
25. Open-source R&D report
26. ADRs
27. Implementation backlog
28. Release plan
29. Risk register
30. Technical roadmap
```

------------------------------------------------------------------------

# 53. RISK REGISTER

Create a risk register with at least:

``` text
Risk
Probability
Impact
Early signal
Mitigation
Owner
Status
```

Include:

-   fake organizations;
-   fake missions;
-   fake proof;
-   payment disputes;
-   volunteer no-shows;
-   mission failure;
-   beneficiary privacy;
-   location abuse;
-   fraud;
-   regulatory uncertainty;
-   low mission liquidity;
-   low user retention;
-   high operational cost;
-   logistics failure;
-   poor organization quality;
-   app performance;
-   backend scaling;
-   notification overload.

------------------------------------------------------------------------

# 54. MOST IMPORTANT PRODUCT PRINCIPLE

NEKI must not become:

> "a pretty donation app."

The core product loop is:

``` text
NEED
 ↓
MISSION
 ↓
DISCOVERY
 ↓
CONTRIBUTION / VOLUNTEERING
 ↓
ASSIGNMENT
 ↓
EXECUTION
 ↓
TRACKING
 ↓
PROOF
 ↓
VERIFICATION
 ↓
IMPACT
 ↓
TRUST
 ↓
REPEAT
```

Everything in the architecture should reinforce this loop.

------------------------------------------------------------------------

# 55. FINAL VISION

NEKI begins as:

> **A mission marketplace for social impact.**

Then becomes:

> **A coordination layer between people, resources and organizations.**

Then:

> **A trust layer showing what happened to contributions.**

Then:

> **An operating platform for organizations and corporate social
> impact.**

Eventually:

> **The infrastructure through which human contribution can move from
> intention to verified impact.**

Brand:

# NEKI

## Humanity, Delivered.

Product promise:

## Track every contribution.

## Verify every mission.

## See every impact.

------------------------------------------------------------------------

# FINAL INSTRUCTION TO THE IMPLEMENTATION AGENT

Do not start by writing the entire app.

First perform a **repository and architecture audit**, then inspect the
open-source R&D references listed above, verify their licenses and
current structures, and produce the documentation system described in
this document.

After the documentation is complete:

1.  Present the architecture summary.
2.  Present the major tradeoffs.
3.  Present the MVP boundary.
4.  Present the implementation sequence.
5.  Identify unresolved risks.
6.  Only then begin implementation.

The final system should feel as polished, fast and operationally mature
as a leading consumer marketplace/delivery application, while being
architecturally original, legally clean, scalable, testable and
unmistakably NEKI.
