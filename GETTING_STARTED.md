# Getting Started with Your AI Employee

## ⚡ Quick Start (5 Minutes)

### Step 1: Push to GitHub (2 minutes)

```bash
./push_to_github.sh
```

When prompted:
- **Username:** MuhammadAsgharramzan
- **Password:** [Your GitHub Personal Access Token]

Don't have a token? Get one here: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Select scope: `repo`
- Copy the token

### Step 2: Start Your AI Employee (1 minute)

```bash
cd watchers
uv run python filesystem_watcher.py
```

This starts monitoring your inbox folder 24/7.

### Step 3: Test It (2 minutes)

Open a new terminal and run:

```bash
# Drop a test file
cp test_file.md inbox/

# Check it was processed
ls need_action/

# Use an Agent Skill
claude /update-dashboard

# View the results
cat Dashboard.md
```

**That's it! Your AI Employee is working!** 🎉

---

## 📚 What You Can Do Now

### Use Agent Skills

```bash
claude /update-dashboard    # Update status
claude /daily-briefing      # Generate daily report
claude /process-inbox       # Process pending tasks
claude /create-plan         # Create task plans
claude /linkedin-post       # Generate LinkedIn posts
claude /review-approvals    # Review approvals
```

### Monitor Files

Just drop any file in the `inbox/` folder and it will be:
1. Detected by the watcher
2. Metadata created automatically
3. Moved to `need_action/` for processing
4. Dashboard updated

### View Your Dashboard

```bash
cat Dashboard.md
# Or open in Obsidian for better viewing
```

---

## 🔧 Optional: Add Silver Tier Features

### Gmail Monitoring

1. Go to https://console.cloud.google.com/
2. Create project → Enable Gmail API
3. Create OAuth credentials → Download `credentials.json`
4. Place in `watchers/` folder
5. Run: `cd watchers && uv run python gmail_watcher.py`

### WhatsApp Monitoring

1. Run: `cd watchers && uv run python whatsapp_watcher.py`
2. Scan QR code with your phone
3. Session saved for future runs

### LinkedIn Automation

1. Generate post: `claude /linkedin-post`
2. Review in `need_action/linkedin_posts/`
3. Approve by changing status to "approved"
4. Run: `cd watchers && uv run python linkedin_automation.py`

---

## 📖 Documentation

- **START_HERE.md** - Overview and quick start
- **QUICK_REFERENCE.md** - Command reference
- **README.md** - Complete setup guide
- **COMPLETION_REPORT.md** - Full project details
- **Dashboard.md** - Real-time status

---

## 🆘 Troubleshooting

**Watcher not starting?**
```bash
cd watchers
uv sync  # Install dependencies
uv run python filesystem_watcher.py
```

**Claude Code not finding skills?**
```bash
ls .claude/skills/  # Should show 6 .md files
```

**Need help?**
- Check `QUICK_REFERENCE.md` for common commands
- Check `README.md` for detailed setup
- Join Wednesday meetings: https://us06web.zoom.us/j/87188707642

---

## ✅ What's Working Right Now

- ✅ File system monitoring
- ✅ 6 Agent Skills
- ✅ Task processing
- ✅ Dashboard updates
- ✅ Company Handbook rules
- ✅ Approval workflows

## ⏳ What Needs Setup (Optional)

- ⏳ Gmail monitoring (needs credentials)
- ⏳ WhatsApp monitoring (needs QR scan)
- ⏳ LinkedIn automation (needs login)

---

**Your AI Employee is ready to start working!** 🚀

Just push to GitHub and start the watcher!
