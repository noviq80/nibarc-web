#!/usr/bin/env python3
"""Builds the Nibarc company site at the domain root. Nexora keeps /nexora/."""
import pathlib, re, hashlib

OUT    = pathlib.Path(__file__).resolve().parent.parent / "site"
EMAIL  = "info@nibarc.com"
PHONE  = "+1 (484) 212-5757"
PHTEL  = "+14842125757"
PLACE  = "San Diego, CA"
DOMAIN = "nibarc.com"

NAV = [("/about/", "About"),
       ("/strategic-consulting/", "Strategic Consulting"),
       ("/digital-transformation/", "Digital Transformation"),
       ("/agentic-framework/", "Agentic Framework")]

MARK = ('<svg viewBox="0 0 100 100" aria-hidden="true"><path d="M10 88 C 10 44.9, 44.9 10, 88 10" '
        'fill="none" stroke="currentColor" stroke-width="14" stroke-linecap="round"/>'
        '<circle cx="88" cy="10" r="11" fill="#0E8F82"/></svg>')
MARK_D = MARK.replace('fill="#0E8F82"', 'fill="#3AD6C4"')

def shell(title, desc, body, path):
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' class="here"' if h == path else '', t) for h, t in NAV)
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{DOMAIN}{PATH}">
<meta property="og:image" content="/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://{DOMAIN}{PATH}">
<meta name="theme-color" content="#0A0E12">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/nibarc.css">
<script defer data-domain="{DOMAIN}" src="https://plausible.io/js/script.js"></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nb-head">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Nibarc home">{MARK}<b>nibarc</b></a>
    <button class="navbtn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nb-nav" id="nav">{NAV}<a class="prod" href="/nexora/"><i></i>Nexora</a><a class="btn btn-solid" href="/contact/">Get in touch</a></nav>
  </div>
</header>
<main id="main">
{BODY}
</main>
<footer class="nb-foot">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="/" aria-label="Nibarc home">{MARKD}<b>nibarc</b></a>
        <p>SAP-native strategy, transformation and agents — advised and built by one team.</p>
      </div>
      <div>
        <h5>Company</h5>
        <nav><a href="/">Home</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav>
      </div>
      <div>
        <h5>Practices</h5>
        <nav><a href="/strategic-consulting/">Strategic Consulting</a><a href="/digital-transformation/">Digital Transformation</a><a href="/agentic-framework/">Agentic Framework</a><a href="/nexora/">Nexora</a></nav>
      </div>
      <div>
        <h5>Contact</h5>
        <nav><a href="mailto:{EMAIL}">{EMAIL}</a><a href="tel:{PHTEL}">{PHONE}</a><span style="color:#9AA7B2;font-size:15px">{PLACE}</span></nav>
      </div>
    </div>
    <div class="legal">
      <span>&copy; 2026 Nibarc. All rights reserved.</span>
      <span><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></span>
    </div>
  </div>
</footer>
<script src="/assets/js/nibarc.js"></script>
</body>
</html>
""".replace("{TITLE}", title).replace("{DESC}", desc).replace("{BODY}", body) \
   .replace("{NAV}", nav).replace("{MARKD}", MARK_D).replace("{MARK}", MARK) \
   .replace("{EMAIL}", EMAIL).replace("{PHTEL}", PHTEL).replace("{PHONE}", PHONE) \
   .replace("{PLACE}", PLACE).replace("{DOMAIN}", DOMAIN).replace("{PATH}", path)

FP = re.compile(r"\.[0-9a-f]{8}$")
def _plain(p):
    stem = p.stem
    return p.with_name(FP.sub("", stem) + p.suffix) if FP.search(stem) else p

def htmls():
    return [h for h in OUT.rglob("*.html") if "nexora" not in h.relative_to(OUT).parts]

def fingerprint():
    mapping = {}
    for p in sorted(q for q in (OUT / "assets").rglob("*") if q.is_file()):
        plain = _plain(p)
        if plain != p:
            p.rename(plain); p = plain
        h = hashlib.sha256(p.read_bytes()).hexdigest()[:8]
        new = p.with_name(p.stem + "." + h + p.suffix)
        p.rename(new)
        mapping["/" + str(p.relative_to(OUT))] = "/" + str(new.relative_to(OUT))
    for h in htmls():
        s = s0 = h.read_text()
        for a, b in mapping.items():
            s = s.replace(a, b)
        if s != s0:
            h.write_text(s)
    return len(mapping)

def page(path, title, desc, body):
    d = OUT / path.strip("/")
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(shell(title, desc, body, path))

def phead(kicker, h1, lede):
    return ('<section class="hero on-dark">\n'
            '  <svg class="heroarc" viewBox="0 0 100 100" aria-hidden="true"><path d="M10 88 C 10 44.9, 44.9 10, 88 10" fill="none" stroke-width="7" stroke-linecap="round"/><circle cx="88" cy="10" r="5.5"/></svg>\n'
            '  <div class="wrap">\n'
            '    <span class="kicker">' + kicker + '</span>\n'
            '    <h1>' + h1 + '</h1>\n'
            '    <p class="lede">' + lede + '</p>\n'
            '  </div>\n'
            '</section>\n')

CTA = """
<section class="sec on-dark cta">
  <div class="wrap">
    <span class="kicker">Start somewhere real</span>
    <h2 style="margin-top:18px">Bring us one decision you can't close.</h2>
    <p class="lede">Not an RFP, not a discovery phase. One ruling your program keeps deferring — we'll tell you what it would take to close it, and what it is costing you while it stays open.</p>
    <div class="btns">
      <a class="btn btn-solid" href="/contact/">Get in touch</a>
      <a class="btn btn-line" href="/nexora/">See Nexora</a>
    </div>
  </div>
</section>
"""

HOME = """
<section class="hero on-dark">
  <svg class="heroarc" viewBox="0 0 100 100" aria-hidden="true"><path d="M10 88 C 10 44.9, 44.9 10, 88 10" fill="none" stroke-width="7" stroke-linecap="round"/><circle cx="88" cy="10" r="5.5"/></svg>
  <div class="wrap">
    <span class="kicker">S/4HANA &middot; SAP BTP &middot; Agents</span>
    <h1>The SAP firm that builds its own tools.</h1>
    <p class="lede">Nibarc advises operating leaders on SAP S/4HANA and BTP — and then builds the software that carries the work. The consultants and the engineers are one team here, which is why the advice survives contact with the system.</p>
    <div class="btns">
      <a class="btn btn-solid" href="#practices">What we do</a>
      <a class="btn btn-line" href="/contact/">Get in touch</a>
    </div>
    <dl class="strip">
      <div><dt>Three</dt><dd>practices, from the value case through agents in production</dd></div>
      <div><dt>Nexora</dt><dd>our first product, running on customer programs today</dd></div>
      <div><dt>Eight</dt><dd>industries, each with its own operating reality</dd></div>
      <div><dt>Native</dt><dd>built on S/4HANA and BTP, not bolted on beside them</dd></div>
    </dl>
  </div>
</section>

<section class="sec" id="practices">
  <div class="wrap">
    <div class="head">
      <span class="kicker">What we do</span>
      <h2 style="margin-top:16px">Three practices. One thesis.</h2>
      <p class="lede">A program fails in the gaps — between the strategy deck and the backlog, between the design and the code, between the decision and the evidence that it was ever made. We work the gaps.</p>
    </div>
    <div class="prac">
      <a href="/strategic-consulting/">
        <span class="no">01</span>
        <h3>Strategic Consulting</h3>
        <p>Where S/4HANA earns its money and where it does not. The value case, the transition path and a roadmap your board can sign — written to be defended twelve months later, not just approved.</p>
        <span class="go">Explore &rarr;</span>
      </a>
      <a href="/digital-transformation/">
        <span class="no">02</span>
        <h3>Digital Transformation</h3>
        <p>The long middle: clean core, integration, data, test, cutover. We run the program against one record, so the ruling made in March is still findable — and still binding — in October.</p>
        <span class="go">Explore &rarr;</span>
      </a>
      <a href="/agentic-framework/">
        <span class="no">03</span>
        <h3>Agentic Framework</h3>
        <p>Agents that read your landscape, produce real work and stop at a human. Built on BTP, inside your four walls, with every output carrying the evidence of where it came from.</p>
        <span class="go">Explore &rarr;</span>
      </a>
    </div>
  </div>
</section>

<section class="sec on-mist">
  <div class="wrap">
    <div class="prod">
      <div>
        <span class="kicker">Our product</span>
        <div class="prodmark" style="margin-top:20px"><img src="/assets/brand/nexora-logo.svg" alt="Nexora" width="168" height="38"></div>
        <h2>One record of your SAP program.</h2>
        <p class="lede">Nexora listens to your workshops, reads your ABAP, and runs the program from a single record. Agents produce; humans approve. Every requirement, every line of code and every task traces back to the words someone said.</p>
        <ul class="plist">
          <li><b>The Brief</b> — workshops in; cited requirements, ruled contradictions and a signed blueprint out.</li>
          <li><b>Forge</b> — reads your landscape from the code, builds from signed specs, tests and transports.</li>
          <li><b>Manage</b> — plan, resources, RAID and process areas, read from that same record.</li>
        </ul>
        <div class="btns"><a class="btn btn-solid" href="/nexora/">See Nexora</a></div>
      </div>
      <div class="prodshot"><img src="/assets/img/nexora-brief.webp" alt="The Nexora Brief: a program's front page, leading with the one ruling that matters today" width="1280" height="623" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <span class="kicker">How we work</span>
      <h2 style="margin-top:16px">Small team. Short leash. Evidence throughout.</h2>
      <p class="lede">We are not a body shop and we do not staff by the month. Specialists arrive for the problem in front of them and leave when it is closed.</p>
    </div>
    <ol class="steps">
      <li><h4>Name the decision</h4><p>We start at the ruling you cannot make yet — not at a discovery phase that defers it.</p></li>
      <li><h4>Assemble for it</h4><p>Domain consultants, SAP architects, data people and engineers, chosen for that decision.</p></li>
      <li><h4>Run against a record</h4><p>Requirements, rulings and code all trace to a source. Nothing becomes truth because a slide said so.</p></li>
      <li><h4>Leave it running</h4><p>Handover, hypercare and the tooling stay with you. We don't rent you a dependency.</p></li>
    </ol>
  </div>
</section>

<section class="sec tight on-mist">
  <div class="wrap">
    <div class="head" style="margin-bottom:36px">
      <span class="kicker">Industries</span>
      <h2 style="margin-top:16px">Shaped for how your operation actually runs.</h2>
    </div>
    <ul class="inds">
      <li><span>01</span>Wholesale &amp; Distribution</li>
      <li><span>02</span>Consumer Goods</li>
      <li><span>03</span>Retail</li>
      <li><span>04</span>Life Sciences</li>
      <li><span>05</span>Manufacturing</li>
      <li><span>06</span>High Tech</li>
      <li><span>07</span>Chemical</li>
      <li><span>08</span>Travel, Hospitality &amp; Leisure</li>
    </ul>
  </div>
</section>
""" + CTA

ABOUT = phead("About Nibarc",
  "Built by people who stay for the build.",
  "Most SAP advice ends at the handover. Ours doesn't — we write the strategy, run the transformation and ship the software that carries it, which means we are still there when the design meets the system.") + """
<section class="sec">
  <div class="wrap">
    <div class="g2">
      <div>
        <h2>Why we exist</h2>
        <p class="lede">Enterprises do not struggle with SAP because the software is hard. They struggle because the program loses its own memory: the decision nobody can find, the requirement nobody can trace, the custom object nobody can explain. By go-live the organisation knows less about its own processes than it did at kickoff.</p>
        <p class="lede">Nibarc was built to close that gap — with consultants who have run the programs, and engineers who build the tooling that keeps the record honest.</p>
      </div>
      <div>
        <h2>The model</h2>
        <p class="lede">We assemble specialists around a decision rather than selling a fixed team. A pricing question pulls a different bench than a cutover question. The engagement is sized to the problem and closes when the problem does.</p>
        <p class="lede">That only works if the knowledge survives the people. It does, because everything we produce lands in a record you own, and the agents that help produce it run inside your four walls.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec on-mist">
  <div class="wrap">
    <div class="head">
      <span class="kicker">What we measure</span>
      <h2 style="margin-top:16px">Outcomes, not deliverables.</h2>
      <p class="lede">A deck is not a result and a milestone is not a result. These are.</p>
    </div>
    <div class="g3">
      <div class="blk"><h3>Decisions closed</h3><p>How many open rulings your program is still carrying, and how fast that number falls.</p></div>
      <div class="blk"><h3>Traceability</h3><p>What share of requirements, designs and code traces to a named source.</p></div>
      <div class="blk"><h3>Cost of delay</h3><p>What each unresolved decision costs per week — stated, not implied.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <span class="kicker">Our commitment</span>
      <h2 style="margin-top:16px">Your data stays inside your four walls.</h2>
      <p class="lede">Everything we build runs in your tenant, on your models, under your controls. Nothing crosses to another customer and nothing trains anybody else's system. It is the first question every CIO asks us, and the answer has never had an asterisk.</p>
    </div>
  </div>
</section>
""" + CTA

SC = phead("01 &middot; Practice",
  "Strategy that survives the steering committee.",
  "We align the business case with what SAP S/4HANA and BTP can actually do — then write it so it still holds when the first hard trade-off arrives.") + """
<section class="sec">
  <div class="wrap">
    <div class="head"><span class="kicker">Capabilities</span><h2 style="margin-top:16px">Four things we are asked for most.</h2></div>
    <div class="g2">
      <div class="blk"><h3>S/4HANA strategy and value case</h3><p>Where the money is, where the risk is, and what the transition path costs under each option — greenfield, brownfield or selective. Numbers you can defend to a board.</p></div>
      <div class="blk"><h3>BTP and extension strategy</h3><p>What belongs in the clean core, what belongs on BTP, and what should not be built at all. The answer usually removes scope.</p></div>
      <div class="blk"><h3>Operating alignment</h3><p>Turning the roadmap into initiatives with owners, gates and a cost of delay — so business and IT argue about the same artefact.</p></div>
      <div class="blk"><h3>Value realisation</h3><p>The governance and KPIs that say whether the thing worked, wired to the program record rather than to a quarterly slide.</p></div>
    </div>
  </div>
</section>

<section class="sec on-mist">
  <div class="wrap">
    <div class="head"><span class="kicker">The outcome</span><h2 style="margin-top:16px">A roadmap that names its own assumptions.</h2>
    <p class="lede">You end with a transition path, a defensible value case and a decision log that shows exactly which assumptions it rests on — so when one of them moves, you know what else has to.</p></div>
  </div>
</section>
""" + CTA

DT = phead("02 &middot; Practice",
  "Bridge the design and the system.",
  "The long middle of a transformation is where programs quietly lose the plot. We run it against one record — clean core, integration, data, test and cutover — so nothing becomes true without a trace.") + """
<section class="sec">
  <div class="wrap">
    <div class="head"><span class="kicker">Capabilities</span><h2 style="margin-top:16px">What we run.</h2></div>
    <div class="g2">
      <div class="blk"><h3>Fit-to-standard, properly</h3><p>Workshops that produce cited requirements and ruled contradictions, not a backlog of notes nobody re-reads.</p></div>
      <div class="blk"><h3>Clean core and custom code</h3><p>We read your ABAP estate to find what is actually used, what blocks the move, and what should be retired instead of fixed.</p></div>
      <div class="blk"><h3>Data and integration</h3><p>Object lists, mappings, interface inventory and reconciliation — built from the landscape rather than from memory.</p></div>
      <div class="blk"><h3>Test and cutover</h3><p>Scripts born with the requirement, rehearsals that are allowed to fail, and a runbook a change board will accept.</p></div>
    </div>
  </div>
</section>

<section class="sec on-mist">
  <div class="wrap">
    <div class="head"><span class="kicker">The outcome</span><h2 style="margin-top:16px">A program that can answer for itself.</h2>
    <p class="lede">Ask why billing works the way it does, or what breaks if a requirement changes, and the answer comes back in a minute with its evidence attached — during the program, and years after it.</p></div>
  </div>
</section>
""" + CTA

AF = phead("03 &middot; Practice",
  "Agents that produce, and then stop.",
  "Automation that drafts the work, shows what it read, and waits for a human to approve. Built on SAP BTP and your own models, running where your data already lives.") + """
<section class="sec">
  <div class="wrap">
    <div class="head"><span class="kicker">Capabilities</span><h2 style="margin-top:16px">How we build them.</h2></div>
    <div class="g2">
      <div class="blk"><h3>Grounded in your landscape</h3><p>Agents read your systems, your code and your documents through governed connections — not a general model guessing at your business.</p></div>
      <div class="blk"><h3>Evidence as a first-class output</h3><p>Every answer carries its citations. If it cannot show where a claim came from, it does not ship.</p></div>
      <div class="blk"><h3>Human gates by design</h3><p>Agents produce; people approve. Nothing becomes part of the record because a model was confident.</p></div>
      <div class="blk"><h3>Inside your four walls</h3><p>Your tenant, your keys, your retention rules. Nothing crosses to another customer, ever.</p></div>
    </div>
  </div>
</section>

<section class="sec on-mist">
  <div class="wrap">
    <div class="prod">
      <div>
        <span class="kicker">Seen in production</span>
        <h2 style="margin-top:16px">Nexora is this framework, shipped.</h2>
        <p class="lede">Our own product is the clearest statement of how we think agents should behave on an enterprise program: read widely, produce real artefacts, cite everything, and stop at a human.</p>
        <div class="btns"><a class="btn btn-solid" href="/nexora/">See Nexora</a></div>
      </div>
      <div class="prodshot"><img src="/assets/img/nexora-proof.webp" alt="Nexora&#39;s Forge: the evidence pack behind a generated build — acceptance criteria, unit tests and screenshots, each content-hashed" width="1280" height="623" loading="lazy"></div>
    </div>
  </div>
</section>
""" + CTA

CONTACT = phead("Contact",
  "Tell us what isn't moving.",
  "A short conversation is usually enough to tell whether we are the right firm for the problem. If we are not, we will say so.") + """
<section class="sec">
  <div class="wrap">
    <div class="cx">
      <div><h4>Email</h4><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div><h4>Phone</h4><p><a href="tel:{PHTEL}">{PHONE}</a></p></div>
      <div><h4>Location</h4><p>{PLACE}</p></div>
    </div>
    <div class="g2" style="margin-top:72px">
      <div class="blk"><h3>Starting an engagement</h3><p>Send the decision you are stuck on and roughly where you are in the journey. We will come back with how we would approach it and who from our bench would be on it.</p></div>
      <div class="blk"><h3>Seeing the product</h3><p>For Nexora, bring one workshop recording. We will show you the record it produces from your own material, every line cited.</p></div>
    </div>
  </div>
</section>
"""

PRIVACY = phead("Privacy", "Privacy", "What this website collects, and what it does not.") + """
<section class="sec"><div class="wrap prose">
  <h2>The short version</h2>
  <p>This site has no accounts, no logins and no advertising trackers. We do not sell or share visitor data. We do not set cookies for analytics.</p>
  <h2>Analytics</h2>
  <p>We use Plausible Analytics to count page views. Plausible is privacy-focused and cookieless: it records the page visited, the referring site, and coarse device and country information derived from your request. It does not build a profile of you and does not track you across other websites.</p>
  <h2>When you contact us</h2>
  <p>If you email or call us, we keep what you send so that we can reply and, if we work together, so that we can run the engagement. We do not add you to a marketing list you did not ask for.</p>
  <h2>Customer data</h2>
  <p>Data belonging to our customers' SAP programs is governed by the agreement with that customer. It is held inside the customer's own environment, is never used to train models for anyone else, and is never shared between customers.</p>
  <h2>Hosting</h2>
  <p>This website is served by Netlify, which keeps standard server logs including IP addresses for a limited period for security and operational purposes.</p>
  <h2>Your choices</h2>
  <p>You can block analytics with any content blocker and the site will work normally. To ask what we hold about you, or to have it deleted, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <h2>Changes</h2>
  <p>If this policy changes we will update this page. Last updated 11 November 2026.</p>
</div></section>
"""

TERMS = phead("Terms", "Terms of use", "The terms on which this website is provided.") + """
<section class="sec"><div class="wrap prose">
  <h2>This website</h2>
  <p>Nibarc provides this website for general information about our services and products. Nothing on it is an offer, a contract, or professional advice for your specific situation. Engagements are governed solely by a signed agreement.</p>
  <h2>No warranty</h2>
  <p>We take care to keep this site accurate, but we provide it "as is" and make no warranties about its completeness, accuracy or availability. Statements about outcomes describe what our approach aims for, not a guaranteed result.</p>
  <h2>Intellectual property</h2>
  <p>The content, design, marks and product names on this site — including Nibarc and Nexora — belong to Nibarc unless stated otherwise. SAP, S/4HANA and SAP BTP are trademarks of SAP SE. Nibarc is an independent firm and is not affiliated with or endorsed by SAP SE.</p>
  <h2>Screenshots</h2>
  <p>Product screenshots on this site use fictional demonstration data. They do not depict any real customer, person, project or system.</p>
  <h2>Links</h2>
  <p>We are not responsible for the content of sites we link to.</p>
  <h2>Liability</h2>
  <p>To the extent permitted by law, Nibarc is not liable for any loss arising from use of this website.</p>
  <h2>Contact</h2>
  <p>Questions about these terms: <a href="mailto:{EMAIL}">{EMAIL}</a>. Last updated 11 November 2026.</p>
</div></section>
"""

SRC = pathlib.Path(__file__).resolve().parent

def sync_static():
    """Copy hand-authored css/js from src/ into the publish tree.
    Keeps one canonical copy, so an edit can never fork into a stale twin."""
    import shutil
    for name, sub in (("nibarc.css", "css"), ("nibarc.js", "js")):
        dest_dir = OUT / "assets" / sub
        dest_dir.mkdir(parents=True, exist_ok=True)
        for stale in dest_dir.glob(pathlib.Path(name).stem + ".*"):
            stale.unlink()
        shutil.copy2(SRC / name, dest_dir / name)

if __name__ == "__main__":
    def f(s):
        return (s.replace("{EMAIL}", EMAIL).replace("{PHTEL}", PHTEL)
                 .replace("{PHONE}", PHONE).replace("{PLACE}", PLACE))
    sync_static()
    page("/", "Nibarc — SAP-native strategy, transformation and agents",
         "Nibarc advises operating leaders on SAP S/4HANA and BTP, and builds the software that carries the work. Home of Nexora.", f(HOME))
    page("/about/", "About — Nibarc",
         "Consultants who have run the programs and engineers who build the tooling that keeps the record honest.", f(ABOUT))
    page("/strategic-consulting/", "Strategic Consulting — Nibarc",
         "The S/4HANA value case, transition path and roadmap — written to be defended twelve months later.", f(SC))
    page("/digital-transformation/", "Digital Transformation — Nibarc",
         "Clean core, integration, data, test and cutover, run against one record so nothing becomes true without a trace.", f(DT))
    page("/agentic-framework/", "Agentic Framework — Nibarc",
         "Agents that read your landscape, produce real work, cite their evidence and stop at a human. Built on SAP BTP.", f(AF))
    page("/contact/", "Contact — Nibarc",
         "Tell us what isn't moving. A short conversation is usually enough to tell whether we are the right firm.", f(CONTACT))
    page("/privacy/", "Privacy — Nibarc", "What this website collects, and what it does not.", f(PRIVACY))
    page("/terms/", "Terms of use — Nibarc", "The terms on which this website is provided.", f(TERMS))
    print("nibarc: fingerprinted", fingerprint(), "assets")
