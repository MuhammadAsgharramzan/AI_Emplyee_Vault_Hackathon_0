#!/bin/bash
# Orchestrator script to run all watchers and scheduled tasks

VAULT_PATH="$(cd "$(dirname "$0")" && pwd)"
WATCHERS_PATH="$VAULT_PATH/watchers"

echo "==================================="
echo "AI Employee Orchestrator"
echo "==================================="
echo ""
echo "Vault: $VAULT_PATH"
echo ""

# Function to check if a process is running
is_running() {
    pgrep -f "$1" > /dev/null
}

# Function to start a watcher
start_watcher() {
    local name=$1
    local script=$2

    if is_running "$script"; then
        echo "✓ $name is already running"
    else
        echo "Starting $name..."
        cd "$WATCHERS_PATH"
        uv run python "$script" "$VAULT_PATH" > "$VAULT_PATH/Logs/${name}.log" 2>&1 &
        echo "✓ $name started (PID: $!)"
    fi
}

# Function to stop all watchers
stop_all() {
    echo ""
    echo "Stopping all watchers..."
    pkill -f "filesystem_watcher.py"
    pkill -f "gmail_watcher.py"
    pkill -f "whatsapp_watcher.py"
    pkill -f "linkedin_automation.py"
    echo "✓ All watchers stopped"
}

# Handle command line arguments
case "$1" in
    start)
        echo "Starting all watchers..."
        echo ""
        start_watcher "Filesystem Watcher" "filesystem_watcher.py"
        # Uncomment when credentials are set up:
        # start_watcher "Gmail Watcher" "gmail_watcher.py"
        # start_watcher "WhatsApp Watcher" "whatsapp_watcher.py"
        # start_watcher "LinkedIn Automation" "linkedin_automation.py"
        echo ""
        echo "✓ Orchestrator started"
        echo "Logs are in: $VAULT_PATH/Logs/"
        ;;

    stop)
        stop_all
        ;;

    status)
        echo "Checking watcher status..."
        echo ""

        if is_running "filesystem_watcher.py"; then
            echo "✓ Filesystem Watcher: Running"
        else
            echo "✗ Filesystem Watcher: Stopped"
        fi

        if is_running "gmail_watcher.py"; then
            echo "✓ Gmail Watcher: Running"
        else
            echo "✗ Gmail Watcher: Stopped"
        fi

        if is_running "whatsapp_watcher.py"; then
            echo "✓ WhatsApp Watcher: Running"
        else
            echo "✗ WhatsApp Watcher: Stopped"
        fi

        if is_running "linkedin_automation.py"; then
            echo "✓ LinkedIn Automation: Running"
        else
            echo "✗ LinkedIn Automation: Stopped"
        fi
        ;;

    daily-briefing)
        echo "Generating daily briefing..."
        cd "$VAULT_PATH"
        claude /daily-briefing
        ;;

    process-inbox)
        echo "Processing inbox..."
        cd "$VAULT_PATH"
        claude /process-inbox
        ;;

    *)
        echo "Usage: $0 {start|stop|status|daily-briefing|process-inbox}"
        echo ""
        echo "Commands:"
        echo "  start           - Start all watchers"
        echo "  stop            - Stop all watchers"
        echo "  status          - Check watcher status"
        echo "  daily-briefing  - Generate daily briefing"
        echo "  process-inbox   - Process pending tasks"
        exit 1
        ;;
esac
