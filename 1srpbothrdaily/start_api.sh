#!/bin/bash

# ============================================================
# Breakout Trading Bot - API Server Startup Script
# ============================================================
# This script starts the FastAPI server using UV
# ============================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default configuration
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
RELOAD="${RELOAD:-true}"

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

# Main startup
clear
print_header "Breakout Trading Bot - API Server"

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

# Check if .env file exists (optional for API server)
if [ ! -f ".env" ]; then
    print_info ".env file not found (optional for API server)"
else
    print_success ".env file found"
fi

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

# Navigate to src directory
cd src

# Display server information
print_header "Server Information"
echo -e "  API Server:     ${GREEN}http://${HOST}:${PORT}${NC}"
echo -e "  Swagger UI:     ${GREEN}http://localhost:${PORT}/docs${NC}"
echo -e "  ReDoc:          ${GREEN}http://localhost:${PORT}/redoc${NC}"
echo -e "  OpenAPI JSON:   ${GREEN}http://localhost:${PORT}/openapi.json${NC}"
echo ""
echo -e "  Host:           ${BLUE}${HOST}${NC}"
echo -e "  Port:           ${BLUE}${PORT}${NC}"
echo -e "  Auto-reload:    ${BLUE}${RELOAD}${NC}"
echo ""

print_info "Press Ctrl+C to stop the server"
echo ""
echo -e "${CYAN}============================================================${NC}"
echo ""

# Start the API server
if [ "$RELOAD" = "true" ]; then
    uv run uvicorn api_server:app --host ${HOST} --port ${PORT} --reload
else
    uv run uvicorn api_server:app --host ${HOST} --port ${PORT}
fi

# Cleanup on exit
cd ..
echo ""
print_info "API server stopped"
echo ""

