# Daily Breakout Trading Bot for Delta Exchange India 🚀

A fully automated, production-ready trading bot that implements a daily breakout strategy with intelligent breakeven logic. Built specifically for Delta Exchange India with Indian Standard Time (IST) support.

[![Tests](https://img.shields.io/badge/tests-48%20passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.12+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Strategy Explanation](#strategy-explanation)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Configuration Guide](#configuration-guide)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Safety & Risk Management](#safety--risk-management)
- [FAQ](#faq)
- [Disclaimer](#disclaimer)

## 🎯 Overview

This bot automates a daily breakout trading strategy on Delta Exchange India. It:

1. Calculates previous day's high and low at midnight IST
2. Places limit orders at breakout levels (buy at high, sell at low)
3. Manages positions with automatic stop-loss and take-profit
4. Implements breakeven logic to protect profits
5. Resets daily for fresh trading opportunities

**Perfect for:** Traders who want to automate breakout strategies without constant monitoring.

## ✨ Features

### Core Trading Features
- ✅ **Automated Daily Breakouts**: Calculates and trades previous day high/low
- ✅ **Breakeven Protection**: Automatically moves stop-loss to entry price after profit threshold
- ✅ **Configurable Risk Management**: Customizable SL, TP, and breakeven triggers
- ✅ **Daily Reset**: Automatic calculation and order placement at midnight IST
- ✅ **Position Monitoring**: Continuous tracking of open positions
- ✅ **Order Management**: Automatic cancellation of opposite orders on fill

### Technical Features
- ✅ **Indian Standard Time (IST) Support**: Configured for Asia/Kolkata timezone
- ✅ **UV Package Manager Compatible**: Modern Python package management
- ✅ **Comprehensive Testing**: 48 unit, integration, and E2E tests (100% passing)
- ✅ **Production-Ready**: Robust error handling and logging
- ✅ **Fully Configurable**: All parameters via YAML config file
- ✅ **API Authentication**: Secure HMAC SHA256 signature

## 📊 Strategy Explanation

### Daily Breakout Strategy

The bot implements a classic breakout strategy that capitalizes on price movements beyond the previous day's range:

**1. Setup Phase (Midnight IST)**
```
Previous Day High = 65,000
Previous Day Low = 59,000
```

**2. Order Placement**
```
Buy Order  → 65,000 (breakout above)
Sell Order → 59,000 (breakout below)
```

**3. Breakout Detection**
```
If price hits 65,500:
  ✓ Buy order fills
  ✓ Sell order cancelled
  ✓ Position opened: LONG @ 65,000
```

**4. Risk Management**
```
Stop Loss    → 55,000 (65,000 - 10,000 points)
Take Profit  → 105,000 (65,000 + 40,000 points)
```

**5. Breakeven Logic** (Unique Feature!)
```
If price reaches 75,000 (10,000 points profit):
  ✓ Bot detects profit threshold
  ✓ Moves SL to 65,000 (entry price)
  ✓ Position now RISK-FREE!
```

**6. Position Exit**
- Take profit hits at 105,000 → +40,000 points profit
- OR Stop loss hits → Position closed at breakeven or small loss
- Bot waits for next daily reset

### Why This Strategy Works

1. **Captures Momentum**: Breakouts often indicate strong directional moves
2. **Risk-Free After Threshold**: Breakeven logic protects profits
3. **Daily Fresh Start**: No overnight risk, clean slate each day
4. **Automated Execution**: Removes emotional decision-making

## 🚀 Installation

### Prerequisites

- **Python 3.12 or higher**
- **UV package manager** (recommended) or pip
- **Delta Exchange India account** with API access
- **API credentials** (API Key and Secret)

### Step 1: Clone or Navigate to Project

```bash
cd 5RsiMAAlgoTrading
```

### Step 2: Install Dependencies

#### Option A: Using UV (Recommended)

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies
uv sync
```

#### Option B: Using pip

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Setup API Credentials

Create a `.env` file:

```bash
cp env.example .env
```

Edit `.env` and add your Delta Exchange API credentials:

```env
DELTA_API_KEY=your_actual_api_key_here
DELTA_API_SECRET=your_actual_api_secret_here
```

**Get API Keys:** https://india.delta.exchange/app/account/api

⚠️ **Security Note:** Never commit your `.env` file to version control!

### Step 4: Configure Strategy

Edit `config.yaml` to customize your strategy:

```bash
nano config.yaml  # or use your preferred editor
```

See [Configuration Guide](#configuration-guide) for detailed parameter explanations.

## ⚙️ Configuration

### Basic Configuration (config.yaml)

```yaml
trading:
  symbol: "BTCUSD"              # Trading pair (BTC/USD, ETH/USD, etc.)
  product_id: 27                # Delta Exchange product ID
  order_size: 1                 # Number of contracts per trade

schedule:
  reset_time: "00:00"           # Daily reset time (HH:MM format)
  timezone: "Asia/Kolkata"      # Indian Standard Time (IST)

risk_management:
  stop_loss_points: 10000       # SL distance from entry (points)
  take_profit_points: 40000     # TP distance from entry (points)
  breakeven_trigger_points: 10000  # Profit to trigger breakeven (points)

monitoring:
  order_check_interval: 10      # How often to check orders (seconds)
  position_check_interval: 5    # How often to monitor positions (seconds)

api:
  base_url: "https://api.india.delta.exchange"

logging:
  level: "INFO"                 # DEBUG, INFO, WARNING, ERROR
  file: "breakout_bot.log"
```

### Finding Product ID

To find the correct `product_id` for your symbol:

```python
python -c "
from src.delta_client import DeltaExchangeClient
client = DeltaExchangeClient('', '', 'https://api.india.delta.exchange')
# Search for your symbol in the products list
"
```

Or check: https://india.delta.exchange/app/trade/BTCUSD (product ID in URL)

## 🎮 Usage

### Running the Bot

#### Start the Bot

```bash
# Using UV
uv run python -m src.main

# Using regular Python
python -m src.main
```

#### Output on Startup

```
✓ Configuration loaded successfully
2025-10-13 17:45:00 - INFO - ============================================================
2025-10-13 17:45:00 - INFO - Daily Breakout Trading Bot Starting
2025-10-13 17:45:00 - INFO - ============================================================
2025-10-13 17:45:01 - INFO - Trading Symbol: BTCUSD
2025-10-13 17:45:01 - INFO - Product ID: 27
2025-10-13 17:45:01 - INFO - Order Size: 1
2025-10-13 17:45:01 - INFO - Reset Time: 00:00 Asia/Kolkata
2025-10-13 17:45:01 - INFO - Stop Loss: 10000 points
2025-10-13 17:45:01 - INFO - Take Profit: 40000 points
2025-10-13 17:45:01 - INFO - Breakeven Trigger: 10000 points
2025-10-13 17:45:02 - INFO - ✓ API connection successful - Current BTCUSD price: 65432
2025-10-13 17:45:03 - INFO - Previous day levels - High: 65000, Low: 59000
2025-10-13 17:45:04 - INFO - Buy breakout order placed at 65000, ID: 12345
2025-10-13 17:45:05 - INFO - Sell breakout order placed at 59000, ID: 12346
2025-10-13 17:45:05 - INFO - Starting main trading loop...
```

#### Stop the Bot

Press `Ctrl+C` to gracefully stop the bot:

```
2025-10-13 18:30:00 - INFO - Bot stopped by user (Ctrl+C)
2025-10-13 18:30:00 - INFO - Performing cleanup...
2025-10-13 18:30:01 - INFO - ============================================================
2025-10-13 18:30:01 - INFO - Daily Breakout Trading Bot Stopped
2025-10-13 18:30:01 - INFO - ============================================================
```

### Monitoring the Bot

#### Watch Live Logs

```bash
# In a separate terminal
tail -f breakout_bot.log
```

#### Check Bot Status

```bash
# View last 50 log lines
tail -n 50 breakout_bot.log

# Search for specific events
grep "Position opened" breakout_bot.log
grep "breakeven" breakout_bot.log
grep "ERROR" breakout_bot.log
```

## 🧪 Testing

The bot includes comprehensive test coverage (48 tests, 100% passing).

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Run Specific Test Categories

```bash
# Unit tests only
python -m pytest tests/test_delta_client.py tests/test_config_loader.py -v

# Integration tests
python -m pytest tests/test_breakout_bot.py -v

# End-to-end tests
python -m pytest tests/test_e2e.py -v
```

### Run with Detailed Output

```bash
# Show print statements
python -m pytest tests/ -v -s

# Show only failures
python -m pytest tests/ -v --tb=short
```

### Test Results

```
============================= test session starts ==============================
collected 48 items

tests/test_breakout_bot.py::TestBreakoutTradingBot::test_initialization PASSED
tests/test_breakout_bot.py::TestBreakoutTradingBot::test_calculate_previous_day_levels_success PASSED
... (46 more tests)

============================== 48 passed in 9.13s ===============================
```

## 📁 Project Structure

```
5RsiMAAlgoTrading/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── config_loader.py         # Configuration management (4.9 KB)
│   ├── delta_client.py          # Delta Exchange API client (13 KB)
│   ├── breakout_bot.py          # Main trading bot logic (20 KB)
│   └── main.py                  # Entry point (4.5 KB)
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── test_config_loader.py    # Config loader tests (9 tests)
│   ├── test_delta_client.py     # API client tests (17 tests)
│   ├── test_breakout_bot.py     # Bot logic tests (16 tests)
│   └── test_e2e.py              # End-to-end tests (6 tests)
│
├── backup_code/                  # Reference code (not used by bot)
│   ├── delta_rest_client/       # Delta client reference
│   ├── 4strategymovingaverage.py
│   └── official_code/           # API examples
│
├── config.yaml                   # Strategy configuration ⚙️
├── .env                         # API credentials (user creates)
├── env.example                  # Environment template
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project metadata
├── README.md                   # This file
├── QUICKSTART.md               # Quick start guide
└── IMPLEMENTATION_SUMMARY.md   # Technical details
```

## 🔄 How It Works

### Daily Cycle Flow

```
┌─────────────────────────────────────────────────────────────┐
│  00:00 IST - DAILY RESET                                    │
│  ├─ Fetch previous day's candle data                        │
│  ├─ Calculate: prev_high and prev_low                       │
│  └─ Cancel any existing orders                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  ORDER PLACEMENT                                            │
│  ├─ Place Buy Order @ prev_high                            │
│  └─ Place Sell Order @ prev_low                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  MONITORING LOOP (every 10 seconds)                         │
│  └─ Check if any order filled                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  ORDER FILLED - POSITION OPENED                             │
│  ├─ Cancel opposite order                                   │
│  ├─ Record entry price and side                             │
│  ├─ Place Stop Loss order                                   │
│  └─ Place Take Profit order                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  POSITION MONITORING (every 5 seconds)                      │
│  ├─ Calculate current profit/loss                           │
│  ├─ Check if profit ≥ breakeven_trigger                    │
│  └─ If YES: Move SL to entry price (BREAKEVEN!)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  POSITION EXIT                                              │
│  ├─ Take Profit hit → Position closed with profit          │
│  ├─ Stop Loss hit → Position closed (breakeven or loss)    │
│  └─ Wait for next daily reset                              │
└─────────────────────────────────────────────────────────────┘
```

### State Machine Diagram

```
                    ┌──────────────┐
                    │   WAITING    │
                    │  FOR RESET   │
                    └──────┬───────┘
                           │ 00:00 IST
                           ↓
                    ┌──────────────┐
                    │ CALCULATING  │
                    │   LEVELS     │
                    └──────┬───────┘
                           │
                           ↓
                    ┌──────────────┐
                    │   ORDERS     │
                    │   PLACED     │
                    └──────┬───────┘
                           │ Order fills
                           ↓
                    ┌──────────────┐
                    │  POSITION    │
                    │    OPEN      │
                    └──────┬───────┘
                           │ Profit ≥ threshold
                           ↓
                    ┌──────────────┐
                    │  BREAKEVEN   │
                    │   APPLIED    │
                    └──────┬───────┘
                           │ TP/SL hit
                           ↓
                    ┌──────────────┐
                    │   POSITION   │
                    │    CLOSED    │
                    └──────┬───────┘
                           │
                           ↓ (repeat)
```

## 📖 Configuration Guide

### Trading Parameters

#### `symbol` (string)
- **Description**: Trading pair symbol
- **Examples**: "BTCUSD", "ETHUSD", "SOLUSD"
- **Important**: Must match Delta Exchange available symbols
- **Default**: "BTCUSD"

#### `product_id` (integer)
- **Description**: Delta Exchange internal product identifier
- **How to find**: Check Delta Exchange API or product page
- **Example**: 27 for BTCUSD
- **Important**: Must match your chosen symbol

#### `order_size` (integer)
- **Description**: Number of contracts per trade
- **Recommendation**: Start with 1 for testing
- **Range**: 1 to your account limit
- **Default**: 1

### Schedule Parameters

#### `reset_time` (string, HH:MM format)
- **Description**: Daily reset time in 24-hour format
- **Default**: "00:00" (midnight IST)
- **Examples**: 
  - "00:00" - Midnight
  - "09:15" - Market open time in India
  - "15:30" - Market close time in India
- **Note**: Time is in your configured timezone

#### `timezone` (string)
- **Description**: Timezone for all time operations
- **Default**: "Asia/Kolkata" (Indian Standard Time)
- **Other options**: 
  - "UTC" - Universal Time
  - "US/Eastern" - New York time
  - See: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
- **IST Offset**: UTC+5:30

### Risk Management Parameters

#### `stop_loss_points` (integer)
- **Description**: Distance from entry price for stop loss
- **Unit**: Price points (not percentage)
- **Example**: If entry is 60,000 and SL is 10,000 points:
  - Long position: SL at 50,000
  - Short position: SL at 70,000
- **Default**: 10000
- **Recommendation**: Adjust based on symbol volatility

#### `take_profit_points` (integer)
- **Description**: Distance from entry price for take profit
- **Unit**: Price points
- **Example**: If entry is 60,000 and TP is 40,000 points:
  - Long position: TP at 100,000
  - Short position: TP at 20,000
- **Default**: 40000
- **Recommendation**: Aim for 2:1 or 3:1 reward:risk ratio

#### `breakeven_trigger_points` (integer)
- **Description**: Profit threshold to move SL to entry (breakeven)
- **Unit**: Price points
- **Example**: If entry is 60,000 and trigger is 10,000:
  - When price reaches 70,000 (long), SL moves from 50,000 to 60,000
- **Default**: 10000
- **Strategy**: Locks in profits and makes trade risk-free
- **Recommendation**: Set at 1x your stop loss distance

### Monitoring Parameters

#### `order_check_interval` (integer)
- **Description**: How often to check if orders are filled
- **Unit**: Seconds
- **Default**: 10
- **Range**: 5-60 seconds
- **Lower value**: More responsive, more API calls
- **Higher value**: Less responsive, fewer API calls

#### `position_check_interval` (integer)
- **Description**: How often to monitor open positions
- **Unit**: Seconds
- **Default**: 5
- **Range**: 1-30 seconds
- **Recommendation**: Keep at 5-10 for timely breakeven execution

### API Parameters

#### `base_url` (string)
- **Description**: Delta Exchange API endpoint
- **Default**: "https://api.india.delta.exchange"
- **Testnet**: "https://cdn-ind.testnet.deltaex.org"
- **Global**: "https://api.delta.exchange"

### Logging Parameters

#### `level` (string)
- **Options**: "DEBUG", "INFO", "WARNING", "ERROR"
- **Default**: "INFO"
- **DEBUG**: Detailed logs (for troubleshooting)
- **INFO**: Normal operations
- **WARNING**: Important warnings
- **ERROR**: Errors only

#### `file` (string)
- **Description**: Log file path
- **Default**: "breakout_bot.log"
- **Example**: "logs/bot_2025_01.log"

## 📝 Logging

### Log Levels

The bot uses Python's logging module with these levels:

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages for non-critical issues
- **ERROR**: Error messages for failures

### Log Format

```
YYYY-MM-DD HH:MM:SS - MODULE - LEVEL - MESSAGE
2025-10-13 17:45:00 - src.breakout_bot - INFO - Position opened: LONG 1 @ 65000
```

### Important Log Messages

#### Startup
```
✓ Configuration loaded successfully
✓ Delta Exchange client initialized
✓ API connection successful - Current BTCUSD price: 65432
```

#### Order Placement
```
Buy breakout order placed at 65000, ID: 12345
Sell breakout order placed at 59000, ID: 12346
```

#### Position Management
```
Position opened: LONG 1 @ 65000
Sell order cancelled
Stop loss order placed at 55000, ID: 12347
Take profit order placed at 105000, ID: 12348
```

#### Breakeven Logic
```
Position monitor - Current: 70500, Entry: 65000, Profit: 5500.00 points
Breakeven trigger reached! Profit: 10200.00 points (threshold: 10000)
Stop loss moved to breakeven: 65000
```

#### Position Close
```
Position closed
Position state reset
```

#### Daily Reset
```
Performing daily reset...
All orders cancelled
Daily counters reset
Previous day levels - High: 66000, Low: 60000
Buy breakout order placed at 66000, ID: 12349
Sell breakout order placed at 60000, ID: 12350
Daily reset completed successfully
```

### Log File Management

#### View Recent Logs
```bash
# Last 50 lines
tail -n 50 breakout_bot.log

# Follow in real-time
tail -f breakout_bot.log
```

#### Search Logs
```bash
# Find errors
grep "ERROR" breakout_bot.log

# Find breakeven events
grep "breakeven" breakout_bot.log

# Find position opens
grep "Position opened" breakout_bot.log

# Find today's activity
grep "2025-10-13" breakout_bot.log
```

#### Log Rotation
```bash
# Manual log rotation
mv breakout_bot.log breakout_bot_2025_10_13.log
# Bot will create new log file on restart
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Bot Won't Start

**Error**: `API credentials not found`

**Solution**:
```bash
# Check .env file exists
ls -la .env

# Verify contents
cat .env

# Should show:
# DELTA_API_KEY=your_key_here
# DELTA_API_SECRET=your_secret_here

# If missing, create it:
cp env.example .env
nano .env  # Add your credentials
```

**Error**: `Configuration file not found`

**Solution**:
```bash
# Check config.yaml exists
ls -la config.yaml

# If missing, restore from backup or template
```

#### 2. Orders Not Placing

**Issue**: Orders aren't being placed after daily reset

**Diagnosis**:
```bash
# Check logs for errors
grep "ERROR" breakout_bot.log | tail -n 10

# Verify API connection
python -c "
from src.config_loader import ConfigLoader
from src.delta_client import DeltaExchangeClient
c = ConfigLoader()
client = DeltaExchangeClient(*c.get_api_credentials(), c.get_api_config()['base_url'])
print(client.get_ticker('BTCUSD'))
"
```

**Solutions**:
- Check API key permissions on Delta Exchange
- Verify sufficient account balance
- Check product_id matches symbol
- Review rate limits

#### 3. Breakeven Not Triggering

**Issue**: Stop loss not moving to breakeven despite profit

**Diagnosis**:
```bash
# Check position monitoring logs
grep "Position monitor" breakout_bot.log | tail -n 20
```

**Common Causes**:
- Profit hasn't reached `breakeven_trigger_points` yet
- Position already closed
- API error during order edit

**Solution**:
- Verify breakeven_trigger_points is set correctly
- Check position_check_interval isn't too high
- Review error logs

#### 4. Daily Reset Not Working

**Issue**: Bot not resetting at configured time

**Diagnosis**:
```bash
# Check current time vs configured time
python -c "
from datetime import datetime
import pytz
ist = pytz.timezone('Asia/Kolkata')
print(f'Current IST time: {datetime.now(ist)}')
print(f'Configured reset: 00:00 IST')
"
```

**Solutions**:
- Verify timezone is correct: "Asia/Kolkata"
- Check reset_time format is "HH:MM"
- Ensure bot is running continuously
- Review logs for reset execution

#### 5. Test Failures

**Issue**: Tests failing after code changes

**Diagnosis**:
```bash
# Run tests with detailed output
python -m pytest tests/ -v -s --tb=short

# Run specific failing test
python -m pytest tests/test_delta_client.py::TestDeltaExchangeClient::test_place_limit_order_success -v
```

**Solutions**:
- Check environment variables are set for tests
- Verify all dependencies installed: `pip list`
- Clear pytest cache: `rm -rf .pytest_cache`

#### 6. High CPU/Memory Usage

**Issue**: Bot consuming excessive resources

**Diagnosis**:
```bash
# Monitor Python process
top -p $(pgrep -f "src.main")
```

**Solutions**:
- Increase `order_check_interval` (reduce API calls)
- Increase `position_check_interval`
- Check for infinite loops in logs
- Restart bot

#### 7. Connection Timeouts

**Issue**: Frequent API timeout errors

**Solutions**:
- Check internet connection
- Verify Delta Exchange API status
- Increase timeout in delta_client.py (line 73, 75, 77)
- Reduce API call frequency

### Getting Help

If you encounter issues not covered here:

1. **Check Logs**: `tail -n 100 breakout_bot.log`
2. **Run Tests**: `python -m pytest tests/ -v`
3. **Verify Config**: Review `config.yaml` and `.env`
4. **Test API**: Ensure Delta Exchange API is accessible
5. **Review Documentation**: Check QUICKSTART.md and IMPLEMENTATION_SUMMARY.md

### Debug Mode

Enable debug logging for detailed information:

```yaml
# In config.yaml
logging:
  level: "DEBUG"  # Change from INFO to DEBUG
```

Restart the bot and check logs for detailed execution traces.

## 🛡️ Safety & Risk Management

### Trading Risks

⚠️ **IMPORTANT WARNINGS:**

1. **Market Risk**: Cryptocurrency markets are highly volatile
2. **Execution Risk**: Orders may not fill at expected prices
3. **Technical Risk**: Software bugs, network issues, API failures
4. **Liquidity Risk**: Low liquidity may cause slippage
5. **Capital Risk**: Only trade with money you can afford to lose

### Best Practices

#### Start Small
```yaml
# Start with minimum order size
trading:
  order_size: 1  # Start with 1 contract
```

#### Test First
```bash
# Always run tests before live trading
python -m pytest tests/ -v

# Test with small amounts for 1-2 days
# Monitor closely before scaling up
```

#### Use Testnet
```yaml
# Test on Delta Exchange testnet first
api:
  base_url: "https://cdn-ind.testnet.deltaex.org"
```

#### Monitor Regularly
- Check logs daily: `tail -f breakout_bot.log`
- Review positions on Delta Exchange dashboard
- Monitor account balance and margin

#### Set Realistic Parameters
```yaml
risk_management:
  stop_loss_points: 10000        # Not too tight
  take_profit_points: 40000      # Reasonable target
  breakeven_trigger_points: 10000  # Conservative
```

#### Backup Your Configuration
```bash
# Backup config regularly
cp config.yaml config_backup_$(date +%Y%m%d).yaml
```

#### Account Security
- Never share API keys
- Use API key restrictions (IP whitelist)
- Set API key permissions (no withdrawals)
- Enable 2FA on Delta Exchange

### Emergency Procedures

#### Stop Bot Immediately
```bash
# Press Ctrl+C or kill process
pkill -f "src.main"
```

#### Cancel All Orders
```python
python -c "
from src.config_loader import ConfigLoader
from src.delta_client import DeltaExchangeClient
c = ConfigLoader()
client = DeltaExchangeClient(*c.get_api_credentials(), c.get_api_config()['base_url'])
client.cancel_all_orders()
print('All orders cancelled')
"
```

#### Check Positions
```bash
# Login to Delta Exchange dashboard
# Or use API:
python -c "
from src.config_loader import ConfigLoader
from src.delta_client import DeltaExchangeClient
c = ConfigLoader()
client = DeltaExchangeClient(*c.get_api_credentials(), c.get_api_config()['base_url'])
print(client.get_positions())
"
```

## ❓ FAQ

### General Questions

**Q: What timezone does the bot use?**
A: The bot is configured for Indian Standard Time (IST / Asia/Kolkata timezone). Daily resets happen at midnight IST.

**Q: Can I run multiple bots for different symbols?**
A: Yes, create separate config files and run multiple instances with different configurations.

**Q: Does the bot work 24/7?**
A: Yes, the bot runs continuously. It monitors positions throughout the day and resets at midnight IST.

**Q: What happens if my internet disconnects?**
A: The bot will stop functioning. Existing orders and positions remain on Delta Exchange. Restart the bot when connection is restored.

### Configuration Questions

**Q: How do I change the reset time?**
A: Edit `config.yaml`, change `schedule.reset_time` to your preferred time in HH:MM format (e.g., "09:15").

**Q: Can I use a different timezone?**
A: Yes, change `schedule.timezone` to any valid timezone (e.g., "UTC", "US/Eastern", "Europe/London").

**Q: What's the difference between points and price?**
A: "Points" refer to actual price units. For example, if BTC is at 60,000 and you set SL at 10,000 points, the SL will be at 50,000.

**Q: Should I use market or limit orders?**
A: The bot uses limit orders for entries at breakout levels, which is optimal for this strategy.

### Trading Questions

**Q: What if both orders get filled?**
A: This is extremely unlikely. When one order fills, the bot immediately cancels the other.

**Q: What happens at the daily reset if I have an open position?**
A: The bot does NOT close existing positions during reset. It only cancels pending orders and places new ones.

**Q: How does breakeven work exactly?**
A: When your position profit reaches the `breakeven_trigger_points`, the bot automatically moves your stop loss to your entry price, making the trade risk-free.

**Q: Can I manually close positions?**
A: Yes, you can manually close positions on Delta Exchange. The bot will detect the closed position and continue monitoring.

### Technical Questions

**Q: Where are API keys stored?**
A: In the `.env` file, which should NEVER be committed to version control. It's listed in `.gitignore`.

**Q: Can I backtest this strategy?**
A: The current implementation doesn't include backtesting. You can modify it to use historical data for backtesting.

**Q: How do I update the bot?**
A: Pull latest changes, run tests, and restart. Your `config.yaml` and `.env` are preserved.

**Q: Does the bot handle API rate limits?**
A: Yes, the bot uses configurable intervals to avoid excessive API calls.

## 📄 Disclaimer

**IMPORTANT - PLEASE READ CAREFULLY**

This software is provided for **EDUCATIONAL PURPOSES ONLY**.

### No Financial Advice

This bot does NOT constitute financial, investment, trading, or other advice. It is a tool that you use at your own discretion and risk.

### Use at Your Own Risk

- **Cryptocurrency trading involves substantial risk of loss**
- Past performance does not guarantee future results
- You could lose your entire investment
- Only trade with money you can afford to lose completely

### No Warranties

This software is provided "AS IS" without warranties of any kind, either express or implied, including but not limited to:

- Merchantability
- Fitness for a particular purpose
- Non-infringement
- Accuracy or reliability

### Your Responsibility

By using this bot, you acknowledge that:

1. You understand cryptocurrency trading risks
2. You have tested the bot thoroughly before live trading
3. You are responsible for all trading decisions and losses
4. You will monitor the bot and intervene if necessary
5. You understand the bot may have bugs or errors
6. You have sufficient knowledge to use and modify the bot

### Liability Limitation

The developers and contributors of this software SHALL NOT be liable for any:

- Financial losses
- Trading losses
- Data loss
- System failures
- API failures
- Network issues
- Or any other damages arising from use of this software

### Regulatory Compliance

Ensure you comply with all applicable laws and regulations in your jurisdiction regarding:

- Cryptocurrency trading
- Automated trading systems
- Tax reporting
- KYC/AML requirements

### Testing Requirement

**ALWAYS:**
- Test on testnet first
- Start with minimum position sizes
- Monitor closely for the first few days
- Have a stop-loss plan
- Never leave the bot completely unattended

## 📜 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

- Delta Exchange India for the API
- Reference code from Delta Exchange documentation
- Python community for excellent libraries

## 📞 Support

For questions or issues:

1. Check this README
2. Review QUICKSTART.md
3. Check logs: `tail -f breakout_bot.log`
4. Run tests: `python -m pytest tests/ -v`
5. Review IMPLEMENTATION_SUMMARY.md

---

## 🎓 Additional Resources

- [Delta Exchange India](https://india.delta.exchange/)
- [Delta Exchange API Documentation](https://docs.delta.exchange/)
- [Python Documentation](https://docs.python.org/3/)
- [PyYAML Documentation](https://pyyaml.org/)
- [Pytest Documentation](https://docs.pytest.org/)

---

**Made with ❤️ for algorithmic traders in India**

**Version**: 1.0.0  
**Last Updated**: October 13, 2025  
**Python Version**: 3.12+  
**Test Status**: ✅ 48/48 passing  
**Timezone**: 🇮🇳 IST (Asia/Kolkata)

---

*Happy Trading! May your breakouts be profitable and your stop losses never hit! 🚀📈*

