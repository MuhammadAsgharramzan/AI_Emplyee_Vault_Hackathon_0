"""Base watcher class for all monitoring scripts."""
import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime


class BaseWatcher(ABC):
    """Abstract base class for all watcher implementations."""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'need_action'
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Ensure needs_action folder exists
        self.needs_action.mkdir(exist_ok=True)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process."""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in need_action folder."""
        pass

    def run(self):
        """Main loop - continuously check for updates."""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Monitoring vault at: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')

        while True:
            try:
                items = self.check_for_updates()
                if items:
                    self.logger.info(f'Found {len(items)} new items')
                    for item in items:
                        filepath = self.create_action_file(item)
                        self.logger.info(f'Created action file: {filepath.name}')
            except KeyboardInterrupt:
                self.logger.info('Watcher stopped by user')
                break
            except Exception as e:
                self.logger.error(f'Error: {e}', exc_info=True)

            time.sleep(self.check_interval)
