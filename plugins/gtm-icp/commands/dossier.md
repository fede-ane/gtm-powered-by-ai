---
description: Build your ICP, buying group and personas from the files in gtm/inputs/, into gtm/outputs/icp/ (icp.md, buying-group.md) and a one-page ICP dossier you can publish.
---

# /gtm-icp:dossier

Read the `icp-buying-group` skill in full first and follow its method. Read `gtm/RULES.md` too: every output follows it. This command says what happens in which order, and when to stop for the owner.

Ask one question at a time and wait for the answer. Save every answer to `gtm/inputs/strategy/intake-answers.md`, with the date, so the next run doesn't ask again (show the saved answers and ask only whether anything changed).

## 0. Set up

If `gtm/` or `gtm/RULES.md` is missing, show the folders that `/gtm-icp:setup` creates and ask: "I'll create these folders, with a README in each. Nothing you already have is changed. OK?" On a yes, run `bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh" "$PWD"` and show its output.

**Sort loose files.** If files sit at the top level of `gtm/inputs/` (anything but `README.md` and the folders), show a table `file | folder | why` and move them only after the owner confirms, without changing their content. Add the source block to each moved file (type, date, origin, speaker role, company), asking the owner for what the file doesn't say. For a CSV or any file that shouldn't be edited, write the block in a note next to it named `<file>.source.md`. A file that doesn't describe the buyer (a press release, a brochure, a generic market report) is listed with the reason it won't be used, and stays where it is.

## 1. Business type

> "Do you sell to businesses, to consumers, or are you a service business (an agency, a consultancy)?"

B2C: build the ICP only, and say the buying group part is built for B2B and services.

## 2. Strategy

Ask, one at a time:
> "Who do you think your best customer is today, and why?"
> "Is anything changing? A new market, segment, product or price, moving up or down market?"

If yes, ask for the document or a short description and save it to `gtm/inputs/strategy/`.
> "Who owns the ICP? If it isn't you, whose sign-off does this need?"
> "Is there a segment you want to grow, or to stop serving, whatever the data says?"

## 3. What you already have

Show the folders and what goes in each, in one table. Then list what is in `gtm/inputs/`: files, row counts, and which essentials from `gtm/inputs/crm/README.md` are missing. Say which customer tools this session can reach; if a CRM is connected, offer a read-only pull, saved as a dated file in `gtm/inputs/crm/` before it is used.

## 4. Other sources

> "Besides review sites like G2 and Capterra, where do your buyers talk about this problem? A forum, a community, a newsletter, a Slack group? Name any, or skip."
> "Do you have customer words that aren't in the CRM? Call recordings, an NPS export, a sales Slack channel, emails? Name any, or skip."
> "Is there any source I should skip?"

Public sources go into `gtm/inputs/market-voice/sources.md`; internal ones into `gtm/inputs/customer-voice/`. For each, say how it can be collected: fetched, blocked, or copied by hand. Fetch the pages in `sources.md` with the web tools this session has, save each with its URL and date, and tag them proxy. If a page blocks the fetch, say which and move on; never guess its content.

## 5. Stage, then go or wait

Say the stage and why in one line (skill section 1). Sum up in one line each: business type, stage, strategy, CRM data, customer words, market words. Then:
> "Start now, or add more first?"

## 6. Data

Follow skill section 2. Show the column map and the defects, and wait for the owner to confirm the map before running `segments`. Personal data in the contacts file: say it is ignored, and suggest removing those columns from the file.

## 7. Synthesise and write

Follow skill sections 3 to 9. Before writing the personas, show the buying group (roles, part in the decision, counts, weight) and the title-to-role map, and wait for the owner's ok: a person decides who is in the room. Then write both files (skill section 11).

If the data and the strategy point at different customers, show both profiles side by side and ask which one copy should speak to today. Record the answer in `icp.md`.

## 8. Checks, then the owner's review

Run the four checks (skill section 10) and print their table. Then go through Open tags line by line: cut, correct or keep. Apply the answers to the `.md` files. Never remove a tag without an answer.

## 9. Draft or final

The files are written as `draft`. Only the owner's yes makes them `final`.

1. Sum up in chat, in about ten lines: who buys now (label and tier table in one line each), who you want next and the decision on it, the buying group (roles and counts), the personas, and the tags still open.
2. If a tag has no decision yet, say the files stay `draft` until it has one, and go to step 4.
3. Ask:
   > "Mark the ICP and the buying group as final? Final means [the ICP owner from the intake] has reviewed them and copy can be written from them. Or keep them as draft."

   On a yes, set in both files `status: final`, `approved_by` (the role who approved, never a personal name), `approved_on` (today, `date +%F`) and `last_updated`. On a no, leave `draft` and say what would need to change.
4. Say the status in one line.

## 10. The page

Build `gtm/outputs/icp/icp-dossier.html` following the `dossier-sync` skill ("Build the page"). Then offer to publish it, following "Publish the page" in the same skill: list what is on it, private by default, and the redacted copy for sharing outside the company.

## 11. Close

- The status: draft, or final with who approved it and when.
- Where the files are: `gtm/outputs/icp/icp.md` and `buying-group.md` (the source) and the page. To change anything, edit the `.md` files or say what to change in chat; after hand edits run `/gtm-icp:sync`.
- The stage, the number of open tags, and the one input that would move the ICP up a stage or close the most tags.
