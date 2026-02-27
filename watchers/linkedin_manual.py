"""Enhanced LinkedIn automation with anti-detection."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('LinkedInPoster')

def post_to_linkedin_manual_login():
    """Post to LinkedIn with manual login support."""

    vault_path = Path(__file__).parent.parent
    session_path = Path(__file__).parent / 'linkedin_session'
    posts_folder = vault_path / 'need_action' / 'linkedin_posts'

    # Find approved posts
    approved_posts = list(posts_folder.glob('LINKEDIN_POST_*.md'))
    approved_posts = [p for p in approved_posts if 'status: approved' in p.read_text()]

    if not approved_posts:
        logger.info("No approved posts found.")
        return

    post_file = approved_posts[0]
    logger.info(f"Found approved post: {post_file.name}")

    # Extract content
    content = post_file.read_text()
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

    logger.info("=" * 60)
    logger.info("POST CONTENT TO BE PUBLISHED:")
    logger.info("=" * 60)
    print(post_text)
    logger.info("=" * 60)

    print("\nOpening LinkedIn in browser...")
    print("INSTRUCTIONS:")
    print("1. Browser will open - log in to LinkedIn if needed")
    print("2. Once logged in, you'll see your feed")
    print("3. The script will try to post automatically")
    print("4. If it fails, you can post manually (content shown above)")
    print("\nStarting in 3 seconds...")
    time.sleep(3)

    with sync_playwright() as p:
        # Launch with anti-detection
        browser = p.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ],
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        # Navigate to LinkedIn
        logger.info("Loading LinkedIn...")
        page.goto('https://www.linkedin.com/feed/', timeout=60000)

        # Wait for user to log in if needed
        logger.info("Waiting for LinkedIn to load...")
        logger.info("If you see a login page, please log in now.")
        logger.info("You have 2 minutes...")

        try:
            # Wait for feed to load (indicates logged in)
            page.wait_for_selector('[aria-label*="Start a post"]', timeout=120000)
            logger.info("LinkedIn loaded successfully!")

            # Try to post
            logger.info("Attempting to post...")

            # Click start post button
            page.click('[aria-label*="Start a post"]')
            time.sleep(2)

            # Find and fill the text area
            page.fill('div[role="textbox"]', post_text)
            time.sleep(2)

            logger.info("Content filled! Review the post in the browser.")
            logger.info("Press Enter here when ready to publish, or Ctrl+C to cancel...")
            input()

            # Click Post button
            page.click('button:has-text("Post")')
            time.sleep(3)

            logger.info("Post published successfully!")

            # Move post to Done
            done_folder = vault_path / 'Done'
            done_folder.mkdir(exist_ok=True)
            post_file.rename(done_folder / post_file.name)
            logger.info(f"Moved post to Done folder")

        except Exception as e:
            logger.error(f"Error: {e}")
            logger.info("\nDon't worry! The browser is still open.")
            logger.info("You can post manually:")
            logger.info("1. Click 'Start a post' on LinkedIn")
            logger.info("2. Copy the content shown above")
            logger.info("3. Paste and post")
            logger.info("\nPress Enter when done...")
            input()

        logger.info("Closing browser...")
        browser.close()
        logger.info("Done!")

if __name__ == '__main__':
    post_to_linkedin_manual_login()
