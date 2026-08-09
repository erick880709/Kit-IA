# Extracting a screen inventory from a PRD

PRDs rarely list screens explicitly — they describe features, user stories, and flows. Derive screens from those.

## Heuristics

- **One user story often implies one screen**, but not always: "As a user I can filter and sort results" is the same screen as "As a user I can browse the catalog" (both live on a listing screen). Group stories that operate on the same object/view together.
- **CRUD verbs imply a screen each**: create, read/view, update, delete/list frequently need distinct screens (e.g. "Create project" form vs. "Project detail" view vs. "Projects list").
- **Auth/onboarding is almost always implied even if unstated**: if the PRD assumes "logged-in users", there's a login screen and probably a first-run/empty state, even if the PRD never mentions them. Mark these as inferred.
- **Look for role/permission language** ("admins can...", "as a manager..."): different roles often mean different screens or at least different states of the same screen — don't silently merge them.
- **Non-happy-path language** ("if no results found", "when the payment fails") is a direct instruction to design that state — don't skip it because it wasn't in a bolded "Screens" section.

## Worked example

PRD excerpt: *"Users can browse available appointment slots for a clinic, book one, and see a confirmation. Clinic staff can view a calendar of all bookings and cancel a booking. If a user tries to book a slot that was just taken, show an error."*

Extracted inventory:

| Screen | Purpose | Key elements | Links to | States |
|---|---|---|---|---|
| Slot browser | User picks a clinic + time | Filter by clinic, list/grid of slots | Booking confirmation | Empty (no slots), Error (slot taken) |
| Booking confirmation | Confirms the booked slot | Summary, confirm CTA | Slot browser (back) | Success |
| Staff calendar | Staff views/cancels bookings | Calendar grid, cancel action | — | Empty (no bookings) |
| Login *(inferred)* | Auth gate before booking/staff views | Email/password or SSO | Slot browser or Staff calendar | — |

Note the "Error (slot taken)" state is called out explicitly in the PRD text — that's a required state on the Slot browser screen, not optional polish.
