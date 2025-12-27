import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from typing import List, Dict


def analyze_js(url: str) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    try:
        resp = requests.get(url, timeout=10, verify=False)
        soup = BeautifulSoup(resp.text, 'html.parser')

        scripts = []
        # Inline scripts
        for s in soup.find_all('script'):
            if s.string:
                scripts.append(s.string) # type: ignore
        # External scripts
        for s in soup.find_all('script', src=True):
            try:
                js_url = urljoin(url, s['src']) # type: ignore
                r = requests.get(js_url, timeout=10, verify=False)
                scripts.append(r.text) # type: ignore
            except Exception:
                continue

        sinks = ['innerHTML', 'document.write', 'eval', 'setTimeout', 'location.href']
        for content in scripts: # type: ignore
            for sink in sinks:
                if re.search(rf'\.{sink}\s*\(', str(content)): # type: ignore
                    issues.append({
                        "issue": f"Potential DOM vuln sink: {sink}",
                        "risk": "High",
                        "desc": "Code JS pakai sink berbahaya → Risk DOM XSS kalau input user tidak sanitized",
                        "recommendation": "Ganti ke textContent atau sanitize input. Test dengan DOMPurify."
                    })
    except Exception:
        issues.append({"issue": "JS analysis failed", "risk": "Medium", "desc": "No JS or error"})
    return issues