# 🚀 Startup Scripts Guide

Complete guide to using the UV-based startup scripts for the Breakout Trading Bot.

---

## 📋 Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup.sh` | First-time setup | Run once to configure everything |
| `start_bot.sh` | Start main trading bot | Daily bot operations |
| `start_api.sh` | Start FastAPI server | API-based bot control |
| `start_tests.sh` | Run test suite | Testing and verification |

---

## 🎯 Quick Start

### 1. First-Time Setup
```bash
# Run the setup script (only once)
./setup.sh
```

**What it does:**
- ✅ Checks/installs UV
- ✅ Syncs all dependencies
- ✅ Creates .env and config.yaml from templates
- ✅ Makes all scripts executable
- ✅ Runs tests to verify installation

---

### 2. Start Trading Bot
```bash
# Start the main 4-hour trading bot
./start_bot.sh
```

**Features:**
- ✅ Validates configuration files
- ✅ Shows current settings (symbol, timeframe, timezone)
- ✅ Optional pre-run testing
- ✅ Color-coded output
- ✅ Proper error handling

**Interactive prompts:**
- Run tests before starting? [y/N]

---

### 3. Start API Server
```bash
# Start the FastAPI server
./start_api.sh

# Or with custom settings
HOST=127.0.0.1 PORT=9000 ./start_api.sh
```

**Features:**
- ✅ Auto-reload in development mode
- ✅ Displays all API endpoints
- ✅ Swagger UI and ReDoc available
- ✅ Configurable host and port

**Default settings:**
- Host: `0.0.0.0` (all interfaces)
- Port: `8000`
- Auto-reload: `true`

**Access:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### 4. Run Tests
```bash
# Interactive test runner
./start_tests.sh
```

**Test options:**
1. Run all tests (verbose)
2. Run all tests (quiet)
3. Run 4-hour timeframe tests only
4. Run API server tests only
5. Run bot logic tests only
6. Run with coverage report
7. Run specific test file

---

## 🔧 Detailed Usage

### Setup Script (`setup.sh`)

**Purpose:** One-time initial setup of the project

**Steps performed:**
1. Check/install UV package manager
2. Sync all dependencies from pyproject.toml
3. Create .env from env.example
4. Create config.yaml from config.example.yaml
5. Make all scripts executable
6. Run test suite (optional)

**Usage:**
```bash
./setup.sh
```

**After setup:**
1. Edit `.env` with your Delta Exchange API credentials:
   ```bash
   nano .env
   # Add: DELTA_API_KEY=your_key
   #      DELTA_API_SECRET=your_secret
   ```

2. (Optional) Customize `config.yaml`:
   ```bash
   nano config.yaml
   # Already configured for 4h timeframe
   ```

---

### Bot Starter (`start_bot.sh`)

**Purpose:** Start the main trading bot

**Pre-flight checks:**
- ✅ UV installation verified
- ✅ .env file exists
- ✅ config.yaml exists
- ✅ Dependencies synced

**Configuration display:**
```
Trading Symbol: BTCUSD
Timeframe:      4h
Timezone:       Asia/Kolkata
```

**Optional testing:**
- Prompts to run tests before starting
- Can skip tests if already verified

**Usage:**
```bash
# Standard start
./start_bot.sh

# View logs in real-time
./start_bot.sh | tee bot.log

# Run in background (screen)
screen -S trading-bot ./start_bot.sh
# Detach: Ctrl+A, then D
# Reattach: screen -r trading-bot
```

**Stopping the bot:**
- Press `Ctrl+C` for graceful shutdown
- Bot will cleanup and exit

---

### API Server Starter (`start_api.sh`)

**Purpose:** Start the FastAPI server for API-based control

**Features:**
- Auto-reload for development
- Configurable host and port
- Full API documentation
- RESTful bot management

**Environment variables:**
```bash
HOST=0.0.0.0      # Default: all interfaces
PORT=8000         # Default: 8000
RELOAD=true       # Default: true (auto-reload)
```

**Usage:**
```bash
# Default (localhost:8000 with auto-reload)
./start_api.sh

# Custom host and port
HOST=127.0.0.1 PORT=9000 ./start_api.sh

# Production mode (no auto-reload)
RELOAD=false ./start_api.sh

# Background mode (screen)
screen -S api-server ./start_api.sh
```

**API Endpoints:**
```
GET  /                       - Health check
POST /api/v1/bot/start       - Start a bot
POST /api/v1/bot/stop/{id}   - Stop a bot
GET  /api/v1/bot/status/{id} - Get bot status
GET  /api/v1/bots            - List all bots
```

**Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### Test Runner (`start_tests.sh`)

**Purpose:** Interactive test suite runner

**Test Options:**

#### 1. Run all tests (verbose)
```bash
# Select option 1
# Shows detailed output for each test
```

#### 2. Run all tests (quiet)
```bash
# Select option 2
# Shows only summary
```

#### 3. Run 4-hour timeframe tests only
```bash
# Select option 3
# Tests: test_4hour_timeframe
#        test_bot_with_4hour_timeframe
```

#### 4. Run API server tests only
```bash
# Select option 4
# Tests all API endpoints
```

#### 5. Run bot logic tests only
```bash
# Select option 5
# Tests: test_breakout_bot.py
#        test_breakout_logic.py
```

#### 6. Run with coverage report
```bash
# Select option 6
# Generates HTML coverage report in htmlcov/
```

#### 7. Run specific test file
```bash
# Select option 7
# Enter: test_timeframes.py
```

**Manual testing:**
```bash
# Run all tests
uv run python -m pytest tests/ -v

# Run specific test
uv run python -m pytest tests/test_timeframes.py -v

# Run with coverage
uv run python -m pytest tests/ --cov=src --cov-report=html
```

---

## 🎨 Color-Coded Output

All scripts use color-coded output for clarity:

- 🟢 **Green (✓)** - Success messages
- 🔴 **Red (✗)** - Error messages
- 🟡 **Yellow (⚠)** - Warnings
- 🔵 **Blue (ℹ)** - Information
- 🔷 **Cyan** - Headers and titles

---

## 📊 Common Workflows

### Daily Trading Workflow
```bash
# 1. Check configuration (optional)
cat config.yaml | grep timeframe

# 2. Start the bot
./start_bot.sh

# 3. Monitor logs
tail -f breakout_bot.log
```

---

### Development Workflow
```bash
# 1. Make code changes
nano src/breakout_bot.py

# 2. Run tests
./start_tests.sh
# Select option 1 (all tests)

# 3. Start API server with auto-reload
./start_api.sh

# 4. Test API
curl http://localhost:8000/
```

---

### Testing Workflow
```bash
# 1. Run specific tests
./start_tests.sh
# Select option 3 (4h timeframe tests)

# 2. Run with coverage
./start_tests.sh
# Select option 6 (coverage report)

# 3. View coverage
open htmlcov/index.html
```

---

### Production Deployment
```bash
# 1. One-time setup
./setup.sh

# 2. Configure credentials
nano .env
nano config.yaml

# 3. Verify with tests
./start_tests.sh
# Select option 1

# 4. Start in screen session
screen -S trading-bot ./start_bot.sh

# 5. Detach from screen
# Press: Ctrl+A, then D

# 6. Monitor logs
tail -f breakout_bot.log

# 7. Reattach to screen
screen -r trading-bot
```

---

## 🔍 Troubleshooting

### UV Not Found
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart terminal
source ~/.bashrc  # or ~/.zshrc

# Verify installation
uv --version
```

---

### Missing .env File
```bash
# Create from template
cp env.example .env

# Edit with your credentials
nano .env
```

---

### Missing config.yaml
```bash
# Create from template
cp config.example.yaml config.yaml

# Already configured for 4h timeframe
# Edit if needed
nano config.yaml
```

---

### Tests Failing
```bash
# Sync dependencies
uv sync

# Run tests with verbose output
./start_tests.sh
# Select option 1

# Check specific failing test
uv run python -m pytest tests/test_name.py::test_function -v
```

---

### Port Already in Use (API Server)
```bash
# Use different port
PORT=9000 ./start_api.sh

# Or kill existing process
lsof -ti:8000 | xargs kill -9
```

---

## 🛠️ Advanced Usage

### Custom UV Commands

**Install specific package:**
```bash
uv add package-name
```

**Update dependencies:**
```bash
uv sync --upgrade
```

**Lock dependencies:**
```bash
uv lock
```

---

### Running in Background

**Using screen:**
```bash
# Start new screen session
screen -S bot-name ./start_bot.sh

# List sessions
screen -ls

# Reattach to session
screen -r bot-name

# Kill session
screen -X -S bot-name quit
```

**Using tmux:**
```bash
# Start new tmux session
tmux new -s bot-name
./start_bot.sh

# Detach: Ctrl+B, then D
# Reattach: tmux attach -t bot-name
```

**Using nohup:**
```bash
# Start in background
nohup ./start_bot.sh > bot.log 2>&1 &

# View log
tail -f bot.log

# Find process
ps aux | grep start_bot.sh

# Kill process
kill PID
```

---

### Environment Variables

**Bot configuration:**
```bash
# None required (uses config.yaml)
```

**API server configuration:**
```bash
HOST=0.0.0.0           # Server host
PORT=8000              # Server port
RELOAD=true            # Auto-reload
```

---

## 📝 Script Maintenance

### Update Scripts
If you modify the scripts, remember to:

```bash
# Make executable
chmod +x script_name.sh

# Test the changes
./script_name.sh
```

---

### Script Locations
```
./setup.sh           - Initial setup
./start_bot.sh       - Main bot
./start_api.sh       - API server
./start_tests.sh     - Test runner
./start_api_server.sh - Legacy API starter (deprecated)
```

---

## 🎯 Best Practices

1. **Always run setup.sh first** on a new installation
2. **Test before trading** using `./start_tests.sh`
3. **Use screen/tmux** for production deployments
4. **Monitor logs** regularly: `tail -f breakout_bot.log`
5. **Keep .env secure** - never commit to git
6. **Verify configuration** before starting bot
7. **Run tests after updates** to ensure compatibility

---

## 📚 Related Documentation

- **README.md** - Main project documentation
- **QUICKSTART.md** - Quick start guide
- **PROJECT_STATUS.md** - Current project status
- **OPTIMIZATION_REPORT.md** - Optimization details

---

## 🎉 Quick Reference

```bash
# Setup (first time only)
./setup.sh

# Start trading bot
./start_bot.sh

# Start API server
./start_api.sh

# Run tests
./start_tests.sh

# Check configuration
cat config.yaml | grep -A 4 "schedule:"

# View logs
tail -f breakout_bot.log
```

---

**Created:** October 19, 2025  
**Version:** 1.0.0  
**UV Compatible:** ✅ Yes  
**Status:** Production Ready 🚀

