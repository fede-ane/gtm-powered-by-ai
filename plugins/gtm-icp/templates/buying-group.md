---
module: gtm-icp
status: template        # template | draft | final (final only on the owner's yes)
approved_by: ""         # the role who marked it final, never a personal name
approved_on: ""
segment: ""             # the Core segment the roles come from
rules_version: 1
last_updated: ""
sources: []
---

# Buying group and personas

<!-- Written by /gtm-icp:dossier. Method: the icp-buying-group skill. Rules: gtm/RULES.md.
     B2C: this file is not built. Roles are labelled by what they do, never with an invented name. -->

## Buying group

<!-- Up to 4 roles, from the contacts on won deals of the Core segment.
     Primary: on at least half of those deals, and a part in the decision (champion, budget owner, technical evaluator).
     Supporting: the rest. Roles with the same decision criteria are merged.
     Source: the deal-role counts, and any quote cited by role, company and file. -->

| Role | Part in the decision | Weight | On won deals | Source |
|---|---|---|---|---|
| | | Primary / Supporting | x of y | |

## Personas

<!-- One per primary role, in this field order. Copy the block for each. -->

### [Role] · [part in the decision]

- **Role:** <!-- the titles seen, the company type; "Seen at" up to three customers -->
- **Needs:**
- **Pain points:** <!-- one or two quotes, word for word, with source; public ones tagged proxy -->
- **Objections:**
- **Message:** <!-- one suggested line, tagged proposed; then "Their words, not ours:" and a quote that supports it -->
- **Proof to show:** <!-- only proof the inputs hold; otherwise blank, with the reason -->

## Supporting roles

- **[Role]:** <!-- one line: what they need, and when they join -->

## Data notes

<!-- The title-to-role map, contacts with no title, columns ignored (personal data). -->

## Open tags

| Section | Line | Tag | Decision |
|---|---|---|---|

## Checks

| Check | Result | Lines |
|---|---|---|
| Question test | | |
| One idea per cell | | |
| Ambiguous words | | |
| Unproven lines | | |
