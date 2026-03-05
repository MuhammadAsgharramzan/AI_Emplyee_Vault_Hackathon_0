"""LinkedIn posting with multiple selector strategies."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

vault_path = Path(__file__).parent.parent
posts_queue = vault_path / 'need_action' / 'linkedin_posts'
session_path = vault_path / 'watchers' / 'linkedin_session'

print("=" * 60)
print("LinkedIn Posting - Advanced Selector Strategy")
print("=" * 60)

# Find the post
post_files = list(posts_queue.glob('LINKEDIN_POST_*.md'))
if not post_files:
    print("No posts found")
    exit(1)

post_file = post_files[0]
print(f"Found: {post_file.name}")

# Read post content
content = post_file.read_text()
lines = content.split('\n')
post_content = []
in_content = False

for line in lines:
    if line.startswith('## Post Content'):
        in_content = True
        continue
    if in_content and line.startswith('##'):
        break
    if in_content and line.strip():
        post_content.append(line)

post_text = '\n'.join(post_content).strip()

print("Opening browser...")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        headless=False,
        viewport={'width': 1280, 'height': 900}
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    try:
        # Navigate to LinkedIn feed
        print("Navigating to LinkedIn feed...")
        page.goto('https://www.linkedin.com/feed/', wait_until='networkidle')
        time.sleep(5)

        # Take screenshot for debugging
        page.screenshot(path=str(vault_path / 'linkedin_debug.png'))
        print("Screenshot saved: linkedin_debug.png")

        # Try multiple selectors for "Start a post" button
        selectors = [
            'button:has-text("Start a post")',
            '[aria-label*="Start a post"]',
            '[aria-label*="start a post"]',
            '.share-box-feed-entry__trigger',
            'button.share-box-feed-entry__trigger',
            '[data-control-name="share_box_trigger"]',
            '.artdeco-button--secondary:has-text("Start")',
            'button:has-text("Start")',
            '.share-box__trigger',
        ]

        clicked = False
        for selector in selectors:
            try:
                print(f"Trying selector: {selector}")
                page.click(selector, timeout=3000)
                print(f"✓ Success with: {selector}")
                clicked = True
                break
            except Exception as e:
                print(f"  Failed: {str(e)[:50]}")
                continue

        if not clicked:
            print("\n❌ Could not find 'Start a post' button")
            print("Trying to click anywhere in the share box area...")

            # Try clicking the share box area directly
            try:
                page.click('.share-box-feed-entry', timeout=3000)
                clicked = True
                print("✓ Clicked share box area")
            except:
                pass

        if not clicked:
            print("\n❌ All selector strategies failed")
            print("Please post manually using the content provided")
            browser.close()
            exit(1)

        time.sleep(3)

        # Try multiple selectors for the text input
        print("\nFilling in post content...")
        text_selectors = [
            '[aria-label*="share"]',
            '[aria-label*="Share"]',
            '.ql-editor',
            '[contenteditable="true"]',
            '[role="textbox"]',
            '.share-creation-state__text-editor',
        ]

        filled = False
        for selector in text_selectors:
            try:
                print(f"Trying text selector: {selector}")
                page.fill(selector, post_text, timeout=3000)
                print(f"✓ Success with: {selector}")
                filled = True
                break
            except Exception as e:
                print(f"  Failed: {str(e)[:50]}")
                continue

        if not filled:
            print("\n❌ Could not fill text content")
            print("Please paste the content manually")
            time.sleep(30)  # Give user time to paste manually
        else:
            time.sleep(2)

        # Try to click Post button
        print("\nClicking 'Post' button...")
        post_button_selectors = [
            'button:has-text("Post")',
            '[aria-label*="Post"]',
            '.share-actions__primary-action',
            'button.share-actions__primary-action',
            '[data-control-name="share.post"]',
        ]

        posted = False
        for selector in post_button_selectors:
            try:
                print(f"Trying post button: {selector}")
                page.click(selector, timeout=3000)
                print(f"✓ Success with: {selector}")
                posted = True
                break
            except Exception as e:
                print(f"  Failed: {str(e)[:50]}")
                continue

        if posted:
            print("\n✅ SUCCESS! Post published!")
            time.sleep(5)

            # Move to Done
            done_path = vault_path / 'Done' / post_file.name
            post_file.rename(done_path)
            print(f"Moved to Done: {post_file.name}")
        else:
            print("\n⚠️  Could not click Post button")
            print("Please click 'Post' manually in the browser")
            time.sleep(30)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please complete posting manually")

    print("\nClosing browser in 5 seconds...")
    time.sleep(5)
    browser.close()

print("\nComplete!")
