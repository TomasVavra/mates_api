from playwright.sync_api import sync_playwright

URL = "https://go.ismates.cz/mates-kk-ski-school/"
path = "login.txt"


def load_credentials(path):
    creds = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                creds[key] = value
    return creds


def save_calendar_html(username, password, filename="calendar.html"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)     # False to see browser window
        page = browser.new_page()

        # 1) Open login page
        page.goto(URL, wait_until="networkidle")

        # 2) Fill in login and password
        page.get_by_label("Login").fill(username)
        page.get_by_label("Heslo").fill(password)

        # 3) Press "Přihlásit se"
        page.get_by_role("button", name="Přihlásit se").click()
        page.wait_for_load_state("networkidle")

        # 4) Press "Plachta - náhled"
        page.get_by_role("button", name="Plachta - náhled").click()
        page.wait_for_load_state("networkidle")

        # 5) Wait for calendar to load
        page.wait_for_selector("div.display-sgantt", timeout=15000)

        # 6) Load HTML of calendar
        html = page.locator("div.display-sgantt").inner_html()

        # 7) Save to file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)

        browser.close()
        print(f"Calendar saved to {filename}")


if __name__ == "__main__":
    creds = load_credentials(path)

    username = creds.get("username")
    password = creds.get("password")

    print("Username:", username)
    print("Password:", password)

    save_calendar_html(username, password)