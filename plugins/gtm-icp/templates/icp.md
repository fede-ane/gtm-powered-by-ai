---
module: gtm-icp
status: template        # template | draft | final (final only on the owner's yes)
approved_by: ""         # the role who marked it final, never a personal name
approved_on: ""
stage: ""               # hypothesis | partly validated | validated
business_type: ""       # B2B | B2C | services
rules_version: 1
last_updated: ""
sources: []             # every file in gtm/inputs/ that was used, with the date range for CRM data
published_url: ""       # the artifact link, once the page is published
---

# ICP

<!-- Written by /gtm-icp:dossier. Method: the icp-buying-group skill. Rules: gtm/RULES.md.
     Blank beats guessed. Tags: to confirm, proposed, hypothesis, proxy. No summary section.
     Leave out a section the stage can't fill (Who you want next, Jobs to be done) instead of padding it. -->

## Who buys now

<!-- The core fields, from the Core segment. The label says in plain words what they are or buy. Never a persona name. -->

- **Label:**
- **Company type and size:**
- **Buying champion:** <!-- one line; the roles in full are in buying-group.md -->
- **What they buy:**
- **Where they find you:**
- **Where they spend time:**
- **Pains:**
- **Objections:**
- **Triggers and what they set off:** <!-- each trigger says the question it raises and what the buyer does next -->

## Who you want next

<!-- Only when the strategy names a different target. Every line tagged "to confirm" until the data backs it. Never blended into "Who buys now". -->

- **Label:**
- **What would validate it:**
- **Decision:** <!-- which profile copy speaks to today, decided by whom, and why -->

## Segments

<!-- From the crm_profile.py scorecard. Ranked on value and loyalty first, then conversion and cost to serve.
     Under 5 won customers: keep the row with deals, won, win rate and revenue share; value, loyalty, cycle and cost
     to serve stay blank, with "too few to rank". A group with no wins stays in the table with its deal count. -->

| Segment | Customers (revenue share) | Value | Loyalty | Conversion | Cost to serve | Tier |
|---|---|---|---|---|---|---|
| | | | | | | Core / Adjacent / Stretch / Negative |

## Negative ICP

- **Screen out before buying:**
- **Shows up after:**

## Their words

<!-- Word for word, from gtm/inputs/customer-voice/ only (or market-voice/, tagged proxy). Cited by role, company and file. -->

| Quote | Who | Source |
|---|---|---|
| | | |

## Jobs to be done

<!-- Only when interviews show the jobs in the buyer's words: "When ..., I want to ..., so I can ...", with the quote behind it. Otherwise delete this section. -->

## Data notes

<!-- What was cleaned, the column map, what is missing and what it costs, files not used and why. -->

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
