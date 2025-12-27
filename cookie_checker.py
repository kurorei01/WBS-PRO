import requests
from requests.cookies import RequestsCookieJar
from typing import List, Dict

def check_cookies(url: str) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    try:
        resp = requests.get(url, timeout=10, verify=False)
        cookies: RequestsCookieJar = resp.cookies
        for cookie in cookies:
            attrs: List[str] = []
            if not getattr(cookie, "secure", False):
                attrs.append("Missing Secure flag → Rentan MITM")
            # Use the cookie's rest dict to check nonstandard attributes like HttpOnly and SameSite
            rest = getattr(cookie, "rest", {}) or {}
            if not bool(rest.get("HttpOnly")):
                attrs.append("Missing HttpOnly → Rentan XSS")
            # SameSite agak tricky, cek manual
            same_site = rest.get('SameSite')
            if same_site not in ['Strict', 'Lax']:
                attrs.append("Weak/Missing SameSite → Rentan CSRF")
            if attrs:
                issues.append({
                    "issue": f"Insecure cookie: {getattr(cookie, 'name', '')}",
                    "risk": "High" if len(attrs) > 1 else "Medium",
                    "desc": "; ".join(attrs),
                    "recommendation": "Set Secure=True, HttpOnly=True, SameSite='Strict' di server"
                })
    except Exception as e:
        issues.append({
            "issue": "Cookie check failed",
            "risk": "Low",
            "desc": str(e),
            "recommendation": "Cek koneksi atau SSL"
        })
    return issues