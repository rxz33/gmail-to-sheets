import json, os
from config import SPREADSHEET_ID, SHEET_NAME, SUBJECT_KEYWORD, STATE_FILE
from src.gmail_service import get_gmail_service
from src.sheets_service import append_rows
from src.email_parser import parse_message

def load_state() -> set[str]:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("processed_message_ids", []))
    return set()

def save_state(processed_ids: set[str]) -> None:
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"processed_message_ids": sorted(processed_ids)}, f, indent=2)

def build_query() -> str:
    q = "is:unread in:inbox"
    if SUBJECT_KEYWORD:
        q += f' subject:"{SUBJECT_KEYWORD}"'
    return q

def main():
    gmail = get_gmail_service()
    processed_ids = load_state()

    q = build_query()
    resp = gmail.users().messages().list(userId="me", q=q, maxResults=50).execute()
    messages = resp.get("messages", [])

    rows_to_append = []
    ids_to_mark_read = []

    for m in messages:
        msg_id = m["id"]
        if msg_id in processed_ids:
            continue

        full = gmail.users().messages().get(userId="me", id=msg_id, format="full").execute()
        parsed = parse_message(full)

        rows_to_append.append([
            parsed["from"],
            parsed["subject"],
            parsed["date"],
            parsed["content"],
        ])
        ids_to_mark_read.append(msg_id)

    if rows_to_append:
        range_name = f"{SHEET_NAME}!A:D"
        append_rows(SPREADSHEET_ID, range_name, rows_to_append)

        for msg_id in ids_to_mark_read:
            gmail.users().messages().modify(
                userId="me",
                id=msg_id,
                body={"removeLabelIds": ["UNREAD"]},
            ).execute()
            processed_ids.add(msg_id)

        save_state(processed_ids)
        print(f"Appended {len(rows_to_append)} emails and marked them as read.")
    else:
        print("No new unread emails to process.")

if __name__ == "__main__":
    main()
