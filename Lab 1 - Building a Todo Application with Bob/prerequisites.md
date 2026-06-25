# Prerequisites for Lab 1: Building a Todo Application with Bob

Before starting Lab 1, ensure you have all the necessary tools and accounts set up. This guide will help you verify your environment and complete any missing setup steps.

## Required Software

### 1. Python 3.8 or Higher

Python is required for the Flask backend.

**Check if installed:**
```bash
python --version
# or
python3 --version
```

**Installation:**
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: 
  ```bash
  brew install python3
  ```
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip python3-venv
  ```

**Verify pip is installed:**
```bash
pip --version
# or
pip3 --version
```

### 2. Node.js 14 or Higher

Node.js and npm are needed for package management (though this lab primarily uses vanilla JavaScript).

**Check if installed:**
```bash
node --version
npm --version
```

**Installation:**
- **Windows/macOS/Linux**: Download from [nodejs.org](https://nodejs.org/)
- **macOS (using Homebrew)**:
  ```bash
  brew install node
  ```
- **Linux (Ubuntu/Debian)**:
  ```bash
  curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
  sudo apt-get install -y nodejs
  ```

### 3. Git

Git is required for version control and GitHub integration.

**Check if installed:**
```bash
git --version
```

**Installation:**
- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win)
- **macOS**:
  ```bash
  brew install git
  ```
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install git
  ```

**Configure Git (if not already done):**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4. Bob AI Assistant

Bob must be installed and running in your development environment.

**Installation:**
- Follow the Bob installation guide for your platform
- Ensure Bob is properly configured with API keys
- Verify Bob is accessible in your IDE/editor

**Verify Bob is running:**
- Open your IDE/editor
- Look for Bob's interface
- Try switching between Bob's modes (Plan, Code, Ask, Advanced)

## Required Accounts

### GitHub Account

A GitHub account is required for the MCP integration section of the lab.

**Setup:**
1. Create an account at [github.com](https://github.com/) if you don't have one
2. Verify your email address
3. Set up two-factor authentication (recommended)

**Generate Personal Access Token (for MCP):**
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "Bob MCP Integration")
4. Select scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. **Important**: Copy the token immediately and store it securely
7. Configure the token in Bob's MCP settings

## Verification Checklist

Before starting the lab, verify all prerequisites:

- [ ] **Python 3.8+**: Run `python --version` or `python3 --version`
- [ ] **pip installed**: Run `pip --version` or `pip3 --version`
- [ ] **Virtual environment support**: Run `python3 -m venv --help`
- [ ] **Node.js 14+**: Run `node --version`
- [ ] **npm installed**: Run `npm --version`
- [ ] **Git installed**: Run `git --version`
- [ ] **Git configured**: Run `git config --global user.name` and `git config --global user.email`
- [ ] **Bob installed**: Verify Bob is accessible in your IDE
- [ ] **Bob modes available**: Can switch between Plan, Code, Ask, and Advanced modes
- [ ] **GitHub account**: Can log in to github.com
- [ ] **GitHub token**: Personal access token generated and stored securely
- [ ] **Text editor**: IDE or editor is installed and working
- [ ] **Terminal access**: Can open and use command line/terminal
- [ ] **Internet connection**: Stable connection for API calls and package downloads

## Optional but Recommended

### Browser Developer Tools

Familiarity with browser developer tools will help during frontend testing.

**Access developer tools:**
- **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I` (Windows/Linux) / `Cmd+Option+I` (macOS)
- **Firefox**: Press `F12` or `Ctrl+Shift+I` (Windows/Linux) / `Cmd+Option+I` (macOS)
- **Safari**: Enable in Preferences → Advanced → Show Develop menu, then press `Cmd+Option+I`

### Python Virtual Environment Knowledge

Understanding virtual environments will help you manage dependencies.

**Quick reference:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Deactivate
deactivate
```

### Basic Command Line Skills

You should be comfortable with:
- Navigating directories (`cd`, `ls`/`dir`)
- Running commands
- Reading command output
- Stopping running processes (`Ctrl+C`)

## Troubleshooting Common Issues

### Python not found
- Ensure Python is in your system PATH
- Try using `python3` instead of `python`
- Restart your terminal after installation

### pip not found
- Python 3.4+ includes pip by default
- If missing, install with: `python3 -m ensurepip --upgrade`

### Git authentication issues
- Use HTTPS with personal access token instead of password
- Or set up SSH keys for GitHub

### Bob not responding
- Check Bob's API key configuration
- Verify internet connection
- Restart Bob or your IDE
- Check Bob's documentation for troubleshooting

### Port already in use (5000)
- Another application is using port 5000
- Kill the process or use a different port
- On macOS, AirPlay Receiver often uses port 5000 (disable in System Preferences)

## Getting Help

If you encounter issues during setup:

1. **Check official documentation**:
   - [Python Documentation](https://docs.python.org/)
   - [Node.js Documentation](https://nodejs.org/docs/)
   - [Git Documentation](https://git-scm.com/doc)
   - [Bob Documentation](https://bob.ibm.com/docs/ide)

2. **Search for error messages**: Copy the exact error message and search online

3. **Ask Bob**: Use Bob's Ask mode to get help with setup issues

4. **Lab instructor**: Reach out to your lab instructor or facilitator

## Ready to Start?

Once you've completed all items in the verification checklist, you're ready to begin Lab 1!

**Next step**: [Start Lab 1: Building a Todo Application with Bob](./README.md)

---

**Last Updated**: February 2026