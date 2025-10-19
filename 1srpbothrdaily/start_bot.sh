#!/bin/bash

# ============================================================
# Breakout Trading Bot - Main Bot Startup Script
# ============================================================
# This script starts the main trading bot using UV
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

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Main startup
clear
print_header "Breakout Trading Bot - Main Bot"

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

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    echo ""
    echo "Please create .env file:"
    echo "  cp env.example .env"
    echo "  # Then edit .env with your API credentials"
    echo ""
    exit 1
fi

print_success ".env file found"

# Check if config.yaml exists
if [ ! -f "config.yaml" ]; then
    print_error "config.yaml not found!"
    echo ""
    echo "Please create config.yaml:"
    echo "  cp config.example.yaml config.yaml"
    echo "  # Then edit config.yaml with your settings"
    echo ""
    exit 1
fi

print_success "config.yaml found"
echo ""

# Display current configuration
print_info "Current Configuration:"
echo ""
TIMEFRAME=$(grep "timeframe:" config.yaml | awk '{print $2}' | tr -d '"')
SYMBOL=$(grep "symbol:" config.yaml | awk '{print $2}' | tr -d '"')
TIMEZONE=$(grep "timezone:" config.yaml | awk '{print $2}' | tr -d '"')

echo "  Trading Symbol: ${GREEN}${SYMBOL}${NC}"
echo "  Timeframe:      ${GREEN}${TIMEFRAME}${NC}"
echo "  Timezone:       ${GREEN}${TIMEZONE}${NC}"
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

# Optional: Run tests
read -p "$(echo -e ${YELLOW}Run tests before starting? [y/N]:${NC} )" -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Running tests..."
    uv run python -m pytest tests/ -v --tb=short
    
    if [ $? -eq 0 ]; then
        print_success "All tests passed!"
        echo ""
    else
        print_error "Tests failed!"
        read -p "$(echo -e ${YELLOW}Continue anyway? [y/N]:${NC} )" -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

# Start the bot
print_header "Starting Trading Bot"
print_info "Bot starting with ${GREEN}${TIMEFRAME}${NC} timeframe..."
print_warning "Press Ctrl+C to stop the bot"
echo ""
echo -e "${CYAN}============================================================${NC}"
echo ""

# Run the bot
uv run python run_bot.py

# Cleanup on exit
echo ""
print_info "Bot stopped"
echo ""

