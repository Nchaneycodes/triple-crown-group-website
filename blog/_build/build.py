#!/usr/bin/env python3
"""Regenerate the Insights section and sitemap.xml.

The site deliberately has no build step on GitHub Pages, so this runs
locally and the generated HTML is committed. Run it after editing any
markdown in blog/_source/, adding a post, or changing the page template.

    python3 blog/_build/build.py

It rewrites blog/index.html, blog/<slug>/index.html for every source
file, and sitemap.xml. It does not touch the six core pages.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "blog" / "_source"
SITE = "https://triplecrown.group"
OG_IMAGE = f"{SITE}/assets/brand/tcg-og-image.png"
ORG_ID = f"{SITE}/#organization"

PHONE = "+1-859-414-4178"
EMAIL = "nchaney@triplecrown.group"

# The organization entity. Every post references it via {"@id": ORG_ID}, so it has
# to be defined on the page too or the reference dangles.
ORG = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "@id": ORG_ID,
    "name": "Triple Crown Group",
    "alternateName": ["TCG", "Triple Crown Group AI Consultants"],
    "url": f"{SITE}/",
    "logo": OG_IMAGE,
    "image": OG_IMAGE,
    "description": ("Triple Crown Group is the AI hire small businesses have not made yet. "
                    "We audit where time and money are going, build the automations and "
                    "agents that fix it, and stay on to run them, for owner run businesses "
                    "across Greater Cincinnati and Northern Kentucky."),
    "slogan": "Driving AI Efficiencies",
    "telephone": PHONE,
    "email": EMAIL,
    "contactPoint": [{"@type": "ContactPoint", "contactType": "sales",
                      "telephone": PHONE, "email": EMAIL,
                      "areaServed": ["US-KY", "US-OH"],
                      "availableLanguage": ["English"]}],
    "areaServed": (
        [{"@type": "City", "name": n} for n in [
            "Cincinnati, OH", "Covington, KY", "Florence, KY", "Newport, KY",
            "Fort Mitchell, KY", "Erlanger, KY", "Crestview Hills, KY",
            "Blue Ash, OH", "Mason, OH", "West Chester, OH", "Liberty Township, OH"]]
        + [{"@type": "AdministrativeArea", "name": n} for n in [
            "Northern Kentucky", "Boone County, KY", "Kenton County, KY",
            "Campbell County, KY", "Hamilton County, OH", "Greater Cincinnati"]]),
    "serviceType": ["AI consulting", "AI audit", "AI training", "Custom AI agent development", "Workflow automation"],
    "knowsAbout": ["AI consulting", "AI audit", "AI adoption for small businesses", "Lead response automation", "Quoting and proposal automation", "Scheduling and follow up automation", "Back office automation", "Document automation", "Custom AI agents", "AI training for small teams", "AI governance and use policy", "Large language models", "ChatGPT", "Claude", "Microsoft Copilot", "Google Gemini"],
    "founder": {"@type": "Person", "@id": f"{SITE}/#noah-chaney",
                "name": "Noah Chaney", "jobTitle": "Founder",
                "email": EMAIL, "telephone": PHONE,
                "url": f"{SITE}/about/", "worksFor": {"@id": ORG_ID}},
    "sameAs": ["https://www.linkedin.com/company/triplecrowngroup",
               "https://maps.google.com/?cid=14527737738999246731"],
}

# Posts carrying a July 2026 date: the two pillars plus the highest
# commercial-intent and most citable pieces. Everything else publishes
# undated as evergreen reference.
DATED_JULY = {
    "how-to-get-your-brand-recommended-by-chatgpt",
    "ai-consulting-cost-cincinnati",
    "where-cincinnati-sales-teams-actually-are-with-ai",
    "ai-use-policy-template-small-business",
    "day-in-the-life-sales-rep-using-ai",
    "ai-sales-enablement-guide",
    "how-to-choose-ai-consultant-cincinnati",
    "what-is-an-ai-audit-sales-team",
    "why-ai-pilots-fail",
    "ai-consulting-northern-kentucky",
}

# Desktop header. Insights is deliberately absent: eight items crowd the bar,
# so the blog is reached from the mobile drawer, the footer, and in page links.
NAV = [
    ("/", "Home"),
    ("/who-we-help/", "Who We Help"),
    ("/what-we-support/", "What We Support"),
    ("/how-we-work/", "How We Work"),
    ("/about/", "About"),
    ("/partnerships/", "Partnerships"),
    ("/contact/", "Contact"),
]

MOBILE_NAV = NAV[:-1] + [("/results/", "Results"), ("/blog/", "Insights")]
FOOTER_NAV = NAV[:-1] + [("/results/", "Results"), ("/blog/", "Insights"),
                         ("/contact/", "Contact")]

CORE_PRIORITY = [
    ("/", "1.0"), ("/who-we-help/", "0.9"), ("/what-we-support/", "0.9"),
    ("/how-we-work/", "0.8"),
    ("/about/", "0.7"), ("/results/", "0.8"), ("/partnerships/", "0.8"),
    ("/contact/", "0.9"),
    ("/blog/", "0.9"),
]

LASTMOD = "2026-07-30"

# bump when css/js changes so returning visitors do not run a stale copy
ASSET_V = "7"


# ------------------------------------------------------------ dash removal
# The brief forbids dashes as pause punctuation. Sources are cleaned on
# import so a freshly pasted post is normalised the same way as the rest.

COMMA_STARTERS = (
    "but ", "and ", "or ", "so ", "yet ", "plus ", "including ", "which ",
    "not ", "no ", "often ", "usually ", "typically ", "sometimes ",
    "especially ", "particularly ", "specifically ", "namely ", "ideally ",
    "generally ", "largely ", "mostly ", "far ", "much ", "well ", "even ",
    "with ", "for ", "from ", "about ", "roughly ", "approximately ",
)
CLAUSE_STARTERS = (
    "it ", "it's", "its ", "they ", "we ", "you ", "i ", "he ", "she ",
    "that ", "this ", "these ", "those ", "there ", "here ",
    "nobody ", "everyone ", "someone ", "anyone ", "nothing ", "everything ",
)
CLAUSE_VERB = re.compile(
    r"^\W*\w+(?:\s+\w+){0,2}\s+"
    r"(is|are|was|were|has|have|had|can|will|would|should|does|do|did|becomes|"
    r"means|makes|gets|goes|comes|remains|stays)\b", re.I)


def strip_dashes(text):
    # paired em dashes wrapping an aside become parentheses, because commas
    # there would separate a subject from its verb
    pat = re.compile(r"\s—\s([^—.!?\n]{3,120}?)\s—\s")
    prev = None
    while prev != text:
        prev = text
        text = pat.sub(lambda m: " (" + m.group(1).strip() + ") ", text, count=1)

    out, i = [], 0
    while True:
        m = re.search(r"\s*—\s*", text[i:])
        if not m:
            out.append(text[i:])
            break
        start, end = i + m.start(), i + m.end()
        out.append(text[i:start])
        after = text[end:end + 80]
        low = after.lstrip().lower()
        if low.startswith(COMMA_STARTERS):
            punct = ","
        elif low.startswith(CLAUSE_STARTERS) or CLAUSE_VERB.match(after):
            punct = "."
        else:
            punct = ","
        if punct == ".":
            rest = text[end:]
            if rest and rest[0].isalpha():
                out.append(". " + rest[0].upper())
                i = end + 1
            else:
                out.append(". ")
                i = end
        else:
            out.append(", ")
            i = end
    text = "".join(out)

    # numeric ranges: "3,000–8,000" reads better as "3,000 to 8,000",
    # including when an assistant quotes the figure aloud
    text = re.sub(r"(?<=[\d%\)])\s*–\s*(?=[\$\d])", " to ", text)
    text = re.sub(r"(?<=[A-Za-z])\s*–\s*(?=\d)", " to ", text)
    text = re.sub(r"\s*–\s*", " to ", text)

    text = re.sub(r",\s*,", ",", text)
    # Only collapse a period that dash replacement left separated by
    # whitespace. Matching ".." directly would eat one dot off an ellipsis
    # on every run, which is exactly what happened the first time.
    text = re.sub(r"(?<!\.)\.\s+\.(?!\.)", ".", text)
    text = re.sub(r",\s*\.", ".", text)
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\s+([.!?])", r"\1", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return re.sub(r",\s*$", "", text, flags=re.M)


# ----------------------------------------------------------- front matter

def parse_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("no front matter")
    raw, body = m.group(1), m.group(2)
    meta, faq, cur, in_faq = {}, [], None, False
    for line in raw.split("\n"):
        if line.startswith("faq:"):
            in_faq = True
            continue
        if in_faq:
            q = re.match(r"\s*-\s*question:\s*(.*)$", line)
            a = re.match(r"\s*answer:\s*(.*)$", line)
            if q:
                cur = {"question": _unquote(q.group(1))}
                faq.append(cur)
                continue
            if a and cur is not None:
                cur["answer"] = _unquote(a.group(1))
                continue
            if line.strip() and not line.startswith(" "):
                in_faq = False
            else:
                continue
        kv = re.match(r"^(\w[\w_]*):\s*(.*)$", line)
        if kv:
            meta[kv.group(1)] = _unquote(kv.group(2))
    meta["faq"] = faq
    return meta, body


def _unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1]
    return s.replace('\\"', '"')


# --------------------------------------------------------------- markdown

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)


def render_table(block):
    rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in block]
    if len(rows) >= 2 and all(re.fullmatch(r":?-{2,}:?", c) for c in rows[1] if c):
        head, body = rows[0], rows[2:]
    else:
        head, body = None, rows
    h = ""
    if head:
        h = "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>"
    b = "<tbody>" + "".join(
        "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody>"
    return f'<div class="table-wrap"><table>{h}{b}</table></div>'


def md_to_html(md):
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if re.match(r"^---+\s*$", line):
            out.append("<hr>")
            i += 1
            continue
        h = re.match(r"^(#{2,4})\s+(.*)$", line)
        if h:
            lvl = len(h.group(1))
            out.append(f"<h{lvl}>{inline(h.group(2).strip())}</h{lvl}>")
            i += 1
            continue
        if line.lstrip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            out.append(render_table(block))
            continue
        if line.lstrip().startswith(">"):
            block = []
            while i < len(lines) and (lines[i].lstrip().startswith(">") or not lines[i].strip()):
                if not lines[i].strip():
                    if i + 1 < len(lines) and lines[i + 1].lstrip().startswith(">"):
                        block.append("")
                        i += 1
                        continue
                    break
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            paras = "\n".join(block).split("\n\n")
            inner = "".join(f"<p>{inline(p.strip())}</p>" for p in paras if p.strip())
            out.append(f"<blockquote>{inner}</blockquote>")
            continue
        if re.match(r"^\d+\.\s+", line.strip()):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        if re.match(r"^[-*]\s+", line.strip()):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip()))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{2,4}\s|\||>|\d+\.\s|[-*]\s|---+\s*$)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


# --------------------------------------------------------------- template

def nav_html(active):
    active_attr = ' class="active"'
    items = "".join(
        f'<li><a href="{u}"{active_attr if u == active else ""}>{n}</a></li>'
        for u, n in NAV)
    mob = "".join(f'<a href="{u}">{n}</a>' for u, n in MOBILE_NAV)
    return f"""  <header class="site-header">
    <div class="container">
      <a href="/" class="brand-mark">
        <img src="/assets/brand/tcg-icon.svg" alt="Triple Crown Group, AI Consultants">
        <span class="brand-wordmark">Triple Crown Group</span>
      </a>
      <nav>
        <ul class="nav-links">{items}</ul>
      </nav>
      <a href="/contact/" class="btn btn-primary nav-cta desktop-only">Get in touch</a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <div class="menu-scrim"></div>
  <nav class="mobile-menu">
{mob}
    <a href="/contact/" class="btn btn-primary">Get in touch</a>
  </nav>"""


FOOTER = ("""  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-logo">
          <img src="/assets/brand/tcg-full-logo.svg" alt="Triple Crown Group, Driving AI Efficiencies">
          <img class="footer-badge" src="/assets/brand/openai-select-partner-badge.svg" alt="OpenAI Select Partner" width="375" height="177">
        </div>
        <ul class="footer-nav">
"""
          + "".join(f'          <li><a href="{u}">{n}</a></li>\n' for u, n in FOOTER_NAV)
          + """        </ul>
      </div>
      <div class="footer-bottom">
        <span>&copy; 2026 Triple Crown Group. AI consultants serving Greater Cincinnati and Northern Kentucky.</span>
        <!--email_off--><span class="footer-contact">
          <a href="tel:+18594144178">(859) 414-4178</a>
          <a href="mailto:nchaney@triplecrown.group">nchaney@triplecrown.group</a>
        </span><!--/email_off-->
      </div>
    </div>
  </footer>

  <script src="/js/main.js?v={ASSET_V_}"></script>
</body>
</html>
""")


def jl(obj):
    return ('  <script type="application/ld+json">\n  '
            + json.dumps(obj, indent=2).replace("\n", "\n  ") + "\n  </script>")


def page(title, desc, canonical, body, schemas, og_type="website", active=""):
    ASSET_V_ = ASSET_V
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc, quote=True)}">
  <link rel="canonical" href="{canonical}">

  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(desc, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:image" content="{OG_IMAGE}">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title, quote=True)}">
  <meta name="twitter:description" content="{html.escape(desc, quote=True)}">
  <meta name="twitter:image" content="{OG_IMAGE}">

  <link rel="icon" type="image/png" href="/assets/brand/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&amp;family=Inter:wght@400;500;600&amp;display=swap">
  <link rel="stylesheet" href="/css/style.css?v={ASSET_V_}">

{chr(10).join(schemas)}
</head>
<body>

{nav_html(active)}

{body}

{FOOTER}"""


# ------------------------------------------------------------------- build

def main():
    if not SRC.exists():
        sys.exit(f"missing {SRC}")

    posts = []
    for path in sorted(SRC.glob("*.md")):
        raw = path.read_text()
        cleaned = strip_dashes(raw)
        if cleaned != raw:
            path.write_text(cleaned)
        meta, body = parse_front_matter(cleaned)
        slug = meta["permalink"].strip("/").split("/")[-1]
        meta.update(slug=slug, dated=slug in DATED_JULY,
                    body_html=md_to_html(body), url=f"/blog/{slug}/")
        posts.append(meta)

    posts.sort(key=lambda p: (not p["dated"], p["category"], p["title"]))

    for p in posts:
        canonical = f"{SITE}{p['url']}"
        article = {
            "@context": "https://schema.org", "@type": "Article",
            "headline": p["title"], "description": p["description"],
            "author": {"@type": "Person", "name": p.get("author", "Noah Chaney"),
                       "url": f"{SITE}/about/"},
            "publisher": {"@id": ORG_ID}, "image": OG_IMAGE,
            "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        }
        if p["dated"]:
            # month precision: published in July 2026, no specific day
            article["datePublished"] = "2026-07"
        schemas = [jl(ORG), jl(article)]
        if p["faq"]:
            schemas.append(jl({
                "@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": f["question"],
                                "acceptedAnswer": {"@type": "Answer", "text": f["answer"]}}
                               for f in p["faq"] if f.get("answer")]}))
        schemas.append(jl({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Insights", "item": f"{SITE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": canonical}]}))

        meta_line = f'<span class="post-cat">{html.escape(p["category"])}</span>'
        if p["dated"]:
            meta_line += ' <time datetime="2026-07">July 2026</time>'
        tags = [t.strip() for t in p.get("tags", "").strip("[]").split(",") if t.strip()]
        tag_html = ('<ul class="post-tags">'
                    + "".join(f"<li>{html.escape(t)}</li>" for t in tags)
                    + "</ul>") if tags else ""

        body = f"""  <main>

    <section class="page-hero post-hero on-dark">
      <div class="container">
        <nav class="crumbs" aria-label="Breadcrumb">
          <a href="/">Home</a> <span aria-hidden="true">/</span>
          <a href="/blog/">Insights</a>
        </nav>
        <p class="post-meta">{meta_line}</p>
        <h1 class="reveal">{html.escape(p["title"])}</h1>
      </div>
    </section>

    <section class="post-section">
      <div class="container">
        <article class="post-body">
{p["body_html"]}
        </article>
        {tag_html}
        <p class="post-back"><a href="/blog/" class="section-foot-link">All insights &rarr;</a></p>
      </div>
    </section>

    <section class="closing-cta on-dark">
      <div class="container">
        <span class="eyebrow reveal">Contact</span>
        <h2 class="reveal">Let's talk about where AI actually helps your team.</h2>
        <a href="/contact/" class="btn btn-primary reveal">Get in touch</a>
      </div>
    </section>

  </main>"""

        out = ROOT / "blog" / p["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(f'{p["title"]} | Triple Crown Group', p["description"],
                            canonical, body, schemas, "article", "/blog/"))

    # index
    cards = []
    for p in posts:
        when = ' <time datetime="2026-07">July 2026</time>' if p["dated"] else ""
        cards.append(f"""          <article class="post-card reveal">
            <p class="post-card-meta"><span class="post-cat">{html.escape(p["category"])}</span>{when}</p>
            <h2><a href="{p["url"]}">{html.escape(p["title"])}</a></h2>
            <p>{html.escape(p["description"])}</p>
            <a href="{p["url"]}" class="post-card-link">Read this &rarr;</a>
          </article>""")

    index_body = f"""  <main>

    <section class="page-hero on-dark">
      <div class="container">
        <span class="eyebrow reveal">Insights</span>
        <h1 class="reveal">Practical AI for sales and marketing teams.</h1>
        <p class="subhead reveal">{len(posts)} pieces on auditing, building and adopting AI, written for teams in Cincinnati and Northern Kentucky and for anyone doing this work seriously.</p>
      </div>
    </section>

    <section>
      <div class="container">
        <div class="post-grid reveal-stagger">
{chr(10).join(cards)}
        </div>
      </div>
    </section>

    <section class="closing-cta on-dark">
      <div class="container">
        <span class="eyebrow reveal">Contact</span>
        <h2 class="reveal">Let's talk about where AI actually helps your team.</h2>
        <a href="/contact/" class="btn btn-primary reveal">Get in touch</a>
      </div>
    </section>

  </main>"""

    (ROOT / "blog" / "index.html").write_text(page(
        "Insights | AI for Sales and Marketing Teams | Triple Crown Group",
        "Practical writing on AI audits, adoption, tooling and training for sales and marketing teams across Cincinnati and Northern Kentucky.",
        f"{SITE}/blog/", index_body,
        [jl(ORG),
         jl({"@context": "https://schema.org", "@type": "Blog", "@id": f"{SITE}/blog/",
             "name": "Triple Crown Group Insights",
             "description": "Practical writing on AI for sales and marketing teams in Cincinnati and Northern Kentucky.",
             "url": f"{SITE}/blog/", "publisher": {"@id": ORG_ID},
             "blogPost": [{"@type": "BlogPosting", "headline": p["title"],
                           "url": f"{SITE}{p['url']}", "description": p["description"]}
                          for p in posts]}),
         jl({"@context": "https://schema.org", "@type": "BreadcrumbList",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                 {"@type": "ListItem", "position": 2, "name": "Insights", "item": f"{SITE}/blog/"}]})],
        active="/blog/"))

    # sitemap
    # sorted by URL so the file is stable across runs and diffs stay readable
    entries = [(loc, pri, "monthly") for loc, pri in CORE_PRIORITY]
    entries += sorted(
        ((p["url"], "0.7" if p["dated"] else "0.6", "yearly") for p in posts),
        key=lambda e: e[0])
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(f"""  <url>
    <loc>{SITE}{loc}</loc>
    <lastmod>{LASTMOD}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{pri}</priority>
  </url>""" for loc, pri, freq in entries) + "\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml)

    print(f"{len(posts)} posts + index generated")
    print(f"dated July 2026: {sum(1 for p in posts if p['dated'])}, undated: {sum(1 for p in posts if not p['dated'])}")
    print(f"sitemap: {xml.count('<loc>')} URLs")


if __name__ == "__main__":
    main()
