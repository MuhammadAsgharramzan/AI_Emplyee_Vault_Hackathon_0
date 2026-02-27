# Silver Tier Setup Guide

**Status:** Ready for Configuration
**Date:** 2026-02-27
**Prerequisites:** Bronze Tier Complete ✅

---

## Overview

Silver Tier adds 4 powerful monitoring channels to your AI Employee:
1. **Gmail Monitoring** - Automatic email processing
2. **WhatsApp Monitoring** - Urgent message detection
3. **LinkedIn Automation** - Business promotion posts
4. **Scheduled Automation** - Cron jobs for recurring tasks

---

## 1. Gmail Monitoring Setup

### Step 1: Create Google Cloud Project (5 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select existing project
3. Name it: "AI Employee Vault" (or your choice)
4. Click "Create"

### Step 2: Enable Gmail API (2 minutes)

1. In your project, go to "APIs & Services" > "Library"
2. Search for "Gmail API"
3. Click "Gmail API" and click "Enable"

### Step 3: Create OAuth Credentials (5 minutes)

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: "AI Employee Vault"
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue" through all steps
4. Back to "Create OAuth client ID":
   - Application type: "Desktop app"
   - Name: "AI Employee Gmail Watcher"
   - Click "Create"
5. Click "Download JSON"
6. Rename downloaded file to `credentials.json`
7. Move it to: `watchers/credentials.json`

### Step 4: Test Gmail Watcher (3 minutes)

```bash
cd watchers
uv run python gmail_watcher.py ..
```

- Browser will open automatically
- Sign in with your Google account
- Click "Allow" to grant permissions
- Token will be saved for future use
- Press Ctrl+C to stop after successful authentication

### Step 5: Start Gmail Watcher

```bash
# Edit orchestrator.sh and uncomment Gmail watcher line
./orchestrator.sh start
```

**What it does:**
- Checks Gmail every 2 minutes
- Monitors for unread important emails
- Creates markdown files in need_action folder
- Tracks processed emails to avoid duplicates

---

## 2. WhatsApp Monitoring Setup

### Prerequisites
- WhatsApp account
- Phone with WhatsApp installed
- Playwright installed ✅

### Step 1: Test WhatsApp Watcher (5 minutes)

```bash
cd watchers
uv run python whatsapp_watcher.py ..
```

- Browser will open with WhatsApp Web
- Scan QR code with your phone:
  - Open WhatsApp on phone
  - Tap Menu (⋮) > Linked Devices
  - Tap "Link a Device"
  - Scan the QR code
- Session will be saved automatically
- Press Ctrl+C after successful login

### Step 2: Configure Keywords

Edit `watchers/whatsapp_watcher.py` to customize urgent keywords:
```python
URGENT_KEYWORDS = ['urgent', 'asap', 'invoice', 'payment', 'help', 'emergency']
```

### Step 3: Start WhatsApp Watcher

```bash
# Edit orchestrator.sh and uncomment WhatsApp watcher line
./orchestrator.sh start
```

**What it does:**
- Checks WhatsApp every 30 seconds
- Monitors for messages with urgent keywords
- Creates markdown files in need_action folder
- Maintains session across restarts

---

## 3. LinkedIn Automation Setup

### Prerequisites
- LinkedIn account
- Playwright installed ✅

### Step 1: Generate LinkedIn Post

```bash
claude /linkedin-post
```

- AI will create a professional post draft
- Saved to `need_action/linkedin_posts/`
- Review and edit as needed

### Step 2: Approve Post

1. Open the post file in `need_action/linkedin_posts/`
2. Review content
3. Change `status: draft` to `status: approved`
4. Save file

### Step 3: Test LinkedIn Automation (5 minutes)

```bash
cd watchers
uv run python linkedin_automation.py ..
```

- Browser will open LinkedIn
- Log in manually (first time only)
- Session will be saved
- Approved posts will be published
- Press Ctrl+C after successful login

### Step 4: Start LinkedIn Automation

```bash
# Edit orchestrator.sh and uncomment LinkedIn automation line
./orchestrator.sh start
```

**What it does:**
- Checks for approved posts every 5 minutes
- Publishes to LinkedIn automatically
- Moves published posts to Done folder
- Maintains login session

---

## 4. Scheduled Automation Setup

### Option A: Linux/Mac (Cron)

1. Open crontab editor:
```bash
crontab -e
```

2. Add these lines (adjust paths):
```bash
# Daily briefing at 8 AM
0 8 * * * cd /path/to/AI_Employee_Vault && ./orchestrator.sh daily-briefing

# Process inbox every hour during business hours (9 AM - 6 PM)
0 9-18 * * * cd /path/to/AI_Employee_Vault && ./orchestrator.sh process-inbox

# Update dashboard every 30 minutes
*/30 * * * * cd /path/to/AI_Employee_Vault && claude /update-dashboard

# Weekly business review (Monday 9 AM)
0 9 * * 1 cd /path/to/AI_Employee_Vault && claude /weekly-review
```

3. Save and exit

### Option B: Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "AI Employee Daily Briefing"
4. Trigger: Daily at 8:00 AM
5. Action: Start a program
   - Program: `bash.exe`
   - Arguments: `-c "cd /h/GIAIC/aI_Employee_Vault/AI_Employee_Vault && ./orchestrator.sh daily-briefing"`
6. Repeat for other tasks

---

## Verification Checklist

### Gmail Monitoring
- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth credentials downloaded
- [ ] credentials.json in watchers folder
- [ ] Successfully authenticated (token.pickle created)
- [ ] Test email detected and processed

### WhatsApp Monitoring
- [ ] Playwright installed
- [ ] Chromium browser installed
- [ ] QR code scanned successfully
- [ ] Session saved
- [ ] Test message detected

### LinkedIn Automation
- [ ] Playwright installed
- [ ] LinkedIn login successful
- [ ] Session saved
- [ ] Test post published

### Scheduled Automation
- [ ] Cron jobs installed (Linux/Mac) OR
- [ ] Task Scheduler configured (Windows)
- [ ] Test automation runs successfully

---

## Troubleshooting

### Gmail Issues
**Error: credentials.json not found**
- Download OAuth credentials from Google Cloud Console
- Rename to credentials.json
- Place in watchers/ folder

**Error: Authentication failed**
- Delete token.pickle
- Run gmail_watcher.py again
- Re-authenticate in browser

### WhatsApp Issues
**QR code not appearing**
- Check Playwright installation
- Run: `uv run python -m playwright install chromium`
- Try again

**Session expired**
- Delete whatsapp_session/ folder
- Run whatsapp_watcher.py again
- Scan QR code again

### LinkedIn Issues
**Login not working**
- Clear linkedin_session/ folder
- Run linkedin_automation.py again
- Log in manually

**Posts not publishing**
- Check post status is "approved"
- Verify LinkedIn session is valid
- Check logs for errors

---

## Next Steps

1. **Start with Gmail** - Most useful and easiest
2. **Add WhatsApp** - For urgent notifications
3. **Configure LinkedIn** - For business promotion
4. **Set up Cron** - For full automation

---

## Support

- Check logs in `Logs/` folder
- Run health check: `./health_check.sh`
- Review Dashboard: `cat Dashboard.md`

---

*Silver Tier Setup Guide*
*Last Updated: 2026-02-27*
