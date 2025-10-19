#!/bin/bash

# ============================================================
# Breakout Trading Bot - Stop Script
# ============================================================
# This script safely stops the running trading bot
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

# Main
clear
print_header "Stop Trading Bot"

# Find running bot processes
print_info "Searching for running bot processes..."
echo ""

# Find Python processes running the bot
BOT_PIDS=$(ps aux | grep -E "(run_bot\.py|src\.main|start_bot\.sh)" | grep -v grep | grep -v "stop_bot" | awk '{print $2}')

if [ -z "$BOT_PIDS" ]; then
    print_warning "No running bot processes found"
    echo ""
    print_info "The bot may already be stopped"
    echo ""
    exit 0
fi

# Display found processes
print_info "Found running processes:"
echo ""
ps aux | grep -E "(run_bot\.py|src\.main|start_bot\.sh)" | grep -v grep | grep -v "stop_bot"
echo ""

# Count processes
PROCESS_COUNT=$(echo "$BOT_PIDS" | wc -l | tr -d ' ')
print_warning "Found ${PROCESS_COUNT} process(es) to stop"
echo ""

# Ask for confirmation
read -p "$(echo -e ${YELLOW}Stop all bot processes? [y/N]:${NC} )" -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "Operation cancelled"
    echo ""
    exit 0
fi

echo ""
print_info "Stopping bot processes..."
echo ""

# Stop each process gracefully
for PID in $BOT_PIDS; do
    if ps -p $PID > /dev/null; then
        print_info "Sending SIGTERM to process $PID..."
        kill -TERM $PID 2>/dev/null || true
    fi
done

# Wait for graceful shutdown
print_info "Waiting for graceful shutdown (5 seconds)..."
sleep 5

# Check if processes are still running
REMAINING=$(ps aux | grep -E "(run_bot\.py|src\.main|start_bot\.sh)" | grep -v grep | grep -v "stop_bot" | awk '{print $2}')

if [ -z "$REMAINING" ]; then
    echo ""
    print_success "All bot processes stopped successfully"
else
    print_warning "Some processes still running, forcing termination..."
    echo ""
    
    for PID in $REMAINING; do
        if ps -p $PID > /dev/null; then
            print_info "Sending SIGKILL to process $PID..."
            kill -9 $PID 2>/dev/null || true
        fi
    done
    
    sleep 2
    
    # Final check
    FINAL_CHECK=$(ps aux | grep -E "(run_bot\.py|src\.main|start_bot\.sh)" | grep -v grep | grep -v "stop_bot" | wc -l | tr -d ' ')
    
    if [ "$FINAL_CHECK" -eq 0 ]; then
        echo ""
        print_success "All bot processes stopped (force killed)"
    else
        echo ""
        print_error "Failed to stop some processes"
        print_info "Please check manually: ps aux | grep python"
        exit 1
    fi
fi

# Check for screen sessions
SCREEN_SESSIONS=$(screen -ls 2>/dev/null | grep -E "(trading-bot|bot-)" || true)

if [ ! -z "$SCREEN_SESSIONS" ]; then
    echo ""
    print_warning "Found screen sessions that may contain the bot:"
    echo ""
    screen -ls | grep -E "(trading-bot|bot-)" || true
    echo ""
    print_info "To kill screen sessions:"
    echo "  screen -X -S session-name quit"
fi

# Check for tmux sessions
TMUX_SESSIONS=$(tmux ls 2>/dev/null | grep -E "(trading-bot|bot-)" || true)

if [ ! -z "$TMUX_SESSIONS" ]; then
    echo ""
    print_warning "Found tmux sessions that may contain the bot:"
    echo ""
    tmux ls | grep -E "(trading-bot|bot-)" || true
    echo ""
    print_info "To kill tmux sessions:"
    echo "  tmux kill-session -t session-name"
fi

echo ""
print_header "Bot Stopped"

print_info "Bot status:"
echo "  Running processes: ${GREEN}0${NC}"
echo ""

print_info "To restart the bot:"
echo "  ${CYAN}./start_bot.sh${NC}"
echo ""

