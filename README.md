# Site Exposure Audit

**Automating Open Source Intelligence (OSINT): A Framework for Passive Threat Intelligence Gathering via Advanced Google Dorking**

**Live tool:** https://hfzlnzm.github.io/Site-exposure-audit/

Site Exposure Audit is a browser-based tool that automates Google dorking against a domain you own. With one click it runs a fixed library of dork queries, collects the publicly indexed results, and (optionally) uses an AI model to turn them into a written exposure report.

> **Authorized use only.** Scan only domains you own or have written permission to test. The tool asks you to confirm this before every scan.

---

## How it works

```
Domain  ->  22 fixed dork queries  ->  Serper (Google results)  ->  Filter to target domain  ->  Report
```

1. **Input:** you enter a domain and confirm you are authorized to test it.
2. **Collection:** the tool runs 22 dork queries, all scoped with `site:yourdomain.com`, through the Serper API, which returns real Google results.
3. **Filtering:** only results that belong to the target domain or its subdomains are kept.
4. **Reporting:**
   - **With only a Serper key:** results are grouped by category with links.
   - **With an Anthropic key as well:** Claude writes a structured exposure report (findings, why they matter, remediation) from those results only, and you can ask follow-up questions.

The tool is **passive**: it only queries a search engine for already-indexed information. It never sends a request to the target website.

---

## Dork categories

| Category | Examples of what is checked |
|---|---|
| Exposed files | `.env`, SQL/database files, logs, backups, config files with secrets, private keys |
| Sensitive documents | PDF, Word, Excel and CSV files marked confidential or containing passwords |
| Open directories | `index of /` listings, folders named backup, config or uploads |
| Backup archives | zip, tar, gz, rar, 7z files and `backup` / `dump` URLs |
| Version control | `.git`, `.svn`, `.hg` exposure |
| Admin / login panels | admin, login, phpMyAdmin, Adminer, cPanel, Webmin |
| Misconfig files | `phpinfo`, PHP config files, Apache status pages |
| Error messages & debug | SQL errors, fatal errors, stack traces |
| API & dev environments | Swagger, GraphQL, staging, dev and test pages |
| Subdomains | Indexed subdomains of the target |

The full list lives in the `DORKS` array inside `index.html`. To add a dork, add a line with a category name and a query, using `{d}` where the domain goes.

---

## Using the tool

1. Open the live link above.
2. Enter your **Serper API key** (required). Get one at [serper.dev](https://serper.dev).
3. Optionally enter an **Anthropic API key** for the AI report and follow-ups. Get one at [console.anthropic.com](https://console.anthropic.com). The API is billed separately from a Claude subscription.
4. Enter the domain, tick the authorization box, and start the scan.
5. Open the "dork queries run" dropdown to see every query that was executed and how many results each returned.

Recent audits are saved in the sidebar so you can reopen them.

---

## Privacy and security

- API keys are stored only in **your own browser** (`localStorage`). They are never sent anywhere except directly to Serper and Anthropic.
- No keys are stored in this repository. Never commit a key to it.
- Set a monthly spend limit in your Anthropic console, and watch your Serper credit balance.

---

## Limitations

- Results depend on what Google has indexed. **No results does not mean the site is safe**; it only means nothing was indexed for that query.
- Search results can include false positives, so confirm every finding manually before acting on it.
- Each scan uses 22 Serper credits.
- AI-written reports can contain mistakes. Treat them as a draft, not a final verdict.
- Follow-up questions answer from the scan results already in the chat.

---

## Project structure

```
index.html   The whole tool (HTML, CSS and JavaScript in one file)
README.md    This file
```

Hosted on GitHub Pages.

---

## Disclaimer

This project is for education and for auditing assets you are authorized to assess. The author is not responsible for misuse. Scanning systems without permission may be illegal in your country.
