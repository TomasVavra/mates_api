import requests
import json

URL = "https://go.ismates.cz/mates-kk-ski-school/UIDL/?v-uiId=1"

COOKIES = {
    "JSESSIONID": "node119pfopatky0b31p3wh1tar4c8l.node1"
}

HEADERS = {
    "Content-Type": "application/json"
}

# 🔥 Payload kliknutí na šipku – uložený jako konstanta
PAYLOAD_CLICK_NEXT_DAY = {
	"csrfToken": "6fd70fc5-c4ac-47e4-acf6-d8ebde3b441e",
	"rpc": [
		[
			"406",
			"com.vaadin.shared.ui.button.ButtonServerRpc",
			"click",
			[
				{
					"altKey": False,
					"button": "LEFT",
					"clientX": 724,
					"clientY": 37,
					"ctrlKey": False,
					"metaKey": False,
					"relativeX": 19,
					"relativeY": 16,
					"shiftKey": False,
					"type": 1
				}
			]
		]
	],
	"syncId": 93
}

def strip_uidl_prefix(text):
    if text.startswith("for(;;);"):
        return text[len("for(;;);"):]
    return text

def get_sync_id():
    r = requests.post(URL, headers=HEADERS, cookies=COOKIES, json={"rpc": [], "syncId": 0})
    raw = strip_uidl_prefix(r.text)
    data = json.loads(raw)
    return data[0]["syncId"]

def fetch_calendar_html(sync_id):
    payload = PAYLOAD_CLICK_NEXT_DAY.copy()
    payload["syncId"] = sync_id

    r = requests.post(URL, headers=HEADERS, cookies=COOKIES, json=payload)
    raw = strip_uidl_prefix(r.text)
    data = json.loads(raw)

    state = data[0].get("state", {})
    html_parts = []

    for key, value in state.items():
        if isinstance(value, dict) and "text" in value:
            html_parts.append(value["text"])

    return "\n".join(html_parts)

def save_calendar(html, filename="calendar.html"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Kalendář uložen do {filename}")

if __name__ == "__main__":
    sync_id = get_sync_id()
    html = fetch_calendar_html(sync_id)
    save_calendar(html)


