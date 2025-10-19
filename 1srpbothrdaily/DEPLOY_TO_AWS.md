# 🚀 Quick AWS EC2 Deployment Guide

**Fast-track deployment for your 4-hour trading bot on AWS EC2**

---

## ⚡ Quick Setup (15 minutes)

### 1️⃣ Launch EC2 Instance (AWS Console)

```
Instance Type:    t4g.micro (ARM - CHEAPEST! 20% less than t3.micro)
                  OR t3.micro (Intel - Free tier)
AMI:              Ubuntu 22.04 LTS ARM64 (for t4g)
                  OR Ubuntu 22.04 LTS (for t3)
Storage:          8 GB gp3
Security Group:   SSH (22) from Your IP
                  HTTPS (443) outbound
Key Pair:         Download .pem file
```

**💰 Cost Tip:** Use t4g.micro (ARM) to save 20% = ~$12-24/year!

### 2️⃣ Connect to Server

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

### 3️⃣ Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.12 python3.12-venv git

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

### 4️⃣ Clone & Setup Bot

```bash
# Clone repo
git clone https://github.com/yourusername/srpprivatetradedailybot.git
cd srpprivatetradedailybot

# Create .env
nano .env
# Add:
# DELTA_API_KEY=your_key
# DELTA_API_SECRET=your_secret

# Setup
./setup.sh

# Use optimized config for EC2 cost savings
cp config.ec2.yaml config.yaml
```

### 5️⃣ Run Bot with Screen

```bash
# Install screen
sudo apt install -y screen

# Start bot in background
screen -S trading-bot
./start_bot.sh

# Detach: Ctrl+A, then D
# Reattach: screen -r trading-bot
```

---

## ✅ Verification

```bash
# Check bot is running
ps aux | grep run_bot

# Monitor logs
tail -f breakout_bot.log

# Check for errors
grep ERROR breakout_bot.log
```

---

## 🛑 Stop Bot

```bash
# Reattach to screen
screen -r trading-bot

# Stop bot
# Press Ctrl+C

# Or from outside screen
./stop_bot.sh
```

---

## 📊 Monitor Trading

```bash
# Real-time logs
tail -f breakout_bot.log

# Check positions
grep "Position opened" breakout_bot.log

# Check breakeven triggers
grep "breakeven" breakout_bot.log
```

---

## 🔒 Security Checklist

- [ ] SSH key saved securely
- [ ] Security group: SSH from your IP only
- [ ] .env file has correct permissions (600)
- [ ] EC2 IP whitelisted on Delta Exchange
- [ ] .env NOT committed to git
- [ ] Elastic IP allocated (recommended)

---

## 💰 Costs

**Free Tier (First 12 months):**
- ✅ 750 hours/month of t3.micro = FREE
- ✅ 30 GB storage = FREE

**After Free Tier:**
- t3.micro: ~$7-8/month
- t3.small: ~$15/month

---

## 🆘 Quick Troubleshooting

**Bot won't start?**
```bash
tail -50 breakout_bot.log
```

**API errors?**
- Check .env credentials
- Whitelist EC2 IP on Delta Exchange

**Out of memory?**
```bash
free -h
# Add swap if needed (see full guide)
```

---

## 📚 Full Documentation

**Detailed guide:** `AWS_EC2_DEPLOYMENT.md`

**Topics covered:**
- Complete EC2 setup
- Systemd service configuration
- Log rotation
- Monitoring
- Security hardening
- Troubleshooting

---

## 🎯 Production Setup (Recommended)

**Create systemd service:**

```bash
sudo nano /etc/systemd/system/trading-bot.service
```

**Add:**
```ini
[Unit]
Description=4H Trading Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/srpprivatetradedailybot
ExecStart=/home/ubuntu/.cargo/bin/uv run python run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable trading-bot
sudo systemctl start trading-bot

# Check status
sudo systemctl status trading-bot

# View logs
sudo journalctl -u trading-bot -f
```

---

## 🔄 Updates

```bash
# Stop bot
./stop_bot.sh

# Pull updates
git pull

# Update deps
uv sync

# Restart
./start_bot.sh
```

---

## 📞 Essential Commands

```bash
# Connect
ssh -i key.pem ubuntu@IP

# Start
./start_bot.sh

# Stop
./stop_bot.sh

# Logs
tail -f breakout_bot.log

# Status
ps aux | grep run_bot

# Screen
screen -S trading-bot  # Create
Ctrl+A, D              # Detach
screen -r trading-bot  # Reattach
```

---

**Ready to deploy? Follow these steps and you're live in 15 minutes! 🚀**

For complete details, see `AWS_EC2_DEPLOYMENT.md`

