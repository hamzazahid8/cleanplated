#!/usr/bin/env python3
"""
Deploy PurePlated Pinterest Automation Scenario to Make.com
----------------------------------------------------------
Deploys and synchronizes the Pinterest recipe publishing scenario
under Team ID 2010020 on https://us2.make.com.
"""

import os
import sys
import json
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLUEPRINT_PATH = os.path.join(BASE_DIR, "config", "make_pinterest_scenario_blueprint.json")
TOKEN = "66fbc9a2-1a3c-4977-beb8-27e064f61f9b"
TEAM_ID = 2010020
SCENARIO_ID = 7094447

def deploy_or_update():
    if not os.path.exists(BLUEPRINT_PATH):
        print(f"[-] Blueprint not found at {BLUEPRINT_PATH}")
        return False

    with open(BLUEPRINT_PATH, "r", encoding="utf-8") as f:
        blueprint = json.load(f)

    headers = {
        "Authorization": f"Token {TOKEN}",
        "Content-Type": "application/json"
    }

    print("\n=======================================================")
    print("      SYNCHRONIZING PUREPLATED MAKE.COM SCENARIO")
    print(f"      Scenario ID: {SCENARIO_ID}")
    print("=======================================================")

    payload = {
        "blueprint": json.dumps(blueprint)
    }

    url = f"https://us2.make.com/api/v2/scenarios/{SCENARIO_ID}"
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="PATCH")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[✓] Scenario {SCENARIO_ID} successfully updated and synchronized!")
            print(f"    Name:          PurePlated - Daily Healthy Meals Pinterest Automation")
            print(f"    Dashboard URL: https://us2.make.com/{TEAM_ID}/scenarios/{SCENARIO_ID}")
            print("=======================================================\n")
            return True
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[-] Make API Error [{e.code}]: {err_msg}")
        return False
    except Exception as e:
        print(f"[-] Exception: {str(e)}")
        return False

if __name__ == "__main__":
    deploy_or_update()
