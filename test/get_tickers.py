import sys, os, json, requests
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config.URL as URL
from tools.quotation_api import *

"""
response.txt example

[
    {
        "market": "KRW-BTC",
        "korean_name": "비트코인",
        "english_name": "Bitcoin"
    },
    ...
]
"""

if __name__ == '__main__':
    krw_codes = get_tickers(exclude_warning=False)
    for code in krw_codes:
        if code.split("-")[0] != "KRW": print(code)
    print(f"KRW codes ({len(krw_codes)}) :")
    print(krw_codes[:10], end="..\n\n")


    nkrw_codes = get_tickers(exclude_warning=False, KRW=False)
    for code in nkrw_codes:
        if code.split("-")[0] == "KRW": print(code)
    print(f"NKRW codes ({len(nkrw_codes)}) :")
    print(nkrw_codes[:10], end="..\n\n")

    codes_safe = get_tickers(exclude_warning=True)
    print(f"Safe KRW codes ({len(codes_safe)}) :")
    print(codes_safe[:10], end="..\n")


