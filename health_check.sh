#!/bin/bash
# Health check script for AI Employee system

echo "==================================="
echo "AI Employee Health Check"
echo "==================================="
echo ""

VAULT_PATH="$(cd "$(dirname "$0")" && pwd)"
ERRORS=0
WARNINGS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check function
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
        ((ERRORS++))
    fi
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# 1. Check Python
echo "Checking Prerequisites..."
python3 --version > /dev/null 2>&1
check "Python 3 installed"

# 2. Check UV
uv --version > /dev/null 2>&1
check "UV package manager installed"

# 3. Check Claude Code
claude --version > /dev/null 2>&1
check "Claude Code CLI installed"

echo ""
echo "Checking Vault Structure..."

# 4. Check folders
for folder in inbox need_action Done Briefings Logs Plans Pending_Approval Approved Rejected; do
    if [ -d "$folder" ]; then
        echo -e "${GREEN}✓${NC} Folder: $folder"
    else
        echo -e "${RED}✗${NC} Folder missing: $folder"
        ((ERRORS++))
    fi
done

echo ""
echo "Checking Core Files..."

# 5. Check core files
for file in Dashboard.md Company_Handbook.md README.md; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} File: $file"
    else
        echo -e "${RED}✗${NC} File missing: $file"
        ((ERRORS++))
    fi
done

echo ""
echo "Checking Agent Skills..."

# 6. Check skills
SKILL_COUNT=$(ls -1 .claude/skills/*.md 2>/dev/null | wc -l)
if [ $SKILL_COUNT -ge 4 ]; then
    echo -e "${GREEN}✓${NC} Agent Skills: $SKILL_COUNT found"
else
    echo -e "${RED}✗${NC} Agent Skills: Only $SKILL_COUNT found (expected 6)"
    ((ERRORS++))
fi

echo ""
echo "Checking Watchers..."

# 7. Check watcher scripts
cd watchers 2>/dev/null
if [ $? -eq 0 ]; then
    for script in base_watcher.py filesystem_watcher.py gmail_watcher.py whatsapp_watcher.py linkedin_automation.py email_mcp_server.py; do
        if [ -f "$script" ]; then
            echo -e "${GREEN}✓${NC} Watcher: $script"
        else
            echo -e "${RED}✗${NC} Watcher missing: $script"
            ((ERRORS++))
        fi
    done
    cd ..
else
    echo -e "${RED}✗${NC} Watchers folder not found"
    ((ERRORS++))
fi

echo ""
echo "Checking Dependencies..."

# 8. Check Python dependencies
cd watchers 2>/dev/null
if [ -f "pyproject.toml" ]; then
    echo -e "${GREEN}✓${NC} pyproject.toml found"

    # Check if venv exists
    if [ -d ".venv" ]; then
        echo -e "${GREEN}✓${NC} Virtual environment exists"
    else
        warn "Virtual environment not found (run: cd watchers && uv sync)"
    fi
else
    echo -e "${RED}✗${NC} pyproject.toml not found"
    ((ERRORS++))
fi
cd ..

echo ""
echo "Checking Optional Components..."

# 9. Check optional credentials
if [ -f "watchers/credentials.json" ]; then
    echo -e "${GREEN}✓${NC} Gmail credentials configured"
else
    warn "Gmail credentials not found (optional for Silver Tier)"
fi

if [ -f "watchers/token.pickle" ]; then
    echo -e "${GREEN}✓${NC} Gmail authenticated"
else
    warn "Gmail not authenticated (optional for Silver Tier)"
fi

if [ -d "watchers/whatsapp_session" ]; then
    echo -e "${GREEN}✓${NC} WhatsApp session exists"
else
    warn "WhatsApp not configured (optional for Silver Tier)"
fi

echo ""
echo "Checking Running Processes..."

# 10. Check if watchers are running
if pgrep -f "filesystem_watcher.py" > /dev/null; then
    echo -e "${GREEN}✓${NC} Filesystem watcher is running"
else
    warn "Filesystem watcher not running (start with: ./orchestrator.sh start)"
fi

if pgrep -f "gmail_watcher.py" > /dev/null; then
    echo -e "${GREEN}✓${NC} Gmail watcher is running"
else
    echo -e "  Gmail watcher not running (optional)"
fi

echo ""
echo "==================================="
echo "Health Check Summary"
echo "==================================="

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo "System is healthy and ready to use."
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ $WARNINGS warnings found${NC}"
    echo "System is functional but some optional features need setup."
    exit 0
else
    echo -e "${RED}✗ $ERRORS errors found${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ $WARNINGS warnings found${NC}"
    fi
    echo "Please fix errors before using the system."
    exit 1
fi
