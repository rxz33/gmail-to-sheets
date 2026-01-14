import base64
from email.utils import parsedate_to_datetime

def _decode_base64(data: str) -> str:
    return base64.urlsafe_b64decode(data.encode("utf-8")).decode("utf-8", errors="replace")

def extract_plain_text(payload: dict) -> str:
    if "parts" in payload:
        for part in payload["parts"]:
            mime = part.get("mimeType", "")
            body = part.get("body", {})
            if mime == "text/plain" and body.get("data"):
                return _decode_base64(body["data"])
    
        for part in payload["parts"]:
            if part.get("parts"):
                txt = extract_plain_text(part)
                if txt:
                    return txt
        return ""
    else:
        body = payload.get("body", {})
        if payload.get("mimeType") == "text/plain" and body.get("data"):
            return _decode_base64(body["data"])
        return ""

def parse_message(message: dict) -> dict:
    headers = {h["name"]: h["value"] for h in message["payload"].get("headers", [])}
    sender = headers.get("From", "")
    subject = headers.get("Subject", "")
    date_str = headers.get("Date", "")

    try:
        dt = parsedate_to_datetime(date_str)
        date_iso = dt.isoformat()
    except Exception:
        date_iso = date_str

    content = extract_plain_text(message["payload"]) or ""

    return {
        "from": sender,
        "subject": subject,
        "date": date_iso,
        "content": content.strip(),
    }
