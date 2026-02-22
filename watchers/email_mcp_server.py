"""Email MCP Server for sending emails via Gmail API."""
import json
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pickle
import os.path


class EmailMCPServer:
    """MCP Server for email operations."""

    def __init__(self, credentials_path: str = 'credentials.json'):
        self.credentials_path = credentials_path
        self.token_path = 'token.pickle'
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API."""
        creds = None

        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            raise Exception('Gmail credentials not found. Run gmail_watcher.py first to authenticate.')

        self.service = build('gmail', 'v1', credentials=creds)

    def send_email(self, to: str, subject: str, body: str, cc: str = None, bcc: str = None) -> dict:
        """Send an email via Gmail API."""
        try:
            message = MIMEMultipart()
            message['to'] = to
            message['subject'] = subject

            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc

            msg_body = MIMEText(body, 'plain')
            message.attach(msg_body)

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            send_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()

            return {
                'status': 'success',
                'message_id': send_message['id'],
                'to': to,
                'subject': subject
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def draft_email(self, to: str, subject: str, body: str) -> dict:
        """Create a draft email (doesn't send)."""
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            draft = self.service.users().drafts().create(
                userId='me',
                body={'message': {'raw': raw_message}}
            ).execute()

            return {
                'status': 'success',
                'draft_id': draft['id'],
                'to': to,
                'subject': subject
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def handle_request(self, request: dict) -> dict:
        """Handle MCP request."""
        action = request.get('action')
        params = request.get('params', {})

        if action == 'send_email':
            return self.send_email(
                to=params.get('to'),
                subject=params.get('subject'),
                body=params.get('body'),
                cc=params.get('cc'),
                bcc=params.get('bcc')
            )

        elif action == 'draft_email':
            return self.draft_email(
                to=params.get('to'),
                subject=params.get('subject'),
                body=params.get('body')
            )

        else:
            return {
                'status': 'error',
                'error': f'Unknown action: {action}'
            }


def main():
    """Run MCP server in CLI mode for testing."""
    import sys

    if len(sys.argv) < 2:
        print('Usage: python email_mcp_server.py <action> [params...]')
        print('Actions:')
        print('  send <to> <subject> <body>')
        print('  draft <to> <subject> <body>')
        sys.exit(1)

    server = EmailMCPServer()
    action = sys.argv[1]

    if action == 'send' and len(sys.argv) >= 5:
        result = server.send_email(
            to=sys.argv[2],
            subject=sys.argv[3],
            body=sys.argv[4]
        )
        print(json.dumps(result, indent=2))

    elif action == 'draft' and len(sys.argv) >= 5:
        result = server.draft_email(
            to=sys.argv[2],
            subject=sys.argv[3],
            body=sys.argv[4]
        )
        print(json.dumps(result, indent=2))

    else:
        print('Invalid action or missing parameters')
        sys.exit(1)


if __name__ == '__main__':
    main()
