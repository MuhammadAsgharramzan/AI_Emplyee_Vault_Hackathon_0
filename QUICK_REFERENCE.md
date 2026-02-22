# AI Employee Quick Reference

## 🚀 Quick Commands

### Start/Stop System
```bash
./orchestrator.sh start    # Start all watchers
./orchestrator.sh stop     # Stop all watchers
./orchestrator.sh status   # Check what's running
```

### Agent Skills (Use with Claude Code)
```bash
claude /update-dashboard   # Update dashboard
claude /daily-briefing     # Generate daily report
claude /process-inbox      # Process pending tasks
claude /create-plan        # Create task plan
claude /linkedin-post      # Generate LinkedIn post
claude /review-approvals   # Review pending approvals
```

### Manual Watcher Start
```bash
cd watchers
uv run python filesystem_watcher.py    # File monitoring
uv run python gmail_watcher.py         # Email monitoring
uv run python whatsapp_watcher.py      # WhatsApp monitoring
uv run python linkedin_automation.py   # LinkedIn posting
```

### Email Operations
```bash
cd watchers
uv run python email_mcp_server.py send "to@email.com" "Subject" "Body"
uv run python email_mcp_server.py draft "to@email.com" "Subject" "Body"
```

---

## 📁 Folder Workflow

### Incoming Items
1. **inbox/** - Drop files here (auto-monitored)
2. **need_action/** - Tasks waiting for processing
3. **need_action/linkedin_posts/** - LinkedIn post queue

### Processing
4. **Plans/** - Multi-step task plans
5. **Pending_Approval/** - Items requiring human approval
6. **Approved/** - Approved actions (ready to execute)
7. **Rejected/** - Rejected actions (archived)

### Completed
8. **Done/** - Completed tasks
9. **Briefings/** - Daily/weekly briefings
10. **Logs/** - System logs and audit trail

---

## 🔧 Common Tasks

### Test the System
```bash
# 1. Start file watcher
cd watchers && uv run python filesystem_watcher.py

# 2. Drop test file (in another terminal)
cp test_file.md inbox/

# 3. Check results
ls -la need_action/
```

### Generate Daily Briefing
```bash
claude /daily-briefing
# Check: Briefings/YYYY-MM-DD_Daily_Briefing.md
```

### Process Pending Tasks
```bash
claude /process-inbox
# Reviews need_action/ folder and processes items
```

### Create LinkedIn Post
```bash
claude /linkedin-post
# Review: need_action/linkedin_posts/LINKEDIN_POST_*.md
# Approve: Change status to "approved"
# Post: cd watchers && uv run python linkedin_automation.py
```

---

## 🔐 Setup Checklist

### Bronze Tier (Ready Now)
- [x] Python 3.12+ installed
- [x] UV package manager installed
- [x] Claude Code CLI installed
- [x] Watchdog library installed
- [x] File system watcher working

### Silver Tier (Needs Setup)
- [ ] Google Cloud credentials (credentials.json)
- [ ] Gmail API enabled
- [ ] WhatsApp QR code scanned
- [ ] LinkedIn session logged in
- [ ] Playwright installed: `cd watchers && uv run playwright install chromium`
- [ ] Cron jobs installed (optional)

---

## 📊 Dashboard Quick View

Check system status:
```bash
cat Dashboard.md
# Or open in Obsidian for better formatting
```

Key metrics shown:
- Tasks completed
- Pending items
- System status
- Recent activity
- Alerts

---

## 🆘 Troubleshooting

### Watcher Not Starting
```bash
# Check if already running
./orchestrator.sh status

# Check logs
tail -f Logs/*.log

# Restart
./orchestrator.sh stop
./orchestrator.sh start
```

### Gmail Authentication Failed
```bash
# Delete old token and re-authenticate
rm watchers/token.pickle
cd watchers && uv run python gmail_watcher.py
```

### WhatsApp Session Expired
```bash
# Delete session and re-scan QR code
rm -rf watchers/whatsapp_session
cd watchers && uv run python whatsapp_watcher.py
```

### Claude Code Not Finding Skills
```bash
# Verify skills location
ls -la .claude/skills/

# Skills must be in .claude/skills/ folder
# Must have .md extension
```

---

## 📝 File Naming Conventions

- **EMAIL_*.md** - Email from Gmail watcher
- **WHATSAPP_*.md** - WhatsApp message
- **LINKEDIN_POST_*.md** - LinkedIn post draft
- **FILE_*.md** - Dropped file from inbox
- **PLAN_*.md** - Multi-step task plan
- **APPROVE_*.md** - Approval request
- **TEST_*.md** - Test task

---

## 🔄 Daily Workflow

### Morning (8:00 AM)
```bash
./orchestrator.sh daily-briefing
# Review: Briefings/YYYY-MM-DD_Daily_Briefing.md
```

### Throughout Day
```bash
# Process inbox every hour
./orchestrator.sh process-inbox

# Or let watchers run continuously
./orchestrator.sh start
```

### Evening (6:00 PM)
```bash
# Update dashboard
claude /update-dashboard

# Review approvals
claude /review-approvals

# Stop watchers
./orchestrator.sh stop
```

---

## 🎯 Company Handbook Rules

The AI Employee follows these rules (see Company_Handbook.md):

**Financial:**
- Payments > $500 require approval
- New payees always require approval

**Communication:**
- New contacts require approval for emails
- Bulk sends always require approval

**Security:**
- Never share credentials
- Log all actions
- Escalate security concerns

**Task Management:**
- Prioritize urgent/high priority
- Move completed to /Done
- Create plans for multi-step tasks

---

## 📞 Support

**Documentation:**
- README.md - Full setup guide
- FINAL_SUMMARY.md - Complete overview
- BRONZE_TIER_COMPLETE.md - Bronze details
- Company_Handbook.md - AI behavior rules

**Logs:**
- Check Logs/ folder for detailed logs
- Each watcher has its own log file

**Community:**
- Wednesday Research Meetings (10 PM)
- Zoom: https://us06web.zoom.us/j/87188707642

---

*Quick Reference v1.0 - 2026-02-22*
