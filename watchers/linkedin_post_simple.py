"""LinkedIn posting script - assumes already logged in."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

vault_path = Path(__file__).parent.parent
posts_queue = vault_path / 'need_action' / 'linkedin_posts'
session_path = vault_path / 'watchers' / 'linkedin_session'

print("LinkedIn Posting - Using saved session")

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

print("Opening browser with saved session...")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        headless=False
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    try:
        # Go to LinkedIn feed
        print("Navigating to LinkedIn...")
        page.goto('https://www.linkedin.com/feed/')
        page.wait_for_load_state('domcontentloaded')
        time.sleep(3)

        print("Clicking 'Start a post'...")
        page.click('[aria-label*="Start a post"]')
        time.sleep(2)

        print("Filling in post content...")
        page.fill('[aria-label*="share"]', post_text)
        time.sleep(2)

        print("Clicking 'Post' button...")
        page.click('button:has-text("Post")')
        time.sleep(5)

        print("SUCCESS! Post published!")

        # Move to Done
        done_path = vault_path / 'Done' / post_file.name
        post_file.rename(done_path)
        print(f"Moved to Done: {post_file.name}")

    except Exception as e:
        print(f"Error: {e}")
        print("Please check the browser window")

    time.sleep(3)
    browser.close()

print("Complete!")
