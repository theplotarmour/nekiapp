# Interactive journey review

Serve from the repository root:

```powershell
.venv-contracts/Scripts/python -m http.server 8769 --bind 127.0.0.1 --directory docs/design
```

Open [the local prototype](http://127.0.0.1:8769/prototype/). Stop the server when finished. This static design artifact simulates nine journeys in 36 review steps; it is not the NEKI app or a backend acceptance test. It makes no provider requests. Theme tokens are loaded from the adjacent checked-in JSON. Fonts currently use local system fallbacks; licensed Instrument Serif/Inter bundling remains in the asset handoff.

Use journey navigation, amount presets/input, Continue/Back/Start again, the recovery selector, light/dark themes and 100%/200% text controls. Recovery controls reset a simulated scenario for review; they do not represent real authorization restoration or reconciliation. Each consequential outcome is explicitly labeled simulated.

## Observed browser evidence — 2026-09-13

Chrome 153 via agent-browser 0.37.1 on Windows:

- All nine journeys advanced through four distinct headings and returned to their initial step (36 step transitions).
- Invalid zero amount kept the first step visible, exposed the linked error and focused the amount input. A ₹2,500 value carried through to allocation review.
- All five recovery variants exposed their message and recovery control: offline, revoked, stale, uncertain and more-information-needed.
- Dark theme at 320×844 with 200% body text produced a 320 px document width. All 36 stages had no horizontal document overflow; all visible buttons/inputs/selects met 44×44 px minimum targets.
- Visual inspection found overlapping narrow review labels and fragmented amount chips; the controls were changed to stack and amount chips reflow. Follow-up measurements confirmed no review-control overlap, and a second screenshot was inspected.
- The initial desktop screenshot and final narrow dark screenshot were visually inspected. Browser page-error collection was empty.

These are bounded browser checks, not a conformance certification. Remaining: full 165-row component/screen realization, 360/390/412 and portal-size matrix, real keyboard/screen-reader tasks, Figma/component assets, reviewed policy copy, and formative sessions with actual contributor, volunteer, organization and ops representatives. Do not invent participant findings or mark P0/P1 accepted from the automated walkthrough.
