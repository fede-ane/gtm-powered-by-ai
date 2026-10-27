# inputs/market-voice/

What people in your market say in public: about the problem, the category and your competitors. Use it when you have little data of your own. It shows what the market says, not what your customers say, so every line built from it is tagged **proxy**.

## Where to look

- **Review sites:** G2, Capterra, TrustRadius, Trustpilot, app stores.
- **One community:** LinkedIn posts and comments, a niche forum, Reddit threads (found through web search, or copied by hand).
- **Your own website:** what you say about yourself. It shows what you claim, not who buys.

List the pages in `sources.md`, one per line. The module fetches what it can. If a page blocks it, it tells you and moves on; you can copy the text by hand instead.

## Start every file with a source block

```
Type: review | post | comment | own site
URL: https://...
Date: 2026-10-14
Role: Head of Finance (if shown)
Tag: proxy
```

For a CSV, a PDF or any file you can't or don't want to edit, put the same block in a note next to it with the same name plus `.source.md` (for example `nps-comments-2026-09.csv.source.md`).

## Two cautions

- **Terms of service.** Many sites don't allow automated collection, LinkedIn in particular. Check before collecting at scale; otherwise copy by hand.
- **Closed groups.** Before pasting posts from a Slack group or a private community, check that its rules allow it. Posts are cited by date and role, never by name.
