import time
import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://go.ismates.cz/mates-kk-ski-school/"
path = "login.txt"
date = "1/16/26"
instructor = "Zahradníček"
# instructor = "None"

# telegram bot
TOKEN = "8408797930:AAFiNFVQZAjbE7pbloXzjb63uvai3sCRynA"
CHAT_ID = "8388403019"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

def save_html(raw_html, output_file="calendar.html"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(raw_html)

    print("Saved HTML to", output_file)

def save_pretty_html(raw_html, output_file="calendar_pretty.html"):
    soup = BeautifulSoup(raw_html, "html.parser")
    pretty = soup.prettify()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pretty)

    print("Saved pretty HTML to", output_file)

def save_text_only(raw_html, output_file="calendar.txt"):
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)

    message = f"{date}\n\n{text}"
    send_message(message)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(message)

    print("Saved clean text to", output_file)

def load_credentials(path):
    creds = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                creds[key] = value
    return creds

def login(username, password, page):
    # Open login page
    page.goto(URL, wait_until="networkidle")

    # Fill in login and password
    page.get_by_label("Login").fill(username)
    page.get_by_label("Heslo").fill(password)

    # Press "Přihlásit se"
    page.get_by_role("button", name="Přihlásit se").click()
    page.wait_for_load_state("networkidle")

def load_calendar(page):
    # Press "Plachta - náhled"
    page.get_by_role("button", name="Plachta - náhled").click()
    page.wait_for_load_state("networkidle")

    # Wait for calendar to load
    page.wait_for_selector("div.display-sgantt", timeout=15000)

def extract_calendar(username, password, filename="calendar.html"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)     # False to see browser window
        page = browser.new_page()

        login(username, password, page)

        load_calendar(page)

        # Fill in date
        page.fill("input.v-datefield-textfield", date)
        page.keyboard.press("Enter")

        # Fill in name filter, "None" = no filter
        if (instructor != "None"):
            page.fill("input.v-textfield-tiny", instructor)
            page.keyboard.press("Enter")

        time.sleep(3)

        # Load HTML of calendar
        html = page.locator("div.display-sgantt").inner_html()

        # Save to files
        save_html(html)
        save_pretty_html(html)
        save_text_only(html)

        browser.close()


if __name__ == "__main__":
    creds = load_credentials(path)
    username = creds.get("username")
    password = creds.get("password")

    # send_message("Hello from matesobot!")
    extract_calendar(username, password)
