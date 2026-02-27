"""LinkedIn automation runner."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from linkedin_automation import LinkedInPoster

def main():
    vault_path = Path(__file__).parent.parent
    poster = LinkedInPoster(str(vault_path))

    print("LinkedIn Automation Starting...")
    print("=" * 50)
    print()

    # Process approved posts
    result = poster.process_post_queue(dry_run=False)

    if result:
        print()
        print("✅ LinkedIn posting complete!")
    else:
        print()
        print("❌ LinkedIn posting failed. Check logs for details.")

if __name__ == '__main__':
    main()
