# GTM powered by AI: plugins for Claude

Modules for AI-native B2B demand generation, built for [federicoanedda.com](https://federicoanedda.com). The repository is a plugin marketplace: each module is its own plugin, works on its own, and adds only its folders to a shared `gtm/` workspace in your project.

## Modules

| Module | What it does | Version |
|---|---|---|
| **gtm-icp** | Builds your ICP, your buying group and one persona per main role from your own CRM deals and customer words, into Markdown files and a one-page dossier. Every number is calculated, every quote is word for word, and what isn't proven is tagged. | 0.1.2 |

## Install

In Claude Code:

```
/plugin marketplace add federicoanedda/gtm-powered-by-ai
/plugin install gtm-icp@gtm-powered-by-ai
```

Then, in a project folder:

1. `/gtm-icp:setup` creates the `gtm/` workspace. It never overwrites a file.
2. Put your deals export and the contacts on those deals in `gtm/inputs/crm/`, and your customer words (calls, interviews, survey answers) in `gtm/inputs/customer-voice/`. The README in each folder lists what it needs.
3. `/gtm-icp:dossier` asks a few questions, then writes `gtm/outputs/icp/icp.md`, `buying-group.md` and the dossier page.
4. After you edit the Markdown files by hand, `/gtm-icp:sync` brings the page back in step.

Your data stays on your machine: the setup adds a block to your `.gitignore` that keeps `gtm/inputs/` and `gtm/outputs/` out of git.

To try it without your own data, use the invented company in [`examples/aldermere/`](examples/aldermere/).

## What is in the repository

```
gtm-powered-by-ai/
├── .claude-plugin/marketplace.json     lists the modules
├── plugins/
│   └── gtm-icp/
│       ├── .claude-plugin/plugin.json
│       ├── commands/                   /gtm-icp:setup, /gtm-icp:dossier, /gtm-icp:sync
│       ├── skills/
│       │   ├── icp-buying-group/       the method
│       │   └── dossier-sync/           keeps the .md files and the page in step
│       ├── scripts/
│       │   ├── setup.sh                creates gtm/ and the .gitignore block
│       │   └── crm_profile.py          read-only: cleans the CRM export and computes the scorecard
│       └── templates/                  workspace files, output templates, the page template
└── examples/aldermere/                 invented data to try the plugin
```

The segment scorecard is computed by `crm_profile.py` (Python 3, standard library only), not estimated by the model.

## Credits

The ICP method is adapted from [`icp-synthesis`](https://github.com/nickyc1/ship-icp-ads-automate-monitoring) by Nick Christensen (MIT; see `NOTICE`). The buying group and personas are this module's own addition.

## Licence

MIT. See `LICENSE`. The example data in `examples/` is invented.
