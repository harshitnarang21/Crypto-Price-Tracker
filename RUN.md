# 🚀 Quick Run Guide - Mac Terminal Commands

## First Time Setup (One-time only)

```bash
# Navigate to project directory
cd ~/Desktop/crypto-tracker

# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt
```

## Running the Application

### Option 1: Simple Run (Recommended)

```bash
# Navigate to project directory
cd ~/Desktop/crypto-tracker

# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
```

### Option 2: One-Line Command

```bash
cd ~/Desktop/crypto-tracker && source venv/bin/activate && python main.py
```

### Option 3: Create an Alias (Optional - for convenience)

Add this to your `~/.zshrc` or `~/.bash_profile`:

```bash
alias cryptotracker='cd ~/Desktop/crypto-tracker && source venv/bin/activate && python main.py'
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

Now you can just run:
```bash
cryptotracker
```

## Daily Usage Commands

Once everything is set up, you only need these two commands:

```bash
cd ~/Desktop/crypto-tracker
source venv/bin/activate && python main.py
```

## Exiting the Application

- Press `7` in the menu to exit gracefully
- Or press `Ctrl+C` to force quit

## Deactivating Virtual Environment

When you're done, you can deactivate the virtual environment:

```bash
deactivate
```

## Troubleshooting Commands

### If dependencies are missing:
```bash
cd ~/Desktop/crypto-tracker
source venv/bin/activate
pip install -r requirements.txt
```

### If virtual environment is corrupted:
```bash
cd ~/Desktop/crypto-tracker
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Check if everything is installed correctly:
```bash
cd ~/Desktop/crypto-tracker
source venv/bin/activate
python -c "import requests, pandas, numpy, sklearn, matplotlib, colorama; print('✅ All dependencies installed!')"
```

## Quick Reference

| Task | Command |
|------|---------|
| Go to project | `cd ~/Desktop/crypto-tracker` |
| Activate venv | `source venv/bin/activate` |
| Run app | `python main.py` |
| Install deps | `pip install -r requirements.txt` |
| Deactivate venv | `deactivate` |

