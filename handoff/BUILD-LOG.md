# Build Log
*Owned by Architect. Updated by Builder after each step.*

---

## Current Status

**Active step:** none
**Last cleared:** proposal Ch.6 rewrite — 2026-08-14
**Pending deploy:** NO

---

## Step History

### Step — Rewrite proposal Chapter 6 to 2 pages + flowchart — COMPLETE
*Date: 2026-08-14*

Files changed:
- `docs/draft/Proposal draft 11.docx` — replaced Ch.6 body; one flowchart (รูปที่ 6.1)
- `docs/draft/figures/fig_ch6_research_flowchart.png` — new procedure flowchart
- `docs/draft/figures/_gen_ch6_schematics.py` — generator for the new figure

Decisions made:
- Keep analysis windows and GC-ppm target from the previous Ch.6 draft.
- Drop the second figure and GPIO pin table to fit 2 pages.

Reviewer findings: not sent to Richard (document rewrite, not a code step)
Deploy: not applicable (local draft only)

---

## Known Gaps
*Logged here instead of fixed. Addressed in a future step.*

- **KG-1** — Auto Mode UI lists Baseline Op ~30 s while Ch.6 records a 300 s analysis window. Text uses the 300 s window. — logged 2026-08-14
- **KG-2** — Solenoid mapping in settings (SV1/SV3 baseline) disagrees with older proposal text (SV2+SV3 / SV1+SV4). Omitted from the 2-page chapter. — logged 2026-08-14

---

## Architecture Decisions
*Locked decisions that cannot be changed without breaking the system.*

- Team names Arch / Bob / Richard — 2026-08-13
- Context file CLAUDE.md — 2026-08-13
