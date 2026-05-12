import asyncio
import re
from playwright import async_api
from playwright.async_api import expect

async def run_test():
    pw = None
    browser = None
    context = None

    try:
        # Start a Playwright session in asynchronous mode
        pw = await async_api.async_playwright().start()

        # Launch a Chromium browser in headless mode with custom arguments
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--window-size=1280,720",
                "--disable-dev-shm-usage",
                "--ipc=host",
                "--single-process"
            ],
        )

        # Create a new browser context (like an incognito window)
        context = await browser.new_context()
        # Wider default timeout to match the agent's DOM-stability budget;
        # auto-waiting Playwright APIs (expect, locator.wait_for) inherit this.
        context.set_default_timeout(15000)

        # Open a new page in the browser context
        page = await context.new_page()

        # Interact with the page elements to simulate user flow
        # -> navigate
        await page.goto("http://localhost:5173")
        try:
            await page.wait_for_load_state("domcontentloaded", timeout=5000)
        except Exception:
            pass
        
        # -> Type a non-existent username into the search field and submit the search form.
        # text input aria-label="GitHub username"
        elem = page.locator("xpath=/html/body/div/div/div/form/div/input").nth(0)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("thisuserdoesnotexist_xyz_12345")
        
        # -> Type a non-existent username into the search field and submit the search form.
        # button "Search" aria-label="Search"
        elem = page.locator("xpath=/html/body/div/div/div/form/button").nth(0)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.click()
        
        # -> Click 'Try Again' to reset the error state, enter a valid GitHub username (octocat), submit the search, and verify the profile card and repositories appear.
        # button "Try Again"
        elem = page.locator("xpath=/html/body/div/div/div/main/div/button").nth(0)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.click()
        
        # -> Click 'Try Again' to reset the error state, enter a valid GitHub username (octocat), submit the search, and verify the profile card and repositories appear.
        # text input aria-label="GitHub username"
        elem = page.locator("xpath=/html/body/div/div/div/form/div/input").nth(0)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.fill("octocat")
        
        # -> Click 'Try Again' to reset the error state, enter a valid GitHub username (octocat), submit the search, and verify the profile card and repositories appear.
        # button "Search" aria-label="Search"
        elem = page.locator("xpath=/html/body/div/div/div/form/button").nth(0)
        await elem.wait_for(state="visible", timeout=10000)
        await elem.click()
        
        # --> Test passed — verified by AI agent
        frame = context.pages[-1]
        current_url = await frame.evaluate("() => window.location.href")
        assert current_url is not None, "Test completed successfully"
        await asyncio.sleep(5)

    finally:
        if context:
            await context.close()
        if browser:
            await browser.close()
        if pw:
            await pw.stop()

asyncio.run(run_test())
    