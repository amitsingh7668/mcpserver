<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Poisoned Package</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --ink:#1a1814;
  --paper:#faf8f4;
  --warm:#f5f0e8;
  --red:#c0392b;
  --red-light:#fdf0ee;
  --red-mid:#f5c6c2;
  --amber:#b7560a;
  --amber-light:#fef6ec;
  --amber-mid:#fad8b0;
  --green:#1a6b3c;
  --green-light:#edf7f2;
  --green-mid:#a8dfc0;
  --blue:#1a4d8c;
  --blue-light:#eef3fb;
  --blue-mid:#b3cef0;
  --gray:#6b6560;
  --border:#e2ddd6;
  --mono:'JetBrains Mono',monospace;
  --serif:'Newsreader',Georgia,serif;
  --sans:'Syne',sans-serif;
}
html,body{background:#faf8f4;color:var(--ink);font-family:var(--serif);font-size:18px;line-height:1.8}

/* ── PAGE SHELL ── */
.page{max-width:860px;margin:0 auto;padding:0 28px 80px}

/* ── MASTHEAD ── */
.masthead{padding:52px 0 0;border-bottom:3px solid var(--ink);margin-bottom:0}
.kicker{font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--gray);margin-bottom:18px;display:flex;align-items:center;gap:10px}
.kicker span{display:inline-block;width:28px;height:1.5px;background:var(--gray)}
h1{font-family:var(--sans);font-size:clamp(42px,6vw,72px);font-weight:800;line-height:1.0;letter-spacing:-.02em;color:var(--ink);margin-bottom:20px}
h1 em{font-style:normal;color:var(--red)}
.deck{font-family:var(--serif);font-size:20px;font-weight:300;font-style:italic;color:#4a4540;line-height:1.55;max-width:620px;margin-bottom:28px}
.byline{font-family:var(--mono);font-size:11px;color:var(--gray);letter-spacing:.1em;padding-bottom:24px;display:flex;gap:20px;flex-wrap:wrap}
.byline b{color:var(--ink)}

/* ── HERO STAT BAND ── */
.hero-band{background:var(--ink);color:#faf8f4;padding:36px 40px;margin-bottom:52px;display:grid;grid-template-columns:repeat(3,1fr);gap:1px}
.hero-stat{padding:0 28px;border-right:1px solid #3a3530}
.hero-stat:first-child{padding-left:0}
.hero-stat:last-child{border:none}
.hero-num{font-family:var(--sans);font-size:48px;font-weight:800;line-height:1;color:#fff;display:block}
.hero-num.red{color:#f08070}
.hero-num.amber{color:#f5c070}
.hero-num.teal{color:#70d4c0}
.hero-unit{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#9a9288;margin-top:8px;display:block;line-height:1.4}

/* ── BODY LAYOUT ── */
.prose{max-width:660px}

/* ── TYPOGRAPHY ── */
h2{font-family:var(--sans);font-size:28px;font-weight:700;letter-spacing:-.01em;color:var(--ink);margin:56px 0 16px;padding-top:52px;border-top:1.5px solid var(--border)}
h3{font-family:var(--sans);font-size:16px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--gray);margin:36px 0 12px}
p{margin-bottom:22px;color:#2a2520;font-size:18px;line-height:1.82}
p.intro{font-size:21px;font-weight:300;line-height:1.7;color:#1a1814;font-style:italic;border-left:4px solid var(--red);padding-left:20px;margin-bottom:32px}
strong{font-weight:600;color:var(--ink)}
code{font-family:var(--mono);font-size:14px;background:#ede8e0;color:#8b1a0a;padding:2px 6px;border-radius:3px}
em{font-style:italic}

/* ── ATTACK CARDS ── */
.attacks{margin:32px 0 8px;display:flex;flex-direction:column;gap:0}
.attack{border:1.5px solid var(--border);border-top:none;padding:28px 32px;position:relative;background:#fff}
.attack:first-child{border-top:1.5px solid var(--border)}
.attack-header{display:flex;align-items:flex-start;gap:16px;margin-bottom:14px}
.sev{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;padding:4px 10px;border-radius:3px;flex-shrink:0;margin-top:3px;font-weight:500}
.sev.critical{background:var(--red-light);color:var(--red);border:1px solid var(--red-mid)}
.sev.high{background:var(--amber-light);color:var(--amber);border:1px solid var(--amber-mid)}
.attack-title{font-family:var(--sans);font-size:18px;font-weight:700;color:var(--ink);line-height:1.2}
.attack-date{font-family:var(--mono);font-size:11px;color:var(--gray);letter-spacing:.08em;margin-bottom:10px}
.attack-body{font-size:16px;line-height:1.7;color:#3a3530;margin-bottom:14px}
.attack-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.tag{font-family:var(--mono);font-size:11px;background:var(--warm);color:#4a4540;padding:4px 10px;border-radius:3px;border:1px solid var(--border)}
.attack-bar{position:absolute;left:0;top:0;bottom:0;width:4px}
.attack-bar.critical{background:var(--red)}
.attack-bar.high{background:var(--amber)}

/* ── STAT TABLE ── */
.stat-table{width:100%;border-collapse:collapse;margin:28px 0;font-size:15px}
.stat-table th{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--gray);padding:10px 14px;border-bottom:2px solid var(--ink);text-align:left;background:var(--warm)}
.stat-table td{padding:12px 14px;border-bottom:1px solid var(--border);vertical-align:top;line-height:1.5}
.stat-table tr:last-child td{border-bottom:none}
.stat-table tr:nth-child(even) td{background:#fdfbf8}
.stat-table td:last-child{font-family:var(--sans);font-weight:700;color:var(--ink);white-space:nowrap}
.stat-table .num{font-family:var(--mono);font-size:17px;font-weight:500}

/* ── COMPARISON ── */
.compare{display:grid;grid-template-columns:1fr 1fr;gap:0;margin:28px 0;border:1.5px solid var(--border)}
.comp-col{padding:28px}
.comp-col+.comp-col{border-left:1.5px solid var(--border)}
.comp-head{font-family:var(--sans);font-size:16px;font-weight:700;margin-bottom:18px;padding-bottom:12px;border-bottom:1px solid var(--border)}
.comp-col.bad .comp-head{color:var(--red)}
.comp-col.good .comp-head{color:var(--green)}
.comp-row{display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);font-size:14px;color:#4a4540;line-height:1.4}
.comp-row:last-child{border:none}
.check{font-size:13px;flex-shrink:0;margin-top:1px}
.check.n{color:var(--red)}
.check.y{color:var(--green)}

/* ── CODE BLOCK ── */
pre{background:#1e1c18;border-radius:6px;padding:28px;margin:24px 0;overflow-x:auto;font-family:var(--mono);font-size:13.5px;line-height:1.75;color:#d4cfc4}
pre .cm{color:#5a574f}
pre .kw{color:#70b8d4}
pre .st{color:#c8a870}
pre .ok{color:#78c878}
pre .er{color:#e08070}

/* ── CALLOUT BOXES ── */
.callout{padding:24px 28px;margin:32px 0;border-radius:4px;position:relative}
.callout.warn{background:var(--amber-light);border:1px solid var(--amber-mid);border-left:4px solid var(--amber)}
.callout.danger{background:var(--red-light);border:1px solid var(--red-mid);border-left:4px solid var(--red)}
.callout.info{background:var(--blue-light);border:1px solid var(--blue-mid);border-left:4px solid var(--blue)}
.callout.good{background:var(--green-light);border:1px solid var(--green-mid);border-left:4px solid var(--green)}
.callout-label{font-family:var(--mono);font-size:10px;letter-spacing:.15em;text-transform:uppercase;font-weight:500;margin-bottom:10px}
.callout.warn .callout-label{color:var(--amber)}
.callout.danger .callout-label{color:var(--red)}
.callout.info .callout-label{color:var(--blue)}
.callout.good .callout-label{color:var(--green)}
.callout p{margin:0;font-size:16px;line-height:1.65;color:var(--ink)}

/* ── PULLQUOTE ── */
.pullquote{margin:44px 0;padding:0 0 0 28px;border-left:4px solid var(--ink)}
.pullquote p{font-family:var(--serif);font-size:22px;font-weight:300;font-style:italic;line-height:1.55;color:var(--ink);margin-bottom:12px}
.pullquote cite{font-family:var(--mono);font-size:11px;color:var(--gray);letter-spacing:.1em;font-style:normal}

/* ── STOLEN LIST ── */
.stolen-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:20px 0}
.stolen-item{background:#fff;border:1.5px solid var(--border);border-left:3px solid var(--red);padding:12px 16px;font-size:15px;color:#2a2520;line-height:1.4}
.stolen-item strong{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--red);margin-bottom:3px}

/* ── CHECKLIST ── */
.checklist{margin:16px 0 24px;display:flex;flex-direction:column;gap:0}
.check-item{display:flex;align-items:flex-start;gap:14px;padding:13px 16px;border:1px solid var(--border);border-top:none;background:#fff;font-size:15px;line-height:1.5;color:#2a2520}
.check-item:first-child{border-top:1px solid var(--border)}
.check-item:nth-child(even){background:var(--warm)}
.check-box{width:18px;height:18px;border:1.5px solid var(--border);border-radius:3px;flex-shrink:0;margin-top:1px}

/* ── VECTOR TABLE ── */
.vector-table{width:100%;border-collapse:collapse;margin:20px 0;font-size:15px}
.vector-table th{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--gray);padding:10px 14px;border-bottom:2px solid var(--ink);text-align:left;background:var(--warm)}
.vector-table td{padding:13px 14px;border-bottom:1px solid var(--border);vertical-align:top;line-height:1.5}
.vector-table tr:last-child td{border-bottom:none}
.vector-table td:first-child{font-family:var(--sans);font-weight:600;font-size:14px;white-space:nowrap;color:var(--ink)}
.vector-table tr:hover td{background:#fdfaf6}

/* ── FOOTER ── */
footer{border-top:1.5px solid var(--border);margin-top:64px;padding-top:28px;font-family:var(--mono);font-size:11px;color:var(--gray);letter-spacing:.08em;line-height:1.8}

/* ── MOBILE ── */
@media(max-width:640px){
  .hero-band{grid-template-columns:1fr;gap:20px;padding:28px}
  .hero-stat{border:none;padding:0}
  .compare{grid-template-columns:1fr}
  .comp-col+.comp-col{border-left:none;border-top:1.5px solid var(--border)}
  .stolen-grid{grid-template-columns:1fr}
  h1{font-size:38px}
}
</style>
</head>
<body>
<div class="page">

<!-- MASTHEAD -->
<header class="masthead">
  <div class="kicker"><span></span>Security Deep Dive &nbsp;·&nbsp; Supply Chain &nbsp;·&nbsp; Python</div>
  <h1>The <em>Poisoned</em><br>Package</h1>
  <p class="deck">How PyPI quietly became one of the most dangerous places in your stack — and why the fix is simpler than you think.</p>
  <div class="byline">
    <span><b>Published</b> &nbsp;April 2026</span>
    <span><b>Read time</b> &nbsp;12 min</span>
    <span><b>Sources</b> &nbsp;JFrog · Endor Labs · ReversingLabs · Checkmarx · Zscaler</span>
  </div>
</header>

<!-- HERO STATS -->
<div class="hero-band">
  <div class="hero-stat">
    <span class="hero-num red">95M</span>
    <span class="hero-unit">LiteLLM monthly downloads exposed in single breach</span>
  </div>
  <div class="hero-stat">
    <span class="hero-num amber">20</span>
    <span class="hero-unit">Malicious packages in one cloud-credential campaign</span>
  </div>
  <div class="hero-stat">
    <span class="hero-num teal">14,100</span>
    <span class="hero-unit">Downloads before anyone noticed</span>
  </div>
</div>

<!-- BODY -->
<div class="prose">

<p class="intro">You run <code>pip install</code>. The name looks right. You've used it before. Then your SSH keys, cloud tokens, and Kubernetes secrets leave your machine without a single warning.</p>

<p>The Python ecosystem has spent the last 18 months under sustained attack. Not from script kiddies throwing misspelled package names at a wall — that kind of noise dropped by 85% in 2024 as PyPI tightened moderation. What replaced it is worse: coordinated groups compromising <em>real, trusted packages</em> with millions of weekly downloads and using them as delivery vehicles for credential stealers, remote access trojans, and persistent backdoors.</p>

<p>The common thread across every incident? A fresh <code>pip install</code> with no lockfile, no hash verification, and no way to know that what arrived today wasn't what you audited last month.</p>

<!-- STATS TABLE -->
<h2>By the numbers</h2>

<table class="stat-table">
  <thead><tr><th>Incident / metric</th><th>Figure</th></tr></thead>
  <tbody>
    <tr><td>LiteLLM daily downloads at time of TeamPCP breach</td><td><span class="num">3.4 million</span></td></tr>
    <tr><td>Malicious packages in 2025 cloud-credential campaign</td><td><span class="num">20</span></td></tr>
    <tr><td>Downloads before that campaign was detected</td><td><span class="num">14,100+</span></td></tr>
    <tr><td>LiteLLM monthly downloads — all exposed during breach</td><td><span class="num">95 million</span></td></tr>
    <tr><td>Decline in simple typosquatted PyPI malware (2023→2024)</td><td><span class="num">−85%</span></td></tr>
    <tr><td>Countries hit by the JarkaStealer AI-lure campaign</td><td><span class="num">30+</span></td></tr>
    <tr><td>Downloads of one JFrog-detected malicious batch</td><td><span class="num">~30,000</span></td></tr>
  </tbody>
</table>

<div class="callout warn">
  <div class="callout-label">Worth noting</div>
  <p>That 85% drop in typosquatting sounds reassuring. It isn't. Attackers stopped publishing junk and started compromising legitimate, well-maintained packages instead. Fewer incidents, far greater blast radius.</p>
</div>

<!-- ATTACK TIMELINE -->
<h2>The attacks</h2>
<p>Not CVEs in a spreadsheet. Real packages. Real engineers. Real production systems.</p>

<div class="attacks">

  <div class="attack">
    <div class="attack-bar critical"></div>
    <div class="attack-date">December 2024</div>
    <div class="attack-header">
      <span class="sev critical">Critical</span>
      <div class="attack-title">Ultralytics</div>
    </div>
    <div class="attack-body">The ML vision library — tens of millions of installs — was backdoored through a compromised GitHub Actions cache. Attackers injected code during the build phase, then published poisoned versions 8.3.41, 8.3.42, 8.3.45 and 8.3.46 using an unrevoked PyPI API token that the project had simply forgotten to rotate.</div>
    <div class="attack-meta">
      <span class="tag">CI/CD cache poisoning</span>
      <span class="tag">Unrevoked API token</span>
      <span class="tag">Build-phase injection</span>
    </div>
  </div>

  <div class="attack">
    <div class="attack-bar critical"></div>
    <div class="attack-date">March 2025</div>
    <div class="attack-header">
      <span class="sev critical">Critical</span>
      <div class="attack-title">Cloud Credential Campaign</div>
    </div>
    <div class="attack-body">ReversingLabs found 20 packages disguised as cloud SDKs and time utilities — <code>acloud-client</code>, <code>enumer-iam</code>, <code>snapshot-photo</code>. Each hid a Base64-encoded payload inside <code>setup.py</code>, which runs automatically the moment you type <code>pip install</code>. AWS, Alibaba Cloud, and Tencent Cloud tokens were the targets. 14,100 downloads happened before anyone noticed.</div>
    <div class="attack-meta">
      <span class="tag">setup.py execution</span>
      <span class="tag">Cloud token theft</span>
      <span class="tag">14,100 downloads</span>
    </div>
  </div>

  <div class="attack">
    <div class="attack-bar high"></div>
    <div class="attack-date">May 2025</div>
    <div class="attack-header">
      <span class="sev high">High</span>
      <div class="attack-title">Colorama Typosquatting Campaign</div>
    </div>
    <div class="attack-body">Checkmarx Zero found packages mimicking <code>colorama</code> using a technique nobody had documented before: cross-ecosystem name confusion. They used NPM package names to attack PyPI users — people who wouldn't think to check npm when vetting Python imports. On Windows: DLL side-loading with Task Scheduler persistence. On Linux: encrypted reverse shells exfiltrated via Pastebin.</div>
    <div class="attack-meta">
      <span class="tag">Cross-ecosystem confusion</span>
      <span class="tag">DLL side-loading</span>
      <span class="tag">Reverse shell</span>
    </div>
  </div>

  <div class="attack">
    <div class="attack-bar high"></div>
    <div class="attack-date">July 2025</div>
    <div class="attack-header">
      <span class="sev high">High</span>
      <div class="attack-title">termncolor / colorinal</div>
    </div>
    <div class="attack-body"><code>termncolor</code> looked harmless. It was. The payload lived in its dependency, <code>colorinal</code> — a package you never installed directly. Once in, it ran DLL side-loading, established C2 communication, and enabled remote code execution. The threat actor had been running this operation since July 10th, with 90,692 messages logged in their Zulip C2 channel before it was caught.</div>
    <div class="attack-meta">
      <span class="tag">Transitive dependency</span>
      <span class="tag">DLL side-loading</span>
      <span class="tag">884 combined downloads</span>
    </div>
  </div>

  <div class="attack">
    <div class="attack-bar critical"></div>
    <div class="attack-date">August 2025</div>
    <div class="attack-header">
      <span class="sev critical">Critical</span>
      <div class="attack-title">SilentSync RAT — sisaws, secmeasure</div>
    </div>
    <div class="attack-body">A full Python-based Remote Access Trojan tucked inside two packages typosquatting on a niche Argentine health system library. Remote command execution, file exfiltration, screen capture, and browser credential harvesting across Chrome, Brave, Edge and Firefox — all phoning home over HTTP with periodic beaconing. Chose an obscure target precisely because nobody monitors it.</div>
    <div class="attack-meta">
      <span class="tag">Full RAT</span>
      <span class="tag">Browser harvesting</span>
      <span class="tag">HTTP C2 beaconing</span>
    </div>
  </div>

  <div class="attack">
    <div class="attack-bar critical"></div>
    <div class="attack-date">March 2026</div>
    <div class="attack-header">
      <span class="sev critical">Critical</span>
      <div class="attack-title">LiteLLM — TeamPCP</div>
    </div>
    <div class="attack-body">The biggest one yet. TeamPCP — who'd previously hit Trivy — compromised LiteLLM and pushed versions 1.82.7 and 1.82.8. Version 1.82.8 installed a <code>.pth</code> file into the Python environment. Python processes every <code>.pth</code> file at startup — so the payload ran even on machines where LiteLLM was never actually called. Three stages: harvest SSH keys, cloud tokens, Kubernetes secrets, and wallets; move laterally across every Kubernetes node; install a <code>systemd</code> backdoor that polls for new payloads.</div>
    <div class="attack-meta">
      <span class="tag">.pth file persistence</span>
      <span class="tag">95M monthly downloads exposed</span>
      <span class="tag">Kubernetes lateral movement</span>
      <span class="tag">systemd backdoor</span>
    </div>
  </div>

</div>

<div class="pullquote">
  <p>"Lack of moderation and automated security controls in public repositories allow even inexperienced attackers to spread malware — through typosquatting, dependency confusion, or simple social engineering."</p>
  <cite>— JFrog Security Research</cite>
</div>

<!-- PIP BLIND -->
<h2>Why pip doesn't see any of this</h2>

<p><code>pip</code> is good at what it does. Installing packages is just not the same job as securing them. When you run <code>pip install requests</code>, pip fetches whatever the registry currently says is the latest compatible version. It doesn't check whether today's version matches what you reviewed last month. It doesn't lock transitive dependencies. It has no concept of "this hash doesn't match what we installed before."</p>

<p>The LiteLLM attack is the clearest demonstration. A new version went up. Millions of CI pipelines pulled it on the next build. A <code>.pth</code> file landed in the environment and started running on every Python process from that point forward. <code>pip</code> had no idea. Your pipeline had no idea. Your monitoring had no idea.</p>

<h3>The lockfile gap</h3>

<p>A <code>requirements.txt</code> that says <code>requests&gt;=2.28.0</code> is functionally an instruction to install whatever the attacker publishes next. The fix needs to be a lockfile — a complete, version-pinned, hash-verified record of every package in your dependency tree, committed to git so changes are visible and auditable.</p>

<div class="compare">
  <div class="comp-col bad">
    <div class="comp-head">pip (no lockfile)</div>
    <div class="comp-row"><span class="check n">✗</span>No lockfile by default</div>
    <div class="comp-row"><span class="check n">✗</span>Resolves "latest compatible" each time</div>
    <div class="comp-row"><span class="check n">✗</span>No SHA-256 hash checks</div>
    <div class="comp-row"><span class="check n">✗</span>Transitive deps update silently</div>
    <div class="comp-row"><span class="check n">✗</span>No dev/prod separation</div>
    <div class="comp-row"><span class="check n">✗</span>setup.py runs arbitrary code on install</div>
  </div>
  <div class="comp-col good">
    <div class="comp-head">Poetry</div>
    <div class="comp-row"><span class="check y">✓</span>poetry.lock pins the full dependency tree</div>
    <div class="comp-row"><span class="check y">✓</span>SHA-256 verified on every install</div>
    <div class="comp-row"><span class="check y">✓</span>Hash mismatch = install aborted</div>
    <div class="comp-row"><span class="check y">✓</span>No silent upgrades — must run poetry update</div>
    <div class="comp-row"><span class="check y">✓</span>Explicit dev / prod / test groups</div>
    <div class="comp-row"><span class="check y">✓</span>Lockfile diffs visible in every PR</div>
  </div>
</div>

<!-- POETRY FIX -->
<h2>What Poetry actually does</h2>

<p>Poetry doesn't stop bad packages from being published. What it does is give you a tamper-evident record of exactly what you installed and when. The moment an attacker swaps out a package version after your lockfile was written, the hash stops matching and the install fails loudly.</p>

<pre><span class="cm"># Old workflow — pip silently pulls whatever is newest</span>
pip install litellm

<span class="cm"># Poetry workflow — pinned to a specific version and hash</span>
<span class="kw">poetry</span> add litellm
<span class="cm"># Writes to poetry.lock:
# litellm = {version = "1.82.6", hash = "sha256:a3f2..."}
# Committed to git. Every change is a PR diff.</span>

<span class="cm"># TeamPCP pushes litellm 1.82.7 with malicious payload</span>
<span class="kw">poetry</span> install
<span class="er">✗  Hash mismatch for litellm==1.82.7</span>
<span class="er">✗  Expected sha256:a3f2...  Got sha256:c0de...</span>
<span class="er">✗  Installation aborted.</span></pre>

<h3>Migration in five commands</h3>

<pre><span class="cm"># 1. Start Poetry in your existing project</span>
<span class="kw">poetry</span> init

<span class="cm"># 2. Pull in your current requirements</span>
cat requirements.txt | xargs <span class="kw">poetry</span> add

<span class="cm"># 3. Commit the lockfile — this is the important part</span>
git add poetry.lock pyproject.toml
git commit -m <span class="st">"chore: switch to poetry lockfile"</span>

<span class="cm"># 4. In CI — always install from lockfile, never re-resolve</span>
<span class="kw">poetry</span> install --no-root --only main

<span class="cm"># 5. Audit against known CVEs as a second layer</span>
pip-audit --requirement &lt;(<span class="kw">poetry</span> export -f requirements.txt)</pre>

<!-- TRANSITIVE -->
<h2>The dependency-of-a-dependency problem</h2>

<div class="callout danger">
  <div class="callout-label">Watch out</div>
  <p>The <code>termncolor</code> attack hid in a package you never directly installed. With Poetry, transitive dependencies are also pinned and hash-verified — so a poisoned update to <code>colorinal</code> after your lockfile was written fails at install time. Without a lockfile, the malicious version resolves silently on every fresh install, on every machine, in every CI run.</p>
</div>

<!-- STOLEN -->
<h2>What they're actually after</h2>

<p>Every campaign in this article targeted the same categories of assets. Once any of these leave your machine, you're in incident response mode.</p>

<div class="stolen-grid">
  <div class="stolen-item"><strong>Credentials</strong>SSH private keys, cloud IAM tokens</div>
  <div class="stolen-item"><strong>Cloud access</strong>AWS, GCP, Azure, Alibaba, Tencent</div>
  <div class="stolen-item"><strong>Kubernetes</strong>Service account tokens, kubeconfig</div>
  <div class="stolen-item"><strong>Env files</strong>API keys, database passwords, secrets</div>
  <div class="stolen-item"><strong>Browser data</strong>Chrome, Firefox, Brave, Edge cookies and saved passwords</div>
  <div class="stolen-item"><strong>Crypto wallets</strong>Seed phrases, private keys</div>
  <div class="stolen-item"><strong>CI/CD secrets</strong>GitHub Actions, GitLab CI environment variables</div>
  <div class="stolen-item"><strong>Source code</strong>.gitconfig, local scripts, internal tooling</div>
</div>

<!-- VECTORS -->
<h2>Attack vectors at a glance</h2>

<table class="vector-table">
  <thead><tr><th>Vector</th><th>How it works</th><th>Real example</th></tr></thead>
  <tbody>
    <tr><td>Typosquatting</td><td>One character off from a popular package name</td><td>colourama vs colorama</td></tr>
    <tr><td>Account compromise</td><td>Phish the maintainer, push a poisoned release directly</td><td>LiteLLM, chalk (npm)</td></tr>
    <tr><td>CI/CD poisoning</td><td>Inject into the build pipeline before the package is signed</td><td>Ultralytics Actions cache</td></tr>
    <tr><td>Transitive dep attack</td><td>Hide the malware in a dependency's dependency</td><td>termncolor → colorinal</td></tr>
    <tr><td>Combosquatting</td><td>Use names from another ecosystem to confuse users</td><td>Colorama cross-ecosystem campaign</td></tr>
    <tr><td>Dependency confusion</td><td>Publish a public package matching an internal name</td><td>company-internal-lib → PyPI</td></tr>
  </tbody>
</table>

<!-- ACTION LIST -->
<h2>What to do about it</h2>

<h3>This sprint</h3>
<div class="checklist">
  <div class="check-item"><div class="check-box"></div>Migrate to Poetry or Pipenv — commit <code>poetry.lock</code> to version control today</div>
  <div class="check-item"><div class="check-box"></div>Replace <code>pip install -r requirements.txt</code> with <code>poetry install --no-root --only main</code> in every CI job</div>
  <div class="check-item"><div class="check-box"></div>Add <code>pip-audit</code> or Dependabot to scan the lockfile on every PR</div>
  <div class="check-item"><div class="check-box"></div>Rotate credentials on any machine that ran bare <code>pip install</code> from a third-party package recently</div>
</div>

<h3>Structural hardening</h3>
<div class="checklist">
  <div class="check-item"><div class="check-box"></div>Enable PyPI Trusted Publishing for packages you maintain — creates cryptographic provenance attestations</div>
  <div class="check-item"><div class="check-box"></div>Enforce 2FA on all PyPI accounts, maintainer accounts included</div>
  <div class="check-item"><div class="check-box"></div>Audit GitHub Actions workflows for <code>pull_request_target</code> misuse and shared cache exposure</div>
  <div class="check-item"><div class="check-box"></div>Block binary and opaque files from being committed — prevents xz-utils-style build injection</div>
</div>

<h3>Runtime detection</h3>
<div class="checklist">
  <div class="check-item"><div class="check-box"></div>Alert on unexpected outbound connections following a package install</div>
  <div class="check-item"><div class="check-box"></div>Monitor IAM API calls — unusual <code>AssumeRole</code> volume is an early indicator</div>
  <div class="check-item"><div class="check-box"></div>Treat any new <code>.pth</code> file appearing in a Python environment as a P1 incident</div>
  <div class="check-item"><div class="check-box"></div>Set up version-change alerts for your most critical dependencies</div>
</div>

<div class="pullquote" style="margin-top:52px">
  <p>"What's unfolding isn't a string of unlucky breaks. It's the same pattern repeating across ecosystems: maintainers get phished, credentials get abused, and malicious code lingers far too long."</p>
  <cite>— Linux Security, 2025</cite>
</div>

<div class="callout good" style="margin-top:16px">
  <div class="callout-label">The bottom line</div>
  <p>A <code>poetry.lock</code> committed to git costs you nothing. An undetected <code>.pth</code> backdoor running on every Python startup across your Kubernetes fleet costs you everything. The trust that made PyPI the most productive package registry in software history is exactly what makes it dangerous — and a lockfile is the simplest thing standing between those two outcomes.</p>
</div>

</div><!-- /prose -->

<footer>
  Research sources: JFrog Security Research &nbsp;·&nbsp; Checkmarx Zero &nbsp;·&nbsp; Endor Labs &nbsp;·&nbsp; ReversingLabs &nbsp;·&nbsp; Zscaler ThreatLabz &nbsp;·&nbsp; PyPI Blog &nbsp;·&nbsp; Kaspersky GReAT &nbsp;·&nbsp; Linux Security<br>
  Published April 2026
</footer>

</div><!-- /page -->
</body>
</html>
