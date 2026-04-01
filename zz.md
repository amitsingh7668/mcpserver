# The Poisoned Package: How PyPI Became a Battleground

**Security Deep Dive · Supply Chain · April 2026 · 12 min read**

---

You run `pip install`. The name looks right. You've used it before. Then your SSH keys, cloud tokens, and Kubernetes secrets leave your machine — silently, automatically, without a single warning.

This isn't a hypothetical. It happened to 95 million downloads worth of users in March 2026 alone.

---

## By the numbers

| Metric | Figure |
|---|---|
| LiteLLM daily downloads at time of breach | **3.4 million** |
| Malicious packages in 2025 cloud-credential campaign | **20** |
| Downloads before that campaign was detected | **14,100+** |
| LiteLLM monthly downloads — all exposed during TeamPCP | **95 million** |
| Drop in simple typosquatted PyPI malware, 2023 → 2024 | **−85%** |
| Countries hit by JarkaStealer AI-lure campaign | **30+** |
| Downloads of one JFrog-detected malicious batch | **~30,000** |

That 85% drop in typosquatting sounds like progress. It isn't. Attackers stopped publishing junk packages and started compromising *real, trusted ones* instead. Fewer incidents — far greater blast radius.

---

## The attacks

Not CVEs in a spreadsheet. Real packages, real engineers, real production systems.

---

### 🔴 `CRITICAL` — Ultralytics · December 2024

The ML vision library with tens of millions of installs was backdoored through a **compromised GitHub Actions cache**. Attackers injected code during the build phase, then published poisoned versions `8.3.41`, `8.3.42`, `8.3.45`, and `8.3.46` using an unrevoked PyPI API token the project had forgotten to rotate.

`CI/CD cache poisoning` · `unrevoked API token` · `build-phase injection`

---

### 🔴 `CRITICAL` — Cloud Credential Campaign · March 2025

ReversingLabs found 20 packages disguised as cloud SDKs and time utilities — `acloud-client`, `enumer-iam`, `snapshot-photo`. Each hid a Base64-encoded payload inside `setup.py`, which runs automatically the moment you type `pip install`. AWS, Alibaba Cloud, and Tencent Cloud tokens were the targets. 14,100 downloads before anyone noticed.

`setup.py execution` · `cloud token theft` · `14,100 downloads`

---

### 🟡 `HIGH` — Colorama Typosquatting · May 2025

Checkmarx Zero found a technique nobody had documented before: **cross-ecosystem name confusion**. Attackers used NPM package names to target PyPI users — betting that Python developers wouldn't think to check npm when vetting imports. Windows payloads used DLL side-loading with Task Scheduler persistence. Linux payloads established encrypted reverse shells exfiltrated via Pastebin.

`cross-ecosystem confusion` · `DLL side-loading` · `reverse shell`

---

### 🟡 `HIGH` — termncolor / colorinal · July 2025

`termncolor` looked harmless. It was. The payload lived in its dependency, `colorinal` — a package you never installed directly. Once loaded, it ran DLL side-loading, established C2 communication, and enabled remote code execution. The threat actor had 90,692 messages logged in their Zulip C2 channel before it was caught.

`transitive dependency` · `DLL side-loading` · `884 combined downloads`

---

### 🔴 `CRITICAL` — SilentSync RAT · August 2025

A full Python-based Remote Access Trojan inside two packages typosquatting on a niche Argentine health system library. It ran remote command execution, file exfiltration, screen capture, and browser credential harvesting across Chrome, Brave, Edge and Firefox — all phoning home over HTTP with periodic beaconing. The obscure target was chosen precisely because nobody monitors it.

`full RAT` · `browser harvesting` · `HTTP C2 beaconing`

---

### 🔴 `CRITICAL` — LiteLLM / TeamPCP · March 2026

The biggest one yet. TeamPCP — who'd previously hit the Trivy vulnerability scanner — compromised LiteLLM and pushed versions `1.82.7` and `1.82.8`. Version `1.82.8` installed a `.pth` file into the Python environment. Python processes every `.pth` file at startup, so the payload ran **even on machines where LiteLLM was never actually called.**

Three-stage attack:
1. Harvest SSH keys, cloud tokens, Kubernetes secrets, crypto wallets, `.env` files
2. Move laterally — deploy privileged pods to every Kubernetes node
3. Install a `systemd` backdoor polling for additional payloads

`.pth file persistence` · `95M monthly downloads exposed` · `Kubernetes lateral movement` · `systemd backdoor`

---

> "Lack of moderation and automated security controls in public repositories allow even inexperienced attackers to spread malware — through typosquatting, dependency confusion, or simple social engineering."
>
> — JFrog Security Research

---

## Why pip doesn't see any of this

`pip` is good at installing packages. That's a different job from securing them.

When you run `pip install requests`, pip fetches whatever the registry currently says is the latest compatible version. It doesn't check whether today's version matches what you reviewed last month. It doesn't lock transitive dependencies. It has no concept of "this hash doesn't match what we installed before."

A `requirements.txt` with `requests>=2.28.0` is functionally an instruction to install whatever the attacker publishes next. The attacker only needs to push `2.28.1`.

### pip vs Poetry

| | pip (bare) | Poetry |
|---|:---:|:---:|
| Lockfile by default | ✗ | ✓ `poetry.lock` |
| Pins transitive dependencies | ✗ | ✓ full tree |
| SHA-256 hash verification | ✗ | ✓ every install |
| Detects tampered packages | ✗ | ✓ hash mismatch = abort |
| Silent upgrades | ✗ possible | ✓ requires explicit command |
| Dev/prod separation | ✗ | ✓ dependency groups |
| Diffs visible in PRs | ✗ | ✓ fully diffable |

---

## What Poetry actually does

Poetry doesn't stop bad packages from being published. What it does is give you a tamper-evident record of exactly what you installed and when. The moment an attacker swaps out a package version after your lockfile was written, the hash stops matching and the install fails loudly.

```bash
# Old workflow — pip silently pulls whatever is newest
pip install litellm

# Poetry workflow — pinned and hash-verified
poetry add litellm
# Writes to poetry.lock:
# litellm = {version = "1.82.6", hash = "sha256:a3f2..."}
# Committed to git. Every change shows up in a PR diff.

# TeamPCP pushes litellm 1.82.7 with malicious payload
poetry install
# ✗  Hash mismatch for litellm==1.82.7
# ✗  Expected sha256:a3f2...  Got sha256:c0de...
# ✗  Installation aborted.
```

### Migration in five commands

```bash
# 1. Start Poetry in your existing project
poetry init

# 2. Pull in your current requirements
cat requirements.txt | xargs poetry add

# 3. Commit the lockfile — this is the important part
git add poetry.lock pyproject.toml
git commit -m "chore: switch to poetry lockfile"

# 4. In CI — always install from lockfile, never re-resolve
poetry install --no-root --only main

# 5. Audit against known CVEs as a second layer
pip-audit --requirement <(poetry export -f requirements.txt)
```

---

## The dependency-of-a-dependency problem

> **Watch out:** The `termncolor` attack hid in a package you never directly installed. With Poetry, transitive dependencies are also pinned and hash-verified — so a poisoned update to `colorinal` after your lockfile was written fails at install time. Without a lockfile, the malicious version resolves silently on every fresh install, on every machine, in every CI run.

---

## What they're actually after

Every campaign above targeted the same categories of assets. Once any of these leave your machine, you're in incident response.

| Category | What's at risk |
|---|---|
| **Credentials** | SSH private keys, cloud IAM tokens |
| **Cloud access** | AWS, GCP, Azure, Alibaba, Tencent |
| **Kubernetes** | Service account tokens, kubeconfig |
| **Env files** | API keys, database passwords, secrets |
| **Browser data** | Chrome, Firefox, Brave, Edge — cookies and saved passwords |
| **Crypto wallets** | Seed phrases, private keys |
| **CI/CD secrets** | GitHub Actions, GitLab CI environment variables |
| **Source code** | `.gitconfig`, local scripts, internal tooling |

---

## Attack vectors

| Vector | How it works | Real example |
|---|---|---|
| Typosquatting | One character off from a popular name | `colourama` vs `colorama` |
| Account compromise | Phish the maintainer, push a poisoned release | LiteLLM, `chalk` on npm |
| CI/CD poisoning | Inject into the build pipeline before signing | Ultralytics Actions cache |
| Transitive dep attack | Hide the malware in a dependency's dependency | `termncolor` → `colorinal` |
| Combosquatting | Use names from another ecosystem to confuse users | Colorama cross-ecosystem campaign |
| Dependency confusion | Publish a public package matching an internal name | `company-internal-lib` on PyPI |

---

## What to do about it

### This sprint

- [ ] Migrate to Poetry or Pipenv — commit `poetry.lock` to version control today
- [ ] Replace `pip install -r requirements.txt` with `poetry install --no-root --only main` in every CI job
- [ ] Add `pip-audit` or Dependabot to scan the lockfile on every PR
- [ ] Rotate credentials on any machine that ran bare `pip install` from a third-party package recently

### Structural hardening

- [ ] Enable PyPI Trusted Publishing for packages you maintain — creates cryptographic provenance attestations
- [ ] Enforce 2FA on all PyPI accounts, maintainer accounts included
- [ ] Audit GitHub Actions workflows for `pull_request_target` misuse and shared cache exposure
- [ ] Block binary and opaque files from being committed — prevents xz-utils-style build injection

### Runtime detection

- [ ] Alert on unexpected outbound connections following a package install
- [ ] Monitor IAM API calls — unusual `AssumeRole` volume is an early indicator
- [ ] Treat any new `.pth` file in a Python environment as a P1 incident
- [ ] Set up version-change alerts for your most critical dependencies

---

> "What's unfolding isn't a string of unlucky breaks. It's the same pattern repeating across ecosystems: maintainers get phished, credentials get abused, and malicious code lingers far too long."
>
> — Linux Security, 2025

---

A `poetry.lock` committed to git costs nothing. An undetected `.pth` backdoor running on every Python startup across your Kubernetes fleet costs everything. The trust that made PyPI the most productive package registry in software history is exactly what makes it dangerous — and a lockfile is the simplest thing standing between those two outcomes.

---

*Sources: JFrog · Checkmarx Zero · Endor Labs · ReversingLabs · Zscaler ThreatLabz · PyPI Blog · Kaspersky GReAT · Linux Security · April 2026*
