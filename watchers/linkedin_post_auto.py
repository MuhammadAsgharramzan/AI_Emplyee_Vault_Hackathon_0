"""LinkedIn automation - fills post and waits for manual publish."""
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

def human_delay(min_sec=1, max_sec=3):
    """Add human-like random delays."""
    time.sleep(random.uniform(min_sec, max_sec))

def post_to_linkedin():
    """Post to LinkedIn with auto-fill."""

    vault_path = Path(__file__).parent.parent
    session_path = Path(__file__).parent / 'linkedin_session'
    posts_folder = vault_path / 'need_action' / 'linkedin_posts'

    # Find approved post
    approved_posts = list(posts_folder.glob('LINKEDIN_POST_*.md'))
    if not approved_posts:
        print("No posts found")
        return False

    post_file = approved_posts[0]
    print(f"Found post: {post_file.name}")

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

    print("\nPOST CONTENT:")
    print("="*60)
    print(post_text)
    print("="*60)

    print("\nOpening LinkedIn...")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
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
            print("Loading LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded', timeout=30000)
            human_delay(2, 4)

            # Check login
            if 'login' in page.url or 'authwall' in page.url:
                print("\nNot logged in - waiting 60 seconds...")
                time.sleep(60)

            print("Looking for Start a post button...")

            # Try to find and click start post
            selectors = [
                'button:has-text("Start a post")',
                '[aria-label*="Start a post"]',
                '.share-box-feed-entry__trigger'
            ]

            clicked = False
            for selector in selectors:
                try:
                    if page.locator(selector).count() > 0:
                        print(f"Clicking: {selector[:40]}...")
                        page.click(selector)
                        clicked = True
                        break
                except:
                    continue

            if not clicked:
                print("\nCould not find Start a post button")
                print("Browser will stay open for 2 minutes - post manually")
                time.sleep(120)
                browser.close()
                return False

            human_delay(2, 3)

            # Find text area
            print("Looking for text area...")
            text_selectors = [
                'div[role="textbox"]',
                '.ql-editor',
                '[contenteditable="true"]'
            ]

            filled = False
            for selector in text_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        print(f"Filling content...")
                        page.click(selector)
                        human_delay(0.5, 1)

                        # Type content
                        for char in post_text:
                            page.keyboard.type(char)
                            if random.random() < 0.05:
                                time.sleep(random.uniform(0.05, 0.15))

                        filled = True
                        break
                except Exception as e:
                    print(f"Error with {selector}: {e}")
                    continue

            if filled:
                print("\nSUCCESS! Content filled in!")
                print("\n" + "="*60)
                print("BROWSER WILL STAY OPEN FOR 3 MINUTES")
                print("="*60)
                print("\nACTIONS:")
                print("1. Review the post in the browser")
                print("2. Click the blue 'Post' button to publish")
                print("3. Browser will auto-close in 3 minutes")
                print("\nWaiting...")

                # Wait 3 minutes
                time.sleep(180)

                print("\nClosing browser...")

                # Move to Done
                done_folder = vault_path / 'Done'
                done_folder.mkdir(exist_ok=True)
                post_file.rename(done_folder / post_file.name)
                print(f"Moved {post_file.name} to Done")

                browser.close()
                return True
            else:
                print("\nCould not fill content")
                print("Browser will stay open for 2 minutes - post manually")
                time.sleep(120)
                browser.close()
                return False

        except Exception as e:
            print(f"\nError: {e}")
            print("Browser will stay open for 2 minutes")
            time.sleep(120)
            browser.close()
            return False

if __name__ == '__main__':
    print("\nLinkedIn Auto-Post")
    print("="*60)
    post_to_linkedin()
    print("\nDone!")
