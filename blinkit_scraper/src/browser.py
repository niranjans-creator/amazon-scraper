from playwright.sync_api import sync_playwright


def create_browser():

    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=False
    )

    context = browser.new_context(
        viewport={
            "width": 1366,
            "height": 768
        }
    )

    page = context.new_page()

    return playwright, browser, context, page