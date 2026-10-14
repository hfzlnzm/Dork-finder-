#!/usr/bin/env python3
"""Dork Finder scanner: light exposure checks for a domain YOU OWN.
Ownership is verified first: place your own secret token in
https://<domain>/.well-known/dorkfinder-verify.txt and pass it with --token.
Output JSON can be imported into index.html. Uses stdlib only."""
import argparse, json, re, sys, time, urllib.request, urllib.error
from urllib.parse import urlparse

UA = "DorkFinder-SelfCheck/1.0 (own-domain exposure check)"
VERIFY = "/.well-known/dorkfinder-verify.txt"
DOMAIN_RE = re.compile(r"^(?=.{4,253}$)([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,24}$")
nothtml = lambda b: "<html" not in b[:500].lower()
CHECKS = [  # id, paths, test(body)->bool, note
 ("env", ["/.env"], lambda b: nothtml(b) and re.search(r"^[A-Za-z0-9_]+\s*=", b, re.M), ".env readable"),
 ("git", ["/.git/HEAD"], lambda b: b.startswith("ref:"), ".git/HEAD readable"),
 ("sql", ["/backup.sql", "/db.sql", "/dump.sql", "/database.sql"], lambda b: re.search(r"CREATE TABLE|INSERT INTO", b), "SQL dump readable"),
 ("bak", ["/backup.zip", "/backup.tar.gz", "/site.zip", "/www.zip"], lambda b: b.startswith("PK\x03\x04") or b.startswith("\x1f\x8b"), "backup archive downloadable"),
 ("log", ["/error.log", "/debug.log", "/access.log", "/logs/error.log"], lambda b: nothtml(b) and re.search(r"\d{4}[-/]\d{2}[-/]\d{2}|\[error\]|GET /", b), "log file readable"),
 ("php", ["/phpinfo.php", "/info.php"], lambda b: "phpinfo()" in b or "PHP Version" in b, "phpinfo page present"),
 ("dir", ["/", "/uploads/", "/images/", "/files/", "/backup/"], lambda b: "Index of /" in b, "directory listing enabled"),
 ("login", ["/admin", "/login", "/wp-login.php", "/administrator"], lambda b: 'type="password"' in b.lower(), "login/admin panel reachable"),
]

def fetch(url, domain):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            host = (urlparse(r.geturl()).hostname or "").lower()
            if host not in (domain, "www." + domain):
                return 0, ""
            return r.status, r.read(65536).decode("latin-1")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return None, ""

def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("domain"); a.add_argument("--token", required=True, help="secret string you placed in the verify file")
    a.add_argument("--out"); a.add_argument("--delay", type=float, default=1.0)
    x = a.parse_args()
    d = x.domain.lower().strip()
    if not DOMAIN_RE.match(d): sys.exit("Invalid domain (IP addresses are not allowed).")
    if len(x.token) < 12: sys.exit("Token must be at least 12 characters.")
    code, body = fetch("https://" + d + VERIFY, d)
    if code != 200 or body.strip() != x.token:
        sys.exit("Ownership not verified. Put the token in https://%s%s and retry." % (d, VERIFY))
    print("Ownership verified. Scanning %s (1 request per path, %.1fs delay)..." % (d, x.delay))
    results = []
    for cid, paths, test, note in CHECKS:
        hit, seen = None, False
        for p in paths:
            code, body = fetch("https://" + d + p, d); time.sleep(x.delay)
            if code is None: continue
            seen = True
            if code == 200 and test(body): hit = p; break
        if hit: results.append({"id": cid, "status": "2", "note": "%s: %s" % (note, hit)})
        elif seen: results.append({"id": cid, "status": "1", "note": "no match on %d path(s)" % len(paths)})
        print("%-6s %s" % (cid, "EXPOSED " + hit if hit else ("clean" if seen else "unreachable")))
    out = x.out or "dork-results-%s.json" % d
    json.dump({"domain": d, "tool": "scanner.py", "results": results}, open(out, "w"), indent=2)
    print("Saved", out, "- import it in the web tool.")

if __name__ == "__main__":
    main()
