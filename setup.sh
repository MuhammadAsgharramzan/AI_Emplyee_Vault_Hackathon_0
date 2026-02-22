#!/bin/bash
# Quick start script for AI Employee Bronze Tier

echo "==================================="
echo "AI Employee - Bronze Tier Setup"
echo "==================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 installed: $(python3 --version)"
else
    echo "✗ Python 3 not found. Please install Python 3.12+"
    exit 1
fi

# Check UV
if command -v uv &> /dev/null; then
    echo "✓ UV installed: $(uv --version)"
else
    echo "✗ UV not found. Please install UV package manager"
    exit 1
fi

# Check Claude Code
if command -v claude &> /dev/null; then
    echo "✓ Claude Code installed: $(claude --version)"
else
    echo "✗ Claude Code not found. Please install Claude Code CLI"
    exit 1
fi

echo ""
echo "Installing Python dependencies..."
cd watchers
uv sync

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Start the file watcher:"
echo "   cd watchers && uv run python filesystem_watcher.py"
echo ""
echo "2. Test by dropping a file in the inbox/ folder"
echo ""
echo "3. Use Agent Skills with Claude Code:"
echo "   claude /update-dashboard"
echo "   claude /process-inbox"
echo "   claude /daily-briefing"
echo ""
echo "4. View Dashboard.md in Obsidian or any markdown viewer"
echo ""
