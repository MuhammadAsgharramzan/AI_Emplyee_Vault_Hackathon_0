"""Interactive LinkedIn posting script."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

vault_path = Path(__file__).parent.parent
posts_queue = vault_path / 'need_action' / 'linkedin_posts'
session_path = vault_path / 'watchers' / 'linkedin_session'

print("=" * 60)
print("LinkedIn Automation - Interactive Mode")
print("=" * 60)

# Find the post
post_files = list(posts_queue.glob('LINKEDIN_POST_*.md'))
if not post_files:
    print("No LinkedIn posts found in queue")
    exit(1)

post_file = post_files[0]
print(f"Found post: {post_file.name}")

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

print("Opening browser... Please log in to LinkedIn if prompted.")
print()

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        str(session_path),
        headless=False,
        viewport={'width': 1280, 'height': 720}
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    # Navigate to LinkedIn
    page.goto('https://www.linkedin.com/feed/', timeout=60000)

    # Wait for page to load
    time.sleep(5)

    # Check if logged in
    if 'login' in page.url or 'authwall' in page.url:
        print("Please log in to LinkedIn in the browser window.")
        print("Waiting 60 seconds for you to log in...")
        time.sleep(60)

        # Try to navigate to feed again
        page.goto('https://www.linkedin.com/feed/', timeout=60000)
        time.sleep(3)

    if 'login' in page.url or 'authwall' in page.url:
        print("Still not logged in. Exiting.")
        browser.close()
        exit(1)

    print("Logged in successfully!")
    print("Attempting to post...")

    try:
        # Click "Start a post" button
        page.click('[aria-label*="Start a post"]', timeout=10000)
        time.sleep(2)

        # Type content
        page.fill('[aria-label*="share"]', post_text, timeout=10000)
        time.sleep(2)

        print("Content filled. Waiting 5 seconds before posting...")
        time.sleep(5)

        # Click Post button
        page.click('button:has-text("Post")', timeout=10000)
        time.sleep(5)

        print("Post published successfully!")

        # Move to Done
        done_path = vault_path / 'Done' / post_file.name
        post_file.rename(done_path)
        print(f"Moved {post_file.name} to Done folder")

    except Exception as e:
        print(f"Error posting: {e}")
        print("You may need to post manually.")

    print("Session saved. Closing browser in 5 seconds...")
    time.sleep(5)
    browser.close()

print("Done!")
