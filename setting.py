THREADS = 5  # Multi-thread buat param discovery & crawl
TIMEOUT = 10  # Detik
WORDLISTS = {
    'params': 'wordlist/common_params.txt',
    'debug': 'wordlist/debug_params.txt',
    'endpoints': 'wordlist/common_endpoints.txt',
    'dom_sinks': 'wordlist/dom_xss_sinks.txt'
}
REPORT_STYLE = 'neon_genz'  # Untuk HTML export