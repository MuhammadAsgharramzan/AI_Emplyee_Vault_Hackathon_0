"""Test WhatsApp Web loading manually."""
from playwright.sync_api import sync_playwright
import time

print("Opening WhatsApp Web in browser...")
print("This will stay open so you can see what's happening.")
print("Press Ctrl+C when done.\n")

with sync_playwright() as p:
    # Launch browser with session
    browser = p.chromium.launch_persistent_context(
        'whatsapp_session',
        headless=False,
        args=['--disable-blink-features=AutomationControlled']
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    print("Loading WhatsApp Web...")
    page.goto('https://web.whatsapp.com')

    print("\n✅ Browser opened!")
    print("What do you see in the browser window?")
    print("1. QR code?")
    print("2. Chat list (already logged in)?")
    print("3. Loading screen?")
    print("4. Error message?")
    print("\nWaiting... (Press Ctrl+C to stop)")

    try:
        time.sleep(300)  # Wait 5 minutes
    except KeyboardInterrupt:
        print("\nStopping...")

    browser.close()
    print("Browser closed.")
