import json
import jdatetime
import random
import sys, os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime, timedelta
from seleniumwire import webdriver
from time import sleep
from Real_info.guid_info import Guid_list
from Real_info.user_info import username, password
from Real_info.Ticket_info import Ticket_Numbers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

def Open_CSP(driver):
    # driver.get("file:///C:/Users/IFIXIT/Desktop/%DA%A9%D8%A7%D8%AA%D8%A7%D9%84%D9%88%DA%AF%20%D8%AE%D8%AF%D9%85%D8%A7%D8%AA.html")
    driver.get("https://csp.mci.ir/")

def Login_To_CSP(driver, USERNAME, PASSWORD, max_retries=3):
    global username_otherformat
    username_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="UserName"]')))
    password_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Password"]')))
    username_.send_keys(USERNAME)
    password_.send_keys(PASSWORD)
    for _ in range(max_retries):
        try:
            login_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "loginSubmit")))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", login_btn)
            sleep(0.5)
            driver.execute_script("arguments[0].click();", login_btn)
            break
        except Exception as e:
            print("Retry login click:", e)
    else:
        raise TimeoutException("Login button not clickable after retries")
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.ID, "navbarDropdownUser")))
    username_otherformat = driver.execute_script(
        "return document.querySelector('.dropdown-menu .dropdown-item.center')?.innerText;"
    )
    print(f"My user: {username_otherformat}")

def Open_ServiceCatalog(driver):
    driver.get("https://csp.mci.ir/ServiceCatalog")

def Search_And_Open_Form(driver, Guid):
    open_form_ = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,  f'//a[contains(@onclick, "{Guid}")]')))
    driver.execute_script("arguments[0].click();", open_form_)
    sleep(3)

def do_Q1(driver):
    TempSubscriberNumber_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="TempSubscriberNumber"]')))
    TempSubscriberNumber_.send_keys('09191401586')
    checkCRM_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@onclick='checkCRM();']")))
    driver.execute_script("arguments[0].click();", checkCRM_)
    request = driver.wait_for_request(r'/SearchCRM', timeout=20)
    if request and request.response:
        data = request.response.body.decode("utf-8")
        json_data_CRM = json.loads(data)
        if json_data_CRM.get("success") == True:
            CallerNumber_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="CallerNumber"]')))
            CallerNumber_.send_keys('09191401586')
            CallerName_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="CallerName"]')))
            CallerName_.send_keys('اشکان نوروزی')
            ContactMethod_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ContactMethod"]')))
            ContactMethod_.send_keys('09191401586')
            City_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[2]/form/div[1]/div[2]/div/div[2]/div/div[4]/div/span/span[1]/span")))
            driver.execute_script("arguments[0].click();", City_)
            City_Search_box_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/span/input')))
            City_Search_box_.send_keys('تهران')
            sleep(1.5)
            click_on_City = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/ul/li/ul/li/div/span')))
            click_on_City.click()
            Port_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[2]/form/div[1]/div[2]/div/div[2]/div/div[5]/div/span/span[1]/span')))
            driver.execute_script("arguments[0].click();", Port_)
            click_on_Port = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[2]/ul/li[5]/div/span')))
            driver.execute_script("arguments[0].click();", click_on_Port)
            Description_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Description"]')))
            Description_.send_keys('Test in Python')
        else:
            raise Exception("CRM Error")

def do_Q2(driver):
    if "Map Information" in driver.page_source:
        txtLatitude_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtLatitude"]')))
        txtLatitude_.send_keys('41.725855')
        txtLongitude_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtLongitude"]')))
        txtLongitude_.send_keys('49.9406')

def do_Q3(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="QuestionsDiv"]')))
    QuestionsDiv = driver.find_element(By.XPATH, '//*[@id="QuestionsDiv"]')
    list_fileds = QuestionsDiv.find_elements(By.XPATH, '//*[@data-role="dropdowntree"]')
    filled_trees_l = set()
    filled_trees_t = set()
    filled_trees_d = set()
    filled_trees_a = set()
    for i in list_fileds:
        tree_id = i.get_attribute("id")
        if tree_id in filled_trees_l:
            continue
        if "drp" in tree_id:
            checked_filed = QuestionsDiv.find_element(By.XPATH, f'//input[@id="{"ho_" + tree_id[4:]}"]')
            if checked_filed.get_attribute("value") == "1":
                open_filed = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//input[@id="{tree_id}"]')))
                driver.execute_script("arguments[0].click();", open_filed)
                tree_containers = driver.find_elements(By.XPATH, '//div[@data-role="treeview" and @aria-hidden="false"]')
                if not tree_containers:
                    continue
                tree_container = tree_containers[-1]
                options = tree_container.find_elements(By.CSS_SELECTOR, 'li span.k-treeview-leaf') 
                if options:
                    driver.execute_script("arguments[0].click();", options[0])
                    filled_trees_l.add(tree_id)
    
    text_fileds = QuestionsDiv.find_elements(By.XPATH, '//input[@data-toggle="tooltip"]')
    for i in text_fileds:
        tree_id = i.get_attribute("id")
        if tree_id in filled_trees_t:
            continue
        if not i.is_displayed():
            continue
        if "inputdate" not in tree_id:
            if "شماره کارت" in i.get_attribute("title"):
                i.send_keys("5022291334528450")
                filled_trees_t.add(tree_id)
            else:
                i.send_keys("Test in Python")
                filled_trees_t.add(tree_id)
    
    date_fileds = QuestionsDiv.find_elements(By.XPATH, '//input[@id[contains(., "inputdate_")]]')
    for i in date_fileds:
        tree_id = i.get_attribute("id")
        if tree_id in filled_trees_d:
            continue
        if not i.is_displayed():
            continue
        value_filed = QuestionsDiv.find_element(By.XPATH, f'//input[@id="{tree_id[10:]}"]')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        driver.execute_script(f"arguments[0].setAttribute('value','{now}')", value_filed)
        i.send_keys(now)
        filled_trees_d.add(tree_id)
    text_fileds = QuestionsDiv.find_elements(By.XPATH, '//textarea[@data-toggle="tooltip"]')
    for i in text_fileds:
        tree_id = i.get_attribute("id")
        if tree_id in filled_trees_a:
            continue
        if not i.is_displayed():
            continue
        if "inputdate" not in tree_id:
            i.send_keys("Test in Python")
            filled_trees_a.add(tree_id)

def submit_finish(driver):
    sleep(1)
    submit_btn = driver.find_element(By.ID, "submitButton")
    driver.execute_script("arguments[0].click();", submit_btn)
    request = driver.wait_for_request(r'/SubmitForm', timeout=20)
    if request and request.response:
        data = request.response.body.decode("utf-8")
        json_data_ID = json.loads(data)
        return json_data_ID.get("Id")
    else:
        raise Exception("Ticket ID Error")

def submit_finish_and_check_ChangeTicketType(driver):
    try:
        submit_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="submitButton"]')))
        driver.execute_script("arguments[0].click();", submit_btn)
        driver.wait_for_request(r'/ChangeTicketType', timeout=20)
        requests = [r for r in driver.requests if "/ChangeTicketType" in r.url]
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
                return result
    except:
        return False

def Check_Network_ServiceType(driver):
    try:
        WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ServiceType"]')))
    except:
        return False
    else:
        return True

def Get_standard_fav(driver):
    sleep(1.5)
    remove_text = "حذف از پسندیده ها"
    try:
        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), remove_text))
    except:
        print("not needed")
    else:
        remove_favorite_stand = driver.find_element(By.XPATH, '//i[@title="حذف از پسندیده ها"]')
        remove_favorite_stand.click()
        print("needed")

def Add_favorite(driver, random_guid):
    Get_standard_fav(driver)
    add_favorite = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//i[@title="اضافه به پسندیده ها"]')))
    add_favorite.click()
    Check_Add_Favorite(driver, random_guid)
    print("everything ok for adding")

def Remove_favorite(driver, random_guid):
    remove_favorite = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//i[@title="حذف از پسندیده ها"]')))
    remove_favorite.click()
    Check_Remove_Favorite(driver, random_guid)
    print("everything ok for removing")

def Check_Add_Favorite(driver, random_guid):
    sleep(5)
    added = False
    data_str = driver.execute_script("return window.sessionStorage.getItem('favOffers');")
    data_json = json.loads(data_str)
    bme_ids = [item["BMEId"] for item in data_json if "BMEId" in item]
    print(bme_ids)
    if random_guid in bme_ids:
        return "Adding Successed"
    else:
        raise Exception("Adding Favorite RO Error")

def Check_Remove_Favorite(driver, random_guid):
    sleep(5)
    removed = False
    data_str = driver.execute_script("return window.sessionStorage.getItem('favOffers');")
    data_json = json.loads(data_str)
    bme_ids = [item["BMEId"] for item in data_json if "BMEId" in item]
    print(bme_ids)
    if random_guid not in bme_ids:
        return "Removing Successed"
    else:
        raise Exception("Removeing Favorite RO Error")

def wait_for_page_load(driver, timeout=30):
    WebDriverWait(driver, timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")

def Refresh_CSP(driver):
    driver.refresh()
    wait_for_page_load(driver)

def Open_Ticket(driver, Ticket_number):
    T_number = Ticket_number
    driver.get(f"https://csp.mci.ir/Incident/IncidentDetail/{T_number}")
    # driver.get("file:///C:/Users/IFIXIT/Desktop/local%20csp/14040605-00010_Resolved.html")
    sleep(1.5)

def Ticket_layer(driver):
    Support_Group_WEB = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="TierQueue"]'))).text
    return Support_Group_WEB

def Check_Befor_After_Task_Status(driver, status, assignee, support_group, taskName=None):
    Status_WEB = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="IncidentStatus"]'))).text
    Assignee_WEB = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Assignee"]/span'))).text
    Support_Group_WEB = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="top"]/div/div/div[3]/div/div[1]/div[1]/div/div[4]/div[2]/div[2]'))).text
    support_group_ok = False
    if type(support_group) == str:
        support_group_ok = (Support_Group_WEB == support_group)
    else:
        support_group_ok = (Support_Group_WEB not in support_group)
    if Status_WEB == status and Assignee_WEB == assignee and support_group_ok:
        print(f"Success {taskName}: Expected (status={status}, assignee={assignee}, support_group={support_group}), Got (status={Status_WEB}, assignee={Assignee_WEB}, support_group={Support_Group_WEB})")
        return f"Success {taskName}: Expected (status={status}, assignee={assignee}, support_group={support_group}), Got (status={Status_WEB}, assignee={Assignee_WEB}, support_group={Support_Group_WEB})"
    else:
        return f"Failed {taskName}: Expected (status={status}, assignee={assignee}, support_group={support_group}), Got (status={Status_WEB}, assignee={Assignee_WEB}, support_group={Support_Group_WEB})"

def is_ChangeSchedule(driver, result_data):
    try:
        date_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#IncidentScheduledStartDate .utc-date")))
        actual_date_str = date_element.text.strip()  # 1404/6/19 07:00:00
        parts = actual_date_str.split(" ")
        y, m, d = parts[0].split("/")
        m, d = m.zfill(2), d.zfill(2)
        normalized_str = f"{y}/{m}/{d} {parts[1]}"
        jalali_dt = jdatetime.datetime.strptime(normalized_str, "%Y/%m/%d %H:%M:%S")
        gregorian_dt = jalali_dt.togregorian()
        gregorian_dt = str(gregorian_dt).split(" ")[0]
        return gregorian_dt == result_data
    except:
        return False

def check_should_exist_Tasks(driver, task_name):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{task_name}"]')))
    except:
        return False
    else:
        return True

def check_not_should_exist_Tasks(driver, task_name):
    script = f"""
    var el = document.getElementById("{task_name}");
    if (el) {{
        if (el.parentElement?.parentElement?.parentElement?.className.includes("disabledTask")) {{
            return false;
        }} else {{
            return true;
        }}
    }} else {{
        return false;
    }}
    """
    return driver.execute_script(script)

def check_layer_map(driver):
    list_of_layer = []
    list_of_SG = []
    all_of_li = driver.find_elements(By.CLASS_NAME, 'breadcrumb-item')
    for i in all_of_li:
        list_of_layer.append(i.find_element(By.CLASS_NAME, 'orangeText').text)
    for i in list_of_layer:
        if ("تحلیل" != i) and ("نظرسنجی" != i):
            list_of_SG.append(i)
    return list_of_SG

def is_file_uploaded(driver, filename="upload_file_1.txt"):
    js_code = """
    const rows = document.querySelectorAll('tbody tr.k-master-row');
    let fileNames = [];
    rows.forEach(row => {
        const links = row.querySelectorAll('td[aria-colindex="3"] a');
        links.forEach(link => {
            const name = link.textContent.trim();
            if (name) fileNames.push(name);
        });
    });
    return Array.from(new Set(fileNames));
    """
    unique_file_names = driver.execute_script(js_code)
    if filename in unique_file_names:
        return True
    else:
        return False

def is_file_downloaded(driver, filename="upload_file_1.txt"):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr.k-master-row')))
    js_get_href = """
    const filename = arguments[0].toLowerCase().trim();
    const callback = arguments[1];
    const rows = document.querySelectorAll('tbody tr.k-master-row');
    let fileLink = null;
    rows.forEach(row => {
        const links = row.querySelectorAll('td[aria-colindex="3"] a');
        links.forEach(link => {
            const name = link.textContent.trim().toLowerCase();
            if (name === filename) {
                fileLink = link.href;
            }
        });
    });
    callback(fileLink);
    """
    file_href = driver.execute_async_script(js_get_href, filename)
    if not file_href:
        return f"File not found: {filename}"
    js_check_download = """
    const fileLink = arguments[0];
    const callback = arguments[1];
    (async () => {
        try {
            const response = await fetch(fileLink, { method: 'HEAD', credentials: 'same-origin' });
            console.log("File accessible:", response.ok);
            callback(response.ok);
        } catch (e) {
            console.log("Fetch error:", e);
            callback(false);
        }
    })();
    """
    downloadable = driver.execute_async_script(js_check_download, file_href)
    if downloadable:
        return True
    else:
        return False

def is_file_removed(driver, filename):
    js_code = """
    const rows = document.querySelectorAll('tbody tr.k-master-row');
    let fileNames = [];
    rows.forEach(row => {
        const links = row.querySelectorAll('td[aria-colindex="3"] a');
        links.forEach(link => {
            const name = link.textContent.trim();
            if (name) fileNames.push(name);
        });
    });
    return Array.from(new Set(fileNames));
    """
    unique_file_names = driver.execute_script(js_code)
    if filename not in unique_file_names:
        return True
    else:
        return False

def remove_uploaded_file_inTicket(driver, filename="upload_file_1.txt"):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody tr.k-master-row")))
        js_code = """
        const filename = arguments[0].toLowerCase().trim();
        const rows = document.querySelectorAll('tbody tr.k-master-row');
        for (const row of rows) {
            const links = row.querySelectorAll('td[aria-colindex="3"] a');
            for (const link of links) {
                const name = link.textContent.trim().toLowerCase();
                if (name && name === filename) {
                    const delBtn = row.querySelector('td[aria-colindex="8"] a.k-gridedit');
                    if (delBtn) {
                        delBtn.click();
                        return true;
                    }
                }
            }
        }
        return false;
        """
        result = driver.execute_script(js_code, filename)
        if result:
            btnRemoveAttach = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnRemoveAttach"]')))
            btnRemoveAttach.click()
            Refresh_CSP(driver)
            print(f"File '{filename}' deleted on ticket.")
            return True
        else:
            print(f"File '{filename}' not found on ticket.")
            return False
    except Exception as e:
        print(f"Error in remove_uploaded_file_inTicket: {e}")
        return False

def remove_uploaded_file_inTask(driver, filename):
    try:
        files = driver.find_elements(By.CSS_SELECTOR, "ul.k-upload-files li.k-file")
        for file_item in files:
            name_span = file_item.find_element(By.CSS_SELECTOR, ".k-file-name")
            file_name = name_span.text.strip()
            if file_name.lower() == filename.strip().lower():
                delete_btn = file_item.find_element(By.CSS_SELECTOR, "button[aria-label='حذف']")
                delete_btn.click()
                print(f"File '{filename}' deleted successfully in task.")
                return True
        print(f"File '{filename}' not found in upload list in task.")
        return False
    except Exception as e:
        print(f"Error in remove_uploaded_file_inTask: {e}")
        return False

def taskAssignIncidentToMe(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="taskAssignIncidentToMe"]'))).click()
    btnAssignIncidentToMe = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAssignIncidentToMe"]')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnAssignIncidentToMe)
    try:
        driver.wait_for_request(r'/AssignIncident', timeout=20)
        requests = [r for r in driver.requests if "/AssignIncident" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return result

def set_kendo_date_super_stable(driver, date_value, input_id="newScheduledStartDate", hidden_id="_newScheduledStartDate", timeout=15, retry_interval=0.25):
    WebDriverWait(driver, timeout).until(lambda d: d.find_element(By.ID, input_id))
    js = f"""
    const inputId='{input_id}', hiddenId='{hidden_id}', dateValue='{date_value}';
    const v=document.getElementById(inputId), h=document.getElementById(hiddenId);
    function triggerAll(el){{ ['focus','input','change','blur'].forEach(ev=>{{ try{{ el.dispatchEvent(new Event(ev,{{bubbles:true}})) }}catch(e){{}} }}); }}
    function setValue(el,val){{ try{{ el.value=val; triggerAll(el); return true }}catch(e){{ return false }} }}
    let success=false, messages=[];
    try {{
        if(window.jQuery) {{
            const $v=jQuery(v);
            const dp=$v.data('kendoDatePicker')||$v.data('kendoDateInput')||$v.data('kendoDateTimePicker');
            if(dp){{
                try{{ dp.value(null) }}catch(e){{}}
                dp.value(new Date(dateValue));
                try{{ if(typeof dp.trigger==='function') dp.trigger('change') }}catch(e){{}}
                triggerAll(v);
                if(h) setValue(h, v.value||dateValue);
                success=true; messages.push('set via Kendo');
            }}
        }}
    }} catch(e){{ messages.push('Kendo error:'+e) }}
    if(!success){{
        try {{
            const btn=document.getElementById('date_'+inputId);
            if(v&&btn){{
                v.removeAttribute('readonly'); v.disabled=false;
                if(h){{ h.removeAttribute('readonly'); h.disabled=false; }}
                setValue(v,dateValue);
                if(h) setValue(h,dateValue);
                triggerAll(v);
                if(h) triggerAll(h);
                success=true; messages.push('set via Persian DTP');
            }}
        }} catch(e){{ messages.push('Persian DTP error:'+e) }}
    }}
    if(!success){{
        try {{
            v.removeAttribute('readonly'); v.disabled=false;
            if(h){{ h.removeAttribute('readonly'); h.disabled=false; }}
            setValue(v,dateValue);
            if(h) setValue(h,dateValue);
            triggerAll(v);
            if(h) triggerAll(h);
            success=true; messages.push('set via direct fallback');
        }} catch(e){{ messages.push('Direct fallback error:'+e) }}
    }}
    return {{success:success,messages:messages}};
    """
    end_time = time.time() + timeout
    last_res = None
    while time.time() < end_time:
        try:
            last_res = driver.execute_script(js)
            hidden_val = driver.find_element(By.ID, hidden_id).get_attribute("value")
            if hidden_val == date_value:
                return last_res
        except Exception as e:
            last_res = {"success": False, "messages": [str(e)]}
        time.sleep(retry_interval)
    raise Exception(f"Failed to set date after {timeout}s, last result: {last_res}")

def taskPark(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="taskPark"]'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ParkComment"]'))).send_keys("Test in Python")
    sleep(1)
    today = datetime.now().strftime("%Y-%m-%d")
    result = set_kendo_date_super_stable(driver, date_value=today)
    if not result.get("success"):
        raise Exception(f"Date set failed: {result}")
    btnParkIncident = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'btnParkIncident')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnParkIncident)
    try:
        driver.wait_for_request(r'/ParkIncident', timeout=20)
        requests = [r for r in driver.requests if "/ParkIncident" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return result

def taskChangeSchedule(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'taskChangeSchedule'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'ChangeScheduleComment'))).send_keys("Test in Python")
    today = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    result = set_kendo_date_super_stable(driver, date_value=today)
    if not result.get("success"):
        raise Exception(f"Date set failed: {result}")
    date = result.get("hid")
    btnChangeSchedule = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'btnChangeSchedule')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnChangeSchedule)
    try:
        driver.wait_for_request(r'/ChangeIncidentSchedule', timeout=20)
        requests = [r for r in driver.requests if "/ChangeIncidentSchedule" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="IncidentScheduledStartDate"]')))
    return (is_ChangeSchedule(driver, date), result)

def wait_for_tree_items_loaded(driver, min_items=1, timeout=20):
    try:
        WebDriverWait(driver, timeout).until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "li.k-item[data-uid]")) >= min_items)
        return driver.find_elements(By.CSS_SELECTOR, "li.k-item[data-uid]")
    except TimeoutException:
        raise TimeoutException(f"Tree items did not load within {timeout} seconds (expected at least {min_items} items)")

def expand_all_tree_nodes(driver, delay=0.2):
    toggles = driver.find_elements(By.CSS_SELECTOR, "span.k-treeview-toggle, span.k-treeview-toggle .k-icon")
    clicked = 0
    for i, el in enumerate(toggles, 1):
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", el)
            driver.execute_script("arguments[0].click();", el)
            clicked += 1
            time.sleep(delay)
        except Exception as e:
            print(f"[WARN] Toggle #{i} کلیک نشد: {e}")
    result = clicked == len(toggles) and len(toggles) > 0
    print(f"[INFO] تعداد کلیک موفق: {clicked}/{len(toggles)}")
    return result

def taskAssignToTechnicals(driver):
    map_ = check_layer_map(driver)
    def wait_click(by, value, timeout=20):
        elem = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", elem)
        return elem
    def wait_find(by, value, timeout=20):
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
    wait_click(By.ID, 'taskAssignToTechnicals')
    driver.wait_for_request(r'/GetEnumsTechnicals', timeout=20)
    reqs = [r for r in driver.requests if "/GetEnumsTechnicals" in r.url]
    if not reqs:
        raise Exception("هیچ درخواست /GetEnumsTechnicals پیدا نشد")
    data = reqs[-1].response.body.decode("utf-8")
    groups = [child["Name"] for i in json.loads(data) for child in i.get("Children", [])]
    if not groups:
        raise Exception("هیچ گروه پشتیبانی‌ای یافت نشد")
    random.shuffle(groups)
    chosen_group = random.choice(groups)
    if map_[-1] == chosen_group:
        chosen_group = random.choice(groups)
    print(f"[INFO] انتخاب گروه: {chosen_group}")
    dropdown = wait_find(By.XPATH, "//div[@id='frmAssignToTechnicals']//span[contains(@class,'k-dropdowntree')]")
    driver.execute_script("arguments[0].click();", dropdown)
    opened = expand_all_tree_nodes(driver)
    if opened:
        group_elem = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f".//*[normalize-space(text())='{chosen_group}']")))
        driver.execute_script("arguments[0].click();", group_elem)
    opinion_box = wait_find(By.ID, "assignTechnichalAnalystOpinionText")
    opinion_box.send_keys("Test with Python")
    btnAssignToTechnicals = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'btnAssignToTechnicals')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnAssignToTechnicals)
    try:
        driver.wait_for_request(r'/AssignToTechnicalsTeam', timeout=20)
        requests = [r for r in driver.requests if "/AssignToTechnicalsTeam" in r.url]
        Refresh_CSP(driver)
        if requests:
            for request in requests:
                if request.response:
                    data = request.response.body.decode("utf-8")
                    json_data_Name = json.loads(data)
                    result = json_data_Name['success'] == True
                    print(json_data_Name)
    except:
        result = False
    return result

def taskChangeTTType(driver):
    list_TTType = []
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="taskChangeTTType"]'))).click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="frmChangeTTType"]/div[1]/div[2]/span/span[1]/span'))).click()
    TTTypes = wait_for_tree_items_loaded(driver, min_items=5)
    for i in TTTypes:
        list_TTType.append(i.get_attribute("data-uid"))
    TTType = random.choice(list_TTType)
    driver.execute_script(f"""
        document.querySelectorAll('span.k-treeview-toggle > span.k-i-expand').forEach(function(el){{
            if (el.offsetParent !== null) {{
                el.click();
            }}
        }});
        let el = document.evaluate(
            '//li[@data-uid="{TTType}"]//span[contains(@class,"k-treeview-leaf-text")]',
            document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null
        ).singleNodeValue;
        if (el) {{
            el.scrollIntoView(true);
            el.click();
        }} else {{
            let targetXpath = '//li[@data-uid="{TTType}"]//span[contains(@class,"k-treeview-leaf-text")]';
            let observer = new MutationObserver(function(mutations, me) {{
                let el2 = document.evaluate(targetXpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (el2) {{
                    el2.scrollIntoView(true);
                    el2.click();
                    me.disconnect();
                }}
            }});
            observer.observe(document.body, {{ childList: true, subtree: true }});
        }}
    """)
    cl = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "loadRo")))
    ActionChains(driver).move_to_element(cl).pause(0.3).click(cl).perform()
    sleep(1)
    do_Q2(driver)
    do_Q3(driver)
    driver.requests.clear()
    result1 = submit_finish_and_check_ChangeTicketType(driver)
    try:
        driver.wait_for_request(r'/ChangeTicketType', timeout=20)
        requests = [r for r in driver.requests if "/ChangeTicketType" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result2 = json_data_Name['success'] == True
    except:
        result2 = False
    return (result1, result2)

def taskSendToAnalysis(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="taskSendToAnalysis"]'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="resolutionDescription"]'))).send_keys("Test in Python")
    btnResolveIncident = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnResolveIncident"]')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnResolveIncident)
    try:
        driver.wait_for_request(r'/SendToAnalysisIncident', timeout=20)
        requests = [r for r in driver.requests if "/SendToAnalysisIncident" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return result

def taskSendToFeedback(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="taskSendToFeedback"]'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="SendToFeedbackComment"]'))).send_keys("Test in Python")
    btnSendToFeedback = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSendToFeedback"]')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnSendToFeedback)
    try:
        driver.wait_for_request(r'/SendToFeedbackIncident', timeout=20)
        requests = [r for r in driver.requests if "/SendToFeedbackIncident" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return result

def wait_for_dropdown_items(driver, timeout=20):
    WebDriverWait(driver, timeout).until(lambda d: len(d.find_elements(By.XPATH, '//ul[@id="cmbAssignee_listbox"]/li')) > 0)
    prev_count = -1
    for _ in range(timeout * 5):
        items = driver.find_elements(By.XPATH, '//ul[@id="cmbAssignee_listbox"]/li')
        if len(items) == prev_count:
            return items
        prev_count = len(items)
        sleep(0.2)
    return items

def taskAssignIncident(driver):
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="taskAssignIncident"]'))).click()
    sleep(1)
    driver.execute_async_script("""
        var callback = arguments[arguments.length - 1];
        function waitForDDL() {
            var ddl = $("#cmbAssignee").data("kendoDropDownList");
            if (ddl) { callback(true); }
            else { setTimeout(waitForDDL, 200); }
        }
        waitForDDL();
    """)
    driver.execute_script(""" 
        var ddl = $("#cmbAssignee").data("kendoDropDownList");
        ddl.open();
    """)
    sleep(1)
    requests = [req for req in driver.requests if "/GetUsersKendo" in req.url]
    if requests:
        request = requests[-1]
        if request.response:
            data = request.response.body.decode("utf-8")
            json_data_Name = json.loads(data)
        usernames = [i["UserName"] for i in json_data_Name if i["UserName"] != username]
        if usernames:
            selected_user = random.choice(usernames)
            display_name = driver.execute_script(f"""
                var selected_user = "{selected_user}";
                var ddl = $('#cmbAssignee').data('kendoDropDownList');
                var value_to_select = null;
                var display_name = selected_user;
                ddl.dataSource.data().forEach(function(item) {{
                    if (item.UserName === selected_user) {{
                        value_to_select = item.Id || item.UserName;
                        display_name = item.DisplayName || item.FullName || item.UserName;
                    }}
                }});
                if (value_to_select !== null) {{
                    ddl.value(value_to_select);
                    ddl.trigger('change');
                    ddl.close();
                }}
                return display_name;
            """)
            selected_user = display_name
    btnAssignIncident = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAssignIncident"]')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnAssignIncident)
    try:
        driver.wait_for_request(r'/AssignIncident', timeout=20)
        requests = [r for r in driver.requests if "/AssignIncident" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return (selected_user, result)

def taskReleaseIncident(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="taskReleaseIncident"]'))).click()
    btnRelease = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnRelease"]')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnRelease)
    try:
        driver.wait_for_request(r'/ReleaseIncident', timeout=20)
        requests = [r for r in driver.requests if "/ReleaseIncident" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return result

def taskAddAttachment(driver, filename1="upload_file_1.txt", filename2="upload_file_2.txt"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    real_info_path1 = os.path.join(base_dir, "..", "Real_info", filename1)
    real_info_path1 = os.path.abspath(real_info_path1)
    real_info_path2 = os.path.join(base_dir, "..", "Real_info", filename2)
    real_info_path2 = os.path.abspath(real_info_path2)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="taskAddAttachment"]'))).click()
    parentAttachment1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="parentAttachment"]')))
    parentAttachment1.send_keys(real_info_path1)
    parentAttachment2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="parentAttachment"]')))
    parentAttachment2.send_keys(real_info_path2)
    sleep(1)
    result_remove_uploaded_file_inTask = remove_uploaded_file_inTask(driver, filename2)
    if result_remove_uploaded_file_inTask == False:
        return "Failed: The uploaded file was deleted from the task and not from within the ticket."
    btnAddAttachment = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAddAttachment"]')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnAddAttachment)
    try:
        driver.wait_for_request(r'/SubmitAttachment', timeout=20)
        requests = [r for r in driver.requests if "/SubmitAttachment" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return result

def taskAssignToPreviousSg(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="taskAssignToPreviousSg"]'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="returnPrevSGNotes"]'))).send_keys("Test in Python")
    btnAssignToPreviousSG = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAssignToPreviousSG"]')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnAssignToPreviousSG)
    try:
        driver.wait_for_request(r'/AssignToTechnicalsTeam', timeout=20)
        requests = [r for r in driver.requests if "/AssignToTechnicalsTeam" in r.url]
        Refresh_CSP(driver)
        if requests:
            for request in requests:
                if request.response:
                    data = request.response.body.decode("utf-8")
                    json_data_Name = json.loads(data)
                    result = json_data_Name['success'] == True
                    print(json_data_Name)
    except:
        result = False
    return result

def taskUpdateCoordinate(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="taskUpdateCoordinate"]'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "frmSetCoordinate")))
    clipboard_text = "(MapPlus-Lat:85.85858585-Lng:69.69696969-2GCoverage:Yes-3GCoverage:Yes-4GCoverage:Yes)"
    text = clipboard_text.replace("MapPlus", "").replace("(", "").replace(")", "")
    items = text.split("-")
    for item in items:
        if not item.strip():
            continue
        key, value = item.split(":")
        value = value.strip()
        if key == "Lat":
            lat_input = driver.find_element(By.ID, "txtLatitude")
            driver.execute_script("arguments[0].removeAttribute('disabled')", lat_input)
            lat_input.clear()
            lat_input.send_keys(value)
        elif key == "Lng":
            lng_input = driver.find_element(By.ID, "txtLongitude")
            driver.execute_script("arguments[0].removeAttribute('disabled')", lng_input)
            lng_input.clear()
            lng_input.send_keys(value)
        elif key == "2GCoverage":
            if value == "Yes":
                driver.execute_script("$('#chk2G').iCheck('check');")
            else:
                driver.execute_script("$('#chk2G').iCheck('uncheck');")
        elif key == "3GCoverage":
            if value == "Yes":
                driver.execute_script("$('#chk3G').iCheck('check');")
            else:
                driver.execute_script("$('#chk3G').iCheck('uncheck');")
        elif key == "4GCoverage":
            if value == "Yes":
                driver.execute_script("$('#chk4G').iCheck('check');")
            else:
                driver.execute_script("$('#chk4G').iCheck('uncheck');")
    update_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "btnUpdateCoordinate")))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", update_btn)
    try:
        driver.wait_for_request(r'/UpdateMapInformation', timeout=20)
        requests = [r for r in driver.requests if "/UpdateMapInformation" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return result

def taskSupplemantaryQuestions(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="taskSupplemantaryQuestions"]'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="CodeSite"]'))).clear()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="CodeSite"]'))).send_keys("Test in Python")
    driver.execute_script("""
        var select = document.getElementById("TicketStatusReason");
        var options = select.options;
        var randomIndex = Math.floor(Math.random() * options.length);
        select.selectedIndex = randomIndex;
        select.dispatchEvent(new Event('change'));
    """)
    btnSupplementaryQuestions = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSupplementaryQuestions"]')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnSupplementaryQuestions)
    try:
        driver.wait_for_request(r'/EnterSupplementaryQuestions', timeout=20)
        requests = [r for r in driver.requests if "/EnterSupplementaryQuestions" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return result

def taskAssignToAudit(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="taskAssignToAudit"]'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="assignAuditNotes"]'))).send_keys("Test in Python")
    btnAssignToAudit = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAssignToAudit"]')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnAssignToAudit)
    try:
        driver.wait_for_request(r'/AssignToAuditTeam', timeout=20)
        requests = [r for r in driver.requests if "/AssignToAuditTeam" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return result

def taskCloseIncident(driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="taskCloseIncident"]'))).click()
    dropdown = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.k-input-value-text.k-readonly")))
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", dropdown)
    options = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-role="treeview"] span.k-treeview-leaf.k-in')))
    choice = random.choice(options)
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", choice)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ArchiveComment"]'))).send_keys("Test in Python")
    btnSubmitCloseIncident = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnSubmitCloseIncident"]')))
    driver.requests.clear()
    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", btnSubmitCloseIncident)
    try:
        driver.wait_for_request(r'/ArchiveIncident', timeout=20)
        requests = [r for r in driver.requests if "/ArchiveIncident" in r.url]
        Refresh_CSP(driver)
        if requests:
            request = requests[-1]
            if request.response:
                data = request.response.body.decode("utf-8")
                json_data_Name = json.loads(data)
                result = json_data_Name['success'] == True
    except:
        result = False
    return result

def STEP_Assigntome_1(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group="ممیزی", taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskAssignIncidentToMe(driver)
    if result_task == False: return "STEP_Assigntome_1 Failed: Request Step wrong!, Function: Assigntome" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe"): return "Failed: Task ReleaseIncident button not should exist but found"
    if "Success" in result_B and "Success" in result_A: return "STEP_Assigntome_1: Success Assign To Me Checked Active status"
    else: 
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_Assigntome_2(driver):
    taskPark(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="متوقف شده", assignee="کارتابل گروهی", support_group="ممیزی", taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskAssignIncidentToMe(driver)
    if result_task == False: return "STEP_Assigntome_2 Failed: Request Step wrong!, Function: Assigntome" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe"): return "Failed: Task ReleaseIncident button not should exist but found"
    if "Success" in result_B and "Success" in result_A: return "STEP_Assigntome_2: Success Assign To Me Checked Pendings to Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_Assigntome_3(driver):
    taskAssignToTechnicals(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskAssignIncidentToMe(driver)
    if result_task == False: return "STEP_Assigntome_3 Failed: Request Step wrong!, Function: Assigntome" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe"): return "Failed: Task ReleaseIncident button not should exist but found"
    if "Success" in result_B and "Success" in result_A: return "STEP_Assigntome_3: Success Assign To Me Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_Assigntome_4(driver):
    taskPark(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="متوقف شده", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskAssignIncidentToMe(driver)
    if result_task == False: return "STEP_Assigntome_4 Failed: Request Step wrong!, Function: Assigntome" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe"): return "Failed: Task ReleaseIncident button not should exist but found"
    if "Success" in result_B and "Success" in result_A: return "STEP_Assigntome_4: Success Assign To Me Checked Pendings to Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_Assigntome_5(driver):
    taskSendToAnalysis(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group="تحلیل", taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskAssignIncidentToMe(driver)
    if result_task == False: return "STEP_Assigntome_5 Failed: Request Step wrong!, Function: Assigntome" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="تحلیل", taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe"): return "Failed: Task ReleaseIncident button not should exist but found"
    if "Success" in result_B and "Success" in result_A: return "STEP_Assigntome_5: Success Assign To Me Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_Assigntome_6(driver):
    taskSendToFeedback(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="حل شده", assignee="کارتابل گروهی", support_group="نظرسنجی", taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskAssignIncidentToMe(driver)
    if result_task == False: return "STEP_Assigntome_6 Failed: Request Step wrong!, Function: Assigntome" 
    result_A = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=username_otherformat, support_group="نظرسنجی", taskName="Assigntome")
    if check_should_exist_Tasks(driver, "taskAssignIncidentToMe"): return "Failed: Task ReleaseIncident button not should exist but found"
    if "Success" in result_B and "Success" in result_A: return "STEP_Assigntome_6: Success Assign To Me Checked Resolved status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignIncident_1(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group="ممیزی", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    selected_user, result_task = taskAssignIncident(driver)
    if result_task == False: return "STEP_AssignIncident_1 Failed: Request Step wrong!, Function: AssignIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=selected_user, support_group="ممیزی", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignIncident_1: Success Assign Incident Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignIncident_2(driver):
    taskPark(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="متوقف شده", assignee="کارتابل گروهی", support_group="ممیزی", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    selected_user, result_task = taskAssignIncident(driver)
    if result_task == False: return "STEP_AssignIncident_2 Failed: Request Step wrong!, Function: AssignIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=selected_user, support_group="ممیزی", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignIncident_2: Success Assign Incident Checked Pendings to Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignIncident_3(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    selected_user, result_task = taskAssignIncident(driver)
    if result_task == False: return "STEP_AssignIncident_3 Failed: Request Step wrong!, Function: AssignIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=selected_user, support_group="ممیزی", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignIncident_3: Success Assign Incident Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignIncident_4(driver):
    taskAssignToTechnicals(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    selected_user, result_task = taskAssignIncident(driver)
    if result_task == False: return "STEP_AssignIncident_4 Failed: Request Step wrong!, Function: AssignIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=selected_user, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignIncident_4: Success Assign Incident Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignIncident_5(driver):
    taskPark(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="متوقف شده", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    selected_user, result_task = taskAssignIncident(driver)
    if result_task == False: return "STEP_AssignIncident_5 Failed: Request Step wrong!, Function: AssignIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=selected_user, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignIncident_5: Success Assign Incident Checked Pendings to Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignIncident_6(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    selected_user, result_task = taskAssignIncident(driver)
    if result_task == False: return "STEP_AssignIncident_6 Failed: Request Step wrong!, Function: AssignIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=selected_user, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignIncident_6: Success Assign Incident Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignIncident_7(driver):
    taskSendToAnalysis(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group="تحلیل", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    selected_user, result_task = taskAssignIncident(driver)
    if result_task == False: return "STEP_AssignIncident_7 Failed: Request Step wrong!, Function: AssignIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=selected_user, support_group="تحلیل", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignIncident_7: Success Assign Incident Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignIncident_8(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="تحلیل", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    selected_user, result_task = taskAssignIncident(driver)
    if result_task == False: return "STEP_AssignIncident_8 Failed: Request Step wrong!, Function: AssignIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=selected_user, support_group="تحلیل", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignIncident_8: Success Assign Incident Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignIncident_9(driver):
    taskSendToFeedback(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="حل شده", assignee="کارتابل گروهی", support_group="نظرسنجی", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    selected_user, result_task = taskAssignIncident(driver)
    if result_task == False: return "STEP_AssignIncident_9 Failed: Request Step wrong!, Function: AssignIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=selected_user, support_group="نظرسنجی", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignIncident_9: Success Assign Incident Checked Resolved status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignIncident_10(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=username_otherformat, support_group="نظرسنجی", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    selected_user, result_task = taskAssignIncident(driver)
    if result_task == False: return "STEP_AssignIncident_10 Failed: Request Step wrong!, Function: AssignIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=selected_user, support_group="نظرسنجی", taskName="AssignIncident")
    if check_should_exist_Tasks(driver, "taskAssignIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignIncident_10: Success Assign Incident Checked Resolved status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_ReleaseIncident_1(driver):
    if check_not_should_exist_Tasks(driver, "taskReleaseIncident"): return "Failed: Task ReleaseIncident button not should exist but found"
    taskAssignIncidentToMe(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="ReleaseIncident")
    if check_should_exist_Tasks(driver, "taskReleaseIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskReleaseIncident(driver)
    if result_task == False: return "STEP_ReleaseIncident_1 Failed: Request Step wrong!, Function: ReleaseIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group="ممیزی", taskName="ReleaseIncident")
    if check_not_should_exist_Tasks(driver, "taskReleaseIncident"): return "Failed: Task ReleaseIncident button not should exist but found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_ReleaseIncident_1: Success Release Incident Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_ReleaseIncident_2(driver):
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskReleaseIncident"): return "Failed: Task AssiReleaseIncidentgn button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_ReleaseIncident_2: Success Release Incident Checked Pending status"

def STEP_ReleaseIncident_3(driver):
    taskAssignToTechnicals(driver)
    if check_not_should_exist_Tasks(driver, "taskReleaseIncident"): return "Failed: Task ReleaseIncident button not should exist but found"
    taskAssignIncidentToMe(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="ReleaseIncident")
    if check_should_exist_Tasks(driver, "taskReleaseIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskReleaseIncident(driver)
    if result_task == False: return "STEP_ReleaseIncident_3 Failed: Request Step wrong!, Function: ReleaseIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="ReleaseIncident")
    if check_not_should_exist_Tasks(driver, "taskReleaseIncident"): return "Failed: Task ReleaseIncident button not should exist but found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_ReleaseIncident_3: Success Release Incident Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_ReleaseIncident_4(driver):
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskReleaseIncident"): return "Failed: Task ReleaseIncident button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_ReleaseIncident_4: Success Release Incident Checked Pending status"

def STEP_ReleaseIncident_5(driver):
    taskSendToAnalysis(driver)
    if check_not_should_exist_Tasks(driver, "taskReleaseIncident"): return "Failed: Task ReleaseIncident button not should exist but found"
    taskAssignIncidentToMe(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="تحلیل", taskName="ReleaseIncident")
    if check_should_exist_Tasks(driver, "taskReleaseIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskReleaseIncident(driver)
    if result_task == False: return "STEP_ReleaseIncident_5 Failed: Request Step wrong!, Function: ReleaseIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group="تحلیل", taskName="ReleaseIncident")
    if check_not_should_exist_Tasks(driver, "taskReleaseIncident"): return "Failed: Task ReleaseIncident button not should exist but found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_ReleaseIncident_5: Success Release Incident Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_ReleaseIncident_6(driver):
    taskSendToFeedback(driver)
    if check_not_should_exist_Tasks(driver, "taskReleaseIncident"): return "Failed: Task ReleaseIncident button not should exist but found"
    taskAssignIncidentToMe(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=username_otherformat, support_group="نظرسنجی", taskName="ReleaseIncident")
    if check_should_exist_Tasks(driver, "taskReleaseIncident") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskReleaseIncident(driver)
    if result_task == False: return "STEP_ReleaseIncident_6 Failed: Request Step wrong!, Function: ReleaseIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="حل شده", assignee="کارتابل گروهی", support_group="نظرسنجی", taskName="ReleaseIncident")
    if check_not_should_exist_Tasks(driver, "taskReleaseIncident"): return "Failed: Task ReleaseIncident button not should exist but found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A:return "STEP_ReleaseIncident_6: Success Release Incident Checked Resolved status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AddAttachment_1(driver):
    if check_not_should_exist_Tasks(driver, "taskAddAttachment"): return "Failed: Task AddAttachment button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_AddAttachment_1: Success Task AddAttachment button not should exist in Active status"

def STEP_AddAttachment_2(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="AddAttachment")
    if check_should_exist_Tasks(driver, "taskAddAttachment") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskAddAttachment(driver, filename1="upload_file_1.txt", filename2="upload_file_2.txt")
    if result_task == False: return "STEP_AddAttachment_2 Failed: Request Step wrong!, Function: AddAttachment" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="AddAttachment")
    if check_should_exist_Tasks(driver, "taskAddAttachment") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    if is_file_removed(driver, filename="upload_file_2.txt") == False: return "Failed: Remove uploaded file on task"
    if is_file_uploaded(driver, filename="upload_file_1.txt") == False: return "Failed: The file is not uploaded"
    if is_file_downloaded(driver, filename="upload_file_1.txt") == False: return "Failed: The file is not downloadable"
    if remove_uploaded_file_inTicket(driver, filename="upload_file_1.txt") == False: return "Failed: remove uploaded file inTicket failed"
    if is_file_removed(driver, filename="upload_file_1.txt") == False: return "Failed: Remove uploaded file on ticket"
    if "Success" in result_B and "Success" in result_A: return "STEP_AddAttachment_2: Success Task AddAttachment Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AddAttachment_3(driver):
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskAddAttachment"): return "Failed: Task AddAttachment button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_AddAttachment_3: Success Task AddAttachment button not should exist in Pending status"

def STEP_AddAttachment_4(driver):
    taskAssignToTechnicals(driver)
    if check_not_should_exist_Tasks(driver, "taskAddAttachment"): return "Failed: Task AddAttachment button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_AddAttachment_4: Success Task AddAttachment button not should exist in Active status"

def STEP_AddAttachment_5(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AddAttachment")
    if check_should_exist_Tasks(driver, "taskAddAttachment") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskAddAttachment(driver, filename1="upload_file_1.txt", filename2="upload_file_2.txt")
    if result_task == False: return "STEP_AddAttachment_5 Failed: Request Step wrong!, Function: AddAttachment" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AddAttachment")
    if check_should_exist_Tasks(driver, "taskAddAttachment") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    if is_file_removed(driver, filename="upload_file_2.txt") == False: return "Failed: Remove uploaded file on task"
    if is_file_uploaded(driver, filename="upload_file_1.txt") == False: return "Failed: The file is not uploaded"
    if is_file_downloaded(driver, filename="upload_file_1.txt") == False: return "Failed: The file is not downloadable"
    if remove_uploaded_file_inTicket(driver, filename="upload_file_1.txt") == False: return "Failed: remove uploaded file inTicket failed"
    if is_file_removed(driver, filename="upload_file_1.txt") == False: return "Failed: Remove uploaded file on ticket"
    if "Success" in result_B and "Success" in result_A: return "STEP_AddAttachment_5: Success Task AddAttachment Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AddAttachment_6(driver):
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskAddAttachment"): return "Failed: Task AddAttachment button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_AddAttachment_6: Success Task AddAttachment button not should exist in Pending status"

def STEP_AddAttachment_7(driver):
    taskSendToAnalysis(driver)
    if check_not_should_exist_Tasks(driver, "taskAddAttachment"): return "Failed: Task AddAttachment button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_AddAttachment_7: Success Task AddAttachment button not should exist in Active status"

def STEP_AddAttachment_8(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="تحلیل", taskName="AddAttachment")
    if check_should_exist_Tasks(driver, "taskAddAttachment") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    result_task = taskAddAttachment(driver, filename1="upload_file_1.txt", filename2="upload_file_2.txt")
    if result_task == False: return "STEP_AddAttachment_5 Failed: Request Step wrong!, Function: AddAttachment" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="تحلیل", taskName="AddAttachment")
    if check_should_exist_Tasks(driver, "taskAddAttachment") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    if check_should_exist_Tasks(driver, "taskAddAttachment") == False: return "Failed: Task ReleaseIncident button should exist but not found"
    if is_file_removed(driver, filename="upload_file_2.txt") == False: return "Failed: Remove uploaded file on task"
    if is_file_uploaded(driver, filename="upload_file_1.txt") == False: return "Failed: The file is not uploaded"
    if is_file_downloaded(driver, filename="upload_file_1.txt") == False: return "Failed: The file is not downloadable"
    if remove_uploaded_file_inTicket(driver, filename="upload_file_1.txt") == False: return "Failed: remove uploaded file inTicket failed"
    if is_file_removed(driver, filename="upload_file_1.txt") == False: return "Failed: Remove uploaded file on ticket"
    if "Success" in result_B and "Success" in result_A: return "STEP_AddAttachment_8: Success Task AddAttachment Checked Active status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AddAttachment_9(driver):
    taskSendToFeedback(driver)
    if check_not_should_exist_Tasks(driver, "taskAddAttachment"): return "Failed: Task AddAttachment button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskAddAttachment"): return "Failed: Task AddAttachment button not should exist but found"
    return "STEP_AddAttachment_10: Success Task AddAttachment button not should exist in resolved status"

def STEP_Park_1(driver):
    if check_not_should_exist_Tasks(driver, "taskPark"): return "Failed: Task Park button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_Park_1: Success Task Park button not should exist in Active status"

def STEP_Park_2(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="Park")
    if check_should_exist_Tasks(driver, "taskPark") == False: return "Failed: Task Park button should exist but not found"
    result_task = taskPark(driver)
    if result_task == False: return "STEP_Park_2 Failed: Request Step wrong!, Function: Park" 
    result_A = Check_Befor_After_Task_Status(driver, status="متوقف شده", assignee="کارتابل گروهی", support_group="ممیزی", taskName="Park")
    if check_not_should_exist_Tasks(driver, "taskPark"): return "Failed: Task Park button not should exist but found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_Park_2: Success Task Park Checked Pending status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_Park_3(driver):
    taskAssignToTechnicals(driver)
    if check_not_should_exist_Tasks(driver, "taskPark"): return "Failed: Task Park button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_Park_3: Success Task Park button not should exist in Active status"

def STEP_Park_4(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="Park")
    if check_should_exist_Tasks(driver, "taskPark") == False: return "Failed: Task Park button should exist but not found"
    result_task = taskPark(driver)
    if result_task == False: return "STEP_Park_4 Failed: Request Step wrong!, Function: Park" 
    result_A = Check_Befor_After_Task_Status(driver, status="متوقف شده", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="Park")
    if check_not_should_exist_Tasks(driver, "taskPark"): return "Failed: Task Park button not should exist but found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_Park_4: Success Task Park Checked Pending status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_Park_5(driver):
    taskSendToAnalysis(driver)
    if check_not_should_exist_Tasks(driver, "taskPark"): return "Failed: Task Park button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskPark"): return "Failed: Task Park button not should exist but found"
    return "STEP_Park_5: Success Task Park button not should exist in Active status"

def STEP_Park_6(driver):
    taskSendToFeedback(driver)
    if check_not_should_exist_Tasks(driver, "taskPark"): return "Failed: Task Park button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskPark"): return "Failed: Task Park button not should exist but found"
    return "STEP_Park_7: Success Task Park button not should exist in Resolved status"

def STEP_ChangeSchedule_1(driver):
    if check_not_should_exist_Tasks(driver, "taskChangeSchedule"): return "Failed: Task ChangeSchedule button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeSchedule"): return "Failed: Task ChangeSchedule button not should exist but found"
    taskPark(driver)
    return "STEP_ChangeSchedule_1: Success Task ChangeSchedule button not should exist in Active status"

def STEP_ChangeSchedule_2(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="متوقف شده", assignee="کارتابل گروهی", support_group="ممیزی", taskName="ChangeSchedule")
    if check_should_exist_Tasks(driver, "taskChangeSchedule") == False: return "Failed: Task ChangeSchedule button should exist but not found"
    result_task = taskChangeSchedule(driver)
    if result_task[0] == False: return "STEP_ChangeSchedule_2 Failed: Task Step wrong!, Function: ChangeSchedule"
    if result_task[1] == False: return "STEP_ChangeSchedule_2 Failed: Request Step wrong!, Function: ChangeSchedule"
    result_A = Check_Befor_After_Task_Status(driver, status="متوقف شده", assignee="کارتابل گروهی", support_group="ممیزی", taskName="ChangeSchedule")
    if check_should_exist_Tasks(driver, "taskChangeSchedule") == False: return "Failed: Task ChangeSchedule button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_ChangeSchedule_2: Success Task ChangeSchedule Checked Pending status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_ChangeSchedule_3(driver):
    taskAssignToTechnicals(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeSchedule"): return "Failed: Task ChangeSchedule button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeSchedule"): return "Failed: Task ChangeSchedule button not should exist but found"
    taskPark(driver)
    return "STEP_ChangeSchedule_3: Success Task ChangeSchedule button not should exist in Active status"

def STEP_ChangeSchedule_4(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="متوقف شده", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="ChangeSchedule")
    if check_should_exist_Tasks(driver, "taskChangeSchedule") == False: return "Failed: Task ChangeSchedule button should exist but not found"
    result_task = taskChangeSchedule(driver)
    if result_task[0] == False: return "STEP_ChangeSchedule_4 Failed: Task Step wrong!, Function: ChangeSchedule"
    if result_task[1] == False: return "STEP_ChangeSchedule_4 Failed: Request Step wrong!, Function: ChangeSchedule"
    result_A = Check_Befor_After_Task_Status(driver, status="متوقف شده", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="ChangeSchedule")
    if check_should_exist_Tasks(driver, "taskChangeSchedule") == False: return "Failed: Task ChangeSchedule button should exist but not found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_ChangeSchedule_4: Success Task ChangeSchedule Checked Pending status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_ChangeSchedule_5(driver):
    taskSendToAnalysis(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeSchedule"): return "Failed: Task ChangeSchedule button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeSchedule"): return "Failed: Task ChangeSchedule button not should exist but found"
    return "STEP_ChangeSchedule_5: Success Task ChangeSchedule button not should exist in Active status"

def STEP_ChangeSchedule_6(driver):
    taskSendToFeedback(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeSchedule"): return "Failed: Task ChangeSchedule button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeSchedule"): return "Failed: Task ChangeSchedule button not should exist but found"
    return "STEP_ChangeSchedule_6: Success Task ChangeSchedule button not should exist in Resolved status"

def STEP_AssignToTechnicals_1(driver):
    if check_not_should_exist_Tasks(driver, "taskAssignToTechnicals"): return "Failed: Task AssignToTechnicals button not should exist but found"
    taskAssignIncidentToMe(driver)
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskAssignToTechnicals"): return "Failed: Task AssignToTechnicals button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_AssignToTechnicals_1: Success Task AssignToTechnicals button not should exist in this Active and Pending status"

def STEP_AssignToTechnicals_2(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="AssignToTechnicals")
    if check_should_exist_Tasks(driver, "taskAssignToTechnicals") == False: return "Failed: Task AssignToTechnicals button should exist but not found"
    result_task = taskAssignToTechnicals(driver)
    if result_task[0] == False: return "STEP_AssignToTechnicals_2 Failed: Task Step wrong!, Function: AssignToTechnicals"
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToTechnicals")
    if check_not_should_exist_Tasks(driver, "taskAssignToTechnicals"): return "Failed: Task AssignToTechnicals button not should exist but found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignToTechnicals_2: Success Task AssignToTechnicals Checked Active (aduit) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A
    
def STEP_AssignToTechnicals_3(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToTechnicals")
    if check_should_exist_Tasks(driver, "taskAssignToTechnicals") == False: return "Failed: Task AssignToTechnicals button should exist but not found"
    result_task = taskAssignToTechnicals(driver)
    if result_task[0] == False: return "STEP_AssignToTechnicals_3 Failed: Task Step wrong!, Function: AssignToTechnicals"
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToTechnicals")
    if check_not_should_exist_Tasks(driver, "taskAssignToTechnicals"): return "Failed: Task AssignToTechnicals button not should exist but found"
    taskAssignIncidentToMe(driver)
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignToTechnicals_3: Success Task AssignToTechnicals Checked Active (Technicals) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignToTechnicals_4(driver):
    taskSendToAnalysis(driver)
    if check_not_should_exist_Tasks(driver, "taskAssignToTechnicals"): return "Failed: Task AssignToTechnicals button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskAssignToTechnicals"): return "Failed: Task AssignToTechnicals button not should exist but found"
    return "STEP_AssignToTechnicals_4: Success Task AssignToTechnicals button not should exist in this Active status"

def STEP_AssignToTechnicals_5(driver):
    taskSendToFeedback(driver)
    if check_not_should_exist_Tasks(driver, "taskAssignToTechnicals"): return "Failed: Task AssignToTechnicals button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskAssignToTechnicals"): return "Failed: Task AssignToTechnicals button not should exist but found"
    return "STEP_AssignToTechnicals_5: Success Task AssignToTechnicals button not should exist in this Resolved status"

def STEP_SendToAnalysis_1(driver):
    if check_not_should_exist_Tasks(driver, "taskSendToAnalysis"): return "Failed: Task SendToAnalysis button not should exist but found"
    taskAssignIncidentToMe(driver)
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskSendToAnalysis"): return "Failed: Task SendToAnalysis button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_SendToAnalysis_1: Success Task SendToAnalysis button not should exist in this Active and Pending status"

def STEP_SendToAnalysis_2(driver):
    taskAssignToTechnicals(driver)
    if check_not_should_exist_Tasks(driver, "taskSendToAnalysis"): return "Failed: Task SendToAnalysis button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_should_exist_Tasks(driver, "taskSendToAnalysis") == False: return "Failed: Task SendToAnalysis button should exist but not found"
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskSendToAnalysis"): return "Failed: Task SendToAnalysis button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_SendToAnalysis_2: Success Task SendToAnalysis button not should exist in this Active and Pending status"

def STEP_SendToAnalysis_3(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="SendToAnalysis")
    result_task = taskSendToAnalysis(driver)
    if result_task == False: return "STEP_SendToAnalysis_3 Failed: Request Step wrong!, Function: SendToAnalysis" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group="تحلیل", taskName="SendToAnalysis")
    if check_not_should_exist_Tasks(driver, "taskSendToAnalysis"): return "Failed: Task SendToAnalysis button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskSendToAnalysis"): return "Failed: Task SendToAnalysis button not should exist but found"
    if "Success" in result_B and "Success" in result_A: return "STEP_SendToAnalysis_3: Success Task SendToAnalysis Checked Active (Technicals) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_SendToAnalysis_4(driver):
    taskSendToFeedback(driver)
    if check_not_should_exist_Tasks(driver, "taskSendToAnalysis"): return "Failed: Task SendToAnalysis button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskSendToAnalysis"): return "Failed: Task SendToAnalysis button not should exist but found"
    return "STEP_SendToAnalysis_4: Success Task SendToAnalysis button not should exist in this resolved status"

def STEP_SendToFeedback_1(driver):
    if check_not_should_exist_Tasks(driver, "taskSendToFeedback"): return "Failed: Task SendToFeedback button not should exist but found"
    taskAssignIncidentToMe(driver)
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskSendToFeedback"): return "Failed: Task SendToFeedback button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_SendToFeedback_1: Success Task SendToFeedback button not should exist in this Active and Pending status"

def STEP_SendToFeedback_2(driver):
    taskAssignToTechnicals(driver)
    if check_not_should_exist_Tasks(driver, "taskSendToFeedback"): return "Failed: Task SendToFeedback button not should exist but found"
    taskAssignIncidentToMe(driver)
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskSendToFeedback"): return "Failed: Task SendToFeedback button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_SendToFeedback_2: Success Task SendToFeedback button not should exist in this Active and Pending status"

def STEP_SendToFeedback_3(driver):
    taskSendToAnalysis(driver)
    if check_not_should_exist_Tasks(driver, "taskSendToFeedback"): return "Failed: Task SendToFeedback button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_should_exist_Tasks(driver, "taskSendToFeedback") == False: return "Failed: Task SendToFeedback button should exist but not found"
    return "STEP_SendToFeedback_3: Success Task SendToFeedback button not should exist in this Active (Analysis) status"

def STEP_SendToFeedback_4(driver):
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='تحلیل', taskName="SendToFeedback")
    result_task = taskSendToFeedback(driver)
    if result_task == False: return "STEP_SendToFeedback_4 Failed: Request Step wrong!, Function: SendToFeedback" 
    result_A = Check_Befor_After_Task_Status(driver, status="حل شده", assignee="کارتابل گروهی", support_group='نظرسنجی', taskName="SendToFeedback")
    if "Success" in result_B and "Success" in result_A: return "STEP_SendToFeedback_4: Success Task SendToFeedback Checked resolved (Feedback) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_ChangeTTType_1(driver):
    if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
    taskAssignIncidentToMe(driver)
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
    taskAssignIncidentToMe(driver)
    befor_ServiceType = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ServiceType"]'))).text
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='ممیزی', taskName="ChangeTTType")
    if check_should_exist_Tasks(driver, "taskChangeTTType") == False: return "Failed: Task ChangeTTType button should exist but not found"
    result_task = taskChangeTTType(driver)
    if result_task[1] == False : return "STEP_ChangeTTType_1 Failed: Task Step wrong!, Function: ChangeTTType"
    after_ServiceType = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ServiceType"]'))).text
    if befor_ServiceType == "Business" and after_ServiceType == "Business" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='ممیزی', taskName="ChangeTTType")
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_1: Success Task ChangeTTType Check Active (aduit) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif befor_ServiceType == "Business" and after_ServiceType == "Network" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group='ممیزی', taskName="ChangeTTType")
        if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
        taskAssignIncidentToMe(driver)
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_1: Success Task ChangeTTType Check Active (aduit) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif befor_ServiceType == "Network" and after_ServiceType == "Network" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='ممیزی', taskName="ChangeTTType")
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_1: Success Task ChangeTTType Check Active (aduit) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif befor_ServiceType == "Network" and after_ServiceType == "Business" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group='ممیزی', taskName="ChangeTTType")
        if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
        taskAssignIncidentToMe(driver)
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_1: Success Task ChangeTTType Check Active (aduit) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif result_task[0] == False:
        "STEP_ChangeTTType_1 Failed: Request Step wrong!, Function: submit_finish_and_check_ChangeTicketType" 
    else:
        raise Exception(f"STEP_ChangeTTType_1 Request Step Error: {result_task[0]}")

def STEP_ChangeTTType_2(driver):
    taskAssignToTechnicals(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
    taskAssignIncidentToMe(driver)
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_ChangeTTType_2: Success Task ChangeTTType button not should exist in this Active and Pending status"

def STEP_ChangeTTType_3(driver):
    taskSendToAnalysis(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
    taskAssignIncidentToMe(driver)
    befor_ServiceType = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ServiceType"]'))).text
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='تحلیل', taskName="ChangeTTType")
    if check_should_exist_Tasks(driver, "taskChangeTTType") == False: return "Failed: Task ChangeTTType button should exist but not found"
    result_task = taskChangeTTType(driver)
    if result_task[1] == False : return "STEP_ChangeTTType_1 Failed: Task Step wrong!, Function: ChangeTTType"
    after_ServiceType = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ServiceType"]'))).text
    if befor_ServiceType == "Business" and after_ServiceType == "Business" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='تحلیل', taskName="ChangeTTType")
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_3: Success Task ChangeTTType Check Active (analysis) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif befor_ServiceType == "Business" and after_ServiceType == "Network" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group='ممیزی', taskName="ChangeTTType")
        if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
        taskAssignIncidentToMe(driver)
        taskSendToAnalysis(driver)
        taskAssignIncidentToMe(driver)
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_3: Success Task ChangeTTType Check Active (analysis) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif befor_ServiceType == "Network" and after_ServiceType == "Network" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='تحلیل', taskName="ChangeTTType")
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_3: Success Task ChangeTTType Check Active (analysis) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif befor_ServiceType == "Network" and after_ServiceType == "Business" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group='ممیزی', taskName="ChangeTTType")
        if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
        taskAssignIncidentToMe(driver)
        taskSendToAnalysis(driver)
        taskAssignIncidentToMe(driver)
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_3: Success Task ChangeTTType Check Active (analysis) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif result_task[0] == False:
        "STEP_ChangeTTType_3 Failed: Request Step wrong!, Function: submit_finish_and_check_ChangeTicketType" 
    else:
        raise Exception(f"STEP_ChangeTTType_3 Request Step Error: {result_task[0]}")

def STEP_ChangeTTType_4(driver):
    taskSendToFeedback(driver)
    if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
    taskAssignIncidentToMe(driver)
    befor_ServiceType = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ServiceType"]'))).text
    result_B = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=username_otherformat, support_group='نظرسنجی', taskName="ChangeTTType")
    if check_should_exist_Tasks(driver, "taskChangeTTType") == False: return "Failed: Task ChangeTTType button should exist but not found"
    result_task = taskChangeTTType(driver)
    if result_task[1] == False : return "STEP_ChangeTTType_1 Failed: Task Step wrong!, Function: ChangeTTType"
    after_ServiceType = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ServiceType"]'))).text
    if befor_ServiceType == "Business" and after_ServiceType == "Business" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=username_otherformat, support_group='نظرسنجی', taskName="ChangeTTType")
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_4: Success Task ChangeTTType Check resolved (feedback) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif befor_ServiceType == "Business" and after_ServiceType == "Network" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group='ممیزی', taskName="ChangeTTType")
        if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_4: Success Task ChangeTTType Check resolved (feedback) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif befor_ServiceType == "Network" and after_ServiceType == "Network" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=username_otherformat, support_group='نظرسنجی', taskName="ChangeTTType")
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_4: Success Task ChangeTTType Check Actresolvedive (feedback) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif befor_ServiceType == "Network" and after_ServiceType == "Business" and result_task[0] == True:
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group='ممیزی', taskName="ChangeTTType")
        if check_not_should_exist_Tasks(driver, "taskChangeTTType"): return "Failed: Task ChangeTTType button not should exist but found"
        if "Success" in result_B and "Success" in result_A: return "STEP_ChangeTTType_4: Success Task ChangeTTType Check resolved (feedback) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    elif result_task[0] == False:
        "STEP_ChangeTTType_4 Failed: Request Step wrong!, Function: submit_finish_and_check_ChangeTicketType" 
    else:
        raise Exception(f"STEP_ChangeTTType_4 Request Step Error: {result_task[0]}")

def STEP_UpdateCoordinate_1(driver):
    if Check_Network_ServiceType(driver) == False: return "STEP_UpdateCoordinate_1: Failed Task UpdateCoordinate, ServiceType should be Network but not"
    if check_not_should_exist_Tasks(driver, "taskUpdateCoordinate"): return "Failed: Task UpdateCoordinate button not should exist but found"
    taskAssignIncidentToMe(driver)
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskUpdateCoordinate"): return "Failed: Task UpdateCoordinate button not should exist but found"
    taskAssignIncidentToMe(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='ممیزی', taskName="UpdateCoordinate")
    if check_should_exist_Tasks(driver, "taskUpdateCoordinate") == False: return "Failed: Task UpdateCoordinate button should exist but not found"
    result_task = taskUpdateCoordinate(driver)
    if result_task == False: return "STEP_UpdateCoordinate_1 Failed: Request Step wrong!, Function: taskUpdateCoordinate" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='ممیزی', taskName="UpdateCoordinate")
    if check_should_exist_Tasks(driver, "taskUpdateCoordinate") == False: return "Failed: Task UpdateCoordinate button should exist but not found"
    if "Success" in result_B and "Success" in result_A: return "STEP_UpdateCoordinate_1: Success Task UpdateCoordinate Check Active (aduit) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_UpdateCoordinate_2(driver):
    taskAssignToTechnicals(driver)
    if check_not_should_exist_Tasks(driver, "taskUpdateCoordinate"): return "Failed: Task UpdateCoordinate button not should exist but found"
    taskAssignIncidentToMe(driver)
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskUpdateCoordinate"): return "Failed: Task UpdateCoordinate button not should exist but found"
    taskAssignIncidentToMe(driver)
    return "STEP_UpdateCoordinate_2: Success Task UpdateCoordinate button not should exist in this Active and Pending status"

def STEP_UpdateCoordinate_3(driver):
    taskSendToAnalysis(driver)
    if check_not_should_exist_Tasks(driver, "taskUpdateCoordinate"): return "Failed: Task UpdateCoordinate button not should exist but found"
    taskAssignIncidentToMe(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='تحلیل', taskName="UpdateCoordinate")
    if check_should_exist_Tasks(driver, "taskUpdateCoordinate") == False: return "Failed: Task UpdateCoordinate button should exist but not found"
    result_task = taskUpdateCoordinate(driver)
    if result_task == False: return "STEP_UpdateCoordinate_3 Failed: Request Step wrong!, Function: taskUpdateCoordinate" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='تحلیل', taskName="UpdateCoordinate")
    if check_should_exist_Tasks(driver, "taskUpdateCoordinate") == False: return "Failed: Task UpdateCoordinate button should exist but not found"
    if "Success" in result_B and "Success" in result_A: return "STEP_UpdateCoordinate_3: Success Task UpdateCoordinate Check Active (analysis) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_UpdateCoordinate_4(driver):
    taskSendToFeedback(driver)
    if check_not_should_exist_Tasks(driver, "taskUpdateCoordinate"): return "Failed: Task UpdateCoordinate button not should exist but found"
    taskAssignIncidentToMe(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=username_otherformat, support_group='نظرسنجی', taskName="UpdateCoordinate")
    if check_should_exist_Tasks(driver, "taskUpdateCoordinate") == False: return "Failed: Task UpdateCoordinate button should exist but not found"
    result_task = taskUpdateCoordinate(driver)
    if result_task == False: return "STEP_UpdateCoordinate_4 Failed: Request Step wrong!, Function: taskUpdateCoordinate" 
    result_A = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=username_otherformat, support_group='نظرسنجی', taskName="UpdateCoordinate")
    if check_should_exist_Tasks(driver, "taskUpdateCoordinate") == False: return "Failed: Task UpdateCoordinate button should exist but not found"
    if "Success" in result_B and "Success" in result_A: return "STEP_UpdateCoordinate_4: Success Task UpdateCoordinate Check Resolved (feedback) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_SupplemantaryQuestions_1(driver):
    if Check_Network_ServiceType(driver) == False: return "STEP_SupplemantaryQuestions_1: Failed Task SupplemantaryQuestions, ServiceType should be Network but not"
    if check_not_should_exist_Tasks(driver, "taskSupplemantaryQuestions"): return "Failed: Task SupplemantaryQuestions button not should exist but found"
    taskAssignIncidentToMe(driver)
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskSupplemantaryQuestions"): return "Failed: Task SupplemantaryQuestions button not should exist but found"
    taskAssignIncidentToMe(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='ممیزی', taskName="SupplemantaryQuestions")
    if check_should_exist_Tasks(driver, "taskSupplemantaryQuestions") == False: return "Failed: Task SupplemantaryQuestions button should exist but not found"
    result_task = taskSupplemantaryQuestions(driver)
    if result_task == False: return "STEP_SupplemantaryQuestions_1 Failed: Request Step wrong!, Function: taskSupplemantaryQuestions" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group='ممیزی', taskName="SupplemantaryQuestions")
    if check_should_exist_Tasks(driver, "taskSupplemantaryQuestions") == False: return "Failed: Task SupplemantaryQuestions button should exist but not found"
    if "Success" in result_B and "Success" in result_A: return "STEP_SupplemantaryQuestions_1: Success Task SupplemantaryQuestions Check Active (aduit) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_SupplemantaryQuestions_2(driver):
    taskAssignToTechnicals(driver)
    if check_not_should_exist_Tasks(driver, "taskSupplemantaryQuestions"): return "Failed: Task SupplemantaryQuestions button not should exist but found"
    taskAssignIncidentToMe(driver)
    taskPark(driver)
    if check_not_should_exist_Tasks(driver, "taskSupplemantaryQuestions"): return "Failed: Task SupplemantaryQuestions button not should exist but found"
    taskAssignIncidentToMe(driver)
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="SupplemantaryQuestions")
    if check_should_exist_Tasks(driver, "taskSupplemantaryQuestions") == False: return "Failed: Task SupplemantaryQuestions button should exist but not found"
    result_task = taskSupplemantaryQuestions(driver)
    if result_task == False: return "STEP_SupplemantaryQuestions_2 Failed: Request Step wrong!, Function: taskSupplemantaryQuestions" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="SupplemantaryQuestions")
    if check_should_exist_Tasks(driver, "taskSupplemantaryQuestions") == False: return "Failed: Task SupplemantaryQuestions button should exist but not found"
    if "Success" in result_B and "Success" in result_A: return "STEP_SupplemantaryQuestions_2: Success Task SupplemantaryQuestions Check Active (technicals) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_SupplemantaryQuestions_3(driver):
    taskSendToAnalysis(driver)
    if check_not_should_exist_Tasks(driver, "taskSupplemantaryQuestions"): return "Failed: Task SupplemantaryQuestions button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskSupplemantaryQuestions"): return "Failed: Task SupplemantaryQuestions button not should exist but found"
    return "STEP_SupplemantaryQuestions_3: Success Task SupplemantaryQuestions button not should exist in this Active status"

def STEP_SupplemantaryQuestions_4(driver):
    taskSendToFeedback(driver)
    if check_not_should_exist_Tasks(driver, "taskSupplemantaryQuestions"): return "Failed: Task SupplemantaryQuestions button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskSupplemantaryQuestions"): return "Failed: Task SupplemantaryQuestions button not should exist but found"
    return "STEP_SupplemantaryQuestions_4: Success Task SupplemantaryQuestions button not should exist in this Resolved status"

def STEP_AssignToAudit_1(driver):
    if check_not_should_exist_Tasks(driver, "taskAssignToAudit"): return "Failed: Task AssignToAudit button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToAudit_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe" 
    if taskPark(driver) == False: return "STEP_AssignToAudit_1 Failed: Request Step wrong!, Function: taskPark" 
    if check_not_should_exist_Tasks(driver, "taskAssignToAudit"): return "Failed: Task AssignToAudit button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToAudit_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe" 
    return "STEP_AssignToAudit_1: Success Task AssignToAudit button not should exist in this Active and Pending status"

def STEP_AssignToAudit_2(driver):
    map = check_layer_map(driver)
    if taskAssignToTechnicals(driver) == False: return "STEP_AssignToAudit_2 Failed: Request Step wrong!, Function: taskAssignToTechnicals" 
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToAudit_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe" 
    if check_not_should_exist_Tasks(driver, "taskAssignToAudit"): return "Failed: Task AssignToAudit button not should exist but found"
    if taskPark(driver) == False: return "STEP_AssignToAudit_2 Failed: Request Step wrong!, Function: taskPark" 
    if check_not_should_exist_Tasks(driver, "taskAssignToAudit"): return "Failed: Task AssignToAudit button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToAudit_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe" 
    if taskAssignToTechnicals(driver) == False: return "STEP_AssignToAudit_2 Failed: Request Step wrong!, Function: taskAssignToTechnicals" 
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToAudit_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe" 
    if map[-2] != "ممیزی": 
        result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToAudit")
        if check_should_exist_Tasks(driver, "taskAssignToAudit") == False: return "Failed: Task AssignToAudit button should exist but not found"
        result_task = taskAssignToAudit(driver)
        if result_task == False: return "STEP_AssignToAudit_2 Failed: Request Step wrong!, Function: AssignToAudit" 
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee='کارتابل گروهی', support_group="ممیزی", taskName="AssignToAudit")
        if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToAudit_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe" 
        if taskAssignToTechnicals(driver) == False: return "STEP_AssignToAudit_2 Failed: Request Step wrong!, Function: taskAssignToTechnicals"
        if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToAudit_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe" 
        if "Success" in result_B and "Success" in result_A: return "STEP_AssignToAudit_2: Success Task AssignToAudit Check Active (technicals) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    else:
        return "Failed: Task AssignToAudit Conditions Error."

def STEP_AssignToAudit_3(driver):
    taskSendToAnalysis(driver)
    if check_not_should_exist_Tasks(driver, "taskAssignToAudit"): return "Failed: Task AssignToAudit button not should exist but found"
    map = check_layer_map(driver)
    taskAssignIncidentToMe(driver)
    map.append("تحلیل")
    if map[-2] != "ممیزی":
        result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="تحلیل", taskName="AssignToAudit")
        if check_should_exist_Tasks(driver, "taskSupplemantaryQuestions") == False: return "Failed: Task AssignToAudit button should exist but not found"
        result_task = taskAssignToAudit(driver)
        if result_task == False: return "STEP_AssignToAudit_3 Failed: Request Step wrong!, Function: AssignToAudit" 
        result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee='کارتابل گروهی', support_group="ممیزی", taskName="AssignToAudit")
        taskAssignIncidentToMe(driver)
        taskSendToAnalysis(driver)
        taskAssignIncidentToMe(driver)
        if check_not_should_exist_Tasks(driver, "taskAssignToAudit"): return "Failed: Task AssignToAudit button not should exist but found"
        if "Success" in result_B and "Success" in result_A: return "STEP_AssignToAudit_3: Success Task AssignToAudit Check Active (analysis) status"
        else:
            if "Failed" in result_B: return result_B
            elif "Failed" in result_A: return result_A
    else:
        return "Failed: Task AssignToAudit Conditions Error." 

def STEP_AssignToAudit_4(driver):
    taskSendToFeedback(driver)
    if check_not_should_exist_Tasks(driver, "taskAssignToAudit"): return "Failed: Task AssignToAudit button not should exist but found"
    taskAssignIncidentToMe(driver)
    if check_not_should_exist_Tasks(driver, "taskAssignToAudit"): return "Failed: Task AssignToAudit button not should exist but found"
    return "STEP_AssignToAudit_4: Success Task AssignToAudit button not should exist in this resolved status"

def STEP_AssignToPreviousSg_1(driver):
    # if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    # if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    # if taskPark(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskPark"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignToTechnicals(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskAssignToTechnicals"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToPreviousSg")
    result_task = taskAssignToPreviousSg(driver)
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee='کارتابل گروهی', support_group="ممیزی", taskName="AssignToPreviousSg")
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if "Failed" in result_B or "Failed" in result_A: return "STEP_AssignToPreviousSg_1 - 0.1 Failed: Task AssignToPreviousSg Conditions Error., Function: taskAssignToPreviousSg"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="AssignToPreviousSg")
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    result_task = taskAssignToPreviousSg(driver)
    if result_task == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskAssignToPreviousSg" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee='کارتابل گروهی', support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToPreviousSg")
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if "Failed" in result_B or "Failed" in result_A: return "STEP_AssignToPreviousSg_1 - 0.2 Failed: Task AssignToPreviousSg Conditions Error., Function: taskAssignToPreviousSg"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToPreviousSg")
    result_task = taskAssignToPreviousSg(driver)
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee='کارتابل گروهی', support_group="ممیزی", taskName="AssignToPreviousSg")
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if "Failed" in result_B or "Failed" in result_A: return "STEP_AssignToPreviousSg_1 - 0.3 Failed: Task AssignToPreviousSg Conditions Error., Function: taskAssignToPreviousSg"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if taskSendToAnalysis(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskSendToAnalysis"    
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="تحلیل", taskName="AssignToPreviousSg")
    result_task = taskAssignToPreviousSg(driver)
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee='کارتابل گروهی', support_group="ممیزی", taskName="AssignToPreviousSg")
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if "Failed" in result_B or "Failed" in result_A: return "STEP_AssignToPreviousSg_1 - 0.4 Failed: Task AssignToPreviousSg Conditions Error., Function: taskAssignToPreviousSg"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignToPreviousSg_1: Success Task AssignToPreviousSg Check Active (aduit) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignToPreviousSg_2(driver):
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="AssignToPreviousSg")
    result_task = taskAssignToPreviousSg(driver)
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="ممیزی", taskName="AssignToPreviousSg")
    if taskAssignToTechnicals(driver) == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskAssignToTechnicals"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if taskPark(driver) == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskPark"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToPreviousSg")
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    result_task = taskAssignToPreviousSg(driver)
    if result_task == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskAssignToPreviousSg" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee='کارتابل گروهی', support_group="ممیزی", taskName="AssignToPreviousSg")
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if "Failed" in result_B or "Failed" in result_A: return "STEP_AssignToPreviousSg_2 - 0.1 Failed: Task AssignToPreviousSg Conditions Error., Function: taskAssignToPreviousSg"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    if taskAssignToTechnicals(driver) == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskAssignToTechnicals"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if taskSendToAnalysis(driver) == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskSendToAnalysis"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="تحلیل", taskName="AssignToPreviousSg")
    result_task = taskAssignToPreviousSg(driver)
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee="کارتابل گروهی", support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToPreviousSg")
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if "Failed" in result_B or "Failed" in result_A: return "STEP_AssignToPreviousSg_2 - 0.2 Failed: Task AssignToPreviousSg Conditions Error., Function: taskAssignToPreviousSg"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToPreviousSg")
    result_task = taskAssignToPreviousSg(driver)
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToPreviousSg")
    if "Failed" in result_B or "Failed" in result_A: return "STEP_AssignToPreviousSg_2 - 0-3 Failed: Task AssignToPreviousSg Conditions Error., Function: taskAssignToPreviousSg"
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignToPreviousSg_2: Success Task AssignToPreviousSg Check Active (technicals) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignToPreviousSg_3(driver):
    if taskSendToAnalysis(driver) == False: return "STEP_AssignToPreviousSg_3 Failed: Request Step wrong!, Function: taskSendToAnalysis"    
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_3 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    result_B = Check_Befor_After_Task_Status(driver, status="فعال", assignee=username_otherformat, support_group="تحلیل", taskName="AssignToPreviousSg")
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    result_task = taskAssignToPreviousSg(driver)
    if result_task == False: return "STEP_AssignToPreviousSg_3 Failed: Request Step wrong!, Function: taskAssignToPreviousSg" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee='کارتابل گروهی', support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToPreviousSg")
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_3 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    if taskSendToAnalysis(driver) == False: return "STEP_AssignToPreviousSg_3 Failed: Request Step wrong!, Function: taskSendToAnalysis"    
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_3 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignToPreviousSg_3: Success Task AssignToPreviousSg Check Active (analysis) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_AssignToPreviousSg_4(driver):
    if taskSendToFeedback(driver) == False: return "STEP_AssignToPreviousSg_4 Failed: Request Step wrong!, Function: taskSendToFeedback"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_4 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    result_B = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=username_otherformat, support_group="نظرسنجی", taskName="AssignToPreviousSg")
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    result_task = taskAssignToPreviousSg(driver)
    if result_task == False: return "STEP_AssignToPreviousSg_4 Failed: Request Step wrong!, Function: taskAssignToPreviousSg" 
    result_A = Check_Befor_After_Task_Status(driver, status="فعال", assignee='کارتابل گروهی', support_group=["ممیزی", "تحلیل", "نظرسنجی"], taskName="AssignToPreviousSg")
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_4 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    if taskSendToAnalysis(driver) == False: return "STEP_AssignToPreviousSg_4 Failed: Request Step wrong!, Function: taskSendToAnalysis"    
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_4 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    if taskSendToFeedback(driver) == False: return "STEP_AssignToPreviousSg_4 Failed: Request Step wrong!, Function: taskSendToFeedback"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task AssignToPreviousSg button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_AssignToPreviousSg_4 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_should_exist_Tasks(driver, "taskAssignToPreviousSg") == False: return "Failed: Task AssignToPreviousSg button should exist but not found"
    if "Success" in result_B and "Success" in result_A: return "STEP_AssignToPreviousSg_4: Success Task AssignToPreviousSg Check Resolved (feedback) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

def STEP_taskCloseIncident_1(driver):
    if check_not_should_exist_Tasks(driver, "taskCloseIncident"): return "Failed: Task CloseIncident button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_taskCloseIncident_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_not_should_exist_Tasks(driver, "taskCloseIncident"): return "Failed: Task CloseIncident button not should exist but found"
    if taskPark(driver) == False: return "STEP_taskCloseIncident_1 Failed: Request Step wrong!, Function: taskPark"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task CloseIncident button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_taskCloseIncident_1 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    return "STEP_taskCloseIncident_1: Success Task CloseIncident button not should exist in Active status"

def STEP_taskCloseIncident_2(driver):
    if taskAssignToTechnicals(driver) == False: return "STEP_taskCloseIncident_2 Failed: Request Step wrong!, Function: taskAssignToTechnicals"
    if check_not_should_exist_Tasks(driver, "taskCloseIncident"): return "Failed: Task CloseIncident button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_taskCloseIncident_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_not_should_exist_Tasks(driver, "taskCloseIncident"): return "Failed: Task CloseIncident button not should exist but found"
    if taskPark(driver) == False: return "STEP_taskCloseIncident_2 Failed: Request Step wrong!, Function: taskPark"
    if check_not_should_exist_Tasks(driver, "taskAssignToPreviousSg"): return "Failed: Task CloseIncident button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_taskCloseIncident_2 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    return "STEP_taskCloseIncident_2: Success Task CloseIncident button not should exist in Active status"

def STEP_taskCloseIncident_3(driver):
    if taskSendToAnalysis(driver) == False: return "STEP_taskCloseIncident_3 Failed: Request Step wrong!, Function: taskSendToAnalysis"
    if check_not_should_exist_Tasks(driver, "taskCloseIncident"): return "Failed: Task CloseIncident button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_taskCloseIncident_3 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    if check_not_should_exist_Tasks(driver, "taskCloseIncident"): return "Failed: Task CloseIncident button not should exist but found"
    return "STEP_taskCloseIncident_3: Success Task CloseIncident button not should exist in Active status"

def STEP_taskCloseIncident_4(driver):
    if taskSendToFeedback(driver) == False: return "STEP_taskCloseIncident_4 Failed: Request Step wrong!, Function: taskSendToFeedback"
    if check_not_should_exist_Tasks(driver, "taskCloseIncident"): return "Failed: Task CloseIncident button not should exist but found"
    if taskAssignIncidentToMe(driver) == False: return "STEP_taskCloseIncident_4 Failed: Request Step wrong!, Function: taskAssignIncidentToMe"
    result_B = Check_Befor_After_Task_Status(driver, status="حل شده", assignee=username_otherformat, support_group="نظرسنجی", taskName="CloseIncident")
    if check_should_exist_Tasks(driver, "taskCloseIncident") == False: return "Failed: Task CloseIncident button should exist but not found"
    result_task = taskCloseIncident(driver)
    if result_task == False: return "STEP_taskCloseIncident_4 Failed: Request Step wrong!, Function: taskCloseIncident" 
    result_A = Check_Befor_After_Task_Status(driver, status="بسته شده", assignee=username_otherformat, support_group="نظرسنجی", taskName="CloseIncident")
    if "Success" in result_B and "Success" in result_A: return "STEP_taskCloseIncident_4: Success Task CloseIncident Check Resolved (feedback) status"
    else:
        if "Failed" in result_B: return result_B
        elif "Failed" in result_A: return result_A

driver = webdriver.Firefox()
driver.maximize_window()
Open_CSP(driver)
Login_To_CSP(driver, username, password)
Open_Ticket(driver, "14040712-00026")
print(STEP_AssignToPreviousSg_1(driver))
print(STEP_AssignToPreviousSg_2(driver))
