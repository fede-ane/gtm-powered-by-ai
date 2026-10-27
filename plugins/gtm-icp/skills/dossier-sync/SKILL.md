---
name: dossier-sync
description: Keep the ICP module's files and their page in step. Use whenever gtm/outputs/icp/icp.md or buying-group.md is edited (in chat, by hand, or in VS Code), when the owner says they changed the published ICP dossier page, and when /gtm-icp:sync runs.
---

# Dossier sync

`gtm/outputs/icp/icp.md` and `gtm/outputs/icp/buying-group.md` are the source. `gtm/outputs/icp/icp-dossier.html` is a view of both: it never holds a line the `.md` files don't.

## An edit to a file

1. **Write the `.md` first.** Never change only the page. If the file was `final`, set it back to `draft`, clear `approved_by` and `approved_on`, and say so. Once the edit is done, ask whether to mark it final again; on a yes, follow step 9 of `/gtm-icp:dossier`.
2. **Check the edited lines** against `gtm/RULES.md`: sources, tags, quotes, personal data, and the four checks (rule 13) on the lines that changed. Update the file's Open tags and Checks tables.
3. **Look across the two files** for a line the edit now contradicts (a persona objection that no longer matches the ICP, a role count that changed). List each as `file | line | conflict | proposed fix` and apply only what the owner approves.
4. **Rebuild the page** following "Build the page" below.
5. **Republish** if the page was published (`published_url` in `icp.md`) and this session can publish artifacts. Otherwise say the local page is updated and the published one is not.

## Edits made on the page

1. Read the page: the published artifact if this session can, otherwise the local file.
2. Compare it with the `.md` files, line by line. List every difference as `file | section | the .md says | the page says`.
3. The owner picks the winner for each line; when they don't choose, the `.md` wins. Never copy a page edit into the `.md` without a yes: a page can hold an old version.
4. Write the winners to the `.md`, then follow "An edit to a file" from step 2.

## Build the page

1. Start from `${CLAUDE_PLUGIN_ROOT}/templates/icp-dossier.html`. Keep its `<style>` block, its sections and their order. Replace every piece of content with the content of the two files, and remove the template banner.
2. Sections, top to bottom: header (label, company, stage, business type, status, date, open tags, checks; the status reads "Draft", or "Final · approved by [role] on [date]"), Who buys now, Who you want next (only when `icp.md` has it), Segments, Negative ICP, Their words, Jobs to be done (only when `icp.md` has it), Buying group, Personas, Supporting roles, Checks, and the footer with sources and blanks. Each role card in the buying group carries a source line: the deal-role counts from `buying-group.md` and the quote that shows the role in the decision.
3. Every tag in the files shows as a tag on the page; every blank shows as a blank with its reason. Every quote on the page, in any section (role cards, personas, Their words, Negative ICP), is cited by role, company and file: "Head of Engineering, Kestrel Freight, call-04.md". Never the file alone, never the company alone. An NPS or survey answer with no company is cited by role, file and date.
4. **Count check:** the number of tags and blanks on the page equals the number in the files, and every customer quote in the files is on the page (role cards and supporting roles included). **Citation check:** every quote on the page has a role, a company (or a date, for survey answers) and a file. If either check fails, fix the `.md` first, then rebuild from the files.
5. Save it as `gtm/outputs/icp/icp-dossier.html`, a complete HTML document that opens in a browser.

## Publish the page

Follow `gtm/RULES.md` rules 14 and 15:
1. **Private by default.** Before publishing, list what is on the page: company names, quotes, figures. Ask for a yes.
2. Publish a copy without the `<!doctype>`, `<html>`, `<head>` and `<body>` wrapper (keep the `<title>`, the `<link>` to the fonts and the `<style>` block at the top), titled "[Company] ICP Dossier". Record the link in `published_url`.
3. **Sharing outside the company:** offer a redacted copy: customer company names replaced by company type, figures the owner marks confidential removed, the Checks section and Open tags left out. Publish it as its own page, "[Company] ICP Dossier (redacted)". Never redact the original.
4. If this session can't publish, give the file path and say to open it in a browser.
5. Say in one line what was shared: which page, private or shared, redacted or not.
