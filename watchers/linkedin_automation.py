"""LinkedIn automation for posting business updates."""
from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import datetime
import json
import time
from base_watcher import BaseWatcher


class LinkedInPoster:
    """LinkedIn automation for posting business updates."""

    def __init__(self, vault_path: str, session_path: str = 'linkedin_session'):
        self.vault_path = Path(vault_path)
        self.session_path = Path(session_path)
        self.posts_queue = self.vault_path / 'need_action' / 'linkedin_posts'
        self.posts_queue.mkdir(exist_ok=True)

        import logging
        self.logger = logging.getLogger(self.__class__.__name__)

    def post_to_linkedin(self, content: str, dry_run: bool = True):
        """Post content to LinkedIn."""
        if dry_run:
            self.logger.info(f'[DRY RUN] Would post to LinkedIn: {content[:100]}...')
            return True

        try:
            with sync_playwright() as p:
                # Launch browser with persistent session
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False  # Set to True for production
                )
                page = browser.pages[0] if browser.pages else browser.new_page()

                # Navigate to LinkedIn
                page.goto('https://www.linkedin.com/feed/')
                page.wait_for_load_state('networkidle')

                # Check if logged in
                if 'login' in page.url:
                    self.logger.error('Not logged in to LinkedIn. Please log in manually first.')
                    browser.close()
                    return False

                # Click "Start a post" button
                page.click('[aria-label*="Start a post"]')
                time.sleep(1)

                # Type content
                page.fill('[aria-label*="share"]', content)
                time.sleep(1)

                # Click Post button
                page.click('button:has-text("Post")')
                time.sleep(2)

                self.logger.info('Successfully posted to LinkedIn')
                browser.close()
                return True

        except Exception as e:
            self.logger.error(f'Error posting to LinkedIn: {e}')
            return False

    def process_post_queue(self, dry_run: bool = True):
        """Process queued LinkedIn posts."""
        post_files = list(self.posts_queue.glob('LINKEDIN_POST_*.md'))

        for post_file in post_files:
            try:
                content = post_file.read_text()

                # Extract content from markdown
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

                if post_text:
                    success = self.post_to_linkedin(post_text, dry_run=dry_run)

                    if success:
                        # Move to Done folder
                        done_path = self.vault_path / 'Done' / post_file.name
                        post_file.rename(done_path)
                        self.logger.info(f'Processed and moved: {post_file.name}')

            except Exception as e:
                self.logger.error(f'Error processing {post_file.name}: {e}')


class LinkedInWatcher(BaseWatcher):
    """Watcher for LinkedIn post scheduling."""

    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=300)  # Check every 5 minutes
        self.posts_queue = self.needs_action / 'linkedin_posts'
        self.posts_queue.mkdir(exist_ok=True)
        self.poster = LinkedInPoster(vault_path)

    def check_for_updates(self) -> list:
        """Check for scheduled LinkedIn posts."""
        post_files = list(self.posts_queue.glob('LINKEDIN_POST_*.md'))

        # Filter for posts that are ready to publish
        ready_posts = []
        for post_file in post_files:
            try:
                content = post_file.read_text()
                if 'status: ready' in content or 'status: approved' in content:
                    ready_posts.append(post_file)
            except Exception as e:
                self.logger.error(f'Error reading {post_file.name}: {e}')

        return ready_posts

    def create_action_file(self, post_file: Path) -> Path:
        """Process approved LinkedIn post."""
        # This is called when a post is ready
        # The actual posting is handled by LinkedInPoster
        self.logger.info(f'Processing LinkedIn post: {post_file.name}')

        # For now, just log - actual posting requires approval
        approval_file = self.vault_path / 'Pending_Approval' / f'APPROVE_{post_file.name}'

        content = f"""---
type: linkedin_post_approval
original_file: {post_file.name}
created: {datetime.now().isoformat()}
status: pending_approval
---

# LinkedIn Post Approval Required

A LinkedIn post is ready to be published.

## Original File
{post_file.name}

## Action Required
Review the post content in: {post_file}

## To Approve
Move this file to /Approved folder

## To Reject
Move this file to /Rejected folder

---
*Approval request created by LinkedIn Watcher*
"""

        approval_file.write_text(content)
        return approval_file


def main():
    """Main function for LinkedIn automation."""
    import sys
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('LinkedInAutomation')

    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent

    vault_path = Path(vault_path).resolve()

    logger.info('Starting LinkedIn Watcher')
    logger.info(f'Vault path: {vault_path}')

    try:
        watcher = LinkedInWatcher(str(vault_path))
        watcher.run()
    except KeyboardInterrupt:
        logger.info('LinkedIn watcher stopped by user')


if __name__ == '__main__':
    main()
