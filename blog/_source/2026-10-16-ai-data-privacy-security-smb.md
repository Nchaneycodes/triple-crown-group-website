---
layout: post
title: "AI Data Privacy and Security for Small Businesses: What to Lock Down First"
description: "A practical security and privacy checklist for SMBs deploying AI, what data must never go in, which settings actually matter, and how to write a usable AI policy."
date: 2026-10-16
author: Noah Chaney
category: National
tags: [ai security, data privacy, ai policy, governance, compliance, smb]
permalink: /blog/ai-data-privacy-security-smb/
image: /assets/brand/tcg-og-image.png
faq:
 - question: "Is it safe to put company data into AI tools?"
 answer: "It depends entirely on the tier. Business and enterprise tiers of major AI platforms typically commit contractually not to train on your data and provide admin controls and retention settings. Consumer free tiers generally do not offer these protections and should never receive company data."
 - question: "What data should never go into an AI tool?"
 answer: "Customer personal information, health or financial records, credentials and API keys, anything under NDA, unreleased financial results, contract terms, employee records, and source code covered by confidentiality obligations. Unless you are using a tool specifically contracted and configured for that data type."
 - question: "Do small businesses need an AI use policy?"
 answer: "Yes, and most need it urgently, because employees are already using AI tools with company data whether or not the company has authorized it. A two-page policy that people actually read is far more useful than a twenty-page document nobody opens."
---

**Quick answer:** The three things to fix first are the tier your team uses (business, never consumer free), a written two-page policy naming what data may never be entered, and admin controls with retention settings configured. Your employees are already using AI tools with company data. A policy is not getting ahead of the risk. It is catching up to it.

This is the least exciting AI topic and the one most likely to produce a bad quarter if ignored.

## The uncomfortable starting point

At nearly every company with more than about ten people, employees are already pasting company information into consumer AI tools. Customer emails, contract language, financial figures, candidate resumes, patient-adjacent notes.

They are not being reckless. They are trying to do their jobs with a useful tool, and nobody told them not to.

Two implications:

1. **Prohibition does not work.** It drives usage to personal devices and personal accounts, where you have zero visibility and zero control. This is worse than sanctioned usage with boundaries.
2. **The policy conversation is overdue, not premature.** Waiting until you have a formal AI program means running unmanaged risk in the meantime.

## Fix 1: Get everyone onto a business tier

This is the single highest-value action and it is mostly a purchasing decision.

**What business and enterprise tiers typically provide:**

- Contractual commitment not to train models on your inputs
- Admin controls over who has access and what they can do
- Configurable data retention
- SSO and centralized account management
- Audit logging
- A real contract with real terms

**What consumer free tiers typically do not.** Terms vary by vendor and change over time, so read the current terms for the specific product rather than assuming.

At roughly $20 to $30 per user per month, this is cheap relative to the exposure. Buy seats for everyone likely to use AI, not just the official pilot group. The alternative is that unlicensed staff keep using personal accounts.

## Fix 2: Write the two-page policy

Long policies do not get read, which means they do not change behavior. Two pages, plain language, four sections.

**Section 1: Approved tools.** Name them. Explain how to get access. Make it easy, because friction here pushes people back to personal accounts.

**Section 2: Never enter this data.** Be specific and concrete rather than categorical:

- Customer or client personal information, names with contact details, account numbers, personal circumstances
- Health information of any kind
- Financial account details, payment card data
- Passwords, API keys, credentials, tokens
- Anything covered by an NDA or confidentiality agreement
- Unreleased financial results or material non-public information
- Contract terms and pricing agreements
- Employee records, performance information, compensation
- Source code, where confidentiality obligations apply

Add a plain-language test people can actually apply: *"If this appearing in a competitor's inbox would be a problem, it does not go in an AI tool."*

**Section 3: Required review.** Nothing goes to a customer, gets published, or enters a system of record without a human reading it. Name who is accountable, the person who sends it, not the tool.

**Section 4: Who to ask.** One name, one email. Questions should be easy to ask, because the alternative is people guessing.

Distribute it, require acknowledgment, and cover it in onboarding.

## Fix 3: Configure the settings that matter

Once you have business tiers, three settings do most of the work:

**Training data usage.** Confirm it is off. On business tiers it is generally off by default, but confirm rather than assume, and document that you confirmed.

**Retention.** Set it to the shortest period consistent with your needs. Shorter retention reduces exposure if the vendor is breached and simplifies any future discovery obligation.

**Access controls.** SSO where available. Offboarding process that removes AI tool access along with everything else, a surprisingly common gap.

Also worth doing: check what data connections you have enabled. Assistants that connect to your email, drive, or CRM inherit those permission scopes. Understand what a given integration can actually read before enabling it broadly.

## The risks worth understanding

**Data exposure through vendor breach.** Any data you send to a vendor is data that vendor could lose. Retention limits and data minimization are the practical mitigations.

**Data exposure through your own people.** Far more common than vendor breach. Addressed by policy and training rather than technology.

**Output errors reaching customers.** AI confidently produces wrong information. The mitigation is human review, which is why it belongs in the policy as a requirement rather than a suggestion.

**Confidentiality obligation breach.** If you have client NDAs or customer contracts with confidentiality terms, entering that information into a third-party tool may breach them regardless of how secure the tool is. Check your agreements. Agencies, consultancies, and professional services firms are most exposed here.

**Regulatory exposure by sector.** Healthcare, financial services, legal, and any business handling data of EU residents have specific obligations that go beyond general good practice. Get sector-specific advice.

**Shadow AI.** Unapproved tools, personal accounts, browser extensions with broad permissions. The mitigation is making the approved path easy, not making the unapproved path forbidden.

## A 30-day plan

**Week 1.** Find out what is actually being used. Ask directly, without blame, a short anonymous survey works. Check expense reports for personal AI subscriptions. Look at browser extension inventories if you have that visibility.

**Week 2.** Purchase business tier licenses. Configure training, retention, and access settings. Set up SSO.

**Week 3.** Write and distribute the policy. Two pages. Collect acknowledgments.

**Week 4.** Run a 45-minute training session. Cover: what tools we use, what data never goes in, what needs review, who to ask. Use real examples from your business rather than generic ones.

Total cost for a 50-person company: roughly **$15,000 to $18,000 annually** in licensing plus a few thousand in setup. Compared with the downside of an unmanaged data incident, this is inexpensive.

## Frequently asked questions

**Is it safe to put company data into AI tools?**
On business and enterprise tiers with training disabled and retention configured, for most non-regulated business data, yes. On consumer free tiers, no.

**What data should never go into an AI tool?**
Customer personal information, health and financial records, credentials, NDA-covered material, unreleased financials, contract terms, employee records, and confidential source code.

**Do small businesses need an AI use policy?**
Yes, and most need it now, because unmanaged usage is already happening.

**Should we block AI tools on our network?**
Generally counterproductive. It moves usage to personal devices where you have no visibility. Provide a sanctioned option with boundaries instead.

**What if we're in a regulated industry?**
Everything above still applies, plus sector-specific requirements, BAAs for healthcare, examiner expectations for financial services, professional responsibility rules for legal. Involve your compliance function in the workflow design, not just the tool selection.

**How often should we revisit this?**
Annually at minimum, and whenever a vendor materially changes terms. Set a calendar reminder, vendor terms change quietly and nobody gets notified in a way they notice.

---

*Triple Crown Group starts engagements with the policy, because the alternative is running risk you cannot see. [Get in touch](/contact/).*
