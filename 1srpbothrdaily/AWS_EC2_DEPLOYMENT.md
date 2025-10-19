# 🚀 AWS EC2 Deployment Guide

Complete guide for deploying your 4-hour trading bot on AWS EC2.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [EC2 Instance Setup](#ec2-instance-setup)
3. [Initial Server Configuration](#initial-server-configuration)
4. [Bot Deployment](#bot-deployment)
5. [Running the Bot](#running-the-bot)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Security Best Practices](#security-best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### What You Need

- ✅ AWS Account
- ✅ SSH key pair (.pem file)
- ✅ Delta Exchange API credentials
- ✅ Basic Linux knowledge

### Recommended EC2 Instance

**Instance Type:** `t3.micro` or `t3.small`
- **vCPU:** 2
- **RAM:** 1-2 GB
- **Storage:** 8-20 GB
- **Cost:** ~$7-15/month
- **OS:** Ubuntu 22.04 LTS or Amazon Linux 2023

---

## EC2 Instance Setup

### Step 1: Launch EC2 Instance

**Via AWS Console:**

1. Go to EC2 Dashboard → Launch Instance
2. **Name:** `trading-bot-4h`
3. **AMI:** Ubuntu Server 22.04 LTS (Free tier eligible)
4. **Instance type:** `t3.micro` (Free tier eligible)
5. **Key pair:** Create new or use existing
6. **Network settings:**
   - Allow SSH (port 22) from your IP
   - Allow HTTPS (port 443) - outbound for API calls
7. **Storage:** 8 GB gp3 (sufficient)
8. Click **Launch Instance**

### Step 2: Configure Security Group

**Inbound Rules:**
```
SSH (22)     - Your IP only (security!)
Custom (8000) - Your IP only (for API server, optional)
```

**Outbound Rules:**
```
HTTPS (443)  - 0.0.0.0/0 (for Delta Exchange API)
HTTP (80)    - 0.0.0.0/0 (for package downloads)
```

### Step 3: Allocate Elastic IP (Recommended)

1. Go to Elastic IPs → Allocate Elastic IP
2. Associate with your instance
3. **Note the IP address**

---

## Initial Server Configuration

### Step 1: Connect to EC2

```bash
# Download your .pem file (from AWS Console)
# Set permissions
chmod 400 your-key.pem

# Connect to instance
ssh -i your-key.pem ubuntu@YOUR_ELASTIC_IP
```

### Step 2: Update System

```bash
# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y git curl wget htop nano
```

### Step 3: Install Python 3.12

```bash
# Add deadsnakes PPA (for latest Python)
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Install Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# Verify installation
python3.12 --version
```

### Step 4: Install UV Package Manager

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (add to ~/.bashrc for persistence)
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify UV installation
uv --version
```

### Step 5: Setup Git

```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Bot Deployment

### Step 1: Clone Repository

```bash
# Clone from GitHub
cd ~
git clone https://github.com/yourusername/srpprivatetradedailybot.git

# Or upload manually using SCP
# From your local machine:
# scp -i your-key.pem -r ./srpprivatetradedailybot ubuntu@YOUR_IP:~/
```

### Step 2: Navigate to Project

```bash
cd srpprivatetradedailybot
ls -la
```

### Step 3: Create Environment File

```bash
# Create .env file
nano .env

# Add your credentials:
DELTA_API_KEY=your_actual_api_key_here
DELTA_API_SECRET=your_actual_api_secret_here

# Save: Ctrl+O, Enter, Ctrl+X
```

**⚠️ IMPORTANT:** Never commit `.env` to git! (Already in .gitignore)

### Step 4: Configure Bot

```bash
# Copy example config
cp config.example.yaml config.yaml

# Edit configuration
nano config.yaml

# Verify 4h timeframe settings:
# - timeframe: "4h"
# - timezone: "Asia/Kolkata"
# - wait_for_next_candle: true
# - startup_delay_minutes: 5
```

### Step 5: Setup Dependencies

```bash
# Run setup script
./setup.sh

# Answer prompts:
# - Install UV: y (if not already installed)
# - Run tests: y (recommended)
```

---

## Running the Bot

### Option 1: Foreground (Testing)

**For testing only:**
```bash
./start_bot.sh
# Press Ctrl+C to stop
```

### Option 2: Background with screen (Recommended)

**Using screen (persistent sessions):**

```bash
# Install screen
sudo apt install -y screen

# Start new screen session
screen -S trading-bot

# Inside screen, start bot
./start_bot.sh

# Detach from screen: Ctrl+A, then D
# Your bot keeps running!

# Reattach to screen
screen -r trading-bot

# List all screens
screen -ls

# Kill screen session
screen -X -S trading-bot quit
```

### Option 3: Background with tmux

**Using tmux:**

```bash
# Install tmux
sudo apt install -y tmux

# Start new session
tmux new -s trading-bot

# Inside tmux, start bot
./start_bot.sh

# Detach: Ctrl+B, then D

# Reattach
tmux attach -t trading-bot

# Kill session
tmux kill-session -t trading-bot
```

### Option 4: Systemd Service (Production)

**Create systemd service:**

```bash
# Create service file
sudo nano /etc/systemd/system/trading-bot.service
```

**Add this content:**
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

**Enable and start service:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable trading-bot

# Start service
sudo systemctl start trading-bot

# Check status
sudo systemctl status trading-bot

# View logs
sudo journalctl -u trading-bot -f

# Stop service
sudo systemctl stop trading-bot

# Restart service
sudo systemctl restart trading-bot
```

---

## Monitoring & Maintenance

### Monitor Bot Logs

```bash
# Real-time log monitoring
tail -f ~/srpprivatetradedailybot/breakout_bot.log

# Last 100 lines
tail -n 100 ~/srpprivatetradedailybot/breakout_bot.log

# Search for errors
grep ERROR ~/srpprivatetradedailybot/breakout_bot.log

# Search for positions
grep "Position opened" ~/srpprivatetradedailybot/breakout_bot.log
```

### Check Bot Status

```bash
# Check if bot is running
ps aux | grep run_bot

# Check system resources
htop

# Check disk space
df -h

# Check memory
free -h
```

### Log Rotation

**Setup log rotation:**

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/trading-bot
```

**Add:**
```
/home/ubuntu/srpprivatetradedailybot/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 ubuntu ubuntu
}
```

### Backup Configuration

```bash
# Backup .env and config.yaml
cd ~/srpprivatetradedailybot
tar -czf backup-$(date +%Y%m%d).tar.gz .env config.yaml

# Download backup to local machine
# From local: scp -i your-key.pem ubuntu@YOUR_IP:~/backup-*.tar.gz ./
```

---

## Security Best Practices

### 1. SSH Security

```bash
# Change default SSH port (optional)
sudo nano /etc/ssh/sshd_config
# Change: Port 2222
sudo systemctl restart ssh

# Disable password authentication
# In /etc/ssh/sshd_config:
# PasswordAuthentication no
```

### 2. Firewall Setup

```bash
# Install UFW
sudo apt install -y ufw

# Allow SSH (change port if modified)
sudo ufw allow 22/tcp

# Allow outbound HTTPS
sudo ufw allow out 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 3. File Permissions

```bash
# Secure .env file
chmod 600 .env

# Secure SSH keys
chmod 400 ~/.ssh/*
```

### 4. Auto Updates

```bash
# Enable automatic security updates
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 5. API IP Whitelisting

**On Delta Exchange:**
1. Go to API settings
2. Add your EC2 Elastic IP to whitelist
3. Save changes

---

## Troubleshooting

### Bot Won't Start

**Check logs:**
```bash
tail -50 breakout_bot.log
```

**Common issues:**
- API credentials incorrect → Check `.env`
- IP not whitelisted → Add EC2 IP to Delta Exchange
- Dependencies missing → Run `./setup.sh`

### Network Issues

**Test API connectivity:**
```bash
curl https://api.india.delta.exchange/v2/tickers/BTCUSD
```

**Check DNS:**
```bash
nslookup api.india.delta.exchange
```

### Out of Memory

**Check memory:**
```bash
free -h
```

**Add swap (if needed):**
```bash
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Bot Crashed

**Check if running:**
```bash
ps aux | grep run_bot
```

**Restart:**
```bash
# If using screen
screen -r trading-bot
# Press Ctrl+C, then restart
./start_bot.sh

# If using systemd
sudo systemctl restart trading-bot
```

### Disk Space Full

**Check disk usage:**
```bash
df -h
du -sh ~/srpprivatetradedailybot/*
```

**Clean old logs:**
```bash
cd ~/srpprivatetradedailybot
rm *.log.1 *.log.2
```

---

## Updates & Maintenance

### Update Bot Code

```bash
# Stop bot
./stop_bot.sh

# Pull latest changes
git pull origin main

# Update dependencies
uv sync

# Run tests
./start_tests.sh

# Restart bot
./start_bot.sh
```

### Regular Maintenance

**Weekly:**
- ✅ Check logs for errors
- ✅ Verify bot is running
- ✅ Check trading performance

**Monthly:**
- ✅ Update system packages
- ✅ Review and rotate logs
- ✅ Backup configuration

---

## Cost Optimization

### Free Tier

**First 12 months:**
- t3.micro: 750 hours/month (FREE)
- 30 GB storage (FREE)

### After Free Tier

**t3.micro:** ~$7-8/month
**t3.small:** ~$15/month

**Savings tips:**
- Use spot instances (risky for trading!)
- Stop instance when not trading
- Use Reserved Instances for commitment

---

## Quick Reference

### Essential Commands

```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@YOUR_IP

# Start bot
./start_bot.sh

# Stop bot
./stop_bot.sh

# View logs
tail -f breakout_bot.log

# Check status
ps aux | grep run_bot

# Screen commands
screen -S trading-bot  # Create
Ctrl+A, D              # Detach
screen -r trading-bot  # Reattach
screen -ls             # List all
```

---

## Emergency Procedures

### Stop All Trading

```bash
# Stop bot
./stop_bot.sh

# Or kill process
pkill -f run_bot.py

# Cancel all orders via Delta Exchange dashboard
```

### Access Issues

```bash
# If locked out, use AWS Console
# 1. Go to EC2 → Connect → Session Manager
# 2. Or use EC2 Instance Connect
```

---

## Deployment Checklist

- [ ] EC2 instance launched
- [ ] Elastic IP allocated
- [ ] Security group configured
- [ ] SSH key saved securely
- [ ] System updated
- [ ] Python 3.12 installed
- [ ] UV installed
- [ ] Repository cloned
- [ ] .env file created with API credentials
- [ ] config.yaml configured
- [ ] Dependencies installed (setup.sh)
- [ ] Tests passed
- [ ] IP whitelisted on Delta Exchange
- [ ] Bot started successfully
- [ ] Logs monitoring setup
- [ ] Backup created

---

## Support

**Issues?**
1. Check logs: `tail -f breakout_bot.log`
2. Review this guide
3. Check AWS CloudWatch
4. Test API connectivity

---

**Created:** October 19, 2025  
**Status:** Production Ready ✅  
**Instance Type:** t3.micro recommended  
**OS:** Ubuntu 22.04 LTS  
**Cost:** ~$7-8/month (after free tier)

---

**Happy Trading on AWS! 🚀☁️📈**

