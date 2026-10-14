# Dork Finder – Exposure Self-Check

Final Year Project, Bachelor in Cybersecurity.

A defensive tool that helps website owners find information their own domain leaks through search engines and common misconfigurations. It has two parts:

1. **Web tool (`index.html`)** – builds search-engine dork queries for your domain, maps each to an OWASP Top 10 (2021) category and risk level, gives a fix, tracks your findings, and exports a Markdown report. Runs fully in the browser; no data is sent anywhere. English and Bahasa Melayu.
2. **Scanner (`scanner.py`)** – optional Python script (standard library only) that checks a small set of well-known paths on your domain and writes a JSON file you can import into the web tool. It refuses to run unless you prove ownership.

## Usage

**Web tool:** open `index.html` (or the GitHub Pages link), enter your domain, tick the permission box, then work through the dork list. Mark each as Clean/Exposed, add notes, export the report.

**Scanner:**
```
# 1. create a secret (12+ chars) and publish it on your own site
echo "my-long-secret-token" > .well-known/dorkfinder-verify.txt
# 2. run
python3 scanner.py example.com --token my-long-secret-token
# 3. in the web tool, use "Import scanner results" with the JSON file
```
The scanner sends one GET request per path (1s delay), identifies itself in the User-Agent, rejects IP addresses, and ignores redirects to other hosts.

## Method (for the report)

- **Approach:** Design Science Research – build an artefact, evaluate it, refine.
- **Research questions:** (1) How well do search-engine dorks and lightweight path checks detect common exposure on a domain compared with manual review? (2) Does mapping findings to OWASP categories with fixes help owners act on them?
- **Evaluation plan:** deploy a test site you control (e.g. a small web app with planted `.env`, `.git`, `backup.sql`, directory listing, `phpinfo.php`, and a few clean controls). Run the tool and compare against a manually verified ground truth. Report true/false positives, false negatives, precision and recall per check, and time taken. Compare features with GHDB, Pagodo and DorkSearch.
- **Risk scoring:** each finding is weighted by tier (Critical 5, High 4, Medium 3, Low 2, Info 1); the score is exposed weight divided by total weight. This is a simple triage aid, not CVSS. Discuss this limitation.

## Limitations

- Dork results depend on what search engines have indexed and change over time.
- Dorks are opened manually, so the review step is human. Search engines may rate-limit or block automated queries, which is why the tool does not automate them.
- Scanner checks use a fixed path list and content signatures to reduce false positives, but cannot find custom-named files.
- Not a substitute for a full vulnerability assessment.

## Ethics and law

Use only on domains you own or have written permission to test. Unauthorised access is an offence under Malaysia's Computer Crimes Act 1997 (Akta Jenayah Komputer 1997). Personal data found should be handled under the PDPA 2010.

## Licence

MIT (add a `LICENSE` file).
