#!/bin/bash

# ============================================================
# Breakout Trading Bot - Test Runner Script
# ============================================================
# This script runs the test suite using UV
# ============================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${CYAN}============================================================${NC}"
    echo -e "${CYAN} $1${NC}"
    echo -e "${CYAN}============================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Main
clear
print_header "Breakout Trading Bot - Test Suite"

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    print_error "UV is not installed!"
    echo ""
    echo "Please install UV first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    exit 1
fi

print_success "UV found: $(uv --version)"
echo ""

# Sync dependencies
print_info "Syncing dependencies with UV..."
uv sync

if [ $? -eq 0 ]; then
    print_success "Dependencies synced"
    echo ""
else
    print_error "Failed to sync dependencies"
    exit 1
fi

# Test options
echo "Test Options:"
echo "  1) Run all tests (verbose)"
echo "  2) Run all tests (quiet)"
echo "  3) Run 4-hour timeframe tests only"
echo "  4) Run API server tests only"
echo "  5) Run bot logic tests only"
echo "  6) Run with coverage report"
echo "  7) Run specific test file"
echo ""

read -p "$(echo -e ${YELLOW}Select option [1-7]:${NC} )" -n 1 -r
echo ""
echo ""

case $REPLY in
    1)
        print_header "Running All Tests (Verbose)"
        uv run python -m pytest tests/ -v --tb=short
        ;;
    2)
        print_header "Running All Tests (Quiet)"
        uv run python -m pytest tests/ -q
        ;;
    3)
        print_header "Running 4-Hour Timeframe Tests"
        uv run python -m pytest tests/test_timeframes.py::TestTimeframeBotIntegration::test_bot_with_4hour_timeframe tests/test_breakout_bot.py::TestBreakoutBotEdgeCases::test_4hour_timeframe -v
        ;;
    4)
        print_header "Running API Server Tests"
        uv run python -m pytest tests/test_api_server.py -v
        ;;
    5)
        print_header "Running Bot Logic Tests"
        uv run python -m pytest tests/test_breakout_bot.py tests/test_breakout_logic.py -v
        ;;
    6)
        print_header "Running Tests with Coverage"
        uv run python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term
        echo ""
        print_success "Coverage report generated in htmlcov/index.html"
        ;;
    7)
        echo "Available test files:"
        ls tests/test_*.py
        echo ""
        read -p "$(echo -e ${YELLOW}Enter test file name:${NC} )" TEST_FILE
        print_header "Running ${TEST_FILE}"
        uv run python -m pytest tests/${TEST_FILE} -v
        ;;
    *)
        print_error "Invalid option!"
        exit 1
        ;;
esac

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    print_success "All tests passed!"
else
    echo ""
    print_error "Some tests failed!"
    exit 1
fi

echo ""

