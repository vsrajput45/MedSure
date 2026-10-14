import urllib.request
import json
import sys

urls = [
    "http://localhost:3000",
    "http://localhost:3000/dashboard",
    "http://localhost:3000/triage",
    "http://localhost:3000/bills/upload",
    "http://localhost:3000/reference-rates",
    "http://localhost:3000/demo",
    "http://127.0.0.1:8000/health",
    "http://127.0.0.1:8000/api/v1/dashboard/summary",
    "http://127.0.0.1:8000/api/v1/reference-rates",
    "http://127.0.0.1:8000/api/v1/bills"
]

all_passed = True
print("--- LIVE VERIFICATION OF MEDSURE PLATFORM ---")
for url in urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MEDSURE-Verification"})
        with urllib.request.urlopen(req, timeout=5) as response:
            code = response.getcode()
            print(f"[SUCCESS {code}] {url}")
    except Exception as e:
        print(f"[FAILED] {url} - Error: {e}")
        all_passed = False

if all_passed:
    print("\nALL 10 ENDPOINTS AND PAGES ARE HEALTHY AND SERVING TRAFFIC!")
    sys.exit(0)
else:
    print("\nSome endpoints failed.")
    sys.exit(1)
