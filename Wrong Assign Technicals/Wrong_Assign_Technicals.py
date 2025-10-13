import json
import sys, os
import traceback
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from Functions.Mother_func import (
    Open_CSP, Login_To_CSP, Open_Ticket, STEP_WrongAssignTechnicals_1, STEP_WrongAssignTechnicals_2, STEP_WrongAssignTechnicals_3
    , STEP_WrongAssignTechnicals_4, STEP_WrongAssignTechnicals_5, STEP_WrongAssignTechnicals_6, Ticket_layer
)
from seleniumwire import webdriver
from Real_info.user_info import username, password
from Real_info.Ticket_info import Ticket_Numbers

def save_log(Ticketnumber, log_data, status="ok"):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    now = datetime.now()
    time_str = now.strftime("%H-%M-%S")
    folder = os.path.join(BASE_DIR, "logs", "WrongAssignTechnicals_Test")
    os.makedirs(folder, exist_ok=True)
    filename = f"{time_str}_{Ticketnumber}_{status}.json"
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)

def process(Ticketnumber):
    DRIVER = webdriver.Firefox()
    DRIVER.maximize_window()
    RANDOM_T = random.choice(Ticketnumber)
    print(f"[INFO] Starting browser for Ticket: {RANDOM_T}")
    log_data = {
        "Ticket_id": RANDOM_T,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "steps": [],
        "status": "in-progress",
        "error": None
    }
    try:
        steps = [
            ("Opening CSP", lambda: Open_CSP(DRIVER)),
            ("Login to CSP", lambda: Login_To_CSP(DRIVER, username, password)),
            ("Opening Ticket", lambda: Open_Ticket(DRIVER, RANDOM_T)),
            ("Check Task WrongAssignTechnicals button not should exist in Active,Pending Status (Audit layer) Step1", lambda: STEP_WrongAssignTechnicals_1(DRIVER)),
            ("Check Task WrongAssignTechnicals Active Status (Audit layer) Step2", lambda: STEP_WrongAssignTechnicals_2(DRIVER)),
            ("Check Task WrongAssignTechnicals Active Status (Technicals layer) Step3", lambda: STEP_WrongAssignTechnicals_3(DRIVER)),
            ("Check Task WrongAssignTechnicals button not should exist in Active,Pending Status (Technicals layer) Step4", lambda: STEP_WrongAssignTechnicals_4(DRIVER)),
            ("Check Task WrongAssignTechnicals button not should exist in Active Status (Analysis layer) Step5", lambda: STEP_WrongAssignTechnicals_5(DRIVER)),
            ("Check Task WrongAssignTechnicals button not should exist in Resolved Status (Feedback layer) Step6", lambda: STEP_WrongAssignTechnicals_6(DRIVER))
        ]
        for name, func in steps:
            step_info = {"function": name, "status": "started", "layer": None, "error": None}
            try:
                result = func()
                if "Check Task CloseIncident button not should exist in Active,Pending Status (Audit layer) Step1" == name:
                    if "Failed" in result: raise Exception(result)
                    step_info["status"] = result
                    print(result)
                    step_info["layer"] = Ticket_layer(DRIVER)
                    log_data["steps"].append(step_info)
                elif "Check Task CloseIncident Active Status (Audit layer) Step2" == name:
                    if "Failed" in result: raise Exception(result)
                    step_info["status"] = result
                    print(result)
                    step_info["layer"] = Ticket_layer(DRIVER)
                    log_data["steps"].append(step_info)
                elif "Check Task CloseIncident Active Status (Technicals layer) Step3" == name:
                    if "Failed" in result: raise Exception(result)
                    step_info["status"] = result
                    print(result)
                    step_info["layer"] = Ticket_layer(DRIVER)
                    log_data["steps"].append(step_info)
                elif "Check Task CloseIncident button not should exist in Active,Pending Status (Technicals layer) Step4" == name:
                    if "Failed" in result: raise Exception(result)
                    step_info["status"] = result
                    print(result)
                    step_info["layer"] = Ticket_layer(DRIVER)
                    log_data["steps"].append(step_info)
                elif "Check Task CloseIncident button not should exist in Active Status (Analysis layer) Step5" == name:
                    if "Failed" in result: raise Exception(result)
                    step_info["status"] = result
                    print(result)
                    step_info["layer"] = Ticket_layer(DRIVER)
                    log_data["steps"].append(step_info)
                elif "Check Task CloseIncident button not should exist in Resolved Status (Feedback layer) Step6" == name:
                    if "Failed" in result: raise Exception(result)
                    step_info["status"] = result
                    print(result)
                    step_info["layer"] = Ticket_layer(DRIVER)
                    log_data["steps"].append(step_info)
                else:
                    step_info["status"] = "success"
                    log_data["steps"].append(step_info)
            except Exception as e:
                step_info["status"] = "Failed"
                step_info["layer"] = Ticket_layer(DRIVER)
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
            else:
                log_data["status"] = "Success"
    except Exception as e:
        log_data["status"] = "Failed"
        log_data["error"] = {
                            "type": type(e).__name__,
                            "message": str(e),
                            "traceback": traceback.format_exc()
                        }
    finally:
        DRIVER.quit()
        save_log(RANDOM_T, log_data, status=log_data["status"])

if __name__ == "__main__":
    process(Ticket_Numbers)
