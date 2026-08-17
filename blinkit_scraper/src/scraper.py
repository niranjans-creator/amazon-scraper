import json
from pathlib import Path

from .browser import create_browser


def scrape_product(url):

    playwright, browser, context, page = create_browser()

    network_responses = []

    def handle_response(response):

        request_url = response.url
        content_type = response.headers.get(
            "content-type",
            ""
        )

        if (
            "json" in content_type.lower()
            or "api" in request_url.lower()
        ):

            try:
                response_body = response.json()

                network_responses.append({
                    "url": request_url,
                    "status": response.status,
                    "content_type": content_type,
                    "data": response_body
                })

            except Exception:
                pass

    page.on(
        "response",
        handle_response
    )

    try:

        print("\nOpening Blinkit:")
        print(url)

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("\nPage loaded.")
        print(
            "Page title:",
            page.title()
        )

        print(
            "Current URL:",
            page.url
        )

        # Give Blinkit time to load API responses
        page.wait_for_timeout(7000)

        # ---------------------------------------------
        # SAVE HTML
        # ---------------------------------------------

        output_directory = Path("output")
        output_directory.mkdir(
            exist_ok=True
        )

        html = page.content()

        html_file = (
            output_directory /
            "page.html"
        )

        html_file.write_text(
            html,
            encoding="utf-8"
        )

        print(
            f"\nHTML saved to: {html_file}"
        )

        # ---------------------------------------------
        # SAVE NETWORK RESPONSES
        # ---------------------------------------------

        network_file = (
            output_directory /
            "network_data.json"
        )

        with open(
            network_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                network_responses,
                file,
                indent=2,
                ensure_ascii=False
            )

        print(
            f"Network data saved to: "
            f"{network_file}"
        )

        print(
            f"\nJSON/API responses captured: "
            f"{len(network_responses)}"
        )

        # Return data instead of page
        return {
            "html": html,
            "network": network_responses
        }

    except Exception as error:

        print(
            f"\nScraping error: {error}"
        )

        return None

    finally:

        browser.close()
        playwright.stop()