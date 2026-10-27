# inputs/crm/

Your deals and the people on them, exported from your CRM. This is the data that shows which customers are worth the most, which stay and which are easy to win.

Two files. Column names don't have to match exactly: the module maps your columns to these and asks you when it isn't sure.

## deals.csv

One row per deal, won and lost, from the last 12 to 24 months.

| Column | What it's for | Level |
|---|---|---|
| `deal_id` | Links contacts to the deal | Essential |
| `outcome` | Won or lost. Without lost deals there is no win rate | Essential |
| `created_date`, `closed_date` | Length of the sales cycle | Essential |
| `amount` | Annual contract value, with the currency | Essential |
| `account_domain` | The company's web domain, so deals from the same customer join up | Essential |
| At least two of `industry`, `employee_count`, `country`, `company_type` | What the module groups customers by | Essential |
| `lead_source` | Where they find you | Helps a lot |
| `lost_reason` | Objections, and why deals are lost | Helps a lot |
| `customer_status`, plus `renewal_date` or `churn_date` | Who stays | Helps a lot |
| `expansion_amount` | Revenue after the first deal | Helps |
| `support_tickets`, `onboarding_days` | What a customer costs to serve | Optional |
| `product_or_plan`, `account_name` | Finer segments, easier reading | Optional |

## deal-contacts.csv

One row per contact on each deal. No names, no email addresses.

| Column | What it's for | Level |
|---|---|---|
| `deal_id` | Links the contact to the deal | Essential |
| `job_title` | Finds the roles in the buying group | Essential |
| `department` | Groups the roles | Helps |
| `deal_role` | Champion, budget owner, technical evaluator, user, blocker. Use it if your CRM records contact roles | Helps a lot |
| `joined_stage` or `joined_date` | Who joins late (often the one who can block) | Optional |
| `person_id` | An anonymous code, to count different people | Optional |

## If something is missing

Nothing here is strictly required: the module still runs and tells you what is missing and what it costs. With won deals only and one segment column, the result is a hint and is labelled as one. Without `deal-contacts.csv`, the buying group comes from calls and interviews in `customer-voice/`, or is built as a hypothesis.

## Live data

If your CRM is connected, the module can pull these for you, read only. Each pull is saved here as a dated file (for example `hubspot-deals-2026-10-26.csv`) before it is used.

This folder stays on your machine and out of git.
