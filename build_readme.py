#!/usr/bin/env python3
"""
Self-contained README builder for a single job-list repo.

Each job-list repo ships a copy of THIS file plus:
  - meta.json   {"role": "...", "title": "..."}
  - jobs.json   [ {company, role, location, type, posted, url, ...}, ... ]

Run inside the repo (this is what the GitHub Action calls):
    python3 build_readme.py

Wire `fetch_jobs()` to your real data source to make the repo auto-update.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent

SITE = "https://landed.jobs"
GH_ORG = "https://github.com/landedjobs"
BRAND = "Landed"

BLURBS = {
    "AI Engineer": "An **AI Engineer** builds products on top of LLMs — RAG, agents, evals, inference. Most roles want shipping ability (Python, LangChain/LlamaIndex, vector DBs, APIs), **not** an ML PhD. US AI Engineer postings rose ~143% YoY.",
    "GTM Engineer": "A **GTM Engineer** automates go-to-market with code + AI — outbound, enrichment, revenue workflows. The technical evolution of the marketer/SDR; high demand, few qualified people.",
    "AI Product Engineer": "An **AI Product Engineer** is the new 'PM who ships' — owning product *and* building AI features. Prompts, evals, and rapid prototyping matter as much as roadmaps.",
    "Forward-Deployed Engineer": "A **Forward-Deployed Engineer (FDE)** embeds with customers to build and ship custom solutions. Part engineer, part consultant — one of the hottest, best-paid AI-native roles.",
}


def fetch_jobs():
    """>>> INTEGRATION POINT <<< — replace with your scrape/DB/ATS API call.
    Default: read the local jobs.json."""
    p = HERE / "jobs.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def main():
    meta = json.loads((HERE / "meta.json").read_text(encoding="utf-8"))
    role, title = meta["role"], meta["title"]
    jobs = fetch_jobs()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    rows = "\n".join(
        f"| **{j.get('company','—')}** | [{j.get('role',role)}]({j.get('url','#')}) "
        f"| {j.get('location','—')} | {j.get('type','Full-time')} | {j.get('posted','—')} |"
        for j in jobs
    ) or "| _List updating — check back soon_ |  |  |  |  |"

    blurb = BLURBS.get(role, f"A **{role}** is an emerging, in-demand AI-native role.")

    readme = f"""# {title} 🚀

> An open, **auto-updated** list of {role} roles. Updated {today} · **{len(jobs)} live roles**.
> Curated by [{BRAND}]({SITE}) — scout, get **referred**, prep, and land AI-native jobs.

⭐ **Star this repo** to track new {role} roles — it refreshes regularly.

---

## What is a {role}? (60-second version)

{blurb}

---

## Live {role} roles

| Company | Role | Location | Type | Posted |
|---|---|---|---|---|
{rows}

> A sample of what's live. **[See every {role} role + 1-click tracking on {BRAND} →]({SITE})**

---

## How to actually land one

Applying cold is the slow path — these roles usually go to people who get **referred**. With {BRAND} you can scout every opening, find a connection at the company and auto-draft a referral message, prep with company-specific mock interviews, and track every application.

**[Get started free → {SITE}]({SITE})**

---

## Related

- 🧭 [awesome-ai-native-jobs]({GH_ORG}/awesome-ai-native-jobs)
- 🧪 [projects-to-land-an-ai-job]({GH_ORG}/projects-to-land-an-ai-job)
- 🗺️ Roadmaps & interview prep — see the [{BRAND} org]({GH_ORG})

## Contributing

Spotted a role we missed? Open a PR or issue.

---

<sub>Maintained by [{BRAND}]({SITE}). Data refreshed automatically. Not affiliated with the listed companies.</sub>
"""
    (HERE / "README.md").write_text(readme, encoding="utf-8")
    print(f"✓ wrote README.md ({len(jobs)} roles)")


if __name__ == "__main__":
    main()
