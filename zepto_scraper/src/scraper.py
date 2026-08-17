from playwright.sync_api import sync_playwright
import json


class ZeptoScraper:

    def __init__(self):
        self.playwright = None
        self.browser = None

    def start(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

    def close(self):
        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()

    def scrape(self, url):

        page = self.browser.new_page()

        api_responses = []

        def handle_response(response):
            try:
                if response.request.resource_type in ["xhr", "fetch"]:

                    content_type = response.headers.get("content-type", "")

                    if "json" in content_type:

                        try:
                            data = response.json()

                            api_responses.append({
                                "url": response.url,
                                "data": data
                            })

                        except:
                            pass

            except:
                pass

        page.on("response", handle_response)

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=120000
        )

        page.wait_for_timeout(15000)

        with open("api_dump.json", "w", encoding="utf-8") as f:
            json.dump(
                api_responses,
                f,
                indent=2,
                ensure_ascii=False
            )

        html = page.content()

        page.close()

        return html, api_responses