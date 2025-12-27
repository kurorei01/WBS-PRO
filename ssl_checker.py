import requests
from typing import List, Dict

def check_ssl(url: str) -> List[Dict[str, str]]:
    """Basic SSL/header check (keeps same heuristics as headers check)."""
    issues: List[Dict[str, str]] = []
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': 'GEN-Z-SCAN/1.0 (+ethical)'})
        
        response = session.get(url, timeout=15, allow_redirects=True, verify=False)
        headers = response.headers

        must_have = {
            "Strict-Transport-Security": "Missing HSTS → Rentan SSL stripping",
            "Content-Security-Policy": "Missing CSP → Rentan XSS",
            "X-Frame-Options": "Missing X-Frame-Options → Rentan clickjacking",
            "X-Content-Type-Options": "Missing nosniff → Rentan MIME attack",
            "Referrer-Policy": "Missing Referrer-Policy → Bocor info referrer",
            "Permissions-Policy": "Missing Permissions-Policy → Fitur browser tidak dibatasi",
        }

        for header, desc in must_have.items():
            if header.lower() not in {h.lower() for h in headers}:
                issues.append({
                    "issue": f"Missing {header}",
                    "risk": "High",
                    "desc": desc,
                    "recommendation": f"Tambahkan header {header} di server (Nginx/Apache/Cloudflare)"
                })

        if any(h.lower() in ["server", "x-powered-by", "x-aspnet-version"] for h in headers):
            issues.append({
                "issue": "Server information exposed",
                "risk": "Medium",
                "desc": "Header seperti Server atau X-Powered-By bocorkan tech stack",
                "recommendation": "Hapus atau samarkan header tersebut di konfigurasi server"
            })

    except requests.exceptions.SSLError:
        issues.append({
            "issue": "SSL Error saat connect",
            "risk": "High",
            "desc": "Certificate invalid atau konfigurasi SSL bermasalah",
            "recommendation": "Perbaiki SSL certificate (gunakan Let's Encrypt)"
        })
    except requests.exceptions.ConnectionError:
        issues.append({
            "issue": "Cannot connect to site",
            "risk": "Critical",
            "desc": "Domain tidak bisa dijangkau atau server down",
            "recommendation": "Cek apakah situs benar-benar online"
        })
    except requests.exceptions.Timeout:
        issues.append({
            "issue": "Connection timeout",
            "risk": "Medium",
            "desc": "Server lambat respon",
            "recommendation": "Coba lagi nanti atau cek performa server"
        })
    except Exception as e:
        issues.append({
            "issue": "Unknown error saat cek headers",
            "risk": "Medium",
            "desc": str(e),
            "recommendation": "Coba URL lain atau update tool"
        })

    return issues