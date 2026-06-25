# Environment Setup Guide

Complete guide for setting up your development environment for IBM Bob and watsonx Orchestrate labs.

## Table of Contents

1. [Overview](#overview)
2. [Install Python 3.11+](#install-python-311)
3. [Install IBM Bob IDE](#install-ibm-bob-ide)
4. [Install watsonx Orchestrate ADK](#install-watsonx-orchestrate-adk)
5. [Configure MCP Servers](#configure-mcp-servers)
6. [Verify Installation](#verify-installation)

---

## Overview

This guide walks you through setting up all required tools for the Bobathon Hungary Labs. You'll install:

- **Python 3.11+**: Required runtime for the watsonx Orchestrate ADK
- **IBM Bob IDE**: AI-powered development assistant
- **watsonx Orchestrate ADK**: Agent Development Kit for building AI agents
- **MCP Servers**: Model Context Protocol servers for Bob integration

**Estimated Time**: 30-45 minutes

---

## Install Python 3.11+

The watsonx Orchestrate ADK requires Python 3.11 or later.

### Check Current Version

```bash
python --version
```

If you have Python 3.11 or later, skip to the [next section](#install-ibm-bob-ide).

### Windows

1. Download the installer from the [official Python website](https://www.python.org/downloads/)
2. Run the setup
3. **Important**: Enable "Add Python to PATH" during installation
4. The installer includes `pip` package manager

**Alternative**: Use a Python version manager like [uv](https://github.com/astral-sh/uv) or [pyenv](https://github.com/pyenv/pyenv)

### macOS

Python usually comes pre-installed. To install a newer version:

**Using Homebrew** (recommended):

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11
```

**Alternative**: Use [uv](https://github.com/astral-sh/uv) or [pyenv](https://github.com/pyenv/pyenv)

### Linux

**Ubuntu/Debian**:

```bash
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip
```

**Fedora**:

```bash
sudo dnf update -y
sudo dnf install -y python3 python3-pip
```

**Arch Linux**:

```bash
sudo pacman -Syu
sudo pacman -S python python-pip
```

**Using uv** (if distribution packages are outdated):

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version

# Install Python 3.11
uv python install 3.11

# Verify Python version
uv python list
```

**Using pyenv**:

```bash
# Install pyenv dependencies first (Ubuntu/Debian)
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

# Install pyenv
curl -fsSL https://pyenv.run | bash

# Add to ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

# Restart shell
exec "$SHELL"

# Install Python 3.11
pyenv install 3.11
pyenv global 3.11

# Verify
python --version
```

---

## Install IBM Bob IDE

IBM Bob is an AI-powered development assistant.

### Installation Steps

1. **Visit**: [https://bob.ibm.com/trial](https://bob.ibm.com/trial)
2. **Sign in** with your IBM ID
3. **Download** the Bob installer for your operating system
4. **Install** the application following the on-screen instructions
5. **Launch** IBM Bob and sign in

### Verify Bob Installation

- Launch the IBM Bob application
- Sign in with your IBM ID
- You should see the Bob chat interface
- Try asking Bob a simple question to test functionality

---

## Install watsonx Orchestrate ADK

The Agent Development Kit (ADK) provides CLI tools for building and deploying agents.

**📄 For detailed ADK installation instructions, please refer to:**

**[env_setup_instructions.md](../env_setup_instructions.md)**

This Markdown file contains the complete, authoritative guide for installing and configuring the watsonx Orchestrate ADK.

### Quick Verification

After following the Markdown file instructions, verify your installation:

```bash
orchestrate --version
```

You should see the ADK version number.

---

## Configure MCP Servers

Model Context Protocol (MCP) servers enable Bob to access watsonx Orchestrate documentation and tools.

**📄 For detailed MCP server configuration instructions, please refer to:**

**[env_setup_instructions.md](../env_setup_instructions.md)**

This file contains the complete, authoritative guide for configuring MCP servers for Bob integration.

---

## Verify Installation

### 1. Check Python Version

```bash
python --version
# Expected: Python 3.11.x or higher
```

### 2. Check ADK Installation

```bash
orchestrate --version
# Expected: Version number (e.g., 1.15.0)
```

### 3. Check Bob Integration

1. Open VS Code
2. Click the Bob icon in the sidebar
3. Start a new chat
4. Ask Bob: "Can you access watsonx Orchestrate documentation?"
5. Bob should confirm access to MCP servers

### 4. Test MCP Servers

In Bob, try asking:
```
Search the watsonx Orchestrate documentation for "agent development"
```

Bob should be able to query the documentation through the MCP server.

---

## Troubleshooting

### Python Not Found

**Issue**: `python: command not found`

**Solution**:
- Ensure Python is in your PATH
- Try `python3` instead of `python`
- Reinstall Python with PATH option enabled

### ADK Installation Fails

**Issue**: `pip install ibm-watsonx-orchestrate` fails

**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Try installing again
pip install ibm-watsonx-orchestrate
```

### MCP Servers Not Working

**Issue**: Bob can't access MCP servers

**Solution**:
1. Verify `mcp.json` is in the `.bob` folder
2. Check that the path in `WXO_MCP_WORKING_DIRECTORY` is absolute (not relative)
3. Ensure `uvx` is installed: `uvx --version`
4. Restart VS Code completely
5. Check Bob's output panel for error messages

### uvx Not Found

**Issue**: `uvx: command not found`

**Solution**:
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload shell
source ~/.bashrc  # or ~/.zshrc on macOS
```

---

## Next Steps

Once your environment is set up:

1. ✅ Complete the [watsonx Orchestrate Signup Guide](watsonx-orchestrate-signup.md)
2. ✅ Start [Lab 2: Build Agentic Workflows](../Lab2%20-%20watsonx%20Orchestrate%20/)

---

## Additional Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [watsonx Orchestrate ADK Documentation](https://developer.watson-orchestrate.ibm.com)
- [IBM Bob Documentation](https://www.ibm.com/products/bob)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [uv Documentation](https://docs.astral.sh/uv/)

---

**Need Help?** If you encounter issues not covered here, please refer to the official documentation or contact IBM Support.