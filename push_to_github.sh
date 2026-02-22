#!/bin/bash
# Push to GitHub helper script

echo "==================================="
echo "Push to GitHub"
echo "==================================="
echo ""

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Check if there are commits
if ! git log -1 > /dev/null 2>&1; then
    echo "❌ Error: No commits found"
    exit 1
fi

# Show what will be pushed
echo "📊 Commit to push:"
git log --oneline -1
echo ""

echo "📁 Files in commit:"
git diff-tree --no-commit-id --name-only -r HEAD | wc -l
echo "files"
echo ""

echo "🎯 Pushing to:"
git remote get-url origin
echo ""

echo "==================================="
echo "⚠️  AUTHENTICATION REQUIRED"
echo "==================================="
echo ""
echo "You will be prompted for:"
echo "  Username: MuhammadAsgharramzan"
echo "  Password: [Your Personal Access Token]"
echo ""
echo "Don't have a token? Create one at:"
echo "https://github.com/settings/tokens"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."
echo ""

# Attempt to push
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "==================================="
    echo "✅ SUCCESS!"
    echo "==================================="
    echo ""
    echo "Your repository has been updated:"
    echo "https://github.com/MuhammadAsgharramzan/AI_Emplyee_Vault_Hackathon_0"
    echo ""
else
    echo ""
    echo "==================================="
    echo "❌ PUSH FAILED"
    echo "==================================="
    echo ""
    echo "Common issues:"
    echo "1. Authentication failed - Use Personal Access Token, not password"
    echo "2. Repository not found - Check the URL is correct"
    echo "3. Permission denied - Verify you own the repository"
    echo ""
    echo "See PUSH_TO_GITHUB.md for detailed instructions"
    exit 1
fi
