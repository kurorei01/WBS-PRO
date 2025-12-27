import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
from typing import List, Dict, Set
from config.setting import THREADS

def crawl_endpoints(url: str, max_depth: int = 2) -> List[Dict[str, str]]:
    visited: Set[str] = set()
    endpoints: Set[str] = set()
    issues: List[Dict[str, str]] = []

    def crawl_page(page_url: str, depth: int):
        if depth > max_depth or page_url in visited:
            return
        visited.add(page_url)
        try:
            resp = requests.get(page_url, timeout=10, verify=False)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_url = urljoin(page_url, str(link['href']))
                if urlparse(full_url).netloc == urlparse(url).netloc:
                    endpoints.add(full_url)
            # Cari JS files buat potential endpoints
            for script in soup.find_all('script', src=True):
                js_url = urljoin(page_url, str(script['src']))
                endpoints.add(js_url)
        except:
            pass

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(crawl_page, url, 0)]
        # Simplified crawling: wait for initial tasks to complete
        for _ in concurrent.futures.as_completed(futures):
            pass

    if endpoints:
        issues.append({
            "issue": f"Discovered {len(endpoints)} endpoints",
            "risk": "Info",
            "desc": "Endpoint ditemukan via crawl: " + ', '.join(list(endpoints)[:5]) + '...',
            "recommendation": "Audit setiap endpoint buat vulns. Gunakan robots.txt buat batasi crawl."
        })
    return issues