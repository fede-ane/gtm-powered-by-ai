# Example data: Aldermere Payments

**Everything here is invented.** Aldermere Payments does not exist. The companies, people, deals, quotes and figures are made up, and the email addresses use the reserved `.example` domain.

It is there so you can try `gtm-icp` end to end without using your own customer data.

## What is in it

| Folder or file | What it is |
|---|---|
| `data/crm/` | A deals export (133 rows) and the contacts on those deals |
| `data/customer-voice/` | 12 call notes and 3 interviews, plus a survey summary in `reports/` |
| `data/loose/` | Files that are not yet filed: NPS comments, board notes, a press release. They test the plugin's sorting step |
| `intake-replies.md` | Answers to the plugin's questions, from the point of view of the made-up company |

The data is deliberately imperfect, the way real exports are: duplicate rows, mixed date formats, a missing column, a document that does not describe the buyer. The plugin should cope with each and say what it did.

## How to use it

1. In an empty folder, run `/gtm-icp:setup`.
2. Copy `data/crm/`, `data/customer-voice/` and `data/market-voice/` into the matching folders in `gtm/inputs/`, and the files in `data/loose/` into `gtm/inputs/` itself.
3. Run `/gtm-icp:dossier` and answer with `intake-replies.md`.
