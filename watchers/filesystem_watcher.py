"""File system watcher for monitoring inbox folder."""
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import time


class DropFolderHandler(FileSystemEventHandler):
    """Handler for file system events in the inbox folder."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'inbox'
        self.needs_action = self.vault_path / 'need_action'
        self.logger = logging.getLogger(self.__class__.__name__)

        # Ensure folders exist
        self.inbox.mkdir(exist_ok=True)
        self.needs_action.mkdir(exist_ok=True)

        # Track processed files to avoid duplicates
        self.processed_files = set()

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Avoid processing the same file multiple times
        if source.name in self.processed_files:
            return

        # Wait a moment to ensure file is fully written
        time.sleep(0.5)

        try:
            # Copy file to needs_action folder
            dest = self.needs_action / f'FILE_{source.name}'
            shutil.copy2(source, dest)

            # Create metadata file
            self.create_metadata(source, dest)

            # Mark as processed
            self.processed_files.add(source.name)

            self.logger.info(f'Processed new file: {source.name}')

        except Exception as e:
            self.logger.error(f'Error processing {source.name}: {e}')

    def create_metadata(self, source: Path, dest: Path):
        """Create a markdown metadata file for the dropped file."""
        meta_path = self.needs_action / f'{dest.stem}_metadata.md'

        # Get file stats
        stats = source.stat()
        size_kb = stats.st_size / 1024

        content = f"""---
type: file_drop
original_name: {source.name}
size: {size_kb:.2f} KB
created: {datetime.now().isoformat()}
status: pending
priority: normal
---

# New File Dropped for Processing

## File Details
- **Original Name:** {source.name}
- **Size:** {size_kb:.2f} KB
- **Location:** {dest}
- **Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions
- [ ] Review file contents
- [ ] Determine appropriate action
- [ ] Process or forward as needed
- [ ] Move to /Done when complete

## Notes
Add any relevant notes or observations here.
"""

        meta_path.write_text(content)


def main():
    """Main function to run the file system watcher."""
    import sys

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('FilesystemWatcher')

    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = Path(__file__).parent.parent

    vault_path = Path(vault_path).resolve()
    inbox_path = vault_path / 'inbox'

    logger.info(f'Starting File System Watcher')
    logger.info(f'Vault path: {vault_path}')
    logger.info(f'Monitoring: {inbox_path}')

    # Create event handler and observer
    event_handler = DropFolderHandler(str(vault_path))
    observer = Observer()
    observer.schedule(event_handler, str(inbox_path), recursive=False)

    # Start monitoring
    observer.start()
    logger.info('Watcher is running. Press Ctrl+C to stop.')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('Stopping watcher...')
        observer.stop()

    observer.join()
    logger.info('Watcher stopped.')


if __name__ == '__main__':
    main()
