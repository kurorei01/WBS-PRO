import requests
from typing import List, Dict, Any

def blind_sqli_check(url: str) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'GEN-Z-SCAN/5.0 (+ethical)'})

    # Common vulnerable parameters
    common_params = ['id', 'q', 'search', 'page', 'cat', 'category', 'product', 'user', 'query', 'name']

    try:
        # Get base response (keep the request for baseline but avoid unused variable)
        session.get(url, timeout=10, verify=False)

        for param in common_params:
            # Test 1: Normal value
            normal_url = f"{url}?{param}=1" if '?' not in url else f"{url}&{param}=1"
            # Test 2: Potentially true condition
            true_url = f"{url}?{param}=1 AND 1=1" if '?' not in url else f"{url}&{param}=1 AND 1=1"
            # Test 3: Potentially false condition
            false_url = f"{url}?{param}=1 AND 1=2" if '?' not in url else f"{url}&{param}=1 AND 1=2"

            try:
                normal_resp = session.get(normal_url, timeout=10, verify=False)
                true_resp = session.get(true_url, timeout=10, verify=False)
                false_resp = session.get(false_url, timeout=10, verify=False)

                normal_len = len(normal_resp.text)
                true_len = len(true_resp.text)
                false_len = len(false_resp.text)

                len_diff_threshold = 100  # Beda panjang >100 karakter dianggap signifikan

                # Blind boolean-based heuristic
                if (abs(true_len - normal_len) < len_diff_threshold and
                    abs(false_len - normal_len) > len_diff_threshold * 2):
                    issues.append({
                        "issue": f"Potential Blind SQL Injection (Boolean-Based)",
                        "risk": "Critical",
                        "desc": f"Parameter: {param} → Response length berubah drastis saat kondisi false (1=2)",
                        "recommendation": "Gunakan prepared statements & input validation. Test manual dengan time-based payload seperti SLEEP(5)"
                    })

                elif (abs(true_len - false_len) > len_diff_threshold * 3):
                    issues.append({
                        "issue": f"Potential Blind SQL Injection (Content Difference)",
                        "risk": "High",
                        "desc": f"Parameter: {param} → Response length beda signifikan antara true/false condition",
                        "recommendation": "Periksa query database, pastikan tidak concat input langsung"
                    })

            except:
                continue

    except Exception as e:
        issues.append({
            "issue": "Blind SQLi check failed",
            "risk": "Low",
            "desc": str(e),
            "recommendation": "Cek koneksi atau SSL"
        })

    return issues