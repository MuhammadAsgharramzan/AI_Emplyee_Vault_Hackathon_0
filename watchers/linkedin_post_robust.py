"""Robust LinkedIn automation with enhanced anti-detection."""
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

def human_delay(min_sec=1, max_sec=3):
    """Add human-like random delays."""
    time.sleep(random.uniform(min_sec, max_sec))

def post_to_linkedin():
    """Post to LinkedIn with robust error handling."""

    vault_path = Path(__file__).parent.parent
    session_path = Path(__file__).parent / 'linkedin_session'
    posts_folder = vault_path / 'need_action' / 'linkedin_posts'

    # Find approved post
    approved_posts = list(posts_folder.glob('LINKEDIN_POST_*.md'))
    if not approved_posts:
        print("❌ No posts found in need_action/linkedin_posts/")
        return False

    post_file = approved_posts[0]
    print(f"📄 Found post: {post_file.name}")

    # Extract content
    content = post_file.read_text(encoding='utf-8')
    lines = content.split('\n')
    post_content = []
    in_content = False

    for line in lines:
        if line.strip() == '## Post Content':
            in_content = True
            continue
        if in_content and line.strip().startswith('##'):
            break
        if in_content and line.strip():
            post_content.append(line)

    post_text = '\n'.join(post_content).strip()

    if not post_text:
        print("❌ No content found in post file")
        return False

    print("\n" + "="*60)
    print("📝 POST CONTENT:")
    print("="*60)
    print(post_text)
    print("="*60 + "\n")

    print("🌐 Opening LinkedIn...")
    print("⏳ This may take a moment...\n")

    with sync_playwright() as p:
        # Launch with anti-detection
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ],
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        # Remove automation indicators
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        try:
            # Navigate to LinkedIn
            print("🔗 Loading LinkedIn feed...")
            page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=30000)
            human_delay(2, 4)

            # Check if we're logged in
            current_url = page.url
            if 'login' in current_url or 'authwall' in current_url:
                print("\n⚠️  NOT LOGGED IN")
                print("📋 Please log in manually in the browser window")
                print("⏳ Waiting 60 seconds for you to log in...")
                time.sleep(60)

                # Check again
                current_url = page.url
                if 'login' in current_url or 'authwall' in current_url:
                    print("❌ Still not logged in. Please try again.")
                    browser.close()
                    return False

            print("✅ Logged in successfully!")
            human_delay(1, 2)

            # Try multiple selectors for "Start a post" button
            selectors = [
                'button:has-text("Start a post")',
                '[aria-label*="Start a post"]',
                '.share-box-feed-entry__trigger',
                'button.share-box-feed-entry__trigger',
                '[data-control-name="share_box_trigger"]'
            ]

            start_button = None
            for selector in selectors:
                try:
                    print(f"🔍 Looking for post button: {selector[:50]}...")
                    if page.locator(selector).count() > 0:
                        start_button = selector
                        print(f"✅ Found button with: {selector[:50]}")
                        break
                except:
                    continue

            if not start_button:
                print("\n⚠️  Could not find 'Start a post' button automatically")
                print("📋 MANUAL POSTING REQUIRED:")
                print("   1. Click 'Start a post' in the browser")
                print("   2. Paste the content shown above")
                print("   3. Click 'Post'")
                print("\n⏳ Press Enter here when you've posted...")
                input()

                # Move to Done
                done_folder = vault_path / 'Done'
                done_folder.mkdir(exist_ok=True)
                post_file.rename(done_folder / post_file.name)
                print("✅ Post marked as complete!")
                browser.close()
                return True

            # Click start post button
            print("🖱️  Clicking 'Start a post'...")
            page.click(start_button)
            human_delay(2, 3)

            # Try multiple selectors for text area
            text_selectors = [
                'div[role="textbox"]',
                '.ql-editor',
                '[contenteditable="true"]',
                'div[data-placeholder*="share"]'
            ]

            text_area = None
            for selector in text_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        text_area = selector
                        print(f"✅ Found text area: {selector[:50]}")
                        break
                except:
                    continue

            if not text_area:
                print("\n⚠️  Could not find text area automatically")
                print("📋 The post dialog should be open - paste content manually")
                print("⏳ Press Enter when you've posted...")
                input()

                done_folder = vault_path / 'Done'
                done_folder.mkdir(exist_ok=True)
                post_file.rename(done_folder / post_file.name)
                print("✅ Post marked as complete!")
                browser.close()
                return True

            # Fill in content
            print("⌨️  Typing post content...")
            page.click(text_area)
            human_delay(0.5, 1)

            # Type with human-like delays
            for char in post_text:
                page.keyboard.type(char)
                if random.random() < 0.1:  # 10% chance of pause
                    time.sleep(random.uniform(0.1, 0.3))

            human_delay(1, 2)
            print("✅ Content filled!")

            # Find and click Post button
            print("\n📋 REVIEW THE POST IN THE BROWSER")
            print("⏳ Press Enter to publish, or Ctrl+C to cancel...")
            input()

            post_button_selectors = [
                'button:has-text("Post")',
                '[aria-label*="Post"]',
                'button[type="submit"]'
            ]

            posted = False
            for selector in post_button_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        print(f"🖱️  Clicking Post button...")
                        page.click(selector)
                        human_delay(3, 5)
                        posted = True
                        break
                except:
                    continue

            if posted:
                print("\n🎉 POST PUBLISHED SUCCESSFULLY!")

                # Move to Done
                done_folder = vault_path / 'Done'
                done_folder.mkdir(exist_ok=True)
                post_file.rename(done_folder / post_file.name)
                print(f"✅ Moved {post_file.name} to Done folder")

                human_delay(2, 3)
                browser.close()
                return True
            else:
                print("\n⚠️  Could not find Post button")
                print("📋 Please click Post manually in the browser")
                print("⏳ Press Enter when done...")
                input()

                done_folder = vault_path / 'Done'
                done_folder.mkdir(exist_ok=True)
                post_file.rename(done_folder / post_file.name)
                print("✅ Post marked as complete!")
                browser.close()
                return True

        except PlaywrightTimeout as e:
            print(f"\n⏱️  Timeout: {e}")
            print("📋 Browser is still open - you can post manually")
            print("⏳ Press Enter when done...")
            input()
            browser.close()
            return False

        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("📋 Browser is still open - you can post manually")
            print("⏳ Press Enter when done...")
            try:
                input()
            except:
                pass
            browser.close()
            return False

if __name__ == '__main__':
    print("\n🤖 LinkedIn Automation - Robust Version")
    print("="*60)
    success = post_to_linkedin()
    if success:
        print("\n✅ All done!")
    else:
        print("\n⚠️  Completed with manual intervention")
