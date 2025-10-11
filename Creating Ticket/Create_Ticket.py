import json
import sys, os
import traceback
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from Functions.Mother_func import (
    Open_CSP, Login_To_CSP, Open_ServiceCatalog,
    Search_And_Open_Form, do_Q1, do_Q2, do_Q3, submit_finish
)
from seleniumwire import webdriver
from Real_info.guid_info import Guid_list
from Real_info.user_info import username, password
from concurrent.futures import ThreadPoolExecutor

def save_log(Guid, log_data, status="ok"):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    now = datetime.now()
    time_str = now.strftime("%H-%M-%S")
    folder = os.path.join(BASE_DIR, "logs", "CreateTicket_Test")
    os.makedirs(folder, exist_ok=True)
    filename = f"{time_str}_{Guid}_{status}.json"
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

def process(Guid):
    DRIVER = webdriver.Firefox()
    DRIVER.maximize_window()
    print(f"[INFO] Starting browser for GUID: {Guid}")
    log_data = {
        "Guid": Guid,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "steps": [],
        "status": "in-progress",
        "ticket_id": None,
        "error": None
    }
    try:
        steps = [
            ("Opening CSP", lambda: Open_CSP(DRIVER)),
            ("Login to CSP", lambda: Login_To_CSP(DRIVER, username, password)),
            ("Opening ServiceCatalog", lambda: Open_ServiceCatalog(DRIVER)),
            ("Opening Request Affering", lambda: Search_And_Open_Form(DRIVER, Guid)),
            ("USER Q", lambda: do_Q1(DRIVER)),
            ("Map INFO Q", lambda: do_Q2(DRIVER)),
            ("Other Q", lambda: do_Q3(DRIVER)),
            ("Created Ticket with geting Ticket ID", lambda: submit_finish(DRIVER)),
        ]
        for name, func in steps:
            step_info = {"function": name, "status": "started", "error": None}
            try:
                result = func()
                step_info["status"] = "success"
                if "Created Ticket with geting Ticket ID" == name:
                    if result == None: raise Exception("Ticket Generate id Failed!")
                    print(result)
                    log_data["ticket_id"] = result
            except Exception as e:
                step_info["status"] = "Failed"
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
            log_data["steps"].append(step_info)
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
    if len(Guid_list) == 1:
        process(Guid_list[0])
    else:
        workers = len(Guid_list)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            executor.map(process, Guid_list)
