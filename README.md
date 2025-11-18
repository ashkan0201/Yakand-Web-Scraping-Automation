# Yakand Web Automation System

> A modern, fully automated workflow system for managing Yakand tickets and processes efficiently.

---

## 🚀 Overview

This project is designed to automate repetitive and time-consuming tasks within the Yakand service platform.  
From ticket creation, incident assignment, and schedule changes to sending feedback and uploading attachments, every workflow step is handled automatically.  

By centralizing all scripts into modular, reusable components, the system reduces manual errors, speeds up processes, and provides a full audit trail through structured logs.

---

## 🛠️ Key Features

- **End-to-End Automation:** Scripts cover ticket creation, assignment, analysis, feedback, and more.  
- **Modular Architecture:** Each task lives in its own folder for maintainability and easy debugging.  
- **Reusable Core Functions:** `Functions/Mother_func.py` contains shared logic for browser interactions and logging.  
- **Comprehensive Logging:** Every action is logged in JSON files (`logs/`) with success/failure tracking.  
- **Offline Capable:** Runs fully on your local environment without any server dependencies.  
- **Configurable:** User info and environment settings stored in `Real_info/`.  
- **Scalable:** Easy to add new automation tasks without touching existing modules.

---

## 📁 Project Structure (Conceptual)

- **Automation Task Folders:** Each folder contains the main Python script for that specific automation action.  
- **Functions:** Core reusable functions for browser automation, element handling, and logging.  
- **Logs:** Structured logs organized by task, capturing detailed execution results.  
- **Real_info:** User-specific and environment configuration files.  
- **Other Modules:** Each module operates independently but shares core functions for consistent behavior.

> This modular design ensures each script is testable individually, while the overall system remains cohesive and easy to maintain.

---

## 📌 Getting Started

1. **Install Dependencies**  
   ```
   pip install -r requirements.txt
   ```

2. **Configure Environment**  
   Add user credentials and environment info inside `Real_info/`.

3. **Run Automation Tasks**  
   Example:
   ```
   python .\Assign_To_Technicals\Assign_To_Technicals.py
   ```

4. **Check Logs**  
   JSON logs will be automatically generated in the corresponding task folder under `/logs/`.

---

## 🔧 Technologies Used

- Python 3.11  
- Selenium WebDriver (GeckoDriver)  
- JSON Logging System  
- Modular Python Packages  

---

## 📄 License

This project is licensed under the **MIT License**. See `LICENSE` for details.
