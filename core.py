import os
import json
from datetime import datetime
from colorama import Fore, Style
from typing import List, Dict, Any
from .headers_checker import check_headers
from .ssl_checker import check_ssl
from .param_discovery import discover_parameters
from .cookie_checker import check_cookies
from .crawler import crawl_endpoints
from .js_analyzer import analyze_js

try:
    # attempt to import the real implementation; silence type checkers if unresolved
    from .vuln_suggestion import error_based_check  # type: ignore
except Exception:
    # fallback stub so runtime and type checkers have a known symbol and signature
    def error_based_check(_url: str) -> List[Dict[str, Any]]:
        return []

def run_scan(url: str) -> bool:
    all_issues: List[Dict[str, Any]] = []
    try:


        print(Fore.WHITE + "[8/8] Parameter Error-Based Detection (SQLi & XSS)...")
        # call directly; error_based_check is already annotated to return List[Dict[str, Any]]
        error_issues = error_based_check(url) or []
        all_issues.extend(error_issues)

        print(Fore.WHITE + "[1/6] Checking Security Headers...")
        header_issues = check_headers(url) or []
        all_issues.extend(header_issues)

        print(Fore.WHITE + "[2/6] Checking SSL/TLS...")
        ssl_issues = check_ssl(url) or []
        all_issues.extend(ssl_issues)

        print(Fore.WHITE + "[3/6] Cookie Security Check...")
        cookie_issues = check_cookies(url) or []
        all_issues.extend(cookie_issues)

        print(Fore.WHITE + "[4/6] Parameter Discovery & Debug Check...")
        param_issues = discover_parameters(url) or []
        all_issues.extend(param_issues)

        print(Fore.WHITE + "[5/6] Endpoint Crawling...")
        crawl_issues = crawl_endpoints(url) or []
        all_issues.extend(crawl_issues)

        print(Fore.WHITE + "[6/6] JS Client-Side Analysis...")
        js_issues = analyze_js(url) or []
        all_issues.extend(js_issues)
    except Exception as e:
        print(Fore.RED + f"Scan error: {e}")
        return False

    # Tampilkan hasil
    print(Fore.GREEN + Style.BRIGHT + "\n" + "="*70)
    print(Fore.GREEN + Style.BRIGHT + "                  GEN Z SCAN RESULTS")
    print(Fore.GREEN + Style.BRIGHT + "="*70 + "\n")

    if not all_issues:
        print(Fore.GREEN + "🎉 Situs ini SUPER AMAN bro! No issues found 🔥\n")
    else:
        for i, issue in enumerate(all_issues, 1):
            risk = issue.get("risk", "")
            risk_color = Fore.RED if "Critical" in risk else Fore.LIGHTRED_EX if "High" in risk else Fore.YELLOW if "Medium" in risk else Fore.CYAN
            print(risk_color + f"[{i}] [{issue.get('risk')}] {issue.get('issue')}")
            safe_desc = str(issue.get('desc', '')).encode('ascii', 'replace').decode('ascii')
            safe_rec = str(issue.get('recommendation', 'Fix segera!')).encode('ascii', 'replace').decode('ascii')
            print(Fore.WHITE + f"    -> {safe_desc}")
            print(Fore.CYAN + f"    [Recommendation] {safe_rec}\n")

    # Export report
    success = export_report(all_issues, url)
    return bool(success)

def export_report(issues: List[Dict[str, Any]], url: str) -> bool:
    os.makedirs("report/output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_url = url.replace('https://', '').replace('http://', '').split('/')[0]
    json_path = f"report/output/{clean_url}_{timestamp}.json"
    html_path = f"report/output/{clean_url}_{timestamp}.html"

    # JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(issues, f, indent=4, ensure_ascii=False)

    # HTML
    template_path = "report/templates/report_template.html"
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as t:
            template = t.read()

        content_list: List[str] = []
        for i in issues:
            risk_class = i.get("risk", "").lower()
            icon = "🔥" if "critical" in risk_class else "⚠️" if "high" in risk_class else "ℹ️" if "medium" in risk_class else "✅"
            content_list.append(
                f'<div class="issue risk-{risk_class}">'
                f'   <span class="issue-icon">{icon}</span>'
                f'   <strong>[{i.get("risk")}] {i.get("issue")}</strong><br>'
                f'   <span class="desc">{i.get("desc", "")}</span><br>'
                f'   <span class="rekom">💡 Rekomendasi: {i.get("recommendation", "Perbaiki segera!")}</span>'
                f'</div>'
            )
        content = ''.join(content_list)

        html = template.replace('{{CONTENT}}', content) \
                       .replace('{{URL}}', url) \
                       .replace('{{TIME}}', datetime.now().strftime("%d %B %Y - %H:%M")) \
                       .replace('{{TOTAL}}', str(len(issues)))

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(Fore.GREEN + f"[OK] Report HTML Neon: {html_path}")
    print(Fore.GREEN + f"[OK] Report JSON: {json_path}")

    return True