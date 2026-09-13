"use strict";
const step = (title, copy, details, action, privacy = "") => ({
  title,
  copy,
  details,
  action,
  privacy,
});
const journeys = [
  {
    name: "A · Give money",
    section: "A little kindness, clearly accounted for",
    steps: [
      step(
        "Support a community kitchen",
        "Choose an amount for this simulated Delhi mission.",
        [
          ["Organization", "Example Community Kitchen"],
          ["Need", "Daily meals"],
        ],
        "Review contribution",
      ),
      step(
        "Know where it goes",
        "Review the allocation before opening checkout.",
        [
          ["You contribute", "{amount}"],
          ["Mission allocation", "{amount}"],
          ["Gateway fee", "Covered by NEKI"],
        ],
        "Open simulated checkout",
        "This is a payment acknowledgement flow. It does not establish tax-document eligibility.",
      ),
      step(
        "Checking your payment",
        "A checkout return is not proof of capture. We’re checking the recorded provider outcome.",
        [
          ["Payment", "Awaiting confirmation"],
          ["Impact", "Not yet verified"],
        ],
        "Simulate confirmed capture",
        "Do not start another payment while the first outcome is uncertain.",
      ),
      step(
        "Contribution received",
        "Your contribution appears in Activity. Delivery and verification will follow.",
        [
          ["Payment", "Captured — simulated"],
          ["Mission", "In progress"],
          ["Impact record", "Not issued yet"],
        ],
        "Finish review",
        "A contribution receipt is separate from verified impact.",
      ),
    ],
  },
  {
    name: "B · Give items",
    section: "From your doorstep to a useful next chapter",
    steps: [
      step(
        "Books with more stories to tell",
        "Review the requested items and condition before scheduling.",
        [
          ["Items", "10 school books"],
          ["Condition", "Good"],
          ["Mission", "Delhi learning centre"],
        ],
        "Review pickup",
      ),
      step(
        "A pickup that works for you",
        "Only an approved service area and available slot can be booked.",
        [
          ["Address", "Private saved address"],
          ["Area", "Synthetic Delhi service zone"],
          ["Pickup", "Example available slot"],
        ],
        "Simulate pickup booking",
        "Your exact address is shared only with currently authorized pickup staff.",
      ),
      step(
        "Your pickup is scheduled",
        "An approved volunteer must accept the assignment before collecting.",
        [
          ["Assignment", "Awaiting approved volunteer"],
          ["Items", "10 books"],
          ["Custody", "With contributor"],
        ],
        "Simulate pickup and delivery",
      ),
      step(
        "Delivery acknowledged",
        "The receiving organization acknowledged the items. Evidence still needs review.",
        [
          ["Items", "10 received"],
          ["Proof", "Awaiting review"],
          ["Impact", "Not yet verified"],
        ],
        "Finish review",
      ),
    ],
  },
  {
    name: "C · Volunteer",
    section: "Give time, with care",
    steps: [
      step(
        "Start your volunteer application",
        "Tell the review team your availability and interests. Phone verification alone does not approve volunteering.",
        [
          ["Phone", "Verified — simulated"],
          ["Application", "Draft"],
          ["Government ID", "Not required for MVP"],
        ],
        "Simulate application submission",
      ),
      step(
        "Your application is under review",
        "You can keep exploring. Booking opens after current ops approval.",
        [
          ["Status", "Under review"],
          ["Booking", "Unavailable until approved"],
        ],
        "Simulate ops approval",
      ),
      step(
        "Choose a volunteer slot",
        "An approved application, current eligibility and available capacity are required.",
        [
          ["Mission", "Community kitchen"],
          ["Role", "Meal preparation"],
          ["Availability", "Simulated open slot"],
        ],
        "Simulate booking and attendance",
      ),
      step(
        "Time recorded, review pending",
        "Check-in and check-out are evidence. Hours become verified after attendance review.",
        [
          ["Attendance", "Checked out"],
          ["Hours", "Awaiting verification"],
          ["Certificate", "Metadata after verification"],
        ],
        "Finish review",
        "No unavailable PDF download is shown.",
      ),
    ],
  },
  {
    name: "D · Discover nearby",
    section: "Find your way to help",
    steps: [
      step(
        "A kinder world, close to home",
        "Use a manually selected area even when location permission is denied.",
        [
          ["Selected area", "New Delhi"],
          ["Location permission", "Not required to browse"],
        ],
        "Explore missions",
      ),
      step(
        "Find something that matters",
        "Browse missions by cause. Search must not replace current results with a late older response.",
        [
          ["Cause", "Education"],
          ["Search", "Learning"],
          ["Result", "Delhi learning centre"],
        ],
        "View mission",
      ),
      step(
        "Help in the way you can",
        "Each need has its own availability. One completed need does not close all the others.",
        [
          ["Money", "Target reached"],
          ["Items", "Books still needed"],
          ["Time", "Slots available"],
        ],
        "Review available needs",
      ),
      step(
        "Keep this mission close",
        "Bookmarks are private to your account. Public share links expose only public mission details.",
        [
          ["Saved mission", "Sign-in required"],
          ["Public share", "Mission page only"],
        ],
        "Finish review",
      ),
    ],
  },
  {
    name: "E · Publish a mission",
    section: "Organization workspace",
    steps: [
      step(
        "Your organization application",
        "Submit evidence for review. Document rework preserves earlier submissions.",
        [
          ["Organization", "Example Community Kitchen"],
          ["Review", "More information needed"],
        ],
        "Simulate document resubmission",
      ),
      step(
        "Prepare a mission draft",
        "Current organization approval is required before publication. Save a clear description and quantified needs.",
        [
          ["Organization", "Verified — simulated"],
          ["Mission", "Draft"],
          ["Needs", "Meals, items and time"],
        ],
        "Submit for moderation",
      ),
      step(
        "Review before publication",
        "The reviewer sees a fixed submission revision. An edit must not silently replace that revision.",
        [
          ["Revision", "3"],
          ["Moderation", "Pending review"],
        ],
        "Simulate reviewer approval",
      ),
      step(
        "Your mission is published",
        "The approved revision is now public. Material changes require their own reviewed change request.",
        [
          ["Revision", "3 — approved"],
          ["Visibility", "Public"],
          ["Target changes", "Approval required"],
        ],
        "Finish review",
      ),
    ],
  },
  {
    name: "F · Review proof",
    section: "Evidence before impact",
    steps: [
      step(
        "A delivery to review",
        "Open the submitted evidence and its provenance. Private files stay purpose-scoped.",
        [
          ["Subject", "Simulated item delivery"],
          ["Evidence revision", "2"],
          ["Review", "Pending"],
        ],
        "Inspect evidence",
      ),
      step(
        "Check the evidence",
        "Confirm receipt, media checks and consent. Illustration cannot stand in for delivery proof.",
        [
          ["Media", "Synthetic placeholder only"],
          ["Receipt", "Example acknowledgement"],
          ["Consent", "Review required"],
        ],
        "Simulate requesting information",
      ),
      step(
        "More information requested",
        "Tell the submitter what is missing. Keep the previous revision and reason visible.",
        [
          ["Decision", "Needs more information"],
          ["Requested", "Receiving acknowledgement"],
          ["Impact", "Not issued"],
        ],
        "Simulate corrected evidence review",
      ),
      step(
        "Verified record ready",
        "In a real flow, only the accepted evidence and committed completion issue a unique record.",
        [
          ["Review", "Accepted — simulated"],
          ["Record", "Example verified metadata"],
          ["Corrections", "Append with reason"],
        ],
        "Finish review",
        "No real delivery or beneficiary claim is made by this prototype.",
      ),
    ],
  },
  {
    name: "G · Approve a payout",
    section: "Finance workspace",
    steps: [
      step(
        "Prepare a manual payout",
        "Review contribution allocations, recipient and supporting evidence.",
        [
          ["Amount", "₹10,000 — simulated"],
          ["Bank revision", "4"],
          ["Status", "Draft"],
        ],
        "Review approval",
      ),
      step(
        "Independent approval",
        "The drafter cannot approve their own payout. Bank or allocation changes invalidate the old approval.",
        [
          ["Drafter", "Example operator A"],
          ["Approver", "Example operator B"],
          ["Bank revision", "4 — bound"],
        ],
        "Simulate independent approval",
      ),
      step(
        "Record the transfer outcome",
        "A timeout is uncertain. Check the transfer reference before doing anything that could send again.",
        [
          ["Status", "Transfer outcome uncertain"],
          ["Reference", "Example reference"],
          ["Next action", "Reconcile existing transfer"],
        ],
        "Simulate matched bank evidence",
      ),
      step(
        "Payout reconciled",
        "A recorded transfer and matching evidence support the paid outcome.",
        [
          ["Transfer", "Paid — simulated"],
          ["Reconciliation", "Matched — simulated"],
          ["Audit", "Operator and reference retained"],
        ],
        "Finish review",
        "No money is transferred. Live funds require the separate legal/provider gate.",
      ),
    ],
  },
  {
    name: "H · Recover a pickup",
    section: "Volunteer workspace",
    steps: [
      step(
        "Your assigned pickup",
        "Check current eligibility and assignment before opening private route details.",
        [
          ["Assignment", "Approved — simulated"],
          ["Custody", "With contributor"],
          ["Address", "Private access only"],
        ],
        "Review pickup action",
      ),
      step(
        "Saved on this device",
        "A pickup captured offline is pending server acceptance. It must not appear as confirmed delivery.",
        [
          ["Local action", "Pending synchronization"],
          ["Assignment version", "7"],
          ["Custody", "Awaiting accepted receipt"],
        ],
        "Simulate reconnect",
      ),
      step(
        "The assignment has changed",
        "The queued action cannot override revoked access. Dispatch needs to resolve custody.",
        [
          ["Action", "Rejected — assignment changed"],
          ["Private route", "Access removed"],
          ["Recovery", "Dispatch case open"],
        ],
        "Review dispatch recovery",
      ),
      step(
        "Handoff needs acknowledgement",
        "A new assignment and custody receipt must be accepted before the timeline advances.",
        [
          ["Dispatch", "Example replacement arranged"],
          ["Custody", "Acknowledgement pending"],
          ["Delivery", "Not complete"],
        ],
        "Finish review",
      ),
    ],
  },
  {
    name: "I · Account and support",
    section: "Your information, handled with care",
    steps: [
      step(
        "How can we help?",
        "A support request needs a staffed queue and a visible status.",
        [
          ["Issue", "Example contribution question"],
          ["Queue", "Staffing not yet configured"],
        ],
        "Review account request",
      ),
      step(
        "Review your deletion request",
        "Explain what will be deleted and which records may need to be retained under reviewed policy.",
        [
          ["Account data", "Deletion review"],
          ["Financial records", "Retention decision required"],
          ["Access", "Step-up required"],
        ],
        "Simulate identity confirmation",
      ),
      step(
        "Your request is being reviewed",
        "A hold is not completion. The case must show its reason and accountable owner.",
        [
          ["Request", "Pending review"],
          ["Hold", "Example financial-record review"],
          ["Completion date", "Not promised"],
        ],
        "Review status detail",
      ),
      step(
        "A clear record of the request",
        "Keep status and support available without promising immediate blanket deletion.",
        [
          ["Case", "Open — simulated"],
          ["Next step", "Policy and hold review"],
          ["Notifications", "When status changes"],
        ],
        "Finish review",
      ),
    ],
  },
];
const $ = (id) => document.getElementById(id);
let journeyIndex = 0,
  stageIndex = 0,
  amount = 1000,
  tokens;
const currency = (value) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
const states = {
  normal: ["Main path", "Continue through the simulated steps."],
  offline: [
    "Connection unavailable. Your current input is preserved. Nothing has been submitted.",
    "Retry connection",
  ],
  revoked: [
    "Your access changed. Private details and the old action are unavailable.",
    "Return to journey start",
  ],
  stale: [
    "This record changed while you were reviewing. Refresh and review the current revision before deciding.",
    "Refresh record",
  ],
  uncertain: [
    "The outcome is not confirmed. Check the existing request before starting another.",
    "Check existing status",
  ],
  rework: [
    "More information is needed. Review the request and prepare a new evidence revision.",
    "Review information request",
  ],
};
function render(focus = false) {
  const j = journeys[journeyIndex],
    s = j.steps[stageIndex],
    state = $("scenario").value;
  $("path-name").textContent = j.name;
  $("section-name").textContent = j.section;
  $("screen-title").textContent = s.title;
  $("screen-copy").textContent = s.copy;
  $("step-count").textContent = `${stageIndex + 1} of ${j.steps.length}`;
  $("progress-fill").style.width =
    `${((stageIndex + 1) / j.steps.length) * 100}%`;
  $("details").replaceChildren();
  const details =
    state === "revoked"
      ? [
          ["Access", "No longer authorized"],
          ["Recovery", "Contact the appropriate support team"],
        ]
      : s.details;
  for (const [key, value] of details) {
    const row = document.createElement("div"),
      dt = document.createElement("dt"),
      dd = document.createElement("dd");
    dt.textContent = key;
    dd.textContent = value.replaceAll("{amount}", currency(amount));
    row.append(dt, dd);
    $("details").append(row);
  }
  $("amount-field").hidden = !(
    journeyIndex === 0 &&
    stageIndex === 0 &&
    state === "normal"
  );
  $("state-message").hidden = state === "normal";
  $("state-message").textContent = states[state][0];
  $("scenario-note").textContent =
    state === "normal"
      ? states.normal[1]
      : "Recovery is simulated. This control does not change any real record.";
  $("continue").textContent = state === "normal" ? s.action : states[state][1];
  $("back").disabled = stageIndex === 0;
  $("privacy").textContent =
    s.privacy || "Synthetic design review. No request is submitted.";
  document
    .querySelectorAll("#journeys button")
    .forEach((button, i) =>
      button.setAttribute("aria-current", String(i === journeyIndex)),
    );
  if (focus) $("screen-title").focus();
}
journeys.forEach((j, i) => {
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = j.name;
  button.addEventListener("click", () => {
    journeyIndex = i;
    stageIndex = 0;
    $("scenario").value = "normal";
    $("amount-error").hidden = true;
    render(true);
  });
  $("journeys").append(button);
});
$("continue").addEventListener("click", () => {
  const state = $("scenario").value;
  if (state !== "normal") {
    if (state === "revoked") stageIndex = 0;
    $("scenario").value = "normal";
    render(true);
    return;
  }
  if (journeyIndex === 0 && stageIndex === 0) {
    const raw = $("amount").value;
    const proposed = Number(raw);
    if (
      !raw.trim() ||
      !Number.isInteger(proposed) ||
      proposed < 1 ||
      proposed > 100000
    ) {
      $("amount-error").hidden = false;
      $("amount").setAttribute("aria-invalid", "true");
      $("amount").setAttribute("aria-describedby", "amount-error");
      $("amount").focus();
      return;
    }
    amount = proposed;
    $("amount-error").hidden = true;
    $("amount").removeAttribute("aria-invalid");
  }
  stageIndex = (stageIndex + 1) % journeys[journeyIndex].steps.length;
  render(true);
});
$("back").addEventListener("click", () => {
  stageIndex = Math.max(0, stageIndex - 1);
  $("scenario").value = "normal";
  render(true);
});
$("restart").addEventListener("click", () => {
  stageIndex = 0;
  $("scenario").value = "normal";
  render(true);
});
$("scenario").addEventListener("change", () => render());
document.querySelectorAll("[data-amount]").forEach((button) =>
  button.addEventListener("click", () => {
    $("amount").value = button.dataset.amount;
  }),
);
function theme() {
  if (!tokens) return;
  for (const [key, value] of Object.entries(tokens.themes[$("theme").value]))
    document.documentElement.style.setProperty(`--${key}`, value);
  document.documentElement.style.colorScheme = $("theme").value;
}
$("theme").addEventListener("change", theme);
$("scale").addEventListener("change", () =>
  document.documentElement.style.setProperty("--scale", $("scale").value),
);
fetch("../tokens.json")
  .then((response) => {
    if (!response.ok) throw Error("Token file unavailable");
    return response.json();
  })
  .then((data) => {
    tokens = data;
    theme();
  })
  .catch((error) => {
    $("scenario-note").textContent =
      "Theme tokens could not load. Serve this prototype over local HTTP.";
    console.error(error);
  });
render();
