# NEKI --- Complete UI/UX Design System & Product Experience Specification

> **Product:** NEKI\
> **Tagline:** Humanity, Delivered.\
> **Reference:** The supplied NEKI mobile UI/UX visual board is the
> primary visual source for this specification.\
> **Target:** Premium iOS + Android application with a marketplace-like
> discovery experience, contribution flow, real-time tracking,
> measurable impact, and organization-led missions.\
> **Design ambition:** Calm, premium, trustworthy, human, highly usable,
> and operationally clear.

------------------------------------------------------------------------

## 1. Purpose of This Document

This document is the **source-of-truth UI/UX specification** for the
NEKI consumer application.

It translates the supplied visual reference into a production-grade
design system and interaction specification.

The implementation team should use this document to define:

-   information architecture
-   navigation
-   screen hierarchy
-   component behavior
-   visual language
-   typography
-   spacing
-   cards
-   buttons
-   forms
-   mission discovery
-   contribution flows
-   tracking
-   impact history
-   profile
-   category browsing
-   empty/loading/error states
-   accessibility
-   animation
-   responsive behavior
-   interaction states
-   design tokens
-   content hierarchy
-   handoff requirements

The goal is **not** to reproduce the reference image as a static mockup.

The goal is to create the same **visual character, hierarchy, density,
emotional tone, and interaction quality** as a complete production
application.

------------------------------------------------------------------------

# 2. Core UX Philosophy

NEKI should feel like:

> **A premium consumer product built around doing good.**

It should NOT feel like:

-   a traditional NGO website
-   a government portal
-   a donation form
-   a corporate CSR dashboard
-   a charity directory
-   a generic fintech app
-   an overly sentimental social-impact application

The experience should communicate:

### Trust

The user should understand where their contribution goes.

### Visibility

The user should always know what happened after contributing.

### Simplicity

Helping someone should be as easy as completing a modern commerce
transaction.

### Humanity

The interface should feel warm without becoming childish.

### Evidence

Impact should be presented as something measurable and visible.

### Momentum

The product should encourage a second contribution, volunteering, or
sharing without using manipulative dark patterns.

------------------------------------------------------------------------

# 3. Brand Personality

NEKI's UI personality should sit between:

-   premium consumer technology
-   modern commerce
-   editorial design
-   social impact
-   human storytelling

### Keywords

**Warm**

**Minimal**

**Elegant**

**Trustworthy**

**Optimistic**

**Soft**

**Modern**

**Human**

**Precise**

**Visible**

------------------------------------------------------------------------

# 4. Reference Image Interpretation

The supplied reference establishes the visual direction.

Major visual characteristics:

-   warm off-white background
-   deep forest/emerald green as the primary action color
-   muted beige/taupe supporting tones
-   very soft pastel category surfaces
-   rounded cards
-   large whitespace
-   premium editorial typography
-   serif display typography paired with clean sans-serif UI typography
-   subtle translucent/glass surfaces
-   soft 3D illustrations
-   floating/blurry ambient objects
-   photography used for missions
-   rounded mission cards
-   compact status indicators
-   bottom navigation
-   large readable numbers
-   strong visual hierarchy
-   minimal borders
-   subtle shadows
-   generous corner radii
-   calm motion

The interface should feel **expensive without feeling luxurious for
luxury's sake**.

------------------------------------------------------------------------

# 5. Product IA

## Primary Consumer Navigation

The reference establishes five primary destinations:

1.  **Home**
2.  **Explore**
3.  **Contribute**
4.  **Activity**
5.  **Profile**

This should remain the primary bottom navigation structure.

### Bottom Navigation

``` text
Home
Explore
Contribute
Activity
Profile
```

Each item has:

-   icon
-   label
-   active state
-   inactive state
-   optional badge

### Active State

Active navigation item:

-   dark green icon
-   stronger label
-   visually grounded indicator
-   no oversized decorative treatment

### Inactive State

Inactive:

-   muted gray
-   lower visual weight
-   still highly readable

### Badge

Use badges only when they represent actionable information:

-   unread activity
-   pending verification
-   contribution requiring attention

Never use arbitrary notification dots for engagement manipulation.

------------------------------------------------------------------------

# 6. Global Application Structure

``` text
App
│
├── Splash
│
├── Authentication
│   ├── Welcome
│   ├── Sign In
│   ├── Sign Up
│   ├── OTP
│   └── Permissions
│
├── Home
│
├── Explore
│   ├── Search
│   ├── Filters
│   ├── Categories
│   ├── Mission Results
│   └── Organization Results
│
├── Mission
│   ├── Mission Detail
│   ├── Contribution
│   ├── Volunteer
│   ├── Save
│   └── Share
│
├── Contribution
│   ├── Money
│   ├── Items
│   ├── Time
│   ├── Skills
│   ├── Review
│   ├── Payment
│   └── Success
│
├── Tracking
│   ├── Active Contribution
│   ├── Map
│   ├── Timeline
│   └── Proof
│
├── Activity
│   ├── Contributions
│   ├── Volunteering
│   ├── Items
│   ├── Certificates
│   └── Impact
│
├── Profile
│   ├── Overview
│   ├── Contributions
│   ├── Bookmarks
│   ├── Certificates
│   ├── Payment Methods
│   ├── Settings
│   └── Help
│
└── Category
    ├── Food
    ├── Education
    ├── Healthcare
    ├── Animals
    ├── Environment
    ├── Mentoring
    └── Other
```

------------------------------------------------------------------------

# 7. Design Grid

## Mobile Base

Primary design target:

-   390 × 844 logical pixels
-   iPhone-class viewport

Support:

-   320 px minimum width
-   375 px
-   390 px
-   393 px
-   412 px
-   larger Android phones

Do not hard-code layout around one device.

------------------------------------------------------------------------

# 8. Global Spacing System

Use a consistent 4/8-point rhythm.

``` text
4   micro
8   compact
12  tight
16  standard
20  comfortable
24  section
32  large
40  major
48  hero
64  editorial
80  extreme
```

Typical screen padding:

``` text
16–20 px horizontal
```

Large editorial sections may use:

``` text
24 px
```

------------------------------------------------------------------------

# 9. Corner Radius System

Reference UI uses soft rounded geometry.

Recommended tokens:

``` text
RADIUS_XS   = 8
RADIUS_SM   = 12
RADIUS_MD   = 16
RADIUS_LG   = 20
RADIUS_XL   = 24
RADIUS_XXL  = 28
RADIUS_PILL = 999
```

Use:

-   12--16 px for compact controls
-   16--20 px for cards
-   20--28 px for major surfaces
-   pill radius for tags/chips

Avoid excessive rounded containers around every single piece of text.

------------------------------------------------------------------------

# 10. Color System

The reference is primarily warm-neutral with green as the action/trust
color.

## Primary

``` text
NEKI Forest
#0B5D45
```

Use for:

-   primary buttons
-   active navigation
-   progress
-   verification
-   positive status
-   important links
-   mission actions

## Dark Primary

``` text
#073D30
```

Use for:

-   pressed states
-   high-contrast text
-   deep backgrounds where needed

## Soft Green

``` text
#E7F4ED
```

Use for:

-   selected cards
-   success surfaces
-   subtle highlights
-   category backgrounds

## Warm Background

``` text
#FAF9F6
```

Primary application background.

## White Surface

``` text
#FFFFFF
```

Cards and elevated surfaces.

## Warm Beige

``` text
#E8DDCF
```

Supporting editorial/accent tone.

## Taupe

``` text
#A58F78
```

Use sparingly for:

-   secondary editorial accents
-   decorative text
-   warm metadata

## Text Primary

``` text
#171A18
```

## Text Secondary

``` text
#66706B
```

## Text Tertiary

``` text
#929A95
```

## Divider

``` text
#E8EBE8
```

------------------------------------------------------------------------

# 11. Semantic Colors

``` text
Success:
#21865B

Warning:
#C28A35

Error:
#C95151

Info:
#4D7EA8
```

Semantic colors should be restrained.

NEKI should not become a rainbow interface.

------------------------------------------------------------------------

# 12. Category Color Language

Each category can have a soft background while preserving NEKI's overall
visual system.

### Food

Soft mint / green

### Education

Soft cream / amber

### Healthcare

Soft rose

### Money

Soft blue

### Mentoring

Soft lavender

### Animals

Soft green

### Environment

Soft natural green

### Disaster Relief

Soft warm gray / muted orange

Category colors are for **orientation**, not decoration.

------------------------------------------------------------------------

# 13. Typography

The reference clearly combines editorial serif typography with modern
sans-serif UI text.

## Display Typeface

Use an elegant high-contrast serif.

Recommended options:

-   Cormorant Garamond
-   Playfair Display
-   DM Serif Display
-   Instrument Serif

Preferred direction:

**Instrument Serif / Cormorant-style editorial serif**

Use for:

-   splash statement
-   major emotional headlines
-   campaign statements
-   impact storytelling
-   selected hero copy

## UI Typeface

Use a clean modern sans-serif.

Recommended:

-   Inter
-   SF Pro
-   Manrope
-   Plus Jakarta Sans

Preferred:

**Inter / SF Pro-like**

Use for:

-   buttons
-   labels
-   metadata
-   cards
-   navigation
-   forms
-   numbers

------------------------------------------------------------------------

# 14. Typography Scale

``` text
Display XL       48–56
Display L        40–48
Display M        32–40
Heading XL       28–32
Heading L        24–28
Heading M        20–22
Heading S        17–18

Body L           17
Body M           15–16
Body S           13–14

Caption          11–12
Micro            10–11
```

Avoid overly small UI text.

Mission information should remain readable outdoors.

------------------------------------------------------------------------

# 15. Typography Hierarchy Rules

A screen should usually have:

``` text
1 primary heading
1 supporting explanation
1 primary action
supporting metadata
```

Avoid:

-   five competing bold headings
-   excessive uppercase
-   long paragraphs
-   overly decorative typography
-   too many font weights

------------------------------------------------------------------------

# 16. Iconography

Icons should be:

-   simple
-   geometric
-   lightweight
-   rounded where appropriate
-   consistent in stroke width

Preferred visual language:

-   Lucide-style
-   SF Symbols-inspired
-   Material Symbols with customization

Use filled icons primarily for active states.

Avoid mixing:

-   outlined icon family
-   cartoon icon family
-   3D icon family
-   unrelated icon styles

------------------------------------------------------------------------

# 17. Photography

Mission photography is central to discovery.

Photography should feel:

-   authentic
-   human
-   documentary
-   warm
-   respectful
-   naturally lit

Avoid:

-   obvious stock photography
-   exaggerated suffering
-   exploitative imagery
-   manipulative emotional framing
-   images that expose vulnerable people without appropriate consent

### Image treatment

Use:

-   rounded corners
-   natural crop
-   subtle overlays when necessary
-   clear category badge
-   strong contrast for text overlays

------------------------------------------------------------------------

# 18. 3D Illustration Language

The reference uses soft 3D objects and ambient translucent forms.

NEKI 3D assets should be:

-   soft
-   rounded
-   minimal
-   slightly toy-like
-   premium
-   non-photorealistic
-   emotionally positive

Examples:

-   butterfly
-   food bowl
-   open book
-   heart
-   medical cross
-   cog
-   water drop
-   tree
-   shelter
-   school bag
-   care package

Objects should feel like **physical representations of impact**, not
generic SaaS illustrations.

------------------------------------------------------------------------

# 19. Ambient Background Objects

The reference uses large, blurry, translucent objects around screens.

These should be:

-   extremely low contrast
-   partially cropped
-   blurred
-   slowly animated
-   non-interactive unless explicitly useful

Purpose:

> Create depth and warmth without distracting from content.

Never allow ambient decoration to reduce text contrast.

------------------------------------------------------------------------

# 20. Global Surface Language

NEKI should use three primary surface levels.

### Level 0 --- Background

Warm off-white.

### Level 1 --- Card

White with very subtle elevation.

### Level 2 --- Featured Surface

Soft tinted background / translucent glass.

Use shadows very lightly.

Example:

``` text
0 4px 18px rgba(20, 40, 30, 0.06)
```

Avoid heavy black shadows.

------------------------------------------------------------------------

# 21. Glass / Blur

Use glass selectively.

Good use cases:

-   floating success card
-   hero object surface
-   contextual floating control
-   bottom-sheet header
-   ambient decorative element

Do not make the entire app glassmorphic.

The main interface must remain highly readable.

------------------------------------------------------------------------

# 22. Motion Philosophy

Motion should communicate:

-   progress
-   continuity
-   confirmation
-   spatial relationships
-   emotional reward

Not:

-   distraction
-   gamification for its own sake
-   unnecessary transitions

Preferred motion language:

**soft + quick + physical**

------------------------------------------------------------------------

# 23. Motion Tokens

``` text
Instant: 100ms
Quick:   160ms
Normal: 220ms
Smooth:  320ms
Hero:    500–700ms
```

Use ease-out for entering elements.

Use spring animation for:

-   buttons
-   cards
-   contribution confirmation
-   navigation transitions

------------------------------------------------------------------------

# 24. Splash Screen

## Purpose

Introduce NEKI emotionally rather than technically.

## Visual Structure

``` text
Large empty space

Butterfly / NEKI mark

NEKI
Humanity, Delivered.

Bottom:
loading / initialization indicator
```

Background:

warm off-white.

Logo:

deep green / muted warm accent.

### Animation

1.  background fades in
2.  butterfly gently appears
3.  wordmark fades upward
4.  tagline appears
5.  application transitions to onboarding/home

Target duration:

\~1--1.5 seconds maximum.

Never make users wait for branding.

------------------------------------------------------------------------

# 25. Welcome / Get Started Screen

The reference shows:

-   large NEKI logo
-   soft green/white ambient forms
-   editorial message
-   primary CTA
-   sign-in option

Suggested hierarchy:

``` text
[NEKI visual]

A kinder world
is a more possible one.

[Get Started →]

Already have an account?
Sign In
```

### Primary CTA

Large pill/rounded button.

Deep green.

White text.

Arrow icon.

### Interaction

Tap:

`Get Started`

→ authentication / onboarding.

Tap:

`Sign In`

→ sign-in.

------------------------------------------------------------------------

# 26. Authentication UX

Keep authentication minimal.

Preferred flow:

``` text
Phone / Email
↓
OTP / Password
↓
Name
↓
Location permission
↓
Notification permission
↓
Home
```

Do not force unnecessary profile completion.

------------------------------------------------------------------------

# 27. Permission UX

Do not ask for permissions immediately without context.

### Location

First explain:

> See missions near you and track contributions in real time.

Then ask OS permission.

### Notifications

Explain:

> Get updates when your contribution is picked up, delivered, or
> verified.

Then ask permission.

------------------------------------------------------------------------

# 28. Home Screen

The reference home screen is one of the most important screens.

It should feel **dense but calm**, similar to a modern commerce
application.

## Header

Top row:

``` text
☰ / menu       Balance / credits       Bell       Avatar
```

Depending on product requirements, the left icon can become
profile/menu.

### Greeting

``` text
Hi, Divo
Good Morning. 👋
```

Dynamic time-of-day greeting:

-   Good Morning
-   Good Afternoon
-   Good Evening

Optional supporting copy:

> Small acts. Big change.

------------------------------------------------------------------------

# 29. Home Search

Immediately beneath greeting.

Search field:

``` text
Search missions, NGOs or causes...
```

Features:

-   magnifier
-   rounded surface
-   subtle border
-   clear button when active
-   voice search optional
-   recent searches
-   suggested searches

Search should support:

-   missions
-   organizations
-   causes
-   categories
-   locations

------------------------------------------------------------------------

# 30. Home Category Grid

Reference uses six category cards.

Recommended default:

``` text
Food
Education
Healthcare

Money
Mentoring
Animals
```

Additional categories accessible through:

`View All`

Possible categories:

-   Environment
-   Disaster Relief
-   Senior Care
-   Women Empowerment
-   Accessibility
-   Community Development
-   Rural Development
-   Volunteering

Each category card:

-   icon
-   title
-   pastel background
-   subtle shadow
-   2-column or 3-column grid depending width

------------------------------------------------------------------------

# 31. Home Featured Mission

Section:

``` text
Today's Highlight                  See All
```

Large featured mission card.

Contains:

-   hero image
-   category badge
-   bookmark
-   mission title
-   location
-   funding/progress
-   CTA

Example:

``` text
FOOD

Provide 200 meals to
underprivileged children

New Delhi

62% funded
```

Progress bar should be immediately understandable.

------------------------------------------------------------------------

# 32. Home Content Modules

After featured mission:

### Nearby Missions

Based on location.

### Urgent Missions

Deadline / urgency driven.

### NEKI Picks

Editorially selected.

### Volunteer This Weekend

Time-based opportunities.

### Recently Completed

Shows successful impact.

### Continue Your Impact

For users with active or incomplete flows.

### Organizations Near You

Optional discovery module.

Do not show all modules to every user.

Use personalization based on behavior.

------------------------------------------------------------------------

# 33. Home Density Principle

The reference has a commerce-style information density.

Therefore:

**Do not make Home a giant hero page.**

The user should be able to discover multiple actions within one scroll.

Ideal first viewport:

``` text
Header
Greeting
Search
Categories
Featured mission
```

------------------------------------------------------------------------

# 34. Explore Screen

The reference shows a dedicated Explore marketplace.

Header:

``` text
Explore                         Search
```

Search bar.

Filter button.

Category chips.

Mission list.

------------------------------------------------------------------------

# 35. Explore Search

Search field:

``` text
Search missions, NGOs or causes...
```

When active:

-   keyboard opens
-   suggestions appear
-   recent searches
-   trending causes
-   organizations
-   categories

Example:

``` text
food
food donation
community kitchen
school meals
```

------------------------------------------------------------------------

# 36. Explore Filters

Filter bottom sheet.

Filters:

### Cause

-   Food
-   Education
-   Healthcare
-   Animals
-   Environment
-   etc.

### Location

-   Near me
-   City
-   Radius

### Contribution Type

-   Money
-   Items
-   Time
-   Skills

### Urgency

-   Urgent
-   This week
-   Flexible

### Mission Status

-   Funding
-   Volunteers needed
-   Active
-   Almost complete

### Organization

-   Verified organizations
-   Community-led

### Amount

Optional contribution range.

CTA:

`Apply Filters`

Secondary:

`Reset`

------------------------------------------------------------------------

# 37. Mission Cards

Mission cards are the primary marketplace component.

## Card Structure

``` text
┌────────────────────────────┐
│ IMAGE                 ♡    │
│                            │
│ FOOD                       │
│                            │
│ Provide 200 meals...       │
│                            │
│ 📍 New Delhi               │
│                            │
│ ███████████░░ 62%          │
│                            │
│ ₹12,400 of ₹20,000         │
└────────────────────────────┘
```

Card hierarchy:

1.  image
2.  category
3.  title
4.  location
5.  progress
6.  contribution status

------------------------------------------------------------------------

# 38. Mission Card Variants

### Compact

Used in lists.

### Standard

Used in Explore.

### Featured

Large image and stronger CTA.

### Horizontal

Used for dense discovery modules.

### Near-complete

Shows urgency:

``` text
92% funded
₹1,600 remaining
```

### Volunteer

Shows:

``` text
12 volunteers needed
Saturday
10:00 AM
```

------------------------------------------------------------------------

# 39. Mission Detail Screen

This is one of the highest-value screens.

Reference:

-   large mission image
-   back button
-   heart
-   share
-   category
-   title
-   location
-   date/time
-   progress
-   statistics
-   primary CTA
-   volunteer CTA
-   save

------------------------------------------------------------------------

# 40. Mission Detail Header

Full-width image.

Overlay controls:

``` text
←
                         ♡   Share
```

Image should use:

-   edge-to-edge media
-   rounded lower corners or controlled clipping
-   safe-area-aware controls

------------------------------------------------------------------------

# 41. Mission Detail Content

Example hierarchy:

``` text
FOOD

Provide 200 meals to
underprivileged children

📍 New Delhi
◷ Today, 12:00 PM

₹12,400 of ₹20,000
62%

[progress bar]

12 Volunteers
200 Meals
1.2 km
From you
```

------------------------------------------------------------------------

# 42. Mission Story

Below summary:

### Why this matters

Explain:

-   problem
-   people affected
-   exact need
-   why now

Avoid manipulative emotional writing.

------------------------------------------------------------------------

# 43. Mission Requirements

Use structured cards.

Example:

``` text
Money
₹20,000 required

Meals
200 required

Volunteers
12 required

Deadline
Today, 12 PM
```

------------------------------------------------------------------------

# 44. Organization Section

Display:

-   organization logo
-   name
-   verification status
-   location
-   previous impact
-   missions completed

CTA:

`View Organization`

------------------------------------------------------------------------

# 45. Trust Section

Show only verified claims.

Possible:

``` text
✓ Organization verified
✓ Mission documents reviewed
✓ Delivery proof required
✓ Impact verification pending
```

Do not show a generic "100% trusted" badge without measurable meaning.

------------------------------------------------------------------------

# 46. Mission CTA Architecture

Primary action:

``` text
Contribute Now
```

Secondary:

``` text
Volunteer for this mission
```

Tertiary:

``` text
Save for later
```

The primary CTA should remain visible near the bottom.

Recommended:

-   sticky bottom action
-   safe-area padding
-   dynamic CTA based on mission state

------------------------------------------------------------------------

# 47. Contribution Screen

Reference:

``` text
Contribute

Money | Items | Time | Skills
```

This is a major NEKI differentiator.

Contribution is not limited to money.

------------------------------------------------------------------------

# 48. Contribution Type Selector

Use segmented tabs or pill tabs:

``` text
Money
Items
Time
Skills
```

Selected state:

-   deep green background
-   white text

Unselected:

-   warm gray / white
-   dark text

------------------------------------------------------------------------

# 49. Money Contribution

Quick amount buttons:

``` text
₹500
₹1,000
₹2,500
₹5,000
```

Then:

``` text
Other amount
₹ ______
```

Do not force users into preset amounts.

------------------------------------------------------------------------

# 50. Contribution Transparency

Reference shows:

> 100% of your contribution goes to the mission.

Only display this if operationally and legally accurate for the relevant
transaction.

Supporting copy:

``` text
Transparent.
Accountable.
Impactful.
```

Potentially show:

-   platform fee
-   payment fee
-   mission allocation
-   taxes where applicable

Never hide required charges.

------------------------------------------------------------------------

# 51. Money Contribution CTA

Primary:

``` text
Proceed to Pay →
```

Disabled until valid amount.

Button state:

``` text
Normal
Pressed
Loading
Success
Error
```

------------------------------------------------------------------------

# 52. Item Contribution

Item contribution flow:

``` text
Select Item
↓
Quantity
↓
Condition
↓
Photos
↓
Pickup Address
↓
Pickup Window
↓
Review
↓
Confirm
```

Examples:

-   books
-   clothes
-   food
-   furniture
-   electronics
-   school supplies

------------------------------------------------------------------------

# 53. Time Contribution

Volunteer flow:

``` text
Mission
↓
Role
↓
Date
↓
Time
↓
Location
↓
Requirements
↓
Confirm
```

Show:

-   expected duration
-   physical requirements
-   age requirements if applicable
-   location
-   organizer
-   capacity

------------------------------------------------------------------------

# 54. Skills Contribution

Skill flow:

``` text
Skill
↓
Experience
↓
Availability
↓
Remote / In-person
↓
Mission matching
↓
Confirm
```

Examples:

-   teaching
-   design
-   coding
-   legal
-   medical
-   mentoring
-   photography
-   operations

------------------------------------------------------------------------

# 55. Review Screen

Before final submission:

``` text
Your Contribution

Mission
Community Kitchen

Type
Money

Amount
₹1,000

Location
New Delhi

Payment method
UPI

[Confirm Contribution]
```

Always give the user a clear final review.

------------------------------------------------------------------------

# 56. Payment UX

Payment UI should feel integrated but secure.

Support where legally/technically available:

-   UPI
-   cards
-   net banking
-   wallets
-   saved payment methods

Never store sensitive payment information in the application itself
unless handled through a compliant payment provider/tokenization layer.

------------------------------------------------------------------------

# 57. Contribution Success Screen

Reference has a very strong success screen.

Visual:

-   large checkmark
-   subtle floating celebration
-   "Thank You!"
-   impact statement
-   share button

Example:

``` text
✓

Thank You!

Your contribution brings us
one step closer to a kinder world.

[Share Impact]

[Back to Home]
```

Do not use excessive confetti.

The emotional payoff should feel calm and meaningful.

------------------------------------------------------------------------

# 58. Success Animation

Sequence:

1.  transaction confirmation
2.  checkmark draws in
3.  subtle scale/spring
4.  background particles/objects drift
5.  headline fades in
6.  CTA becomes active

Animation duration:

\~600--900ms total.

Provide reduced-motion alternative.

------------------------------------------------------------------------

# 59. Tracking Screen

Reference establishes tracking as a first-class experience.

Header:

``` text
‹ Tracking                         ⋮
```

Map occupies approximately the upper half.

------------------------------------------------------------------------

# 60. Tracking Map

Map elements:

-   origin
-   route
-   volunteer / delivery marker
-   destination
-   current position
-   ETA
-   status bubble

Example:

``` text
      Mission
         │
         │
      ●───●
          │
          🚚
       8 min away
```

Use a clean map style that does not overpower the mission status.

------------------------------------------------------------------------

# 61. Tracking Timeline

Below map:

``` text
Your contribution is on the way

Providing 200 meals · New Delhi

● Order confirmed       10:14 AM
● Picked up             10:28 AM
● On the way            Live
○ Delivered
○ Verified
```

Completed states:

-   green check
-   strong text

Current:

-   green pulse
-   live label

Future:

-   muted outline

------------------------------------------------------------------------

# 62. Tracking Detail Card

Display the responsible volunteer/delivery person only when appropriate
and consented.

Example:

``` text
Ravi has picked up your contribution
and is on the way.

ETA: 8 minutes
```

Potential actions:

-   contact support
-   call volunteer where permitted
-   view route
-   report issue

Avoid exposing personal information unnecessarily.

------------------------------------------------------------------------

# 63. Tracking States

Mission tracking should support:

``` text
Confirmed
Preparing
Assigned
Picked Up
On the Way
Arrived
Delivered
Verification
Verified
Completed
```

Exceptional:

``` text
Delayed
Rescheduled
Issue Reported
Verification Required
Cancelled
```

Every state needs a clear explanation.

------------------------------------------------------------------------

# 64. Activity / Impact Screen

Reference calls the section:

**Your Impact**

The bottom navigation label can remain:

**Activity**

while the primary page title is:

**Your Impact**

This avoids making the navigation label overly long.

------------------------------------------------------------------------

# 65. Impact Header

``` text
Your Impact

All
Donations
Volunteering
Items
```

Segmented filters.

------------------------------------------------------------------------

# 66. Impact Statistics

Reference uses four metrics.

Example:

``` text
12
Missions Supported

48
People Helped

28
Hours Volunteered

3
NGOs Supported
```

Important:

Only display metrics backed by actual platform data.

------------------------------------------------------------------------

# 67. Impact Activity Feed

Chronological feed.

Example:

``` text
♥  Contributed ₹1,000
   to Community Kitchen
   2 hours ago

👥 Volunteered for
   Clothing Drive
   1 day ago

📖 Donated 5 Books
   to Rural School
   3 days ago
```

Each activity should open the related record.

------------------------------------------------------------------------

# 68. Impact Ledger UX

Each contribution should have a detailed record.

Display:

``` text
NEKI ID
NK-XXXXXX

Contribution
₹1,000

Mission
Community Kitchen

Organization
Verified Organization

Location
New Delhi

Delivered
Date

Proof
Available

Impact
200 meals supported
```

This becomes the user's personal **Impact Ledger**.

------------------------------------------------------------------------

# 69. Certificates

Where applicable:

-   volunteering certificate
-   contribution certificate
-   impact certificate

Certificate cards should show:

-   title
-   date
-   organization
-   mission
-   verification
-   download/share

------------------------------------------------------------------------

# 70. Profile Screen

Reference profile:

-   avatar
-   name
-   short impact statement
-   stats
-   account sections

Example:

``` text
[Avatar]

Divo Sharma

Making a kinder world ✨

12 Missions
28 Hours
3 NGOs
48 People
```

------------------------------------------------------------------------

# 71. Profile Information Architecture

``` text
My Contributions
My Bookmarks
My Certificates
Payment Methods
Settings
Help & Support
```

Each row:

-   icon
-   label
-   chevron
-   optional metadata

------------------------------------------------------------------------

# 72. Profile Header

Use a clean centered profile composition.

Avatar:

-   circular
-   approximately 72--88 px
-   editable control

Edit button should be small and secondary.

------------------------------------------------------------------------

# 73. Category Page

Reference includes a dedicated Food category page.

Header:

``` text
←     Food                     ⋮
```

Category icon.

Title:

``` text
Food

Nourishment for a
brighter tomorrow.
```

Category tabs:

``` text
All
Meals
Rations
Kitchen Kits
```

Mission list.

------------------------------------------------------------------------

# 74. Category Page Design

Category page should be reusable.

Data-driven:

``` text
CategoryPage(
  category,
  icon,
  description,
  subcategories,
  missions
)
```

Do not create separate hard-coded screens for each category.

------------------------------------------------------------------------

# 75. Empty States

Empty states should be useful.

Example:

``` text
No missions found nearby.

Try expanding your location
or changing your filters.

[Explore All Missions]
```

Avoid:

> "Oops! Nothing here 😢"

NEKI should remain mature.

------------------------------------------------------------------------

# 76. Loading States

Use skeletons rather than blank screens.

Mission skeleton:

``` text
Image block
Title lines
Location line
Progress bar
```

Skeleton animation should be subtle.

Avoid aggressive shimmer.

------------------------------------------------------------------------

# 77. Error States

Example:

``` text
We couldn't load this mission.

Check your connection and try again.

[Retry]
```

For payments:

``` text
Your payment could not be confirmed.

No contribution has been recorded yet.

[Try Again]
[Contact Support]
```

Never falsely show success.

------------------------------------------------------------------------

# 78. Offline UX

The application should degrade gracefully.

Offline:

-   previously viewed missions remain accessible where cached
-   profile remains visible
-   contribution history remains visible
-   tracking shows last known status
-   new financial transactions require connectivity
-   volunteer updates can be queued where appropriate

Show:

``` text
You're offline.
Showing your latest saved information.
```

------------------------------------------------------------------------

# 79. Network Reconnection

When connectivity returns:

-   silently resync
-   update stale records
-   refresh tracking
-   resolve queued operations
-   notify user only when meaningful

Do not create duplicate contributions.

------------------------------------------------------------------------

# 80. Search UX

Global search should search:

``` text
Missions
Organizations
Categories
Causes
Locations
```

Search result sections:

``` text
Missions
Organizations
Categories
```

Use recent searches.

Allow:

`Clear all`

------------------------------------------------------------------------

# 81. Search Result Ranking

Ranking should consider:

-   text relevance
-   location
-   mission status
-   urgency
-   user interests
-   freshness
-   trust/verification
-   availability
-   contribution compatibility

Never allow payment amount alone to determine visibility.

------------------------------------------------------------------------

# 82. Bookmark UX

Bookmark icon on mission cards.

Tap:

-   icon fills
-   subtle scale animation
-   mission added to bookmarks

Optional toast:

``` text
Saved to your missions
```

Undo should be available.

------------------------------------------------------------------------

# 83. Share UX

Share a mission with:

-   native share sheet
-   deep link
-   campaign preview

Share message should communicate:

``` text
Mission
Need
Location
Progress
NEKI link
```

Do not auto-share private contribution information.

------------------------------------------------------------------------

# 84. Bottom Sheets

Use bottom sheets for:

-   filters
-   contribution details
-   payment method
-   volunteer details
-   report issue
-   location selection

Bottom sheets:

-   rounded top corners
-   drag indicator
-   clear title
-   scrollable content
-   sticky CTA when necessary

------------------------------------------------------------------------

# 85. Toasts

Use lightweight toast/snackbar messages for:

-   saved
-   copied
-   updated
-   offline
-   action undone

Never use toasts for critical financial information.

------------------------------------------------------------------------

# 86. Dialogs

Use dialogs only for:

-   destructive actions
-   important confirmation
-   permission rationale
-   irreversible state changes

Avoid dialog overload.

------------------------------------------------------------------------

# 87. Button System

## Primary

Deep green.

Used for:

-   contribute
-   pay
-   confirm
-   start
-   volunteer

## Secondary

Light surface with dark text.

## Tertiary

Text-only.

## Destructive

Semantic error color.

------------------------------------------------------------------------

# 88. Button Geometry

Primary mobile CTA:

-   height: 48--56 px
-   horizontal padding: 20--24 px
-   radius: 14--18 px

Large hero CTA:

-   height: 52--56 px

Minimum touch target:

**44 × 44 px**

Prefer 48 × 48 px for key controls.

------------------------------------------------------------------------

# 89. Chips

Use chips for:

-   categories
-   filters
-   contribution types
-   mission states

Selected:

deep green fill.

Unselected:

warm neutral.

Avoid excessive chips on small screens.

------------------------------------------------------------------------

# 90. Progress Bars

Progress should communicate real status.

Structure:

``` text
₹12,400 of ₹20,000

████████████░░░░ 62%
```

Use:

-   green fill
-   neutral track
-   rounded ends

For non-monetary goals:

``` text
140 / 200 meals
70%
```

------------------------------------------------------------------------

# 91. Status Badges

Examples:

``` text
FOOD
EDUCATION
HEALTHCARE
VERIFIED
LIVE
URGENT
COMPLETED
```

Use compact typography.

Do not rely on color alone.

------------------------------------------------------------------------

# 92. Trust Badges

Trust badges must have precise meanings.

Examples:

``` text
✓ Organization Verified
✓ Mission Verified
✓ Delivery Proof
✓ Impact Verified
```

Each badge should have an accessible explanation.

Tap:

→ opens verification details.

------------------------------------------------------------------------

# 93. Impact Visualization

Do not over-gamify.

Useful visualizations:

-   missions supported
-   people helped
-   hours volunteered
-   items donated
-   meals delivered
-   trees planted
-   school kits supplied

Use simple:

-   cards
-   numbers
-   timelines
-   progress rings
-   contribution history

------------------------------------------------------------------------

# 94. Personalization

Home can personalize:

-   nearby missions
-   previously explored causes
-   saved missions
-   preferred contribution type
-   volunteer availability
-   upcoming deadlines

However, users should always be able to explore everything.

------------------------------------------------------------------------

# 95. Location UX

Location is important for:

-   nearby missions
-   pickup
-   volunteering
-   delivery tracking

Location selection:

``` text
Use current location
Search city
Select area
```

Always provide manual selection.

Do not force GPS.

------------------------------------------------------------------------

# 96. Mission Detail Sticky Footer

On mission details, use:

``` text
[ Volunteer ]     [ Contribute Now ]
```

or when volunteer is unavailable:

``` text
[ Save ]           [ Contribute Now ]
```

Sticky footer must respect:

-   keyboard
-   safe area
-   bottom navigation
-   modal states

------------------------------------------------------------------------

# 97. Keyboard UX

When keyboard opens:

-   CTA should remain reachable
-   inputs should scroll into view
-   bottom navigation may hide
-   keyboard dismissal should be intuitive

Never allow keyboard to obscure:

-   amount
-   address
-   final CTA

------------------------------------------------------------------------

# 98. Form UX

Forms should use:

-   clear labels
-   examples
-   inline validation
-   input formatting
-   keyboard type optimization
-   error message directly below field

Avoid placeholder-only labels.

------------------------------------------------------------------------

# 99. Accessibility

NEKI must support:

### Dynamic text

Do not break layout when text increases.

### Screen readers

Every interactive element gets:

-   semantic label
-   role
-   state

### Contrast

Meet WCAG AA for normal text where possible.

### Touch targets

Minimum 44 × 44 px.

### Reduced motion

Respect OS reduced-motion settings.

### Color blindness

Never communicate status only through color.

------------------------------------------------------------------------

# 100. Internationalization

Design for future multilingual support.

Do not hard-code:

``` text
₹12,400 of ₹20,000
```

into image assets.

Support:

-   Hindi
-   English
-   future Indian languages
-   pluralization
-   date localization
-   number formatting

Text should expand naturally.

------------------------------------------------------------------------

# 101. Android UX

Respect Android conventions:

-   system back gesture
-   predictive back where supported
-   edge-to-edge
-   Android permission patterns
-   haptic behavior
-   system bars

Do not make Android feel like a badly ported iOS app.

------------------------------------------------------------------------

# 102. iOS UX

Respect iOS conventions:

-   swipe back
-   sheets
-   haptics
-   safe areas
-   Dynamic Type
-   native share sheet
-   status bar behavior

The visual language can remain NEKI-branded while interaction follows
platform expectations.

------------------------------------------------------------------------

# 103. Haptics

Use haptics sparingly.

Recommended:

-   contribution confirmation
-   successful bookmark
-   toggle selection
-   important tracking transition
-   payment success

Avoid haptics for every tap.

------------------------------------------------------------------------

# 104. Navigation Transitions

Recommended:

### Home → Mission

Shared-image / push transition.

### Explore → Mission

Push transition.

### Mission → Contribution

Push or modal flow.

### Contribution → Success

Dedicated full-screen success state.

### Activity → Contribution Record

Push.

### Profile → Settings

Push.

------------------------------------------------------------------------

# 105. Hero Motion

The NEKI butterfly can be a recurring brand motion element.

Behavior:

-   subtle floating
-   slight rotation
-   slow movement
-   never distracting

It can appear in:

-   splash
-   onboarding
-   success
-   empty states
-   impact storytelling

Do not put the butterfly on every screen.

------------------------------------------------------------------------

# 106. Ambient 3D Motion

Objects can have:

``` text
translateY
rotation
scale
opacity
blur
```

Movement should be very slow.

Example:

``` text
8–16 px vertical movement
2–4° rotation
4–8 second cycle
```

Randomize phases to avoid synchronized movement.

------------------------------------------------------------------------

# 107. Scroll Behavior

Home:

-   header compresses subtly
-   search may remain accessible
-   bottom nav remains stable

Mission:

-   hero image collapses into compact navigation header

Explore:

-   search/filter controls remain accessible

Impact:

-   stats remain near top
-   feed scrolls naturally

------------------------------------------------------------------------

# 108. Pull to Refresh

Use where meaningful:

-   Home
-   Explore
-   Activity
-   tracking

Do not use it during active payment.

------------------------------------------------------------------------

# 109. Real-Time UI

Tracking must update without requiring manual refresh.

States:

``` text
Connecting
Live
Reconnecting
Last updated
```

If connection is lost:

``` text
Connection interrupted.
Showing latest update from 10:42 AM.
```

------------------------------------------------------------------------

# 110. Microcopy Principles

NEKI copy should be:

-   short
-   direct
-   warm
-   confident
-   transparent

Good:

> Your contribution is on the way.

Good:

> Impact verified.

Bad:

> Congratulations! You have successfully changed someone's entire
> life!!!

Avoid exaggerated claims.

------------------------------------------------------------------------

# 111. Emotional Design

The product should create three emotional moments:

### Before

> I can help.

### During

> I know what's happening.

### After

> I can see the impact.

This is the core NEKI UX loop.

------------------------------------------------------------------------

# 112. Contribution UX Loop

``` text
Discover
   ↓
Understand
   ↓
Trust
   ↓
Contribute
   ↓
Track
   ↓
Verify
   ↓
See Impact
   ↓
Return
```

Every major feature should reinforce this loop.

------------------------------------------------------------------------

# 113. Trust UX Loop

``` text
Organization
     ↓
Mission
     ↓
Contribution
     ↓
Execution
     ↓
Proof
     ↓
Verification
     ↓
Impact Ledger
```

The interface should make this chain visible.

------------------------------------------------------------------------

# 114. Design System Component Inventory

The implementation should create reusable components.

### Navigation

-   AppBottomNav
-   TopAppBar
-   BackButton
-   ProfileButton
-   NotificationButton

### Cards

-   MissionCard
-   FeaturedMissionCard
-   ImpactCard
-   CategoryCard
-   OrganizationCard
-   ActivityCard
-   CertificateCard

### Inputs

-   SearchField
-   AmountField
-   TextField
-   AddressField
-   DateSelector
-   TimeSelector

### Controls

-   PrimaryButton
-   SecondaryButton
-   IconButton
-   Chip
-   SegmentedControl
-   FilterButton
-   BookmarkButton
-   ShareButton

### Feedback

-   Snackbar
-   Toast
-   EmptyState
-   ErrorState
-   Skeleton
-   LoadingIndicator

### Trust

-   VerificationBadge
-   MissionStatusBadge
-   ProofCard
-   ImpactRecordCard

### Tracking

-   TrackingMap
-   TrackingTimeline
-   DeliveryMarker
-   ETAChip

------------------------------------------------------------------------

# 115. Component State Requirements

Every component must document:

``` text
Default
Pressed
Focused
Disabled
Loading
Success
Error
Selected
Unselected
Offline
```

Interactive components must never be designed only for their happy path.

------------------------------------------------------------------------

# 116. Mission Card Component Contract

A mission card should support:

``` text
image
category
title
location
progress
goal
currentAmount
urgency
bookmark
verified
distance
status
```

Optional:

``` text
volunteersNeeded
deadline
contributionTypes
```

The component must gracefully handle missing optional data.

------------------------------------------------------------------------

# 117. Image Loading

Mission images:

1.  placeholder
2.  low-resolution preview
3.  full-resolution image
4.  cached image on repeat visits

Use appropriate image caching.

Never block the entire screen on one image.

------------------------------------------------------------------------

# 118. Content Moderation UX

User-uploaded:

-   photos
-   descriptions
-   mission updates
-   proof

must have:

-   moderation state
-   review state
-   rejected state
-   appeal/report pathway where applicable

UI should avoid presenting unreviewed content as verified evidence.

------------------------------------------------------------------------

# 119. Verification UX

Possible verification states:

``` text
Not Reviewed
Under Review
Verified
Needs More Information
Rejected
Expired
```

Use exact language.

Never blur these into a generic "trusted" state.

------------------------------------------------------------------------

# 120. Error Prevention

Before contribution:

-   confirm amount
-   confirm mission
-   confirm payment method
-   confirm pickup address for items
-   confirm volunteer time

After payment:

-   show transaction status
-   reconcile server-side
-   prevent duplicate taps

Buttons should enter loading state immediately.

------------------------------------------------------------------------

# 121. Double-Submission Prevention

For all irreversible actions:

``` text
Tap
↓
Disable action
↓
Show progress
↓
Server confirmation
↓
Success
```

If request times out:

Do not assume failure.

Show:

> We're confirming your contribution.

Then reconcile against backend status.

------------------------------------------------------------------------

# 122. Security UX

Never display:

-   full payment credentials
-   private beneficiary information
-   private organization documents
-   unnecessary volunteer personal information

Sensitive actions may require:

-   biometric confirmation
-   re-authentication
-   OTP

------------------------------------------------------------------------

# 123. Privacy UX

Privacy controls should be understandable.

Examples:

``` text
Profile visibility
Contribution visibility
Impact sharing
Location permissions
Notification preferences
```

Defaults should be privacy-conscious.

------------------------------------------------------------------------

# 124. Notifications

Notification categories:

### Contribution

> Your contribution has been picked up.

### Tracking

> Your contribution is 8 minutes away.

### Verification

> Your contribution has been verified.

### Impact

> Your ₹1,000 contribution supported 200 meals.

### Volunteer

> Your volunteer mission starts tomorrow at 10 AM.

Notifications should deep-link to the relevant screen.

------------------------------------------------------------------------

# 125. Deep Links

Every important object should have a deep link.

Examples:

``` text
neki://mission/{id}
neki://organization/{id}
neki://contribution/{id}
neki://category/{slug}
```

Universal/app links should resolve correctly.

------------------------------------------------------------------------

# 126. Share Preview

When a mission is shared externally:

``` text
NEKI
Provide 200 meals to
underprivileged children

62% funded
New Delhi

Humanity, Delivered.
```

The preview should feel premium and trustworthy.

------------------------------------------------------------------------

# 127. Onboarding Strategy

Do not use a five-screen tutorial explaining obvious features.

Prefer:

``` text
Welcome
↓
Why NEKI
↓
Location / causes preference
↓
Home
```

Progressive education should happen through product usage.

------------------------------------------------------------------------

# 128. First-Time User Experience

For a new user:

1.  welcome
2.  authentication
3.  location
4.  optional cause selection
5.  home
6.  contextual explanation of first mission
7.  contribution
8.  tracking
9.  impact

The user should understand NEKI within one session.

------------------------------------------------------------------------

# 129. Returning User Experience

Returning users should land directly on Home.

If an active contribution exists:

Show a high-priority module:

``` text
Your contribution is on the way
Track now →
```

This should be more prominent than generic discovery.

------------------------------------------------------------------------

# 130. Personal Impact Summary

The profile/impact system should eventually show:

``` text
Your NEKI Journey

12 missions
48 people helped
28 volunteer hours
5 items donated
3 organizations supported
```

Only verified or platform-recorded values should be counted.

------------------------------------------------------------------------

# 131. Gamification Rules

NEKI may use light progression, but avoid competitive charity mechanics.

Avoid:

-   leaderboards based on money
-   public wealth comparisons
-   "donate more than your friends"
-   manipulative streaks

Prefer:

-   impact milestones
-   certificates
-   meaningful contribution history
-   volunteering milestones

------------------------------------------------------------------------

# 132. Accessibility-Friendly Emotional Design

Emotional impact must never depend on:

-   flashing animation
-   color-only signals
-   tiny text
-   audio-only feedback

Every important state has:

-   visual
-   textual
-   semantic

representation.

------------------------------------------------------------------------

# 133. Analytics Events

UI should instrument major actions.

Examples:

``` text
screen_view
mission_viewed
mission_saved
search_started
search_completed
filter_applied
contribution_started
contribution_type_selected
amount_selected
payment_started
payment_completed
payment_failed
volunteer_started
volunteer_completed
tracking_opened
tracking_status_viewed
impact_viewed
certificate_opened
mission_shared
```

Analytics must never capture sensitive payment credentials.

------------------------------------------------------------------------

# 134. UX Funnel

Track:

``` text
Home
 ↓
Mission View
 ↓
Contribution Start
 ↓
Contribution Review
 ↓
Payment
 ↓
Success
 ↓
Tracking
 ↓
Verified Impact
```

Primary conversion metric:

**completed meaningful impact action**, not merely app opens.

------------------------------------------------------------------------

# 135. Performance Targets

UI should feel instant.

Targets:

### App launch

Fast first frame.

### Home

Render cached shell immediately.

### Navigation

Respond immediately to taps.

### Search

Debounce network requests.

### Images

Progressively load.

### Tracking

Keep map and timeline responsive.

Avoid:

-   giant initial bundles
-   unnecessary rebuilds
-   blocking animations
-   unoptimized images

------------------------------------------------------------------------

# 136. Flutter Implementation Guidance

Recommended UI architecture:

``` text
lib/
  app/
    theme/
    router/
    navigation/

  core/
    design_system/
    networking/
    storage/
    analytics/

  shared/
    widgets/
    animations/
    models/

  features/
    home/
    explore/
    mission/
    contribution/
    tracking/
    impact/
    profile/
    category/
    authentication/
```

Design components should be reusable and feature-independent.

------------------------------------------------------------------------

# 137. Flutter Design Tokens

Create a central token layer:

``` text
NekiColors
NekiTypography
NekiSpacing
NekiRadius
NekiShadows
NekiMotion
NekiIcons
```

No random colors or spacing values throughout feature code.

------------------------------------------------------------------------

# 138. Theme Architecture

Support:

``` text
NekiLightTheme
NekiDarkTheme
```

Dark mode should preserve the brand rather than simply invert colors.

Primary green should remain recognizable.

Warm neutrals become darker charcoal-green surfaces.

------------------------------------------------------------------------

# 139. Dark Mode Direction

Background:

deep warm charcoal.

Cards:

dark green-gray.

Primary:

slightly brighter green.

Text:

warm white.

Secondary:

desaturated gray-green.

Avoid pure black + pure white everywhere.

------------------------------------------------------------------------

# 140. Responsive Layout

At widths below 360:

-   reduce horizontal padding
-   switch dense grids
-   allow horizontal scrolling category chips

At 390--430:

-   default composition

At tablets:

-   two-column mission browsing
-   persistent side navigation may be considered
-   larger map/detail composition

Do not simply stretch mobile cards.

------------------------------------------------------------------------

# 141. Tablet Layout

Suggested:

``` text
Sidebar / Navigation

Main content
├── Search
├── Categories
├── Mission grid
└── Featured mission
```

Mission detail can use:

``` text
Image / map     Mission information
                Contribution CTA
```

------------------------------------------------------------------------

# 142. Landscape

Support landscape where reasonable.

Tracking can become:

``` text
Map | Timeline
```

Contribution forms should remain readable.

------------------------------------------------------------------------

# 143. Safe Areas

All full-screen screens must respect:

-   notch
-   Dynamic Island
-   Android cutouts
-   home indicator
-   gesture navigation

No content should collide with system UI.

------------------------------------------------------------------------

# 144. Design QA

Every screen must be checked for:

### Visual

-   spacing
-   alignment
-   typography
-   image crop
-   color
-   radius
-   shadow

### Functional

-   buttons
-   navigation
-   back
-   keyboard
-   loading
-   error

### Accessibility

-   screen reader
-   dynamic type
-   contrast
-   touch targets

### Performance

-   scroll
-   image loading
-   animation
-   memory

------------------------------------------------------------------------

# 145. Screenshot Review Checklist

For every implemented screen compare against the reference direction:

``` text
Does it feel premium?
Does it feel warm?
Is the green used intentionally?
Is there enough whitespace?
Is the hierarchy obvious?
Are cards too heavy?
Are shadows too strong?
Are fonts too generic?
Is the screen too crowded?
Is the CTA obvious?
Does the screen communicate trust?
Does the screen communicate action?
```

------------------------------------------------------------------------

# 146. Visual Anti-Patterns

Do NOT introduce:

-   excessive gradients
-   neon green
-   generic NGO stock imagery
-   huge dashboard widgets
-   excessive glassmorphism
-   giant shadows
-   excessive badges
-   excessive animations
-   dense tables on mobile
-   crypto-style "impact scores"
-   gamified donation leaderboards
-   generic purple SaaS UI
-   cartoonish charity graphics
-   giant floating action buttons everywhere

------------------------------------------------------------------------

# 147. Premium Quality Rules

The app should feel premium because of:

-   typography
-   spacing
-   photography
-   motion
-   consistency
-   interaction detail
-   content quality
-   trust transparency

Not because of:

-   gold
-   glossy gradients
-   ornamental decoration
-   unnecessary 3D
-   excessive animations

------------------------------------------------------------------------

# 148. Screen-by-Screen Implementation Priority

## P0 --- Critical

1.  Splash
2.  Welcome
3.  Authentication
4.  Home
5.  Explore
6.  Mission Detail
7.  Contribution
8.  Payment
9.  Success
10. Tracking
11. Activity / Impact
12. Profile

## P1

13. Category
14. Search
15. Filters
16. Bookmarks
17. Certificates
18. Organization
19. Notifications
20. Help

## P2

21. Advanced impact visualization
22. Personalized recommendations
23. Advanced volunteering
24. Corporate-facing experiences

------------------------------------------------------------------------

# 149. Critical User Journeys

## Journey A --- Money

``` text
Home
→ Explore
→ Mission
→ Contribute
→ Money
→ ₹1,000
→ Review
→ Payment
→ Success
→ Track
→ Verified Impact
```

## Journey B --- Item

``` text
Home
→ Category
→ Mission
→ Contribute
→ Items
→ Item details
→ Photos
→ Pickup
→ Review
→ Confirmation
→ Tracking
→ Verification
```

## Journey C --- Volunteer

``` text
Explore
→ Mission
→ Volunteer
→ Role
→ Date
→ Time
→ Confirm
→ Activity
→ Certificate
```

## Journey D --- Discover Anything

``` text
Home
→ Explore
→ Search
→ Mission
→ Understand need
→ Choose contribution type
→ Contribute
```

------------------------------------------------------------------------

# 150. Critical Edge Cases

Design explicit UI for:

### Mission becomes fully funded

Replace:

`Contribute Now`

with:

`Mission Fully Funded`

Then offer:

`Explore Similar Missions`

### Mission deadline passes

Show:

`Mission Closed`

### Organization becomes unverified

Show:

`Verification status changed`

and explain.

### Payment succeeds but response is delayed

Show:

`Confirming contribution`

not failure.

### Delivery is delayed

Show:

`Delayed`

with updated ETA.

### Proof is pending

Show:

`Impact verification in progress`

### Contribution is cancelled

Show:

-   reason
-   refund status
-   next steps

------------------------------------------------------------------------

# 151. Design for Trust, Not Just Conversion

A user should be able to answer:

``` text
Who needs help?
What exactly is needed?
Who is organizing it?
Where is it happening?
How much is required?
How much has been completed?
What happens after I contribute?
How do I know it was delivered?
How do I know the impact is real?
```

If the interface cannot answer these questions, the experience is
incomplete.

------------------------------------------------------------------------

# 152. Mission Detail Information Priority

The mission screen should answer the questions in this order:

``` text
What is this?
↓
Why does it matter?
↓
Who is responsible?
↓
What is needed?
↓
How much progress has happened?
↓
What can I contribute?
↓
How will it be tracked?
↓
How will it be verified?
```

------------------------------------------------------------------------

# 153. Home Personalization Priority

The first screen should prioritize:

``` text
Active contribution
↓
Urgent nearby mission
↓
Recommended mission
↓
Category discovery
↓
Broader exploration
```

For new users:

``` text
Category discovery
↓
Featured mission
↓
Nearby
↓
Urgent
```

------------------------------------------------------------------------

# 154. Emotional Hierarchy by Screen

  Screen         Primary Emotion
  -------------- -----------------
  Splash         Hope
  Welcome        Possibility
  Home           Discovery
  Explore        Curiosity
  Mission        Trust
  Contribution   Agency
  Payment        Confidence
  Success        Gratitude
  Tracking       Reassurance
  Impact         Pride
  Profile        Belonging

------------------------------------------------------------------------

# 155. UX Writing Examples

### Discovery

> Find a mission worth supporting.

### Contribution

> Choose how you want to help.

### Tracking

> Your contribution is on the way.

### Verification

> Delivery confirmed. Impact verification is in progress.

### Completion

> Impact verified.

### Empty

> No missions match these filters.

### Error

> Something went wrong. Let's try again.

------------------------------------------------------------------------

# 156. Avoiding Emotional Manipulation

Never use:

-   countdowns unless there is a real deadline
-   fake urgency
-   fabricated beneficiary numbers
-   fake scarcity
-   exaggerated claims
-   guilt-based copy
-   misleading progress

Urgency must come from actual mission data.

------------------------------------------------------------------------

# 157. Design Relationship With the NEKI Brand

The logo and butterfly are the brand anchor.

The butterfly should represent:

-   transformation
-   movement
-   kindness
-   connection
-   possibility

But it should remain restrained.

Use the mark prominently in:

-   splash
-   onboarding
-   success
-   impact storytelling
-   empty states

Use it minimally elsewhere.

------------------------------------------------------------------------

# 158. Brand Signature

Use:

**Humanity, Delivered.**

as the recurring brand signature.

Potential placements:

-   splash
-   onboarding
-   share cards
-   success
-   footer/about

Do not place it beneath every section.

------------------------------------------------------------------------

# 159. About NEKI UX

About screen should communicate:

``` text
NEKI

Humanity, Delivered.

A platform built to make helping
visible, trackable and trustworthy.

Discover.
Contribute.
Track.
Make a real impact.
```

It should connect the consumer experience to the broader NEKI mission.

------------------------------------------------------------------------

# 160. Future Expansion Compatibility

The UI system must be able to support future NEKI functionality without
redesigning the entire app.

Future surfaces may include:

-   corporate CSR
-   NGO dashboards
-   community missions
-   surplus redistribution
-   employee volunteering
-   impact reports
-   campaigns
-   institutional giving
-   organization profiles
-   recurring contributions

The consumer app should therefore use reusable concepts:

``` text
Mission
Organization
Contribution
Volunteer
Proof
Impact
```

rather than hard-coded donation-only concepts.

------------------------------------------------------------------------

# 161. Design System Naming

Recommended Flutter naming:

``` text
NekiButton
NekiCard
NekiChip
NekiSearchField
NekiMissionCard
NekiCategoryCard
NekiProgressBar
NekiStatusBadge
NekiVerificationBadge
NekiAvatar
NekiBottomNav
NekiSectionHeader
NekiBottomSheet
NekiEmptyState
NekiErrorState
NekiSkeleton
NekiTimeline
NekiImpactStat
```

------------------------------------------------------------------------

# 162. UX Documentation Per Screen

Every production screen must have a separate design specification
containing:

``` text
1. Purpose
2. Entry points
3. Exit points
4. User goal
5. Content hierarchy
6. Component inventory
7. Layout
8. Typography
9. Colors
10. States
11. Interactions
12. Animation
13. Accessibility
14. Analytics
15. API/data dependencies
16. Loading state
17. Empty state
18. Error state
19. Offline behavior
20. Edge cases
```

------------------------------------------------------------------------

# 163. Design Handoff Requirements

Every Figma/design implementation should include:

-   exact spacing
-   typography tokens
-   component variants
-   states
-   interactive prototypes
-   responsive behavior
-   dark mode
-   accessibility notes
-   content examples
-   asset names
-   image crop rules
-   animation specifications

Do not hand off only static screenshots.

------------------------------------------------------------------------

# 164. Final Visual Benchmark

The finished application should visually read as:

> **A premium, calm, modern marketplace for real-world impact.**

The first impression should be:

``` text
Beautiful
↓
Simple
↓
Trustworthy
↓
Useful
↓
Actionable
```

Not:

``` text
Charity website
↓
Donation request
↓
Form
```

------------------------------------------------------------------------

# 165. Final Product Experience

The ideal NEKI session should feel like:

``` text
I opened the app.

I immediately understand what NEKI does.

I can see real missions.

I can understand exactly what each mission needs.

I can choose how I want to help.

I can contribute with minimal friction.

I can see what happened to my contribution.

I can see when it was delivered.

I can see when it was verified.

I can see the impact afterward.

I want to come back.
```

That is the complete NEKI UI/UX north star.

------------------------------------------------------------------------

# 166. Implementation Directive

When implementing this design:

### MUST

-   follow the NEKI design tokens
-   preserve the warm editorial aesthetic
-   use deep green as the primary action color
-   use serif typography for emotional/editorial moments
-   use sans-serif typography for UI
-   use rounded cards and controls
-   use mission photography thoughtfully
-   support real-time tracking
-   make impact visible
-   provide complete loading/error/empty states
-   implement accessibility
-   implement responsive behavior
-   use reusable components
-   use real data states
-   make contribution status unambiguous

### SHOULD

-   use subtle 3D ambient elements
-   use restrained glass surfaces
-   use gentle motion
-   use native platform interaction conventions
-   use skeleton loading
-   personalize discovery

### MUST NOT

-   turn the app into a generic NGO dashboard
-   overuse green
-   overuse 3D
-   overuse gradients
-   use fake urgency
-   hide contribution mechanics
-   fabricate impact
-   use manipulative charity copy
-   sacrifice accessibility for aesthetics
-   treat iOS and Android as identical platforms

------------------------------------------------------------------------

# 167. Final UI/UX Quality Bar

A screen is not considered complete merely because it looks like the
reference.

It is complete only when:

``` text
Visual quality       ✓
Interaction quality  ✓
Content hierarchy    ✓
Accessibility        ✓
Performance          ✓
Loading states       ✓
Error states         ✓
Empty states         ✓
Offline behavior     ✓
Analytics            ✓
Security             ✓
Responsive layout    ✓
Platform conventions ✓
```

**NEKI should feel like the intersection of modern commerce UX,
editorial design, trustworthy infrastructure, and human impact.**

## Brand

**NEKI**

**Humanity, Delivered.**

> Discover. Contribute. Track. Make a real impact.
