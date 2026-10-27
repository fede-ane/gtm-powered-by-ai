# gtm/

The shared workspace for the GTM powered by AI modules. Each module adds only the folders it needs. The ICP module (ICP, buying group and personas) creates the ones below.

```
gtm/
├── README.md            this file
├── RULES.md             the rules every module follows
├── inputs/              what you know: data and documents, shared by all modules
│   ├── crm/
│   ├── customer-voice/
│   │   └── reports/
│   ├── market-voice/
│   └── strategy/
└── outputs/
    └── icp/             what the ICP module writes
```

## Fill it in this order

1. **`inputs/crm/`**: your deals, won and lost, and the contacts on those deals. This is what turns guesses into findings.
2. **`inputs/customer-voice/`**: what customers say in their own words: call notes, interviews, reviews, tickets, survey answers.
3. **`inputs/strategy/`**: where the business is going. The module asks you a few questions and saves your answers here.
4. **`inputs/market-voice/`**: only if you have little data of your own. Public reviews and posts about your market.

**Not sure where a file goes?** Drop it in `inputs/` as it is: a PDF, a deck, an email, loose notes, a screenshot. The module proposes where it belongs and moves it only after you confirm. Audio and video need a transcript first.

You can start with nothing. The module then builds a hypothesis and tags every line as one. Each folder's README says what is essential, what helps and what is optional.

## What stays on your machine

Everything in `inputs/` and `outputs/` is kept out of git, apart from the README files. Outputs hold company names and customer quotes, so treat them like your inputs.

## How the modules work together

Inputs are shared: you add your deals export once, and every module reads it. Each module writes to its own folder in `outputs/`. A module works on its own. If it needs another module's output and can't find it, it asks you instead.

## Rules

Every module reads `RULES.md` before it starts. If two modules carry different versions, the newer one wins, and you're asked before your copy is replaced.
