"""Gmail watcher for monitoring email inbox."""
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pathlib import Path
from datetime import datetime
import pickle
import os.path
from base_watcher import BaseWatcher


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailWatcher(BaseWatcher):
    """Watcher for Gmail inbox monitoring."""

    def __init__(self, vault_path: str, credentials_path: str = 'credentials.json'):
        super().__init__(vault_path, check_interval=120)  # Check every 2 minutes
        self.credentials_path = credentials_path
        self.token_path = 'token.pickle'
        self.service = None
        self.processed_ids = set()

        # Initialize Gmail API
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API."""
        creds = None

        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    self.logger.error(f'Credentials file not found: {self.credentials_path}')
                    self.logger.error('Please download credentials.json from Google Cloud Console')
                    raise FileNotFoundError(f'Missing {self.credentials_path}')

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info('Gmail API authenticated successfully')

    def check_for_updates(self) -> list:
        """Check for new unread important emails."""
        try:
            # Query for unread important messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important',
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            # Filter out already processed messages
            new_messages = [
                m for m in messages
                if m['id'] not in self.processed_ids
            ]

            return new_messages

        except HttpError as error:
            self.logger.error(f'Gmail API error: {error}')
            return []

    def create_action_file(self, message) -> Path:
        """Create markdown file for email in need_action folder."""
        try:
            # Get full message details
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = {
                h['name']: h['value']
                for h in msg['payload']['headers']
            }

            sender = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', datetime.now().isoformat())

            # Get email body (simplified - handles plain text)
            body = self._get_email_body(msg)

            # Create markdown content
            content = f"""---
type: email
from: {sender}
subject: {subject}
received: {datetime.now().isoformat()}
gmail_id: {message['id']}
priority: high
status: pending
---

# Email: {subject}

## From
{sender}

## Received
{date}

## Content
{body[:1000]}{'...' if len(body) > 1000 else ''}

## Suggested Actions
- [ ] Read full email
- [ ] Draft reply
- [ ] Forward if needed
- [ ] Archive after processing

## Notes
Add any relevant notes or observations here.

---
*Email captured by Gmail Watcher*
"""

            # Save to need_action folder
            safe_subject = "".join(c for c in subject if c.isalnum() or c in (' ', '-', '_'))[:50]
            filepath = self.needs_action / f'EMAIL_{safe_subject}_{message["id"][:8]}.md'
            filepath.write_text(content, encoding='utf-8')

            # Mark as processed
            self.processed_ids.add(message['id'])

            return filepath

        except Exception as e:
            self.logger.error(f'Error processing email {message["id"]}: {e}')
            raise

    def _get_email_body(self, msg):
        """Extract email body from message."""
        try:
            if 'parts' in msg['payload']:
                # Multipart message
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            import base64
                            return base64.urlsafe_b64decode(data).decode('utf-8')
            else:
                # Simple message
                data = msg['payload']['body'].get('data', '')
                if data:
                    import base64
                    return base64.urlsafe_b64decode(data).decode('utf-8')
        except Exception as e:
            self.logger.error(f'Error extracting email body: {e}')

        return '[Email body could not be extracted]'


def main():
    """Main function to run Gmail watcher."""
    import sys

    # Setup logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('GmailWatcher')

    # Get vault path
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent

    vault_path = Path(vault_path).resolve()

    logger.info('Starting Gmail Watcher')
    logger.info(f'Vault path: {vault_path}')

    try:
        watcher = GmailWatcher(str(vault_path))
        watcher.run()
    except FileNotFoundError as e:
        logger.error(str(e))
        logger.error('Setup instructions:')
        logger.error('1. Go to https://console.cloud.google.com/')
        logger.error('2. Create a project and enable Gmail API')
        logger.error('3. Create OAuth 2.0 credentials')
        logger.error('4. Download credentials.json to this directory')
    except KeyboardInterrupt:
        logger.info('Gmail watcher stopped by user')


if __name__ == '__main__':
    main()
