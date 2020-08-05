# coding=utf-8

import os
import sys

from lib.banner import show_banner
from lib.conf import MITM_RUN

def main():
    show_banner()
    if "win" in sys.platform:
        mitm_type = input("[*]Please select a way to start mitm on Windows:\n  1.mitmdump\n  2.mitmweb\n[*]Choose: ")
        if int(mitm_type) < 1 or int(mitm_type) > 2:
            print("[-]Input must between 1-2.")
            sys.exit(1)
    else:
        mitm_type = input("[*]Please select a way to start mitm on Linux:\n  1.mitmdump\n  2.mitmweb\n  3.mitmproxy\n[*]Choose: ")
        if int(mitm_type) < 1 or int(mitm_type) > 3:
            print("[-]Input must between 1-3.")
            sys.exit(1)

    print("[*]Startup " + MITM_RUN[int(mitm_type) - 1] + " and load addon...")
    addon_path = os.getcwd() + "/mitm_addon.py"
    try:
        os.system(MITM_RUN[int(mitm_type) - 1] + " -s " + addon_path)
    except KeyboardInterrupt as e:
        print("[*]User aborted.")
        print("[*]Passive Reflection XSS scan result is saved in: ./result/result.txt")

if __name__ == '__main__':
    main()
