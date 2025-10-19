# ⚡ Quick Start with UV

**Fast setup guide for UV-based startup scripts**

---

## 🚀 30-Second Start

```bash
# 1. Setup (first time only)
./setup.sh

# 2. Add API credentials
nano .env
# Add: DELTA_API_KEY=your_key
#      DELTA_API_SECRET=your_secret

# 3. Start trading bot (4h timeframe)
./start_bot.sh
```

**That's it! Your 4-hour trading bot is running! 🎉**

---

## 📋 All Scripts

| Script | Description | Command |
|--------|-------------|---------|
| 🔧 **Setup** | First-time setup | `./setup.sh` |
| 🤖 **Bot** | Start trading bot | `./start_bot.sh` |
| 🌐 **API** | Start API server | `./start_api.sh` |
| 🧪 **Tests** | Run test suite | `./start_tests.sh` |

---

## 🎯 Common Commands

### Start Trading
```bash
./start_bot.sh
```

### Start API Server
```bash
./start_api.sh

# Access:
# http://localhost:8000/docs
```

### Run Tests
```bash
./start_tests.sh
# Select: 1 (all tests)
```

### Check Configuration
```bash
cat config.yaml | grep -A 4 "schedule:"
```

### View Logs
```bash
tail -f breakout_bot.log
```

---

## 🔧 Requirements

- ✅ **UV installed** (scripts will install if missing)
- ✅ **.env file** with API credentials
- ✅ **config.yaml** (already set to 4h)

---

## 📊 Current Setup

**Timeframe:** 4 hours (4h)  
**Symbol:** BTCUSD  
**Timezone:** Asia/Kolkata (IST)  
**Strategy:** Breakout trading with breakeven logic

---

## 🎨 Features

All scripts include:
- ✅ Color-coded output
- ✅ Error checking
- ✅ Interactive prompts
- ✅ Auto-dependency management
- ✅ Configuration validation

---

## 🆘 Help

**Detailed docs:** `SCRIPTS_GUIDE.md`  
**Main docs:** `README.md`  
**Project status:** `PROJECT_STATUS.md`

---

**Ready to trade! 🚀📈**

