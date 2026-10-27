#!/usr/bin/env python3
"""Read-only helper for the gtm-icp module. Standard library only.

It never writes to the input files. It prints Markdown, so the numbers in the ICP
come from a calculation instead of an estimate.

  inspect  DEALS [--contacts CONTACTS]
      Columns, a suggested column map, row counts, defects, and the values of the
      columns that could define segments.

  segments DEALS --map MAP.json --segments SEGMENTS.json [--contacts CONTACTS] [--core NAME] [--roles ROLES.json]
      Cleans the deals (duplicates, dates, amounts) and prints the scorecard per segment:
      deals, won, win rate, value, loyalty, cycle, cost to serve, revenue share. With
      --contacts, counts the job titles, departments, deal roles and joined stages on the
      won deals of each segment (or of --core only). With --roles, also counts the distinct
      won deals per role, where ROLES.json maps each job title to a role:
      {"CTO": "Technology leader", "VP Finance": "Finance lead", ...}

MAP.json maps the module's field names to your column headers, for example
  {"deal_id": "Record ID", "outcome": "Deal Stage", "amount": "Amount", ...}
SEGMENTS.json lists the segments in order; the first match wins:
  [{"name": "Mid-market SaaS, 3+ countries",
    "all": [{"col": "Company Type", "op": "eq", "value": "B2B SaaS"},
            {"col": "Markets Served", "op": "gte", "value": 3}]}, ...]
Operators: eq, ne, in, not_in, gt, gte, lt, lte, between, contains, empty, not_empty.
"""
import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter, OrderedDict
from datetime import datetime

DEAL_FIELDS = OrderedDict([
    ("deal_id", ["dealid", "recordid", "id", "opportunityid", "dealrecordid"]),
    ("outcome", ["outcome", "dealstage", "stage", "result", "wonlost", "isWon".lower()]),
    ("created_date", ["createddate", "createdate", "created", "opendate", "createdat"]),
    ("closed_date", ["closeddate", "closedate", "closed", "closedat"]),
    ("amount", ["amount", "acv", "annualcontractvalue", "dealvalue", "value", "arr"]),
    ("account_domain", ["accountdomain", "companydomainname", "companydomain", "domain", "website"]),
    ("account_name", ["accountname", "companyname", "company", "account"]),
    ("industry", ["industry"]),
    ("employee_count", ["employeecount", "numberofemployees", "employees", "companysize"]),
    ("country", ["country", "countryregion", "region", "hqcountry"]),
    ("company_type", ["companytype", "businessmodel", "type"]),
    ("lead_source", ["leadsource", "source", "originalsource", "dealsource", "channel"]),
    ("lost_reason", ["lostreason", "closedlostreason", "reasonlost"]),
    ("customer_status", ["customerstatus", "accountstatus", "status"]),
    ("renewal_date", ["renewaldate", "nextrenewaldate"]),
    ("churn_date", ["churndate", "churneddate", "cancellationdate"]),
    ("expansion_amount", ["expansionamount", "expansionrevenue", "expansion", "upsell"]),
    ("support_tickets", ["supporttickets", "supportticketspermonth", "ticketspermonth", "tickets"]),
    ("onboarding_days", ["onboardingdays", "onboardingtime", "daystoonboard"]),
    ("product_or_plan", ["productorplan", "plan", "product"]),
])
CONTACT_FIELDS = OrderedDict([
    ("deal_id", ["dealid", "recordid", "opportunityid", "deal"]),
    ("job_title", ["jobtitle", "title", "role"]),
    ("department", ["department", "function"]),
    ("deal_role", ["dealrole", "contactrole", "buyingrole", "associationlabel"]),
    ("joined_stage", ["joinedstage", "stageadded", "joinedat", "joineddate"]),
    ("person_id", ["personid", "contactid", "id"]),
])
PERSONAL = ["firstname", "lastname", "fullname", "name", "email", "emailaddress", "phone", "phonenumber", "mobile"]
DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d.%m.%Y", "%d-%m-%Y", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]
SMALL = 5  # fewer won customers than this: counts and win rate only; value, loyalty, cycle and cost stay blank


def norm(h):
    return re.sub(r"[^a-z0-9]", "", h.lower())


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.DictReader(f, dialect=dialect))
    return rows, (list(rows[0].keys()) if rows else [])


def suggest_map(headers, fields):
    out, used = {}, set()
    for field, syns in fields.items():
        for h in headers:
            if h not in used and norm(h) in syns:
                out[field] = h
                used.add(h)
                break
    return out


def parse_date(v):
    v = (v or "").strip()
    if not v:
        return None, "empty"
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(v, fmt).date(), fmt
        except ValueError:
            continue
    return None, "unreadable"


def parse_num(v):
    v = (v or "").strip()
    if not v:
        return None
    v = re.sub(r"[^0-9,.\-]", "", v)
    if "," in v and "." in v:
        v = v.replace(",", "") if v.rfind(".") > v.rfind(",") else v.replace(".", "").replace(",", ".")
    elif "," in v:
        v = v.replace(",", "") if re.search(r",\d{3}$", v) else v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None


def parse_outcome(v):
    t = (v or "").strip().lower()
    if not t:
        return None
    if "won" in t or t in ("win", "yes", "true", "1", "closedwon"):
        return "won"
    if "lost" in t or t in ("loss", "no", "false", "0", "closedlost"):
        return "lost"
    return None


def fmt_pct(x):
    return "" if x is None else f"{x:.0f}%"


def fmt_money(x):
    return "" if x is None else f"{x:,.0f}"


def mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def median(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None


# ---------------------------------------------------------------- inspect
def cmd_inspect(a):
    rows, headers = read_csv(a.deals)
    m = suggest_map(headers, DEAL_FIELDS)
    print(f"# Inspect: {a.deals}\n")
    print(f"Rows: {len(rows)}. Columns: {len(headers)}.\n")
    print("## Suggested column map (confirm with the owner)\n")
    print("```json\n" + json.dumps(m, indent=2) + "\n```\n")
    missing = [f for f in DEAL_FIELDS if f not in m]
    print("Not found: " + (", ".join(missing) if missing else "none") + "\n")
    extra = [h for h in headers if h not in m.values()]
    print("Columns not mapped (may still define segments): " + (", ".join(extra) if extra else "none") + "\n")

    print("## Defects\n")
    idcol = m.get("deal_id")
    if idcol:
        ids = Counter(r[idcol] for r in rows)
        dup = {k: v for k, v in ids.items() if v > 1}
        same = sum(1 for k in dup if len({json.dumps(r, sort_keys=True) for r in rows if r[idcol] == k}) == 1)
        print(f"- Repeated deal IDs: {len(dup)} ({same} exact duplicate rows, {len(dup) - same} with different values)")
    for f in ("created_date", "closed_date"):
        if f in m:
            kinds = Counter(parse_date(r[m[f]])[1] for r in rows)
            print(f"- {f} ({m[f]}): " + ", ".join(f"{k} {v}" for k, v in kinds.most_common()))
    if "amount" in m:
        bad = sum(1 for r in rows if parse_num(r[m["amount"]]) is None)
        print(f"- amount ({m['amount']}): {bad} empty or unreadable")
    if "outcome" in m:
        oc = Counter(parse_outcome(r[m["outcome"]]) or f"other: {r[m['outcome']]}" for r in rows)
        print(f"- outcome ({m['outcome']}): " + ", ".join(f"{k} {v}" for k, v in oc.most_common()))
    print()

    print("## Values of possible segment columns\n")
    for h in headers:
        if h in (m.get("deal_id"), m.get("account_name"), m.get("account_domain"), m.get("created_date"),
                 m.get("closed_date"), m.get("churn_date"), m.get("renewal_date")):
            continue
        vals = [r[h] for r in rows if (r[h] or "").strip()]
        nums = [parse_num(v) for v in vals]
        if vals and all(n is not None for n in nums) and len(set(vals)) > 12:
            print(f"- **{h}** (numeric, {len(vals)} filled): min {min(nums):g}, median {statistics.median(nums):g}, max {max(nums):g}")
        else:
            top = Counter(vals).most_common(12)
            print(f"- **{h}** ({len(vals)} filled, {len(set(vals))} values): " + ", ".join(f"{k} ({v})" for k, v in top))
    print()

    if a.contacts:
        crows, cheaders = read_csv(a.contacts)
        cm = suggest_map(cheaders, CONTACT_FIELDS)
        print(f"## Contacts: {a.contacts}\n\nRows: {len(crows)}.\n")
        print("```json\n" + json.dumps(cm, indent=2) + "\n```\n")
        personal = [h for h in cheaders if norm(h) in PERSONAL]
        if personal:
            print(f"**Personal data found:** {', '.join(personal)}. These columns are never copied into an output. "
                  "Suggest the owner removes them from the file.\n")
        for f in ("deal_role", "joined_stage", "department"):
            if f in cm:
                filled = sum(1 for r in crows if (r[cm[f]] or "").strip())
                print(f"- {f} ({cm[f]}): filled on {filled} of {len(crows)}")


# ---------------------------------------------------------------- segments
def match(row, rule):
    v = (row.get(rule["col"]) or "").strip()
    op, target = rule["op"], rule.get("value")
    if op == "empty":
        return not v
    if op == "not_empty":
        return bool(v)
    if op in ("eq", "ne", "in", "not_in", "contains"):
        lv = v.lower()
        if op == "eq":
            return lv == str(target).lower()
        if op == "ne":
            return lv != str(target).lower()
        if op == "in":
            return lv in [str(t).lower() for t in target]
        if op == "not_in":
            return lv not in [str(t).lower() for t in target]
        return str(target).lower() in lv
    n = parse_num(v)
    if n is None:
        return False
    if op == "gt":
        return n > float(target)
    if op == "gte":
        return n >= float(target)
    if op == "lt":
        return n < float(target)
    if op == "lte":
        return n <= float(target)
    if op == "between":
        return float(target[0]) <= n <= float(target[1])
    raise SystemExit(f"Unknown operator: {op}")


def clean_deals(rows, m):
    notes = []
    idcol = m.get("deal_id")
    seen, out, dups, conflicts = {}, [], 0, 0
    for r in rows:
        key = r[idcol] if idcol else None
        if key and key in seen:
            if json.dumps(seen[key], sort_keys=True) == json.dumps(r, sort_keys=True):
                dups += 1
            else:
                conflicts += 1
            continue
        if key:
            seen[key] = r
        out.append(r)
    if dups:
        notes.append(f"{dups} exact duplicate rows removed")
    if conflicts:
        notes.append(f"{conflicts} rows with a repeated deal ID but different values: first row kept")
    formats = Counter()
    deals = []
    for r in out:
        d = dict(raw=r)
        d["outcome"] = parse_outcome(r.get(m.get("outcome", ""), "")) if "outcome" in m else None
        d["created"], f1 = parse_date(r.get(m["created_date"])) if "created_date" in m else (None, "none")
        d["closed"], f2 = parse_date(r.get(m["closed_date"])) if "closed_date" in m else (None, "none")
        formats.update([f1, f2])
        d["amount"] = parse_num(r.get(m["amount"])) if "amount" in m else None
        for f in ("expansion_amount", "support_tickets", "onboarding_days"):
            d[f] = parse_num(r.get(m[f])) if f in m else None
        status = (r.get(m["customer_status"]) or "").strip().lower() if "customer_status" in m else ""
        churn = (r.get(m["churn_date"]) or "").strip() if "churn_date" in m else ""
        d["churned"] = True if ("churn" in status or "cancel" in status or "lost" in status or churn) else \
            (False if status else None)
        deals.append(d)
    odd = {k: v for k, v in formats.items() if k not in ("%Y-%m-%d", "empty", "none")}
    if odd:
        notes.append("date values in other formats, read as: " + ", ".join(f"{k} ({v})" for k, v in odd.items()))
    undecided = sum(1 for d in deals if d["outcome"] is None)
    if undecided:
        notes.append(f"{undecided} deals neither won nor lost: left out")
    no_amount = sum(1 for d in deals if d["amount"] is None)
    if no_amount:
        notes.append(f"{no_amount} deals with no readable amount: left out of value figures only")
    return [d for d in deals if d["outcome"]], notes


def cmd_segments(a):
    rows, _ = read_csv(a.deals)
    m = json.load(open(a.map))
    segs = json.load(open(a.segments))
    deals, notes = clean_deals(rows, m)
    for d in deals:
        d["segment"] = next((s["name"] for s in segs if all(match(d["raw"], r) for r in s["all"])), "Unassigned")
    total_won_amount = sum(d["amount"] or 0 for d in deals if d["outcome"] == "won")

    print("# Segment scorecard\n")
    print(f"Source: {a.deals}. Deals used: {len(deals)} "
          f"({sum(d['outcome'] == 'won' for d in deals)} won, {sum(d['outcome'] == 'lost' for d in deals)} lost).")
    dates = [d["closed"] for d in deals if d["closed"]]
    if dates:
        print(f"Close dates from {min(dates)} to {max(dates)}.")
    print("\nCleaning: " + ("; ".join(notes) if notes else "nothing to clean") + ".\n")

    print("| Segment | Deals | Won | Win rate | Revenue share (won) | Mean value (won) | Median value (won) | "
          "Loyalty (not churned, of won) | Mean cycle, days (won) | Expanded | Tickets a month | Onboarding days | Note |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    names = [s["name"] for s in segs] + (["Unassigned"] if any(d["segment"] == "Unassigned" for d in deals) else [])
    for name in names:
        ds = [d for d in deals if d["segment"] == name]
        won = [d for d in ds if d["outcome"] == "won"]
        if not ds:
            print(f"| {name} | 0 | | | | | | | | | | | no deals |")
            continue
        winrate = 100.0 * len(won) / len(ds)
        share = 100.0 * sum(d["amount"] or 0 for d in won) / total_won_amount if total_won_amount else None
        if len(won) < SMALL:
            # Too few won customers: counts and win rate only. Everything that is an average of won deals stays blank.
            note = f"{len(won)} won: too few to rank" if won else "no won deals"
            print(f"| {name} | {len(ds)} | {len(won)} | {winrate:.0f}% | {fmt_pct(share)} | | | | | | | | {note} |")
            continue
        known = [d for d in won if d["churned"] is not None]
        loyalty = f"{100.0 * sum(not d['churned'] for d in known) / len(known):.0f}% ({sum(not d['churned'] for d in known)} of {len(known)})" if known else ""
        cycles = [(d["closed"] - d["created"]).days for d in won if d["closed"] and d["created"]]
        expanded = sum(1 for d in won if (d["expansion_amount"] or 0) > 0) if "expansion_amount" in m else None
        tix, onb = mean(d["support_tickets"] for d in won), mean(d["onboarding_days"] for d in won)
        print(f"| {name} | {len(ds)} | {len(won)} | {winrate:.0f}% | {fmt_pct(share)} | {fmt_money(mean(d['amount'] for d in won))} | "
              f"{fmt_money(median(d['amount'] for d in won))} | {loyalty} | {'' if not cycles else f'{statistics.mean(cycles):.0f}'} | "
              f"{'' if expanded is None else f'{expanded} of {len(won)}'} | {'' if tix is None else f'{tix:.1f}'} | "
              f"{'' if onb is None else f'{onb:.0f}'} | |")
    print()

    if "lost_reason" in m:
        print("## Lost reasons, per segment\n")
        for name in names:
            lost = [d for d in deals if d["segment"] == name and d["outcome"] == "lost"]
            if lost:
                c = Counter((d["raw"].get(m["lost_reason"]) or "").strip() or "(blank)" for d in lost)
                print(f"- **{name}** ({len(lost)} lost): " + ", ".join(f"{k} {v}" for k, v in c.most_common()))
        print()
    print("## Lead source\n")
    if "lead_source" in m:
        for name in names:
            won = [d for d in deals if d["segment"] == name and d["outcome"] == "won"]
            c = Counter((d["raw"].get(m["lead_source"]) or "").strip() or "(blank)" for d in won)
            print(f"- **{name}**: " + ", ".join(f"{k} {v}" for k, v in c.most_common()))
    else:
        print("Not in the file: \"where they find you\" stays blank.")
    print()

    if a.contacts:
        crows, cheaders = read_csv(a.contacts)
        cm = json.load(open(a.contact_map)) if a.contact_map else suggest_map(cheaders, CONTACT_FIELDS)
        personal = [h for h in cheaders if norm(h) in PERSONAL]
        idcol = m.get("deal_id")
        print("# Contacts on won deals\n")
        if personal:
            print(f"Personal data columns ignored: {', '.join(personal)}.\n")
        targets = [a.core] if a.core else [s["name"] for s in segs]
        for name in targets:
            won_ids = {d["raw"][idcol] for d in deals if d["segment"] == name and d["outcome"] == "won"}
            cs = [r for r in crows if r.get(cm["deal_id"]) in won_ids]
            print(f"## {name}: {len(won_ids)} won deals, {len(cs)} contacts\n")
            for f in ("job_title", "department", "deal_role", "joined_stage"):
                if f not in cm:
                    continue
                per = {}
                for r in cs:
                    v = (r.get(cm[f]) or "").strip() or "(blank)"
                    per.setdefault(v, set()).add(r[cm["deal_id"]])
                items = sorted(per.items(), key=lambda kv: -len(kv[1]))
                print(f"- **{f}** (won deals with it): " + ", ".join(f"{k} {len(v)}" for k, v in items))
            if a.roles:
                roles = json.load(open(a.roles))
                per, unmapped = {}, Counter()
                for r in cs:
                    t = (r.get(cm["job_title"]) or "").strip()
                    if t in roles:
                        per.setdefault(roles[t], set()).add(r[cm["deal_id"]])
                    elif t:
                        unmapped[t] += 1
                print(f"\n| Role | Won deals with this role (of {len(won_ids)}) | Share |\n|---|---|---|")
                for role, ids in sorted(per.items(), key=lambda kv: -len(kv[1])):
                    print(f"| {role} | {len(ids)} | {100.0 * len(ids) / len(won_ids):.0f}% |")
                if unmapped:
                    print("\nTitles not in ROLES.json: " + ", ".join(f"{k} ({v})" for k, v in unmapped.most_common()))
            print()


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("inspect")
    i.add_argument("deals")
    i.add_argument("--contacts")
    s = sub.add_parser("segments")
    s.add_argument("deals")
    s.add_argument("--map", required=True)
    s.add_argument("--segments", required=True)
    s.add_argument("--contacts")
    s.add_argument("--contact-map")
    s.add_argument("--core")
    s.add_argument("--roles")
    a = p.parse_args()
    {"inspect": cmd_inspect, "segments": cmd_segments}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
