import requests
from colorama import Fore
import time
from typing import List, Dict

COMMON_PARAMS = 'wordlist/common_params.txt'
DEBUG_PARAMS = 'wordlist/debug_params.txt'


def load_wordlist(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception:
        return []


def discover_parameters(url: str) -> List[Dict[str, str]]:
    issues: List[Dict[str, str]] = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'GEN-Z-SCAN/2.0 (+ethical)'})

    try:
        base_resp = session.get(url, timeout=10, verify=False)
        base_len = len(base_resp.text)
        base_status = base_resp.status_code
    except Exception:
        return [{"issue": "Cannot reach base URL", "risk": "High", "desc": "Site down atau blokir request"}]

    # Load wordlists
    params = load_wordlist(COMMON_PARAMS) + load_wordlist(DEBUG_PARAMS)

    print(Fore.WHITE + "[+] Auto discovering hidden/debug parameters... (this may take a while)")

    for param in params:
        try:
            test_url = f"{url}?{param}=GENZTEST" if '?' not in url else f"{url}&{param}=GENZTEST"
            resp = session.get(test_url, timeout=10, verify=False)

            # Heuristic detection
            diff_len = abs(len(resp.text) - base_len)
            if (resp.status_code != base_status or
                diff_len > 100 or
                "error" in resp.text.lower() or
                "database" in resp.text.lower() or
                "sql" in resp.text.lower() or
                "debug" in resp.text.lower() or
                "stack" in resp.text.lower()):

                risk = "High" if any(k in param.lower() for k in ["debug", "admin", "db", "config", "env"]) else "Medium"
                issues.append({
                    "issue": f"Potential hidden/debug parameter: {param}",
                    "risk": risk,
                    "desc": f"Response berubah (status: {resp.status_code}, length diff: {diff_len}) → Mungkin accept param ini atau bocor info!",
                    "recommendation": f"Cek manual {test_url} dan pastikan tidak expose debug/DB info. Hapus atau validasi param tidak digunakan."
                })
        except Exception:
            pass
        time.sleep(0.2)  # Be gentle, anti-rate limit

    return issues or [{"issue": "No hidden/debug parameters detected", "risk": "Low", "desc": "Bagus! Tapi cek manual tetap ya."}]