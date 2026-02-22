"""WhatsApp watcher for monitoring messages via WhatsApp Web."""
from playwright.sync_api import sync_playwright
from pathlib import Path
from datetime import datetime
import time
from base_watcher import BaseWatcher


class WhatsAppWatcher(BaseWatcher):
    """Watcher for WhatsApp Web messages."""

    def __init__(self, vault_path: str, session_path: str = 'whatsapp_session'):
        super().__init__(vault_path, check_interval=30)  # Check every 30 seconds
        self.session_path = Path(session_path)
        self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'important']
        self.processed_chats = set()

    def check_for_updates(self) -> list:
        """Check for new WhatsApp messages with urgent keywords."""
        messages = []

        try:
            with sync_playwright() as p:
                # Launch browser with persistent session
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False  # Set to True for production
                )

                page = browser.pages[0] if browser.pages else browser.new_page()
                page.goto('https://web.whatsapp.com', timeout=60000)

                # Wait for WhatsApp to load
                try:
                    page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                except:
                    self.logger.error('WhatsApp not loaded. Please scan QR code manually.')
                    browser.close()
                    return []

                # Find unread chats
                unread_chats = page.query_selector_all('[aria-label*="unread"]')

                for chat in unread_chats[:5]:  # Limit to 5 most recent
                    try:
                        # Get chat name and preview text
                        chat_text = chat.inner_text().lower()

                        # Check if any keyword is present
                        if any(keyword in chat_text for keyword in self.keywords):
                            # Click to open chat
                            chat.click()
                            time.sleep(1)

                            # Get chat name
                            chat_name_elem = page.query_selector('[data-testid="conversation-info-header"]')
                            chat_name = chat_name_elem.inner_text() if chat_name_elem else 'Unknown'

                            # Get recent messages
                            message_elems = page.query_selector_all('[data-testid="msg-container"]')
                            recent_messages = []

                            for msg_elem in message_elems[-5:]:  # Last 5 messages
                                msg_text = msg_elem.inner_text()
                                recent_messages.append(msg_text)

                            # Create message object
                            chat_id = f"{chat_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

                            if chat_id not in self.processed_chats:
                                messages.append({
                                    'chat_name': chat_name,
                                    'chat_id': chat_id,
                                    'messages': recent_messages,
                                    'timestamp': datetime.now().isoformat()
                                })
                                self.processed_chats.add(chat_id)

                    except Exception as e:
                        self.logger.error(f'Error processing chat: {e}')
                        continue

                browser.close()

        except Exception as e:
            self.logger.error(f'Error checking WhatsApp: {e}')

        return messages

    def create_action_file(self, message_data) -> Path:
        """Create markdown file for WhatsApp message in need_action folder."""
        chat_name = message_data['chat_name']
        chat_id = message_data['chat_id']
        messages = message_data['messages']
        timestamp = message_data['timestamp']

        # Create safe filename
        safe_name = "".join(c for c in chat_name if c.isalnum() or c in (' ', '-', '_'))[:30]

        content = f"""---
type: whatsapp_message
from: {chat_name}
received: {timestamp}
chat_id: {chat_id}
priority: high
status: pending
---

# WhatsApp Message: {chat_name}

## From
{chat_name}

## Received
{timestamp}

## Recent Messages
"""

        for i, msg in enumerate(messages, 1):
            content += f"\n### Message {i}\n{msg}\n"

        content += """

## Suggested Actions
- [ ] Read full conversation
- [ ] Draft reply
- [ ] Take requested action
- [ ] Mark as resolved

## Notes
Add any relevant notes or observations here.

---
*Message captured by WhatsApp Watcher*
"""

        filepath = self.needs_action / f'WHATSAPP_{safe_name}_{chat_id[:8]}.md'
        filepath.write_text(content)

        return filepath


def main():
    """Main function to run WhatsApp watcher."""
    import sys
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('WhatsAppWatcher')

    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent

    vault_path = Path(vault_path).resolve()

    logger.info('Starting WhatsApp Watcher')
    logger.info(f'Vault path: {vault_path}')
    logger.info('First run will require QR code scan')

    try:
        watcher = WhatsAppWatcher(str(vault_path))
        watcher.run()
    except KeyboardInterrupt:
        logger.info('WhatsApp watcher stopped by user')


if __name__ == '__main__':
    main()
