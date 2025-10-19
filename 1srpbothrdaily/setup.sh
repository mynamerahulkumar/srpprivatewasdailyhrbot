#!/bin/bash

# ============================================================
# Breakout Trading Bot - Setup Script
# ============================================================
# This script sets up the bot for first-time use with UV
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

# Main setup
clear
print_header "Breakout Trading Bot - Setup"

# Step 1: Check UV installation
print_info "Step 1/5: Checking UV installation..."
echo ""

if ! command -v uv &> /dev/null; then
    print_error "UV is not installed!"
    echo ""
    print_info "Installing UV..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    if [ $? -eq 0 ]; then
        print_success "UV installed successfully"
        print_warning "Please restart your terminal and run this script again"
        exit 0
    else
        print_error "Failed to install UV"
        exit 1
    fi
else
    print_success "UV found: $(uv --version)"
fi

echo ""

# Step 2: Sync dependencies
print_info "Step 2/5: Syncing dependencies..."
echo ""

uv sync

if [ $? -eq 0 ]; then
    print_success "Dependencies synced successfully"
else
    print_error "Failed to sync dependencies"
    exit 1
fi

echo ""

# Step 3: Create configuration files
print_info "Step 3/5: Setting up configuration files..."
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    print_info "Creating .env file..."
    cp env.example .env
    print_success ".env file created"
    print_warning "Please edit .env and add your Delta Exchange API credentials"
else
    print_success ".env file already exists"
fi

# Create config.yaml if it doesn't exist
if [ ! -f "config.yaml" ]; then
    print_info "Creating config.yaml file..."
    cp config.example.yaml config.yaml
    print_success "config.yaml file created (configured for 4h timeframe)"
else
    print_success "config.yaml file already exists"
    CURRENT_TF=$(grep "timeframe:" config.yaml | awk '{print $2}' | tr -d '"')
    print_info "Current timeframe: ${GREEN}${CURRENT_TF}${NC}"
fi

echo ""

# Step 4: Make scripts executable
print_info "Step 4/5: Making startup scripts executable..."
echo ""

chmod +x start_bot.sh
chmod +x start_api.sh
chmod +x start_tests.sh
chmod +x setup.sh

print_success "All scripts are now executable"
echo ""

# Step 5: Run tests
print_info "Step 5/5: Running tests..."
echo ""

read -p "$(echo -e ${YELLOW}Run tests now? [Y/n]:${NC} )" -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    uv run python -m pytest tests/ -v --tb=short
    
    if [ $? -eq 0 ]; then
        echo ""
        print_success "All tests passed!"
    else
        echo ""
        print_error "Some tests failed!"
        print_warning "Please fix the issues before running the bot"
    fi
else
    print_info "Skipping tests"
fi

echo ""

# Setup complete
print_header "Setup Complete!"

echo "Next steps:"
echo ""
echo "  1. Edit .env file with your API credentials:"
echo -e "     ${CYAN}nano .env${NC}"
echo ""
echo "  2. (Optional) Edit config.yaml for your trading preferences:"
echo -e "     ${CYAN}nano config.yaml${NC}"
echo ""
echo "  3. Start the trading bot:"
echo -e "     ${GREEN}./start_bot.sh${NC}"
echo ""
echo "  Or start the API server:"
echo -e "     ${GREEN}./start_api.sh${NC}"
echo ""
echo "  Run tests:"
echo -e "     ${GREEN}./start_tests.sh${NC}"
echo ""

print_info "Documentation:"
echo "  - Main docs: ${BLUE}README.md${NC}"
echo "  - Quick start: ${BLUE}QUICKSTART.md${NC}"
echo "  - Status: ${BLUE}PROJECT_STATUS.md${NC}"
echo ""

print_success "Setup complete! Happy trading! 🚀"
echo ""

