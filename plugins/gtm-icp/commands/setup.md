---
description: Set up the GTM workspace (gtm/) and the ICP module's folders in this folder, with a README in each and the .gitignore block that keeps your data local. Never overwrites a file.
---

# /gtm-icp:setup

1. **Check the folder.** Any project folder works. If `gtm/` already exists and holds `gtm/RULES.md`, the workspace is there: say that existing files are kept and continue.
2. **Run the setup script** with the shell and show its output:
   `bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup.sh" "<this folder's absolute path>"`
   It adds the `.gitignore` block first, then copies the workspace files without overwriting, and reports the `RULES.md` version and whether `python3` is available.
   - **Exit code 3** means a `gtm/` folder exists that this plugin didn't make. Stop, say so, and ask the owner to rename or move it.
   - **No bash** (Windows without Git Bash): point to `winget install Git.Git` and stop.
   - **Rules version**: if the script says the plugin has a newer `RULES.md`, show what changed and replace the owner's copy only on a yes.
3. **Next step, in three lines:** drop your deals export and the contacts on those deals into `gtm/inputs/crm/` (the README there lists the columns); add customer words to `gtm/inputs/customer-voice/`; then run `/gtm-icp:dossier`. Files you're not sure about can go loose into `gtm/inputs/`.
4. If the folder is a git repo, show `git status --short` and ask whether to commit ("Add the GTM workspace"). Commit only on a yes.
