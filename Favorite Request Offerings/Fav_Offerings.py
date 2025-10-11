import json
import sys, os
import random
import traceback
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from seleniumwire import webdriver
from Functions.Mother_func import (
    Open_CSP, Login_To_CSP, Open_ServiceCatalog, Search_And_Open_Form,
    Add_favorite, Remove_favorite
)
from seleniumwire import webdriver
from Real_info.guid_info import Guid_list
from Real_info.user_info import username, password

def save_log(Guid, log_data, status="ok"):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    now = datetime.now()
    time_str = now.strftime("%H-%M-%S")
    folder = os.path.join(BASE_DIR, "logs", "Favorite_Test")
    os.makedirs(folder, exist_ok=True)
    filename = f"{time_str}_{Guid}_{status}.json"
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

def process(Guid):
    DRIVER = webdriver.Firefox()
    DRIVER.maximize_window()
    RANDOM_G = random.choice(Guid)
    print(f"[INFO] Starting browser for GUID: {Guid}")
    log_data = {
        "Guid": RANDOM_G,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "steps": [],
        "status": "in-progress",
        "error": None
    }
    try:
        steps = [
            ("Opening CSP", lambda: Open_CSP(DRIVER)),
            ("Login to CSP", lambda: Login_To_CSP(DRIVER, username, password)),
            ("Opening ServiceCatalog", lambda: Open_ServiceCatalog(DRIVER)),
            ("Search And Open Offerings", lambda: Search_And_Open_Form(DRIVER, RANDOM_G)),
            ("Adding Offering Step", lambda: Add_favorite(DRIVER, RANDOM_G)),
            ("Search And Open Offerings", lambda: Search_And_Open_Form(DRIVER, RANDOM_G)),
            ("Removing Offering Step", lambda: Remove_favorite(DRIVER, RANDOM_G))
        ]
        for name, func in steps:
            step_info = {"function": name, "status": "started", "error": None}
            try:
                result = func()   
                if name == "Adding Offering Step":   
                    step_info["status"] = result
                    log_data["steps"].append(step_info)
                elif name == "Removing Offering Step":
                    step_info["status"] = result
                    log_data["steps"].append(step_info)
                else:
                    step_info["status"] = "success"
                    log_data["steps"].append(step_info)
            except Exception as e:
                step_info["status"] = result
                step_info["error"] = {
                                    "type": type(e).__name__,
                                    "message": str(e),
                                    "traceback": traceback.format_exc()
                                }
                log_data["error"] = {
                                    "type": type(e).__name__,
                                    "message": str(e),
                                    "traceback": traceback.format_exc()
                                }
                log_data["status"] = "Failed"
                log_data["steps"].append(step_info)
                raise
        log_data["status"] = "Success"
    except Exception as e:
        log_data["error"] = {
                            "type": type(e).__name__,
                            "message": str(e),
                            "traceback": traceback.format_exc()
                        }
    finally:
        DRIVER.quit()
        save_log(Guid, log_data, status=log_data["status"])

if __name__ == "__main__":
    process(Guid_list)
