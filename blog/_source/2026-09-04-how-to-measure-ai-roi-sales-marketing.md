---
layout: post
title: "How to Measure ROI on AI for Sales and Marketing"
description: "A concrete measurement framework for AI investments, which metrics to baseline, how to attribute results honestly, and the four numbers that actually matter at 90 days."
date: 2026-09-04
author: Noah Chaney
category: National
tags: [ai roi, measurement, sales metrics, marketing metrics, analytics]
permalink: /blog/how-to-measure-ai-roi-sales-marketing/
image: /assets/brand/tcg-og-image.png
faq:
 - question: "How do you measure ROI on AI?"
 answer: "Baseline a specific operational metric before deployment, measure the same metric the same way at 90 days, convert the delta to dollars using fully loaded labor cost or revenue impact, and divide by total cost including licensing and internal time. Skipping the baseline makes honest measurement impossible."
 - question: "What is a good ROI for an AI investment?"
 answer: "For time-savings use cases, a reasonable target is 2 to 4x total first-year cost, driven by hours returned. Revenue-side use cases are harder to attribute and should be measured on leading indicators like cycle time and coverage rather than claimed revenue lift."
 - question: "How long before AI shows ROI?"
 answer: "Time-savings metrics typically move within 30 to 60 days of adoption. Revenue metrics take a full sales cycle plus a quarter to read reliably, for most B2B companies, 90 to 180 days."
---

**Quick answer:** Measure AI ROI by baselining one specific operational metric before deployment, re-measuring it the same way at 90 days, converting the change into dollars using fully loaded labor cost, and dividing by total cost including licensing and internal time. Time-savings use cases should target 2 to 4x first-year cost. If you did not take a baseline, you cannot measure ROI. You can only tell a story about it.

Most AI ROI numbers presented in board decks are unfalsifiable. Here is how to produce ones that survive scrutiny.

## The core problem: attribution

If your pipeline grew 18% in the quarter you rolled out AI, how much of that was AI? Possibly some. Also possibly the two reps you hired, the seasonal pattern, the competitor who raised prices, and the product update.

Attribution is genuinely hard, and the honest response is not to fabricate precision. It is to measure things closer to the intervention where causation is more traceable.

**Measure inputs you changed, not outcomes you hoped for.** If you deployed a research brief workflow, measure research hours. That number is directly caused by the intervention and defensible. Revenue is not.

## The four numbers that matter

### 1. Hours returned per person per week

The most defensible AI metric, because it is closest to the intervention.

**How to baseline:** before deployment, have a representative sample of 5 to 10 people log time in the target category for one week. Not estimates from memory, a real log. Memory-based estimates are consistently off by 30 to 50%.

**How to re-measure:** identical method, same people, at day 90.

**How to convert to dollars:** hours saved × fully loaded hourly cost. For a rep with a $110,000 fully loaded cost, that is roughly $53/hour. Five hours a week is $13,780 per rep per year.

**The honest caveat:** hours returned are only worth their labor cost if those hours go to something valuable. Track what filled them. If reps saved five hours and their selling time did not move, you bought slack, not productivity. That may be fine, but say so accurately.

### 2. Cycle time on a specific process

Proposal turnaround. Lead response time. Onboarding time. Content production time.

These are clean because they are usually already timestamped in your systems, which means the baseline exists retroactively even if you forgot to take one. Pull the last two quarters, compare to the current quarter.

**Why it matters:** cycle time has a well-established relationship to conversion in most sales motions. A proposal turnaround dropping from five days to one is a defensible business claim, not just an efficiency claim.

### 3. Coverage or throughput per person

How many accounts can one rep actively work? How many campaigns can one marketer run? This is where AI creates operating leverage rather than just savings.

Triple Crown Group has seen lead coverage per sales rep improve by roughly 1.87x on engagements where research and prep workflows were adopted. Coverage is measurable, attributable to the workflow change, and directly translates into either more pipeline or fewer required hires.

**How to convert to dollars:** if a rep can cover 1.8x the accounts, the value is either incremental pipeline from the additional coverage or the avoided cost of the hire you did not need to make. The second is usually the more conservative and more defensible number.

### 4. Adoption rate

Not a financial metric, but the leading indicator for all of them. Percentage of eligible events where the workflow was actually used.

If adoption is under 50% at day 90, none of the other numbers are real. You measured a subset of enthusiasts and extrapolated.

## What not to measure

**Total prompts sent.** Volume of AI usage is not a business outcome. Teams game it instantly once it becomes a metric.

**"AI-influenced revenue."** This is a marketing-attribution style metric with all of that category's problems and less rigor. It attributes any deal touched by an AI-assisted activity to AI. Do not put it in front of a CFO who is paying attention.

**Satisfaction surveys alone.** Useful as a supplement, useless as the primary case. People report liking things they do not use.

**Vendor-supplied dashboards, unquestioned.** Tool vendors measure engagement with their tool. That is their business metric, not yours.

## The full cost side of the equation

ROI denominators get understated constantly. Include all of:

- Consulting or build fees
- Software licensing (per seat × seats × 12, the number that surprises people)
- Internal time in discovery, training, and rollout, valued at fully loaded cost
- Ongoing maintenance and ownership time
- The cost of anything you retired or duplicated during transition

A "$25,000 project" with 40 seats at $30/month is actually $39,400 in year one before internal time. Model it honestly or the ROI figure is fiction.

## A worked example

A 30-person B2B company, 12 sales reps, deploys research briefs and call capture.

**Costs, year one:**
- Consulting (audit, build, training): $28,000
- Licensing: 12 seats × $30/mo × 12 = $4,320; conversation intelligence 12 × $35/mo × 12 = $5,040
- Internal time: ~120 hours across the team at $60/hr = $7,200
- **Total: $44,560**

**Measured results at 90 days:**
- Research hours: 7.2 → 2.9 per rep per week (4.3 saved)
- CRM admin: 4.1 → 2.2 per rep per week (1.9 saved)
- Total: 6.2 hours × 12 reps = 74.4 hours/week
- Annualized at $53/hr fully loaded: **$205,000 in returned capacity**
- Proposal turnaround: 6.5 days → 2.1 days
- Adoption: 78% of eligible calls

**The honest framing:** $205,000 is returned capacity, not cash saved. You did not reduce headcount. The defensible claims are: the same 12 reps now cover meaningfully more accounts, proposal turnaround dropped 68%, and the company deferred a planned 13th hire worth roughly $110,000 fully loaded.

That framing survives a CFO conversation. "We generated $205,000 in savings" does not.

## Measurement timeline

| When | What to measure |
|---|---|
| Before deployment | Baseline: time logs, cycle times, coverage, current costs |
| Day 30 | Adoption only. Outcome metrics are still novelty-inflated |
| Day 60 | Adoption plus early time metrics; expect a dip from day 30 |
| Day 90 | Full re-measure of baseline metrics |
| Day 180 | Downstream business metrics: win rate, cycle time, pipeline coverage |
| Annually | Total cost of ownership review and license utilization audit |

## Frequently asked questions

**How do you measure ROI on AI?**
Baseline a specific operational metric, re-measure identically at 90 days, convert the delta to dollars at fully loaded cost, and divide by total cost including licensing and internal time.

**What is a good ROI for an AI investment?**
2 to 4x first-year total cost for time-savings use cases. Revenue-side use cases should be measured on leading indicators rather than claimed revenue lift.

**What if we didn't take a baseline?**
Use retroactive system data where it exists, timestamps in your CRM give you cycle times without a prospective baseline. For time-use metrics, take the baseline now and treat the first 90 days as unmeasured.

**How do we handle the fact that hours saved aren't cash?**
Say so explicitly and report it as returned capacity. Then report what actually filled the hours. Leaders trust the second number far more than the first, and it is the one that eventually shows up in results.

**Should we measure per-tool or per-workflow?**
Per-workflow. Tools support multiple workflows and workflows span multiple tools. The workflow is the unit of change, so it is the unit of measurement.

---

*Triple Crown Group defines the measurement before the build, so you know at 90 days whether it worked. [See our early results](/results/).*
