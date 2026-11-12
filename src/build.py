#!/usr/bin/env python3
"""Builds the Nexora marketing site: one shell, eight pages, no framework."""
import os, pathlib, re, hashlib

BASE = "/nexora"                        # the site lives at novi-q.com/nexora
OUT = pathlib.Path(__file__).resolve().parent.parent / "site" / BASE.strip("/")
EMAIL = "info@nibarc.com"               # Nibarc, the company behind Nexora
DOMAIN = "nibarc.com"                   # Plausible data-domain

NAV = [("/brief/", "Brief"), ("/forge/", "Forge"), ("/manage/", "Manage"),
       ("/how-it-works/", "How it works"), ("/deliverables/", "Deliverables")]

def shell(title, desc, body, path):
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="/assets/img/og.png">
<meta name="theme-color" content="#8A1C3B">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,500&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
<script defer data-domain="{DOMAIN}" src="https://plausible.io/js/script.js"></script>
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Nexora home"><img src="/assets/brand/logo.svg" alt="Nexora" width="448" height="102"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav">{nav}<a class="cta" href="/contact/">Bring a recording</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-brand"><img src="/assets/brand/logo-tagline.svg" alt="Nexora — own the program record" width="562" height="152">
      <p class="byline">A <a href="//ROOT">Nibarc</a> product &mdash; SAP-native strategy, transformation and agents.</p></div>
    <nav>
      <a href="/brief/">Brief</a><a href="/forge/">Forge</a><a href="/manage/">Manage</a><a href="/how-it-works/">How it works</a>
      <a href="/deliverables/">Deliverables</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </nav>
  </div>
</footer>
<script src="/assets/js/site.js"></script>
</body>
</html>
"""

def rebase(html):
    """Rewrite every root-absolute href/src onto BASE, so the site works under a subpath."""
    if not BASE:
        return html
    return re.sub(r'(href|src)="/(?!/)', r'\1="' + BASE + '/', html)

FP = re.compile(r"\.[0-9a-f]{8}$")

def _plain(p):
    """Strip a previous build's fingerprint so rebuilds are idempotent."""
    stem = p.stem
    return p.with_name(FP.sub("", stem) + p.suffix) if FP.search(stem) else p

def fingerprint():
    """Rename every asset to name.<hash>.ext and rewrite the references.

    The assets are served with a one-year immutable cache, which is only safe
    when a changed file also changes its URL. Without this, a browser holds the
    old stylesheet and the page renders unstyled.
    """
    assets = sorted(p for p in (OUT / "assets").rglob("*") if p.is_file())
    mapping = {}
    for p in assets:
        plain = _plain(p)
        if plain != p:
            p.rename(plain)
            p = plain
        h = hashlib.sha256(p.read_bytes()).hexdigest()[:8]
        new = p.with_name(f"{p.stem}.{h}{p.suffix}")
        p.rename(new)
        ref = lambda q: "/" + str(q.relative_to(OUT.parent)).replace(os.sep, "/")
        mapping[ref(p)] = ref(new)
    for h in OUT.rglob("*.html"):
        s = h.read_text()
        for old, new in mapping.items():
            s = s.replace(old, new)
        h.write_text(s)
    return len(mapping)

def page(path, title, desc, body):
    p = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(rebase(shell(title, desc, body, path)).replace('href="//ROOT"', 'href="/"'))
    print("wrote", p.relative_to(OUT.parent))


AIDEN = """
<div class="aiden" id="aiden-panel" aria-label="Aiden, reading the program record">
  <div class="aiden-head">
    <div class="aiden-av">A</div>
    <div><div class="name">Aiden</div><div class="sub">Reads the record · never writes</div></div>
    <div class="aiden-scope"><span class="on">Record</span><span>As-Is</span></div>
  </div>
  <div class="aiden-body">
    <div class="aiden-q">Why did we defer service credits?</div>
    <span class="aiden-chip">• Walking the decision graph</span>
    <div class="aiden-a">
      <p>Service credits were <strong>deferred to the parent landscape</strong>. The process owner ruled it in session 3 and recorded the two options rejected: building them locally, or dropping them.</p>
      <p>Twelve artifacts rest on that ruling — the revenue-recognition design, two test families and the finance change-impact notes. None is on superseded ground.</p>
      <div class="aiden-cites"><span>DC-04</span><span>S-03 · 15:47</span><span>EV-212</span><span>BP-2.4</span></div>
    </div>
  </div>
  <div class="aiden-compose">Ask the record…<b aria-hidden="true"></b></div>
  <div class="aiden-foot"><span>AI-generated. Verify figures before acting.</span><span class="mono">1 / 200 today · $0.013</span></div>
</div>
"""

how = """
<section class="page-head">
  <div class="wrap">
    <h1>Nothing becomes memory until a person says so.</h1>
    <p class="lede">The record under the Brief, Forge and Manage: its layers, the pipeline, the four human gates and the controls. This is what Nexora does, how it is enforced, and what it refuses.</p>
  </div>
</section>

<section class="section tight on-ink">
  <div class="wrap grid grid-5-7" style="align-items:start">
    <div class="stack">
      <h2>Three layers. One source of truth.</h2>
      <p class="lede">An append-only event log is the authority. A property graph is projected from it for reasoning. A vector index finds candidates by meaning, and is never the authority.</p>
      <div class="claims" style="grid-template-columns:1fr;gap:16px">
        <div><h4>Event log</h4><p>Facts are never updated; a new event supersedes. The source of truth.</p></div>
        <div><h4>Property graph</h4><p>Typed nodes and edges the product reasons over, projected from the log.</p></div>
        <div><h4>Vector index</h4><p>pgvector. Finds candidates by meaning. Never the authority.</p></div>
      </div>
    </div>
    <table class="plain">
      <thead><tr><th>The question</th><th>Pattern</th><th>Layer</th></tr></thead>
      <tbody>
        <tr><td>Why does billing work this way?</td><td>Lookup</td><td>Graph</td></tr>
        <tr><td>If I change this requirement, what breaks?</td><td>Traversal</td><td>Graph</td></tr>
        <tr><td>What did anyone say about intercompany?</td><td>Similarity</td><td>Vectors, then graph</td></tr>
        <tr><td>Which deliverables lack approval evidence?</td><td>Query</td><td>Graph</td></tr>
        <tr><td>What did we believe in March that is no longer true?</td><td>Temporal</td><td>Event log</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Every fact is a typed, addressable object.</h2>
      <p class="lede">Session, evidence, requirement, conflict, decision, fit theme, delta item, blueprint section, test artifact, interface, risk, deliverable. Every node carries state, confidence, provenance, as-of, confirmed-by and supersedes. An object missing any of them cannot be promoted to memory.</p>
    </div>
    <div class="grid grid-2" style="align-items:center">
      <div class="stack">
        <p><span class="pill">proposed</span> → <span class="pill">confirmed</span> → <span class="pill">superseded</span></p>
        <p class="muted">Only confirmed objects are memory. A draft is always labelled a draft.</p>
      </div>
      <p class="note">IDs are never reused or renumbered. In the field, a renumbering done outside Nexora silently broke 278 conflict citations. Nexora's counter makes that failure impossible.</p>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head"><h2>From a workshop to a signed blueprint.</h2></div>
    <ol class="steps">
      <li><h4>Ingest</h4><p>Parse, hash and chunk each session; flag capture gaps. Idempotent and resumable. A shared room microphone is flagged, never credited as a speaker.</p></li>
      <li><h4>Extract</h4><p>One requirement per node, never compound, each cited to its evidence. Scored against hand-written expert cases; on a weak score it stops.</p></li>
      <li><h4>Detect and fit</h4><p>Contradictions across sessions by exhaustive review, not similarity search. Themes checked against a pinned Best Practices baseline.</p></li>
      <li class="gate"><h4>Adjudicate</h4><p>A ruling pack goes to the owner: both positions, the evidence, a labelled root-cause hypothesis, candidate rulings. The ruling binds.</p></li>
      <li><h4>Graph</h4><p>Confirmed facts and rulings become nodes and edges in the property graph, so Aiden can walk them and the impact of any change can be traced.</p></li>
      <li class="gate"><h4>Blueprint</h4><p>Assembled from fits and rulings; signed, then immutable. The signed version stays retrievable byte for byte, for as long as the system runs.</p></li>
      <li class="gate"><h4>Regenerate</h4><p>Scoped rebuilds: tests, change impact, BPMN, training. Only what the ruling touches; a person reviews the diff and commits.</p></li>
      <li><h4>Controls</h4><p>Citation check, format steward, test evaluator, value manifest. Each one refuses rather than guesses, and says in plain words why it refused.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap grid grid-5-7" style="align-items:start">
    <div class="stack">
      <h2>The Gatekeeper is the only way into memory.</h2>
      <p class="lede">Six conditions, checked twice: the application explains every refusal in plain language, and a database trigger guarantees it. A test fails if the two ever disagree.</p>
    </div>
    <table class="plain ids">
      <thead><tr><th>#</th><th>Condition</th><th>Why it exists</th></tr></thead>
      <tbody>
        <tr><td>1</td><td>A named person confirmed it</td><td>Machine confidence is not ratification.</td></tr>
        <tr><td>2</td><td>Requirements and rulings cite evidence</td><td>Without a citation it asserts what the record cannot support.</td></tr>
        <tr><td>3</td><td>Every citation resolves</td><td>A citation pointing at nothing reads as support, so it is worse than none.</td></tr>
        <tr><td>4</td><td>No superseded ground beneath it</td><td>Otherwise it is a confident fact on a decision that no longer holds.</td></tr>
        <tr><td>5</td><td>Rulings carry rationale and rejected options</td><td>Six months on, the question is always "did we consider X?"</td></tr>
        <tr><td>6</td><td>Confidence is stated</td><td>An unqualified assertion is the dangerous kind.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head"><h2>Those who decide, and those who do, are kept apart.</h2></div>
    <div class="grid grid-7-5" style="align-items:start">
      <table class="plain">
        <thead><tr><th>Role</th><th>Rule</th><th>Override</th><th>Sign</th><th>Commit</th><th>Produce</th><th>Read</th></tr></thead>
        <tbody>
          <tr><td>Process expert</td><td>Yes</td><td>Yes</td><td>—</td><td>—</td><td>—</td><td>Yes</td></tr>
          <tr><td>Process owner</td><td>Yes</td><td>Yes</td><td>Yes</td><td>—</td><td>—</td><td>Yes</td></tr>
          <tr><td>Program lead</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td><td>—</td><td>Yes</td></tr>
          <tr><td>Change and training lead</td><td>—</td><td>—</td><td>—</td><td>—</td><td>Yes</td><td>Yes</td></tr>
          <tr><td>Test lead</td><td>—</td><td>—</td><td>—</td><td>—</td><td>Yes</td><td>Yes</td></tr>
          <tr><td>Viewer</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>Yes</td></tr>
        </tbody>
      </table>
      <div class="claims" style="grid-template-columns:1fr">
        <div><h4>Every ruling has a name</h4><p>Rulings bind, so each names a person who can be asked why.</p></div>
        <div><h4>Reversal is supersession</h4><p>A new ruling replaces the old; the old stays readable in full.</p></div>
        <div><h4>Refused before written</h4><p>A test lead attempting a ruling is stopped before anything reaches the record.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Signed means signed. Change means a new version.</h2>
      <p class="lede">When a ruling lands, only the sections it touches are rebuilt. The rest stays byte-identical, and v1.0 stays retrievable forever.</p>
    </div>
    <div class="bp" aria-label="Blueprint versions: a ruling rebuilds only the sections it touches">
      <span class="lab">v1.0 · signed</span><span class="cell">BP-1.1</span><span class="cell">BP-1.2</span><span class="cell">BP-2.1</span><span class="cell">BP-2.4</span><span class="cell">BP-3.2</span><span class="cell">BP-4.1</span>
      <span class="lab" style="color:var(--seal)">a ruling lands</span><span class="state">identical</span><span class="state">identical</span><span class="state">identical</span><span class="state hot">rebuilt</span><span class="state hot">rebuilt</span><span class="state">identical</span>
      <span class="lab">v1.1 · draft</span><span class="cell draft">BP-1.1</span><span class="cell draft">BP-1.2</span><span class="cell draft">BP-2.1</span><span class="cell rebuilt">BP-2.4</span><span class="cell rebuilt">BP-3.2</span><span class="cell draft">BP-4.1</span>
    </div>
    <div class="claims" style="margin-top:48px;grid-template-columns:repeat(4,1fr)">
      <div><h4>Immutable</h4><p>v1.0 stays retrievable byte for byte, forever.</p></div>
      <div><h4>Scoped</h4><p>Only what the ruling touches is rebuilt.</p></div>
      <div><h4>Committed</h4><p>A person reviews the diff and commits it.</p></div>
      <div><h4>Governed</h4><p>Each change feeds the change control board.</p></div>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head">
      <h2>Tests that prove your design, not SAP's standard.</h2>
      <p class="lede">A pack that runs green and proves nothing is refused.</p>
    </div>
    <ol class="steps" style="grid-template-columns:repeat(4,minmax(0,1fr))">
      <li><h4>Test plan</h4><p>Cycles, coverage and traceability from the signed blueprint. Test lead approves.</p></li>
      <li><h4>Test scenarios</h4><p>One per process variant, each with an outcome a tester can see. Process owner approves.</p></li>
      <li><h4>Test cases</h4><p>Steps, test data and the negative cases each rule implies. Test lead approves.</p></li>
      <li><h4>Results read</h4><p>Results in, coverage-weighted maturity out, anomalies flagged. You sign the read.</p></li>
    </ol>
    <div class="claims" style="margin-top:48px">
      <div><h4>Every section has a test; critical sections have two</h4><p>An untested section is named up front, not discovered in UAT when it is expensive.</p></div>
      <div><h4>At least fifteen percent are negative</h4><p>A rule that forbids something gets a test that tries it. In the field, 51% of 96 seeds were negative.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>When something changes, see everything it touches.</h2></div>
    <div class="grid grid-3">
      <div class="rule-ink" style="padding-top:20px"><h3>Change Navigator</h3><p class="muted" style="margin-top:10px">Every artifact a change touches, with its next version. The bar is 95% recall: a miss is the failure; an extra is noise a person can discard.</p></div>
      <div class="rule-ink" style="padding-top:20px"><h3>Change plan</h3><p class="muted" style="margin-top:10px">Who is affected and how they'll react: named groups, today's real practice, honest resistance, then training mapped to ADKAR stages with behavioural objectives.</p></div>
      <div class="rule-ink" style="padding-top:20px"><h3>Process Cartographer</h3><p class="muted" style="margin-top:10px">The current process drawn in BPMN 2.0, with layout, so it opens in Signavio, Cloud ALM, Camunda or Visio. Every step carries the requirement and ruling behind it.</p></div>
    </div>
    <p class="note" style="margin-top:40px">Honest about coverage: "We can trace 7 affected artifacts; coverage in P2P is 40%, so there may be more."</p>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head"><h2>Eighteen agents. Three roles. No self-approval.</h2></div>
    <div class="grid grid-3">
      <div class="rule-top"><h3>Authors <span class="muted" style="font-size:.6em">12</span></h3><p class="muted" style="margin-top:10px">Draft the work. Never approve it. Extractor, conflict detector, fit mapper, blueprint assembler, regenerator, test authors, change impact, brand steward.</p></div>
      <div class="rule-top"><h3>Reviewers <span class="muted" style="font-size:.6em">2</span></h3><p class="muted" style="margin-top:10px">Check every draft, on a different model from its author. The auditor confirms each citation supports its claim; the judge rules on quality.</p></div>
      <div class="rule-top"><h3>Readers <span class="muted" style="font-size:.6em">4</span></h3><p class="muted" style="margin-top:10px">Answer from the record. Never write. Aiden, navigator, documentarian, cartographer — every answer carries its citations.</p></div>
    </div>
    <div class="claims" style="margin-top:48px;grid-template-columns:repeat(3,1fr)">
      <div><h4>Model choice is configuration</h4><p>Each agent's provider and model is set in one file, never in code.</p></div>
      <div><h4>Evals on every agent</h4><p>A regression gate runs on any model or prompt change.</p></div>
      <div><h4>Two providers, proven</h4><p>The runtime is trusted only after two vendors pass with real keys.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Fit is measured against a baseline you declare.</h2>
      <p class="lede">Before a theme can be called standard or a gap, Nexora needs to know what standard means here. You declare the slice — platform, edition, release, region and the process areas in scope — and that pinned baseline is what every fit decision is checked against, so "fit to standard" means something specific rather than someone's recollection.</p>
    </div>
    <div class="grid grid-7-5" style="align-items:start">
      <div class="frame"><img src="/assets/img/standards.webp" alt="The standards corpus: declaring a slice by platform, edition, release and region, with the copyright switch set to references only" width="1280" height="630" loading="lazy"></div>
      <div class="claims" style="grid-template-columns:1fr;gap:16px">
        <div><h4>You dictate the scope</h4><p>No baseline is assumed. Nothing is pulled until you declare what belongs in it.</p></div>
        <div><h4>References only, by default</h4><p>The corpus stores scope item IDs, titles, taxonomy and your own embeddings. SAP's copyrighted descriptions are not copied — the safe default, and the one we ship.</p></div>
        <div><h4>Pinned, so fit is reproducible</h4><p>A theme checked last month was checked against the same release it would be checked against today.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap grid grid-5-7" style="align-items:start">
    <div class="stack">
      <h2>Sovereign memory, portable by design.</h2>
      <p class="lede">Every project declares one origin: fresh, inherit or consolidate. Consolidation raises every disagreement as a conflict and never picks a winner by precedence. Read-across stays within one customer — refused in code, and again by the database.</p>
    </div>
    <table class="plain ids">
      <thead><tr><th>Export</th><th>What it is</th></tr></thead>
      <tbody>
        <tr><td>events.jsonl</td><td>Append-only log, the source of truth</td></tr>
        <tr><td>graph.jsonld</td><td>Nodes and edges, regenerable</td></tr>
        <tr><td>manifest.json</td><td>Counts and round-trip proof</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="section on-seal">
  <div class="wrap">
    <h2>Nothing asserted that cannot be cited.</h2>
    <div class="claims" style="margin-top:40px;color:#fff">
      <div style="border-top-color:rgba(255,255,255,.2)"><h4>Citation check</h4><p style="color:rgba(255,255,255,.8)">Confirms the cited passage actually supports the claim before it is promoted.</p></div>
      <div style="border-top-color:rgba(255,255,255,.2)"><h4>Format steward</h4><p style="color:rgba(255,255,255,.8)">Restyles form only, with meaning guarded. Client-facing output needs a person.</p></div>
      <div style="border-top-color:rgba(255,255,255,.2)"><h4>Test evaluator</h4><p style="color:rgba(255,255,255,.8)">Turns results into coverage-weighted maturity and flags anomalies for sign-off.</p></div>
      <div style="border-top-color:rgba(255,255,255,.2)"><h4>Value manifest</h4><p style="color:rgba(255,255,255,.8)">Each value claim is measured from the record or attributed to who said it. Unbacked claims are refused; AI spend is reported against value.</p></div>
    </div>
  </div>
</section>
"""


deliverables = """
<section class="page-head">
  <div class="wrap">
    <h1>Deliverables that write themselves.</h1>
    <p class="lede">Nobody on this program types a deliverable into a template at midnight. The pack is generated from the record, cited to the second — and when a ruling lands, everything downstream of it rebuilds. You don't update documents. You rule, and the documents follow.</p>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head">
      <h2>One sentence, traced all the way down.</h2>
      <p class="lede">Every line in every document carries this lineage. Pick any number in the readout and walk it back to the person who said it.</p>
    </div>
    <ol class="steps six">
      <li><h4>The word</h4><p><em>"Every order over the limit waits for finance."</em> Said in session S-09, at 00:12:48.</p></li>
      <li><h4>The requirement</h4><p>It becomes R-0931, cited to that second. Nobody retyped it, so nobody mistyped it.</p></li>
      <li><h4>The conflict</h4><p>S-04 had said the opposite. C-14 opens on its own, both rooms quoted.</p></li>
      <li><h4>The ruling</h4><p>The order-to-cash owner rules: enforce the limit. Named, dated, round three.</p></li>
      <li><h4>The documents</h4><p>Delta design §4.2, test TC-0412 and the change-impact note rewrite themselves overnight.</p></li>
      <li><h4>The proof</h4><p>Forge builds ZR_CREDITHOLD from §4.2 and files the 18-of-18 test evidence next to it.</p></li>
    </ol>
    <p class="lede" style="margin-top:44px;text-align:center;max-width:none"><strong style="color:var(--on-ink)">Nobody updated a document anywhere in that chain. One ruling — the pack did the rest.</strong></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>You don't fill these in. You receive them.</h2>
      <p class="lede">Six of the documents Nexora writes itself — generated into your house templates, every number derived from the record at build time, rebuilt after every ruling.</p>
    </div>
    <div class="grid grid-3">
      <div class="face"><span class="face-k">Every Monday</span><h3>Explore Readout</h3><p>The steering deck that is never stale: what was ruled this week, what each ruling unblocked, what the program costs now.</p><p class="dsample">72 themes mapped · 7 conflicts open · gate in 72 days</p></div>
      <div class="face"><span class="face-k">From the room</span><h3>Requirements Register</h3><p>4,209 requirements and not one of them typed. Each is a sentence someone said, carrying the second they said it.</p><p class="dsample">R-0931 · S-09 · 00:12:48</p></div>
      <div class="face"><span class="face-k">Ruled, not parked</span><h3>Conflict Register &amp; Decision Log</h3><p>The disagreements the rooms didn't know they had — both positions quoted, each ruled with a name against it.</p><p class="dsample">C-14 · ruled · round 3 · decider: O2C owner</p></div>
      <div class="face"><span class="face-k">Designed from deltas</span><h3>Delta Design Documents</h3><p>Every gap against standard, designed — and every section points back at the requirements that forced it.</p><p class="dsample">§4.2 ← R-0931, R-0612</p></div>
      <div class="face"><span class="face-k">Felt by people</span><h3>Change Impact Analysis</h3><p>Who feels each change, how hard, and the training it demands. It moves the moment scope does.</p><p class="dsample">O2C · 3 roles · 2 courses · 1 SOP</p></div>
      <div class="face"><span class="face-k">Born with the rule</span><h3>Test Scripts</h3><p>Written with the requirement, not after the build. A rule that forbids something gets a test that tries it.</p><p class="dsample">TC-0412 · negative · blocks release</p></div>
    </div>
  </div>
</section>

<section class="section tight">
  <div class="wrap">
    <div class="section-head">
      <h2>And everything else Activate expects.</h2>
      <p class="lede">Eighty deliverables across the six phases. The §-marked ones Nexora generates; the rest it tracks to the same gates, with evidence attached — so the manifest is one view, not three spreadsheets.</p>
    </div>
    <div class="msum">
      <div class="msrow"><span class="n">01</span><span class="nm">Discover</span><span class="ds">Build the case — value, strategy, transition path</span><span class="ct">8 deliverables</span><span class="nx">&nbsp;</span></div>
      <div class="msrow"><span class="n">02</span><span class="nm">Prepare</span><span class="ds">Set up the project — plans, governance, team, systems</span><span class="ct">19 deliverables</span><span class="nx">1 §</span></div>
      <div class="msrow"><span class="n">03</span><span class="nm">Explore</span><span class="ds">Fit-to-Standard — validate processes, capture deltas</span><span class="ct">19 deliverables</span><span class="nx">5 §</span></div>
      <div class="msrow"><span class="n">04</span><span class="nm">Realize</span><span class="ds">Build &amp; test — configure, develop, migrate, test</span><span class="ct">19 deliverables</span><span class="nx">1 §</span></div>
      <div class="msrow"><span class="n">05</span><span class="nm">Deploy</span><span class="ds">Go live — cutover, go/no-go, hypercare</span><span class="ct">9 deliverables</span><span class="nx">&nbsp;</span></div>
      <div class="msrow"><span class="n">06</span><span class="nm">Run</span><span class="ds">Operate &amp; improve — operations, upgrades, adoption</span><span class="ct">6 deliverables</span><span class="nx">&nbsp;</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Your templates, not ours.</h2>
      <p class="lede">Every deliverable is generated into your own house template. The library is company-wide and organised by SAP Activate phase — replace any template and the next build uses it, so what Nexora produces arrives already looking like your firm's work rather than something that has to be reformatted.</p>
    </div>
    <div class="frame"><img src="/assets/img/templates.webp" alt="The template library: 48 templates organised by Activate phase, each with its format and an option to replace it" width="1280" height="630" loading="lazy"></div>
  </div>
</section>

<section class="section">
  <div class="wrap grid grid-5-7" style="align-items:start">
    <div class="stack">
      <h2>Inside a conflict register.</h2>
      <p class="lede">Each contradiction is a page: the question, both positions quoted to the second, a reading, a root-cause hypothesis, the consequence if never ruled, the ruling options — and then the ruling, with a name against it.</p>
    </div>
    <div class="frame" style="padding:28px 32px;font-size:15px;line-height:1.5">
      <div class="mono" style="color:var(--seal)">C-14 · Critical · cross-session</div>
      <h3 style="margin:10px 0 14px;font-size:24px">Is customer credit assessed before an order is released?</h3>
      <div style="border-left:3px solid var(--ink);padding-left:14px;margin-bottom:12px"><em class="italic" style="font-family:var(--display);font-size:17px">"We don't block anything — sales would never accept it."</em><div class="mono" style="color:var(--muted);margin-top:4px">S-04 · Order management · ~41:10 · R-0612</div></div>
      <div style="border-left:3px solid var(--move);padding-left:14px;margin-bottom:16px"><em class="italic" style="font-family:var(--display);font-size:17px">"Every order over the limit waits for finance. That is the policy."</em><div class="mono" style="color:var(--muted);margin-top:4px">S-09 · Finance · 00:12:48 · R-0931</div></div>
      <p class="muted"><strong style="color:var(--ink)">Reading.</strong> A control disagreement, not an as-is difference: one room describes practice, the other policy. Six artifacts wait on it: the credit-management design, two test scenarios, the O2C narrative, a RAID entry and a training objective.</p>
      <p class="muted" style="margin-top:10px"><strong style="color:var(--ink)">Ruling options.</strong> (a) Enforce the limit with a release step. (b) Enforce with a warning and a weekly report. (c) Record the policy as not applied and revisit in Realize.</p>
      <div style="margin-top:16px;padding:12px 14px;background:#F7E1E6;border-radius:10px"><strong>Ruled</strong> — option (a). Decider: process owner, Order to cash. Round 3. Rejected: (b), (c).</div>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head"><h2>A ruling round, end to end.</h2></div>
    <ol class="steps six">
      <li><h4>The team returns its own tracker</h4><p>The conflict tracker, as a spreadsheet, filled in by the people who own the answers.</p></li>
      <li><h4>Nexora diffs it, cell by cell</h4><p>Every changed cell is read against the previous round.</p></li>
      <li><h4>A second agent checks it</h4><p>A second model, not the one that read the cell.</p></li>
      <li><h4>Only settled answers are applied</h4><p>An answer with no name against it is applied but waits for a decider before it can close.</p></li>
      <li><h4>Effects traced downstream</h4><p>Backlog, interfaces, themes, narratives, risks, test seeds, fit evidence.</p></li>
      <li><h4>Every generated deliverable rebuilt, verified, returned</h4><p>Undoable: every prior value is kept.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Every ruling narrows the estimate. You watch it move.</h2></div>
    <div class="est">
      <svg viewBox="0 0 720 300" role="img" aria-label="Estimate in person-days falling across four ruling rounds, with the uncertainty range narrowing">
        <g font-family="JetBrains Mono, monospace" font-size="12" fill="#6B7280">
          <text x="60" y="290" text-anchor="middle">Baseline</text><text x="210" y="290" text-anchor="middle">Round 1</text><text x="360" y="290" text-anchor="middle">Round 2</text><text x="510" y="290" text-anchor="middle">Round 3</text><text x="660" y="290" text-anchor="middle">Round 4</text>
        </g>
        <g stroke="#E5E7EB"><line x1="20" y1="60" x2="700" y2="60"/><line x1="20" y1="150" x2="700" y2="150"/><line x1="20" y1="240" x2="700" y2="240"/></g>
        <g fill="#E7C8D1"><rect x="44" y="30" width="32" height="130" rx="10"/><rect x="194" y="128" width="32" height="56" rx="10"/><rect x="344" y="134" width="32" height="50" rx="10"/><rect x="494" y="186" width="32" height="40" rx="10"/></g>
        <rect x="644" y="228" width="32" height="22" rx="8" fill="#8A1C3B"/>
        <polyline points="60,95 210,156 360,159 510,206 660,239" fill="none" stroke="#0F172A" stroke-width="2"/>
        <g fill="#0F172A"><circle cx="60" cy="95" r="5"/><circle cx="210" cy="156" r="5"/><circle cx="360" cy="159" r="5"/><circle cx="510" cy="206" r="5"/><circle cx="660" cy="239" r="5"/></g>
        <g font-family="Fraunces, serif" font-size="16" fill="#0F172A" text-anchor="middle"><text x="60" y="20">8,525</text><text x="210" y="118">8,217</text><text x="360" y="124">8,206</text><text x="510" y="176">8,093</text><text x="660" y="218" fill="#8A1C3B">7,991</text></g>
      </svg>
      <div class="figures">
        <div><div class="fig">−534</div><p>person-days, as rulings replaced assumptions</p></div>
        <div><div class="fig">±3.4% → ±0.6%</div><p>uncertainty range, as open items closed</p></div>
        <div><div class="fig">68 → 0</div><p>contradictions open, by the board review</p></div>
      </div>
    </div>
  </div>
</section>
"""


contact = f"""
<section class="page-head">
  <div class="wrap">
    <h1>Bring one workshop recording.</h1>
    <p class="lede">We'll show you the record Nexora makes from it, every line cited, on your own data. No slides about what it could do — the thing itself, built from one session you already have.</p>
    <div class="btn-row" style="margin-top:36px"><a class="btn btn-seal" href="mailto:{EMAIL}?subject=One%20workshop%20recording">Email {EMAIL}</a></div>
  </div>
</section>
<section class="section tight">
  <div class="wrap grid grid-3">
    <div class="rule-ink" style="padding-top:20px"><h3>What to bring</h3><p class="muted" style="margin-top:10px">One recording or transcript of a discovery workshop, and whatever documents were in the room.</p></div>
    <div class="rule-ink" style="padding-top:20px"><h3>What you get back</h3><p class="muted" style="margin-top:10px">A cited requirements register, the contradictions inside your own session, and a ruling pack for the first critical one.</p></div>
    <div class="rule-ink" style="padding-top:20px"><h3>How Nexora is delivered</h3><p class="muted" style="margin-top:10px">As a service per engagement, inside your four walls, with Aiden staying on after go-live. Your recordings stay in your Drive.</p></div>
  </div>
</section>
"""


privacy = f"""
<section class="page-head"><div class="wrap"><h1>Privacy.</h1><p class="lede">What this website collects, and what it does not.</p></div></section>
<section class="section tight"><div class="wrap legal">
  <p>This site is a description of Nexora. It does not require an account, set tracking cookies, or collect personal data through forms.</p>
  <h2>Analytics</h2>
  <p>We measure visits with Plausible Analytics, a privacy-focused service that uses no cookies and collects no personal data. Page views are aggregated; your IP address is not stored. There is nothing to opt out of because nothing identifies you.</p>
  <h2>Email</h2>
  <p>If you write to us at <a href="mailto:{EMAIL}">{EMAIL}</a>, we keep your message to reply to it. We do not add you to a mailing list and we do not share your address.</p>
  <h2>Workshop recordings you bring</h2>
  <p>Anything you share for a demonstration is processed inside an environment set up for you, is not used to train models, is not mixed with any other customer's material, and is deleted when you ask.</p>
  <h2>Fonts</h2>
  <p>Typefaces are loaded from Google Fonts, which may log the request. No other third-party scripts run on this site.</p>
  <h2>Changes</h2>
  <p>If any of the above changes, this page changes first.</p>
</div></section>
"""


# ------------------------------------------------------------------ HOME
# One record. Three faces (Brief · Forge · Manage). Three journeys (greenfield · acquisition · upgrade).
HOME = """
<section class="hero hero-q">
  <div class="wrap">
    <span class="kicker">The one-minute test</span>
    <h1>Can your program answer this <span style="white-space:nowrap">in a minute?</span></h1>
    <div class="qcycle" aria-label="Questions a running SAP program should be able to answer">
      <div class="qc"><span>lookup</span><q>Why does billing work this way?</q></div>
      <div class="qc"><span>from code</span><q>What does ZORD_HOLD actually do today?</q></div>
      <div class="qc"><span>memory</span><q>What rule is hiding in that 2009 user exit?</q></div>
      <div class="qc"><span>impact</span><q>If I change this requirement, what code breaks?</q></div>
      <div class="qc"><span>build</span><q>How fast can a signed spec become tested code?</q></div>
      <div class="qc"><span>evidence</span><q>Which deliverables have no approval evidence?</q></div>
      <div class="qc"><span>as-of</span><q>What did we believe in March that is no longer true?</q></div>
      <div class="qc"><span>training</span><q>What did the last fifty builds teach the next one?</q></div>
    </div>
    <p class="lede"><strong class="can">Nexora can.</strong> It listens to your workshops, reads your code and runs your program from one record — so every answer arrives with the session, the line and the second it came from.</p>
    <div class="btn-row">
      <a class="btn btn-seal" href="/contact/">Bring one workshop recording</a>
      <a class="btn btn-ghost" href="/how-it-works/">See how it works</a>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(64px,8vw,112px)">
    <div class="section-head">
      <h2>One record of your SAP program.</h2>
      <p class="lede">Read from the room, read from the system, kept for life. Agents produce; humans approve. Every requirement, every line of code and every task traces back to the words someone said.</p>
    </div>
    <div class="spine" aria-label="The three faces of the Nexora record">
      <a class="face" href="/brief/">
        <span class="face-k">Reads the room</span>
        <h3>The Brief</h3>
        <p>Workshops in. Cited requirements, ruled contradictions and a signed blueprint out. Aiden answers from it.</p>
      </a>
      <div class="spine-core">
        <img src="/assets/brand/logo-reversed.svg" alt="" width="180" height="41">
        <div class="core-h">The record</div>
        <p>Append-only. Every object typed, cited, confirmed by a named person. Nothing crosses customers.</p>
      </div>
      <a class="face" href="/forge/">
        <span class="face-k">Reads the system</span>
        <h3>Forge</h3>
        <p><b>Reads</b> your landscape from the code. <b>Builds</b> from signed specs. <b>Tests</b> with evidence a change board accepts. <b>Trains</b> on every proven build.</p>
      </a>
      <a class="face face-wide" href="/manage/">
        <span class="face-k">Runs the program</span>
        <h3>Manage</h3>
        <p>The plan and its gates, the delivery plan, the work and who answers for each area. Read straight from the record, so Manage and Governance can never disagree.</p>
      </a>
    </div>
    <div class="frame bleed"><img src="/assets/img/brief-live.webp" alt="The Brief, live: the program's front page leading with the one ruling that matters today" width="1280" height="623" loading="eager" fetchpriority="high"></div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head">
      <h2>Why one record, and not three tools.</h2>
      <p class="lede">A ruling made in a workshop is the reason a line of code exists, and the reason a task closes. When the three live in one place, nothing has to be reconciled.</p>
    </div>
    <ol class="thread" aria-label="One decision travelling through the record">
      <li><span class="id">S-07 · 00:23:15</span><b>Said in the room</b><q>Customs asks for origin on every line.</q><span>Logistics lead, workshop seven.</span></li>
      <li><span class="id">R-0132 → DC-04</span><b>Ruled in the Brief</b><span>Batches carry origin. Process owner, round 3, options rejected recorded.</span></li>
      <li><span class="id">BS-12 → TS-12 → code</span><b>Built and proved</b><span>Clean-core class built from the section, 18 of 18 unit tests, screenshots attached.</span></li>
      <li><span class="id">T-118 · Health</span><b>Tracked in Manage</b><span>Task closed by the owner. Explore gate shows no open critical conflict in Logistics.</span></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Three ways programs arrive. One way they're kept.</h2>
    </div>
    <div class="journeys">
      <article>
        <span class="jk">Greenfield</span>
        <h3>No SAP yet.</h3>
        <p>The Brief runs discovery: workshops become cited requirements, contradictions get ruled, the specifications are signed. Forge turns them into tested, evidenced code.</p>
        <div class="jflow"><span>Brief</span><i></i><span>Specs</span><i></i><span>Build</span><i></i><span>Train</span></div>
      </article>
      <article>
        <span class="jk">Acquisition</span>
        <h3>Fit into the parent.</h3>
        <p>The acquired business goes through the Brief. Forge reads the parent's landscape, so the fit is decided against what the parent actually runs, not what people recall.</p>
        <div class="jflow"><span>Brief</span><i></i><span>Parent system</span><i></i><span>Fit</span></div>
      </article>
      <article>
        <span class="jk">Upgrade</span>
        <h3>ECC to S/4HANA.</h3>
        <p>Forge reads the current system, measures every custom object against S/4HANA and rebuilds what has to move. Where the process changes too, the Brief rules first.</p>
        <div class="jflow"><span>Scan</span><i></i><span>Build</span><i></i><span>Prove</span></div>
      </article>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head"><h2>You trigger. They produce. You approve.</h2></div>
    <div class="model">
      <div><span class="who">You</span><h3>Trigger</h3><p>Commission work from the Desk: ingest a session, scan a system, assemble the blueprint, modernize a class. Nothing runs by itself.</p></div>
      <div><span class="who">The agents</span><h3>Produce</h3><p>Specialist agents draft the work — extraction, fit, code, tests. A second agent, on a different model, reviews every draft before you see it.</p></div>
      <div><span class="who">You</span><h3>Approve</h3><p>A named person rules, signs, activates or commits. Only then does a draft cross the Gatekeeper and become memory.</p></div>
    </div>
    <div class="claims" style="margin-top:40px">
      <div><h4>No agent approves its own work</h4><p>Author, reviewer and approver are always different, and on different models where it matters.</p></div>
      <div><h4>Four human gates, only four</h4><p>Expert ruling, blueprint sign-off, regeneration commit, comms delivery. Everything else is machine work surfaced for a person.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid grid-5-7">
    <div class="stack">
      <h2>Ask the record. Get the receipt.</h2>
      <p class="lede">Aiden answers any question about the program — a ruling, a line of code, an overdue task — and cites the session, the object and the second. Aiden reads the record; it never writes to it.</p>
      <p><a class="btn btn-primary" href="/brief/#aiden">Meet Aiden</a></p>
    </div>
    {AIDEN}
  </div>
</section>

<section class="section on-seal">
  <div class="wrap">
    <div class="section-head">
      <h2>Proven in the field.</h2>
      <p class="lede">Nexora runs live on S/4HANA programs today. Three engagements, with every figure drawn from the delivered record.</p>
    </div>
    <div class="stories" style="color:#fff">
      <article style="border-top-color:#fff">
        <span class="sector" style="color:#F4A7B9">High-tech manufacturing · acquisition</span>
        <h3>From eighteen workshops to a signed blueprint</h3>
        <dl><dt>18</dt><dd>discovery workshops, two weeks on site</dd><dt>4,600</dt><dd>statements captured, each cited to its source</dd><dt>61 / 61</dt><dd>contradictions found and settled by their owners</dd><dt>7</dt><dd>ruling rounds; the generated deliverables rebuilt after each</dd></dl>
        <p style="color:rgba(255,255,255,.78)">Acquired entity moving onto the parent's S/4HANA. Nine days from first deliverable set to a board-ready verdict.</p>
      </article>
      <article style="border-top-color:#fff">
        <span class="sector" style="color:#F4A7B9">Consumer goods · greenfield</span>
        <h3>An RFP pack read before the first workshop</h3>
        <dl><dt>4</dt><dd>recorded review sessions and 26 documents</dd><dt>1,500</dt><dd>requirements extracted and cited, pre-kickoff</dd><dt>58</dt><dd>contradictions inside the customer's own pack</dd><dt>49</dt><dd>interfaces inventoried, 45 L3 processes scoped</dd></dl>
        <p style="color:rgba(255,255,255,.78)">The program was re-planned from the customer's own requirements. The estimate narrowed with every ruling.</p>
      </article>
      <article style="border-top-color:#fff">
        <span class="sector" style="color:#F4A7B9">Retail and distribution · upgrade</span>
        <h3>Legacy code read into the same record</h3>
        <dl><dt>400+</dt><dd>custom objects scanned and documented</dd><dt>230</dt><dd>legacy-sourced requirements fed to the As-Is</dd><dt>85%</dt><dd>S/4HANA readiness, measured not estimated</dd><dt>DEV→PRD</dt><dd>clean-core code transported with its trace</dd></dl>
        <p style="color:rgba(255,255,255,.78)">Undocumented custom code became business facts; the blueprint became clean-core code, traceable line by line.</p>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Built to be believed.</h2></div>
    <div class="grid grid-7-5" style="align-items:start">
      <div class="claims">
        <div><h4>Machines propose</h4><p>Only a named person turns a draft into memory.</p></div>
        <div><h4>Models check models</h4><p>Author and reviewer run on different models.</p></div>
        <div><h4>Rulings are never edited</h4><p>A change is a new ruling; the old one stays readable.</p></div>
        <div><h4>Signed means signed</h4><p>The signed blueprint stays retrievable byte for byte.</p></div>
        <div><h4>Uncertainty is stated</h4><p>Approximate times carry a ~. Thin coverage is labelled thin.</p></div>
        <div><h4>Weak citations flagged</h4><p>A claim its source does not support is marked, never hidden.</p></div>
      </div>
      <div class="on-ink" style="border-radius:16px;padding:32px 30px">
        <h3 style="margin-bottom:18px">Sovereign by design</h3>
        <div class="stack" style="--s:12px;color:var(--on-ink-mute)">
          <p>Runs inside your own environment.</p>
          <p>Original recordings stay in your Drive. Your code stays in your systems; Forge reads it over MCP.</p>
          <p>Nothing crosses between customers: not content, not patterns, not statistics. Refused in code, and again by the database.</p>
          <p>The memory exports as open JSONL and JSON-LD, readable without Nexora.</p>
          <p>Model choice is configuration, never code.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head"><h2>Start in Explore. Keep it for the life of the system.</h2></div>
    <div class="grid grid-3">
      <div class="rule-top"><h3>Explore</h3><p class="muted" style="margin-top:10px">The Brief turns workshops into a cited register, ruled contradictions and a signed blueprint. Forge reads what you run today. Manage sets the plan and the gates.</p></div>
      <div class="rule-top"><h3>Realize</h3><p class="muted" style="margin-top:10px">Forge turns the signed design into code, proves it with evidence a change board accepts, and records the journey as training.</p></div>
      <div class="rule-top"><h3>Run</h3><p class="muted" style="margin-top:10px">Aiden answers why the system works the way it does, long after the project team has gone. The next project can inherit the memory, within your company only.</p></div>
    </div>
  </div>
</section>

<section class="section on-seal">
  <div class="wrap" style="text-align:center">
    <h2 style="max-width:none">See your own program in the record.</h2>
    <p class="lede" style="margin:16px auto 0;max-width:62ch">One workshop recording is enough. We'll return the record Nexora makes from it — every requirement cited to the second, on your own data, inside your own walls.</p>
    <div class="btn-row" style="justify-content:center;margin-top:30px">
      <a class="btn" style="background:#fff;color:var(--seal)" href="mailto:{EMAIL}?subject=One%20workshop%20recording">Email us</a>
      <a class="btn" style="border-color:rgba(255,255,255,.35);color:#fff" href="/how-it-works/">See how it works</a>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------ BRIEF
BRIEF = """
<section class="page-head">
  <div class="wrap">
    <span class="kicker">The Brief</span>
    <h1>Every word heard. Every decision kept.</h1>
    <p class="lede">The Brief is the process side of Nexora. It reads your discovery workshops, extracts requirements cited to the second, finds the contradictions between rooms, takes each one to the person who owns the answer, and assembles the signed blueprint that everything downstream is derived from.</p>
  </div>
</section>

<section class="section tight">
  <div class="wrap">
    <div class="frame"><img src="/assets/img/brief-live.webp" alt="The Brief: the program's front page, leading with the one ruling that matters today" width="1280" height="623" loading="eager" fetchpriority="high"></div>
    <div class="frame-cap"><span>The Brief, live. The first ruling of the day, with the words behind it and the timestamp.</span><span>81 rulings waiting · 4,209 requirements captured · 72 fit themes mapped</span></div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head"><h2>From a room full of people to a record you can sign.</h2></div>
    <ol class="steps">
      <li><h4>Listen</h4><p>Recordings and documents in, from your own Drive. Originals never leave it.</p></li>
      <li><h4>Extract</h4><p>Atomic requirements, each cited to the second. Uncited is invalid.</p></li>
      <li><h4>Contradict</h4><p>Disagreements found across sessions, both positions quoted to the second.</p></li>
      <li class="gate"><h4>Rule</h4><p>A named expert decides. The ruling binds, and records what it rejected.</p></li>
      <li class="gate"><h4>Sign</h4><p>A blueprint assembled from rulings. Immutable once signed.</p></li>
      <li><h4>Derive</h4><p>Specs, tests, change impact, training and BPMN, all from the signed design.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap grid grid-5-7" style="align-items:start">
    <div class="stack">
      <h2>One page each morning: what needs you.</h2>
      <p class="lede">The program's front page leads with the one decision that matters today, quotes the words behind it with the timestamp, and says how many artifacts wait on it.</p>
      <div class="claims" style="grid-template-columns:1fr;gap:18px">
        <div><h4>The Situation</h4><p>Rulings waiting, deliverables ready, AI spend against value delivered.</p></div>
        <div><h4>The Queue</h4><p>Ranked by what each ruling unblocks, not by when it arrived.</p></div>
        <div><h4>What Moved</h4><p>Every entry carries its receipt.</p></div>
        <div><h4>The Manifest</h4><p>Every deliverable SAP Activate expects — 80 across six phases — and where each one stands.</p></div>
      </div>
    </div>
    <div class="frame"><img src="/assets/img/brief-demo.webp" alt="The Brief on the demo record: a revenue-recognition ruling holding twelve artifacts" width="1280" height="800" loading="lazy"></div>
  </div>
</section>

<section class="section on-ink" id="aiden">
  <div class="wrap">
    <div class="grid grid-5-7" style="align-items:start">
      <div class="stack">
        <span class="kicker">Aiden</span>
        <h2>The one who read everything, and remembers who said it.</h2>
        <p class="lede">Aiden is Nexora's reader. Ask it anything about the program — what is waiting on you, where a decision came from, what breaks if you re-rule C-05, what the legacy system actually does today — and it answers from the record, with the ruling, the session and the second attached.</p>
        <div class="claims" style="grid-template-columns:1fr;gap:18px;margin-top:8px">
          <div><h4>Reads, never writes</h4><p>Aiden cannot add a fact, correct a ruling or infer a decision. The record changes only through the four human gates.</p></div>
          <div><h4>Every answer cites</h4><p>Decision, session and evidence chips under every claim. Open the citation before you act on an answer.</p></div>
          <div><h4>Two scopes</h4><p><strong>Record</strong> answers from confirmed memory. <strong>As-Is</strong> answers only from what Forge read out of the running system — what exists today, nothing to-be.</p></div>
          <div><h4>Cost in the open</h4><p>Requests and spend are metered per day and shown to the person asking.</p></div>
        </div>
      </div>
      {AIDEN}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid-7-5" style="align-items:start">
      <div class="frame"><img src="/assets/img/desk-demo.webp" alt="The Desk: produce, prove and remember commissions, each naming its reviewer and approver" width="1280" height="794" loading="lazy"></div>
      <div class="stack">
        <h2>The Desk. Everything you can ask for.</h2>
        <p class="lede">Every line is something you commission. Each has a reviewer, and each ends with a person.</p>
        <div class="grid grid-3" style="gap:24px;font-size:15px">
          <div class="rule-top"><h4>Produce</h4><p class="muted">Ingest a session · Extract requirements · Find contradictions · Map fit · Assemble the blueprint</p></div>
          <div class="rule-top"><h4>Prove</h4><p class="muted">Draft the test plan · Draft scenarios and cases · Evaluate results · Draft the change plan · Build a ruling pack</p></div>
          <div class="rule-top"><h4>Remember</h4><p class="muted">Ask the record · Trace a change · Document the process · Draw it in BPMN 2.0 · Export the memory as JSONL</p></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section on-seal">
  <div class="wrap grid grid-7-5">
    <div>
      <h2>The Brief hands Forge its specifications, and Manage its gates.</h2>
      <p class="lede" style="margin-top:16px">A signed section becomes the specification Forge builds from, with acceptance criteria cited back to the room. An open critical conflict is what keeps a Manage gate shut. Same record, three faces.</p>
    </div>
    <div class="btn-row" style="justify-content:flex-end;gap:12px"><a class="btn btn-ghost" style="border-color:rgba(255,255,255,.4);color:#fff" href="/forge/">Forge</a><a class="btn btn-ghost" style="border-color:rgba(255,255,255,.4);color:#fff" href="/manage/">Manage</a></div>
  </div>
</section>
"""

# ------------------------------------------------------------------ FORGE
FORGE = """
<section class="page-head">
  <div class="wrap">
    <span class="kicker">Forge</span>
    <h1>Read the system. Build what was asked for. Prove it works.</h1>
    <p class="lede">Forge is the code side of Nexora. It connects to your SAP landscape, reads what actually runs, recovers the business process from the code, turns signed specifications into working ABAP, proves the result with evidence you can hand to a change board, and records the finished journey so your users can learn it. Six stages, each one ending with a person.</p>
  </div>
</section>

<section class="section tight">
  <div class="wrap">
    <ol class="stages" aria-label="The six stages of Forge">
      <li><a href="#connect"><span class="sk">01 · Connect</span><h3>Systems</h3><p>Source read-only, target write-enabled, production refused on sight.</p></a></li>
      <li><a href="#scan"><span class="sk">02 · Scan</span><h3>Land</h3><p>Every custom object measured: what blocks the move, what nobody runs.</p></a></li>
      <li><a href="#map"><span class="sk">03 · Understand</span><h3>Map</h3><p>The business process recovered from the code, confirmed by its owners.</p></a></li>
      <li><a href="#build"><span class="sk">04 · Create</span><h3>Build</h3><p>Signed specification in, clean-core code out, always on a transport.</p></a></li>
      <li><a href="#proof"><span class="sk">05 · Evidence</span><h3>Proof</h3><p>Criteria, tests, screenshots — a runbook for the change board.</p></a></li>
      <li><a href="#learn"><span class="sk">06 · Train</span><h3>Learn</h3><p>The finished journey recorded in the live system, for your users.</p></a></li>
    </ol>
  </div>
</section>

<section class="section on-ink" id="connect">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">01 · Connect</span>
      <h2>Your production system is never on the table.</h2>
      <p class="lede">Forge reads from one system and builds into another. The source is opened read-only — it reads code, where-used and change history, and cannot write. The target takes clean-core code into a single package, always onto a transport. Any system that reports itself as production is refused on sight.</p>
    </div>
    <div class="grid grid-7-5" style="align-items:start">
      <div class="frame"><img src="/assets/img/forge-connect.webp" alt="Forge stage one: ECC source connected read-only and S/4HANA target write-enabled, both verified non-production" width="1280" height="623" loading="eager" fetchpriority="high"></div>
      <div class="claims" style="grid-template-columns:1fr;gap:16px">
        <div><h4>Read-only at the source</h4><p>Forge reads your ECC system. It has no write path to it at all.</p></div>
        <div><h4>One package, always on a transport</h4><p>Everything Forge writes to the target lands in one named package and moves through your own transport process.</p></div>
        <div><h4>Models are opt-in, per project</h4><p>Landing and scanning need no model whatsoever. Mapping and building do, so it stays off until you decide — and when it is on, two providers are compared and the run is recorded in the project log.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="scan">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">02 · Scan</span>
      <h2>412 custom objects. 138 haven't run in a year, and 5 will stop your move.</h2>
      <p class="lede">Forge lands on the system and measures every custom object: how ready it is for S/4HANA, what it blocks, how often it runs, how much it has changed. Two of the five blockers in this landscape had not run in a year — retiring them is cheaper than fixing them, and you only know that because the usage was measured.</p>
    </div>
    <div class="frame"><img src="/assets/img/forge-scan.webp" alt="Forge stage two: clean-core readiness, blocking objects, change rate and database growth, with a readiness heat map by process area" width="1280" height="623" loading="lazy"></div>
    <div class="figures" style="margin-top:48px">
      <div><div class="fig">85<small>%</small></div><p>clean-core readiness, from ATC findings on scanned code</p></div>
      <div><div class="fig">5</div><p>P1 findings that block S/4HANA, named object by object</p></div>
      <div><div class="fig">171</div><p>objects changed in twelve months, a quarter of the landscape</p></div>
    </div>
  </div>
</section>

<section class="section on-ink" id="map">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">03 · Understand</span>
      <h2>How your business actually runs, read out of the code.</h2>
      <p class="lede">Forge groups what it scanned into the processes they implement — order entry to billing, standard steps beside the custom ones and the enhancements. You can see the As-Is, the To-Be and the delta between them. None of it is the record until the people who own the process confirm it.</p>
    </div>
    <div class="grid grid-5-7" style="align-items:start">
      <div class="claims" style="grid-template-columns:1fr;gap:16px">
        <div><h4>Standard, custom, enhancement</h4><p>Every step is labelled for what it is, with the object behind it named.</p></div>
        <div><h4>Why it is here</h4><p>Select a step and see the code, the usage, and the words behind it.</p></div>
        <div><h4>Confirmed, not asserted</h4><p>The owner confirms each step. Until then it is a proposal, however confident the machine was.</p></div>
      </div>
      <div class="frame"><img src="/assets/img/forge-map.webp" alt="Forge stage three: order-to-cash recovered from code, each step labelled standard, custom or enhancement, with As-Is, To-Be and Delta views" width="1280" height="623" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section" id="build">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">04 · Create</span>
      <h2>From words to working code.</h2>
      <p class="lede">A signed blueprint section becomes a specification with numbered acceptance criteria, each cited back to the session and second where it was asked for. Forge builds against that specification, checks its own work, and stops at your approval.</p>
    </div>
    <div class="frame"><img src="/assets/img/forge-build.webp" alt="Forge stage four: the specification with numbered acceptance criteria beside the generated CDS view, with the citation chain beneath" width="1280" height="623" loading="lazy"></div>
    <div class="claims" style="margin-top:48px;grid-template-columns:repeat(3,1fr)">
      <div><h4>The spec names what was asked</h4><p>Four criteria, each traced through requirement, ruling and blueprint section to the sentence someone said.</p></div>
      <div><h4>Built from the delta</h4><p>Work orders come from what changed — new from spec, and what already exists in code.</p></div>
      <div><h4>It stops at your approval</h4><p>Write access is scoped to one system, one package, and nothing activates without a person.</p></div>
    </div>
  </div>
</section>

<section class="section on-seal" id="proof">
  <div class="wrap">
    <div class="section-head">
      <h2>Evidence, not assurance.</h2>
      <p class="lede">What Forge did, in order, with the screenshots to show it. The failures stay in. Anyone can claim a green test run; Forge runs its tests against a deliberately broken build to prove they can fail — 18 of 18 caught it.</p>
    </div>
    <div class="frame"><img src="/assets/img/forge-proof.webp" alt="Forge stage five: acceptance criteria, ABAP unit results, UI scenarios and content-hashed screenshots, with a runbook to export" width="1280" height="623" loading="lazy"></div>
    <div class="figures" style="margin-top:48px;color:#fff">
      <div style="border-top-color:rgba(255,255,255,.3)"><div class="fig">4 of 4</div><p>acceptance criteria, each mapped to a test</p></div>
      <div style="border-top-color:rgba(255,255,255,.3)"><div class="fig">18 of 18</div><p>ABAP unit tests at 91% statement coverage</p></div>
      <div style="border-top-color:rgba(255,255,255,.3)"><div class="fig">4</div><p>screenshots of the run, each content-hashed</p></div>
    </div>
    <div class="claims" style="margin-top:40px;color:#fff">
      <div style="border-top-color:rgba(255,255,255,.2)"><h4>The runbook exports as a PDF</h4><p style="color:rgba(255,255,255,.8)">Every step Forge took, timestamped, ready to hand to the change board as it stands.</p></div>
      <div style="border-top-color:rgba(255,255,255,.2)"><h4>Masked data, attested</h4><p style="color:rgba(255,255,255,.8)">Tests run on masked development data only, and the customer attests to it.</p></div>
    </div>
  </div>
</section>

<section class="section" id="learn">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">06 · Train</span>
      <h2>See how it actually works.</h2>
      <p class="lede">After the build is tested, Forge records the end-to-end journey once in the live system. New users walk through it — the final process, step by step, exactly as it runs in SAP, with the real screens rather than a slide about them. Training stops being a document written months before go-live and becomes a recording of the system you actually built.</p>
    </div>
    <div class="frame"><img src="/assets/img/forge-learn.webp" alt="Forge stage six: a seven-step order-to-cash training journey beside the live SAP Fiori screen for each step" width="1280" height="623" loading="lazy"></div>
    <div class="claims" style="margin-top:48px;grid-template-columns:repeat(3,1fr)">
      <div><h4>Recorded from the real system</h4><p>Each step shows the actual transaction or Fiori app, on masked data.</p></div>
      <div><h4>Published, with a version</h4><p>Trainees see only the journey. Re-curate it when the process changes.</p></div>
      <div><h4>The same record underneath</h4><p>The training follows the process that was signed, so it cannot drift from the design.</p></div>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap grid grid-7-5">
    <div>
      <h2>Forge is a face of the record, not a separate tool.</h2>
      <p class="lede" style="margin-top:16px">The Brief rules on the process; Forge builds and proves the code; Manage tracks the work and the gates. A ruling made in Explore is the reason a line of code exists in Realize — and the reason a trainee sees the screen they see.</p>
    </div>
    <div class="btn-row" style="justify-content:flex-end"><a class="btn btn-primary" href="/contact/">Bring one workshop recording</a></div>
  </div>
</section>
"""

# ------------------------------------------------------------------ MANAGE
MANAGE = """
<section class="page-head">
  <div class="wrap">
    <span class="kicker">Manage</span>
    <h1>Run the program from the record it is built on.</h1>
    <p class="lede">Manage is the project side of Nexora: the plan and its quality gates, the delivery plan with its people and cost, the work the team owns, and who is accountable for each process area. Nothing here is a second source of truth — critical conflicts and deliverable sign-off are read straight from the record, so what Manage shows and what Governance holds can never disagree.</p>
  </div>
</section>

<section class="section tight">
  <div class="wrap">
    <div class="frame"><img src="/assets/img/manage-plan.webp" alt="Manage, Plan: the Explore quality gate counting down, with critical conflicts, gates and overdue tasks, above a phase board" width="1280" height="623" loading="eager" fetchpriority="high"></div>
    <div class="frame-cap"><span>The plan leads with the next gate and what stands between you and it.</span><span>7 critical conflicts open · gates on track · 2 overdue</span></div>
  </div>
</section>

<section class="section on-seal">
  <div class="wrap">
    <div class="section-head">
      <h2>One platform. Many programs. Nothing shared between them.</h2>
      <p class="lede">Above the single program sits the portfolio: every project you run, grouped by the customer it belongs to, each with its own members, its own Drive and its own record. A project is sovereign — complete on its own, exportable, readable without Nexora. Read-across happens within one customer and never between them.</p>
    </div>
    <div class="grid grid-2" style="align-items:start">
      <div>
        <div class="frame"><img src="/assets/img/portfolio.webp" alt="The portfolio: projects grouped by customer, each with settings, members and Drive" width="1280" height="623" loading="lazy"></div>
        <h4 style="margin-top:20px;color:#fff">Projects, by customer</h4>
        <p style="margin-top:6px;color:rgba(255,255,255,.8)">Each project declares one origin when it is created — fresh, inherit or consolidate — and that origin is immutable from then on, so no memory arrives without a stated provenance.</p>
      </div>
      <div>
        <div class="frame"><img src="/assets/img/platform-metrics.webp" alt="Instance metrics: projects, customers, agent runs, spend, error rate and latency, broken down by project, customer and model" width="1280" height="630" loading="lazy"></div>
        <h4 style="margin-top:20px;color:#fff">What it ran, and what it cost</h4>
        <p style="margin-top:6px;color:rgba(255,255,255,.8)">Agent runs, failures, latency and spend — per project, per customer and per model. The bill is never a mystery, and neither is which model did the work.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Every area has its judge.</h2>
      <p class="lede">A program is only as decisive as its ownership. Each business domain has exactly one owner — a process expert whose ruling on that area's conflicts is binding — and Nexora will tell you how many of your areas actually have one. Ownership is date-delimited, so a handover is recorded rather than overwritten, and you can read the tenure history long after the person has moved on.</p>
    </div>
    <div class="frame"><img src="/assets/img/process-areas.webp" alt="Process areas: each domain owned, with owner, tenure start, and hand over, end tenure and history actions" width="1280" height="623" loading="lazy"></div>
    <div class="claims" style="margin-top:48px;grid-template-columns:repeat(3,1fr)">
      <div><h4>Proposed from the record</h4><p>Nexora reads the areas already tagged in the record and proposes them; a human still activates each one.</p></div>
      <div><h4>Hand over, don't overwrite</h4><p>Ending one tenure and starting another is an event in the record, with both sets of dates kept.</p></div>
      <div><h4>Unowned means unrulable</h4><p>An area with no owner cannot have its conflicts ruled, which is why the count of owned areas is shown up front.</p></div>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap">
    <div class="section-head">
      <h2>A date is not a plan. The gate is.</h2>
      <p class="lede">Every phase ends in a quality gate, and a gate opens when the record says it can. The countdown is honest because the thing it counts down to is checked against open conflicts and signed deliverables, not against a status someone typed in a meeting.</p>
    </div>
    <div class="claims">
      <div><h4>Phases you can see at once</h4><p>Discover through Run, each with its milestones, owners and dates. The current phase is marked.</p></div>
      <div><h4>Gates read from Governance</h4><p>Critical conflicts and deliverable sign-off are never recomputed here — they come from the record.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>The plan holds — except the ABAP lead at 120% in Realize.</h2>
      <p class="lede">The delivery plan is one model, not a stack of spreadsheets. Effort, cost, duration and loading all derive from the same resource profiles, so changing an allocation moves every figure together — and an over-allocated person is a headline rather than a cell you had to go looking for.</p>
    </div>
    <div class="frame"><img src="/assets/img/manage-delivery.webp" alt="Manage, Delivery Plan: total effort, plan cost, duration and peak loading above a workstream timeline" width="1280" height="623" loading="lazy"></div>
    <div class="figures" style="margin-top:48px">
      <div><div class="fig">5,200</div><p>person-days, derived from the resource profiles</p></div>
      <div><div class="fig">17</div><p>months across five SAP Activate phases</p></div>
      <div><div class="fig">19.7</div><p>concurrent FTE at peak loading, in Realize</p></div>
    </div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap grid grid-7-5" style="align-items:start">
    <div class="frame"><img src="/assets/img/manage-people.webp" alt="Manage, the people view: each resource shown by initials and role with allocation per phase" width="1280" height="623" loading="lazy"></div>
    <div class="stack">
      <h2>The work and the people, from one model.</h2>
      <p class="lede">Look at the plan by workstream or by person. Allocation is coloured by utilization, effort and cost are derived per row, and Forge (Code) sits in the plan as a workstream like any other — because generated code still has to be reviewed, tested and transported by someone.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Needs someone, before to-do.</h2>
      <p class="lede">The work list opens with what is stuck and how late it is — not a flat backlog you have to read to the bottom of. These are working rows, not the record: tasks, not rulings. Each one names an owner and a process area, so "who is blocking this" is answered on the page.</p>
    </div>
    <div class="frame"><img src="/assets/img/manage-work.webp" alt="Manage, Work: a Needs Someone section with overdue items above the to-do list" width="1280" height="623" loading="lazy"></div>
  </div>
</section>

<section class="section on-ink">
  <div class="wrap grid grid-5-7" style="align-items:start">
    <div class="stack">
      <h2>Exactly one person answers for each area.</h2>
      <p class="lede">The owner rules the area's conflicts; the Accountable answers for its delivery — exactly one per area. Owners seed as Accountable and every other cell is a deliberate call, not a default. Ownership is date-delimited, so a handover is recorded rather than overwritten.</p>
      <p class="note">An unowned area cannot have its conflicts ruled, which means its gate cannot open. The RACI is not paperwork here; it is what makes the record able to move.</p>
    </div>
    <div class="frame"><img src="/assets/img/manage-team.webp" alt="Manage, Team: a RACI grid across process areas with responsible, accountable, consulted and informed" width="1280" height="623" loading="lazy"></div>
  </div>
</section>

<section class="section on-seal">
  <div class="wrap grid grid-7-5">
    <div>
      <h2>Why a gate stays shut is never a mystery.</h2>
      <p class="lede" style="margin-top:16px">The Explore gate reads the open critical conflicts from the Brief. The Realize gate reads the readiness gate from Forge. Manage shows the state; the record holds the reason.</p>
    </div>
    <div class="btn-row" style="justify-content:flex-end;gap:12px"><a class="btn btn-ghost" style="border-color:rgba(255,255,255,.4);color:#fff" href="/brief/">The Brief</a><a class="btn btn-ghost" style="border-color:rgba(255,255,255,.4);color:#fff" href="/forge/">Forge</a></div>
  </div>
</section>
"""


if __name__ == "__main__":
    def fill(s): return s.replace("{AIDEN}", AIDEN).replace("{EMAIL}", EMAIL)
    page("/", "Nexora — One record of your SAP program",
         "Read from the room, read from the system, kept for life. The Brief, Forge and Manage over one record. Agents produce. Humans approve.", fill(HOME))
    page("/brief/", "The Brief — Nexora",
         "Workshops in. Cited requirements, ruled contradictions and a signed blueprint out. Aiden answers from the record.", fill(BRIEF))
    page("/forge/", "Forge — Nexora",
         "Read the landscape from the code, build from specifications, modernize ECC to S/4HANA. Tested, transported, traceable.", fill(FORGE))
    page("/manage/", "Manage — Nexora",
         "Plan, resources, tasks, RAID, process areas, team and RACI, health — read from the same record.", fill(MANAGE))
    page("/how-it-works/", "How it works — Nexora",
         "The record, the pipeline, the four human gates and the controls. Nothing becomes memory until a person says so.", fill(how))
    page("/deliverables/", "Deliverables — Nexora",
         "Every deliverable SAP Activate expects, phase by phase — generated or tracked from one record, rebuilt after every ruling.", fill(deliverables))
    page("/contact/", "Contact — Nexora",
         "Bring one workshop recording. We'll show you the record Nexora makes from it.", contact)
    page("/privacy/", "Privacy — Nexora", "What this website collects, and what it does not.", privacy)
    print("fingerprinted", fingerprint(), "assets")
