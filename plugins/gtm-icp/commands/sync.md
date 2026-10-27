---
description: Bring the ICP module's files (icp.md, buying-group.md) and the ICP dossier page back in step after edits made by hand, in VS Code or on the published page.
---

# /gtm-icp:sync

Run the `dossier-sync` skill on `gtm/outputs/icp/`. Use it after edits Claude wasn't told about; edits made through Claude sync on their own.

1. Skip a file still at `status: template`, and say so.
2. Compare each `.md` with the local page and, if this session can reach it, the published page (`published_url` in `icp.md`). List the differences as `file | section | the .md says | the page says`. No differences: say "in sync".
3. The owner picks the winner per line; the `.md` wins when they don't choose. Write the winners to the `.md`, check the changed lines against `gtm/RULES.md`, rebuild the page and republish where you can. A `final` file that changes goes back to `draft` until the owner marks it final again.
4. End with one line: in sync, updated, or needs the owner.
