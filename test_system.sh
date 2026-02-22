#!/bin/bash
# Test script to verify AI Employee functionality

echo "==================================="
echo "AI Employee System Test"
echo "==================================="
echo ""

VAULT_PATH="$(cd "$(dirname "$0")" && pwd)"
TEST_PASSED=0
TEST_FAILED=0

# Test 1: Check if Dashboard exists and is readable
echo "Test 1: Dashboard accessibility"
if [ -f "Dashboard.md" ] && [ -r "Dashboard.md" ]; then
    echo "✓ PASS: Dashboard.md exists and is readable"
    ((TEST_PASSED++))
else
    echo "✗ FAIL: Dashboard.md not accessible"
    ((TEST_FAILED++))
fi

# Test 2: Check if Company Handbook exists
echo "Test 2: Company Handbook accessibility"
if [ -f "Company_Handbook.md" ] && [ -r "Company_Handbook.md" ]; then
    echo "✓ PASS: Company_Handbook.md exists and is readable"
    ((TEST_PASSED++))
else
    echo "✗ FAIL: Company_Handbook.md not accessible"
    ((TEST_FAILED++))
fi

# Test 3: Check folder structure
echo "Test 3: Folder structure"
REQUIRED_FOLDERS="inbox need_action Done"
ALL_FOLDERS_EXIST=true
for folder in $REQUIRED_FOLDERS; do
    if [ ! -d "$folder" ]; then
        ALL_FOLDERS_EXIST=false
        break
    fi
done

if $ALL_FOLDERS_EXIST; then
    echo "✓ PASS: All required folders exist"
    ((TEST_PASSED++))
else
    echo "✗ FAIL: Some required folders are missing"
    ((TEST_FAILED++))
fi

# Test 4: Check Agent Skills
echo "Test 4: Agent Skills"
SKILL_COUNT=$(ls -1 .claude/skills/*.md 2>/dev/null | wc -l)
if [ $SKILL_COUNT -ge 4 ]; then
    echo "✓ PASS: Found $SKILL_COUNT Agent Skills"
    ((TEST_PASSED++))
else
    echo "✗ FAIL: Only $SKILL_COUNT Agent Skills found (expected at least 4)"
    ((TEST_FAILED++))
fi

# Test 5: Check watcher scripts
echo "Test 5: Watcher scripts"
if [ -f "watchers/filesystem_watcher.py" ]; then
    echo "✓ PASS: Filesystem watcher exists"
    ((TEST_PASSED++))
else
    echo "✗ FAIL: Filesystem watcher not found"
    ((TEST_FAILED++))
fi

# Test 6: Check if Python dependencies are installed
echo "Test 6: Python dependencies"
cd watchers 2>/dev/null
if [ -d ".venv" ]; then
    echo "✓ PASS: Virtual environment exists"
    ((TEST_PASSED++))
else
    echo "⚠ WARNING: Virtual environment not found (run: cd watchers && uv sync)"
    ((TEST_FAILED++))
fi
cd ..

# Test 7: Create a test file and check if it can be processed
echo "Test 7: File processing simulation"
TEST_FILE="inbox/TEST_$(date +%s).txt"
echo "This is a test file" > "$TEST_FILE"
if [ -f "$TEST_FILE" ]; then
    echo "✓ PASS: Can create files in inbox"
    rm "$TEST_FILE"
    ((TEST_PASSED++))
else
    echo "✗ FAIL: Cannot create files in inbox"
    ((TEST_FAILED++))
fi

# Test 8: Check if Claude Code is available
echo "Test 8: Claude Code availability"
if command -v claude &> /dev/null; then
    echo "✓ PASS: Claude Code CLI is installed"
    ((TEST_PASSED++))
else
    echo "✗ FAIL: Claude Code CLI not found"
    ((TEST_FAILED++))
fi

echo ""
echo "==================================="
echo "Test Results"
echo "==================================="
echo "Passed: $TEST_PASSED"
echo "Failed: $TEST_FAILED"
echo ""

if [ $TEST_FAILED -eq 0 ]; then
    echo "✓ All tests passed! System is ready to use."
    echo ""
    echo "Next steps:"
    echo "1. Start watchers: ./orchestrator.sh start"
    echo "2. Drop a file in inbox/ to test"
    echo "3. Use Agent Skills: claude /update-dashboard"
    exit 0
else
    echo "✗ Some tests failed. Please review the errors above."
    exit 1
fi
