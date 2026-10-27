# inputs/customer-voice/

What your customers say, in their own words. This is the only place quotes come from.

## What goes here

| Input | Format | What it gives |
|---|---|---|
| Sales or customer call notes and transcripts | Markdown | Why they buy, and what nearly stopped them |
| Interview transcripts, win/loss interviews | Markdown | The decision, told by the buyer |
| Reviews you've collected | Markdown, pasted word for word | How they describe the outcome |
| Support tickets | Markdown, trimmed threads | Pains, in their words |
| Survey answers (open text) | CSV or Markdown | Patterns at volume |

Keep the words exactly as written: grammar, slang, typos. Don't clean them up.

## Start every file with a source block

```
Type: call | interview | review | ticket | survey
Date: 2026-10-14
Origin: Gong recording, Zendesk export, a G2 page...
Speaker role: Finance lead
Company: Aldermere
```

For a CSV, a PDF or any file you can't or don't want to edit, put the same block in a note next to it with the same name plus `.source.md` (for example `nps-comments-2026-09.csv.source.md`).

The module uses it to cite the quote ("Finance lead, Aldermere, call-12.md"). One conversation per file works best, named simply: `call-12.md`, `interview-03.md`.

## Not sure where a file goes?

If someone else has already analysed the words (a research report, a deck, a win/loss summary written by sales), it goes in `reports/`. If a file mixes both, split it, or put it in `reports/`.

Names of people can stay in these files: the module never copies them into an output. This folder stays on your machine and out of git.
