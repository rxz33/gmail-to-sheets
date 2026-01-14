# Gmail-to-Google Sheets Automation Using Python 3

**Name:** Rashi Gupta 

## Project Summary 
This project is a Python script that reads **unread emails from my Gmail Inbox** using the Gmail API, extracts key fields (From, Subject, Date, Content), appends them to a Google Sheet using the Sheets API, and then marks those emails as read.



---

## 1) High-level Architecture Diagram

+---------------------------+
| Gmail Inbox (unread only) |
+-------------+-------------+
              |
              | OAuth 2.0 (Gmail API)
              v
+----------------------------+
| Python Script (src/main.py)|
+----------------------------+
| 1) Fetch unread emails     |
| 2) Extract: From/Subject/  |
| Date/Body (plain text)     |
| 3) Check state.json to     | 
| prevent duplicates         |
| 4) Append rows to Sheet    |
| 5) Mark emails as read     |
+-------------+--------------+
              |
              | OAuth 2.0 (Google Sheets API)
              v
+---------------------------+
| Google Sheet (rows added) |
+---------------------------+



## 2) Step-by-step setup instructions 

### A. Google Cloud setup
1. Create a project in Google Cloud Console.
2. Enable APIs:
   - Gmail API
   - Google Sheets API
3. Configure OAuth consent screen:
   - Keep it in **Testing**
   - Add your Gmail account as a **Test User**
4. Create OAuth Client ID:
   - Type: **Desktop app**
5. Download JSON and save it as:
   - 'credentials/credentials.json

### B. Google Sheet setup
1. Create a Google Sheet.
2. Copy Spreadsheet ID from the URL. (between /d and /edit)
3. Update 'config.py':
   - 'SPREADSHEET_ID = "<your_spreadsheet_id>"'
   - 'SHEET_NAME = "Sheet1"' (must match your tab name) 

### C. Install and run (Windows Powershell)
1. Create/activate venv:
'''bash
python -m venv venv - create virtual environment for the project
venv\Scripts\Activate.ps1 - activate virtual environment

2. Install dependencies:
pip install -r requirements.txt

3. Run the script:
python -m src.main



## 3) Explanations

### A. OAuth flow used
I used **OAuth 2.0 Desktop (Installed App) flow**:
- The script reads `credentials/credentials.json`
- A browser opens for Google login + consent
- Google redirects back to localhost
- A token is generated and saved locally as `credentials/token.json`
- Next runs reuse the token so login is not needed every time

### B. Duplicate prevention logic
To avoid duplicate rows, the script stores processed Gmail **message IDs** in `credentials/state.json`.
- When the script runs, it checks each unread email ID
- If the ID already exists in the state file, it skips that email
- Only new unread emails are appended to the sheet

### C. State persistence method
State is persisted in:
- `credentials/state.json`

This file contains a list of processed message IDs. I used message IDs because they are unique for each email and are reliable for preventing duplicates across multiple runs.



## 4) Challenge Faced + Solution

**Challenge:** I got `Error 403: access_denied` because the OAuth app was in Testing mode and my Gmail was not added as a test user.

**Solution:** I added my Gmail account under OAuth consent screen → **Test users**, then re-ran the script and authentication worked successfully.



## 5) Limitations

- This script only processes **unread emails** (as required).
- Email body parsing prioritizes plain text; HTML-only emails may not extract perfectly.
- If `credentials/state.json` is deleted, older emails could be reprocessed unless additional sheet-side dedupe is added.

## Design choices (why I did it this way)
- I used OAuth Desktop flow because this project needs access to a real Gmail account and service accounts are not suitable for personal Gmail.
- I used `state.json` with message IDs because it is simple, reliable, and prevents duplicate rows on reruns.
- I mark emails as read only after the sheet append succeeds to avoid losing emails.
