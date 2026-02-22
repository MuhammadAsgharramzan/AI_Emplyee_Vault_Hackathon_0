# AI Employee Vault - Bronze Tier

This is a Bronze Tier implementation of the Personal AI Employee system using Claude Code and Obsidian.

## Project Structure

```
AI_Employee_Vault/
├── .claude/
│   └── skills/              # Agent Skills for AI functionality
│       ├── update-dashboard.md
│       ├── daily-briefing.md
│       └── process-inbox.md
├── watchers/                # Python watcher scripts
│   ├── base_watcher.py
│   ├── filesystem_watcher.py
│   └── pyproject.toml
├── inbox/                   # Drop files here for processing
├── need_action/             # Tasks waiting to be processed
├── Done/                    # Completed tasks
├── Dashboard.md             # Central status dashboard
├── Company_Handbook.md      # Rules and guidelines
└── README.md               # This file
```

## Bronze Tier Features

✓ **Obsidian Vault**: Fully configured with Dashboard and Company Handbook
✓ **File System Watcher**: Monitors inbox folder for new files
✓ **Agent Skills**: 3 skills for AI Employee functionality
✓ **Folder Structure**: Organized workflow folders
✓ **Claude Code Integration**: Ready to read/write to vault

## Setup Instructions

### Prerequisites

- Python 3.12+ installed
- UV package manager installed
- Claude Code CLI installed
- Obsidian (optional, for GUI viewing)

### Installation

1. **Install Python dependencies:**
   ```bash
   cd watchers
   uv sync
   ```

2. **Verify Claude Code:**
   ```bash
   claude --version
   ```

3. **Open vault in Obsidian** (optional):
   - Open Obsidian
   - Open folder as vault: `AI_Employee_Vault`

## Usage

### Quick Start (Bronze Tier)

**Option 1: Using Orchestrator (Recommended)**
```bash
# Start all watchers
./orchestrator.sh start

# Check status
./orchestrator.sh status

# Stop all watchers
./orchestrator.sh stop

# Generate daily briefing
./orchestrator.sh daily-briefing

# Process inbox
./orchestrator.sh process-inbox
```

**Option 2: Manual Watcher Start**
```bash
cd watchers
uv run python filesystem_watcher.py
```

**Using Agent Skills**
```bash
# Update the dashboard
claude /update-dashboard

# Generate daily briefing
claude /daily-briefing

# Process pending tasks
claude /process-inbox

# Create a task plan
claude /create-plan

# Generate LinkedIn post
claude /linkedin-post

# Review approvals
claude /review-approvals
```

### Advanced Usage (Silver Tier)

#### Gmail Monitoring
1. Set up Google Cloud credentials (see setup instructions below)
2. Run: `cd watchers && uv run python gmail_watcher.py`
3. First run will authenticate via browser
4. Subsequent runs use saved token

#### WhatsApp Monitoring
1. Run: `cd watchers && uv run python whatsapp_watcher.py`
2. First run will open browser - scan QR code
3. Session saved for future runs
4. Monitors for urgent keywords

#### LinkedIn Posting
1. Create post: `claude /linkedin-post`
2. Review in `need_action/linkedin_posts/`
3. Approve by changing status to "approved"
4. Run: `cd watchers && uv run python linkedin_automation.py`

#### Email MCP Server
```bash
# Send email
cd watchers
uv run python email_mcp_server.py send "recipient@example.com" "Subject" "Body"

# Create draft
uv run python email_mcp_server.py draft "recipient@example.com" "Subject" "Body"
```

#### Scheduled Automation
```bash
# Linux/Mac: Install cron jobs
crontab -e
# Then add entries from cron_schedule.txt

# Windows: Use Task Scheduler
# Import tasks from cron_schedule.txt (convert to Task Scheduler format)
```

## Agent Skills

### 1. update-dashboard
Updates the central Dashboard.md with current statistics and recent activity.

### 2. daily-briefing
Generates a comprehensive daily briefing summarizing activities, pending items, and recommendations.

### 3. process-inbox
Processes all pending tasks in the need_action folder according to Company Handbook rules.

## Folder Workflow

1. **inbox/** - Drop new files here (monitored by watcher)
2. **need_action/** - Tasks waiting for processing
3. **Done/** - Completed tasks (archive)

## Company Handbook

The `Company_Handbook.md` defines rules for:
- Communication guidelines
- Financial approval thresholds
- Task management priorities
- Security protocols

The AI Employee follows these rules when processing tasks.

## Dashboard

The `Dashboard.md` provides real-time status:
- Quick stats (balance, messages, projects)
- Recent activity log
- System alerts
- Pending actions

## Next Steps (Silver Tier)

To upgrade to Silver Tier, add:
- Gmail watcher for email monitoring
- WhatsApp watcher for message monitoring
- MCP server for external actions
- Human-in-the-loop approval workflow
- Scheduled automation via cron

## Troubleshooting

**Watcher not starting:**
- Check Python version: `python3 --version`
- Reinstall dependencies: `cd watchers && uv sync`

**Claude Code not finding files:**
- Ensure you're in the vault directory
- Check file permissions

**Skills not working:**
- Verify skills are in `.claude/skills/` folder
- Check skill file format (must be .md)

## Security Notes

- Never commit credentials or API keys
- Keep sensitive data in `.env` files (add to .gitignore)
- Review all AI actions in the audit log
- Use approval workflows for sensitive operations

## License

This is a hackathon project for educational purposes.

---
**Status:** Bronze Tier Complete ✓
**Last Updated:** 2026-02-22
