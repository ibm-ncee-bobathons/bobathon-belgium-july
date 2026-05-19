# Prerequisites

Essential setup guides for IBM Bobathon Amsterdam Labs.

## Overview

Before starting any lab, complete these prerequisite steps to set up your development environment and access to IBM watsonx Orchestrate.

## Setup Guides

### 1. [Environment Setup Guide](environment-setup.md)

**What You'll Install:**
- Python 3.11+
- IBM Bob IDE (VS Code extension)
- watsonx Orchestrate ADK
- MCP Servers for Bob integration

**Time Required**: 30-45 minutes

**Start Here**: [environment-setup.md](environment-setup.md)

---

### 2. [watsonx Orchestrate Signup Guide](watsonx-orchestrate-signup.md)

**What You'll Configure:**
- watsonx Orchestrate free trial account
- watsonx Orchestrate service instance
- API credentials
- ADK environment connection

**Time Required**: 15-20 minutes

**Prerequisites**: Complete Environment Setup first

**Start Here**: [watsonx-orchestrate-signup.md](watsonx-orchestrate-signup.md)

---

## Quick Start Checklist

Use this checklist to track your setup progress:

- [ ] Python 3.11+ installed and verified
- [ ] IBM Bob IDE extension installed in VS Code
- [ ] watsonx Orchestrate ADK installed (`orchestrate --version` works)
- [ ] MCP servers configured in `.bob/mcp.json`
- [ ] watsonx Orchestrate free trial account created
- [ ] watsonx Orchestrate service provisioned
- [ ] API credentials generated and saved securely
- [ ] ADK environment configured and activated
- [ ] Connection verified with `orchestrate env info`

---

## Setup Order

Follow these guides in order:

1. **First**: [Environment Setup](environment-setup.md)
   - Install all required software
   - Configure Bob and MCP servers

2. **Second**: [watsonx Orchestrate Signup](watsonx-orchestrate-signup.md)
   - Create watsonx Orchestrate free trial account
   - Provision service
   - Configure credentials

3. **Then**: Start the labs!
   - [Lab 2: Build Agentic Workflows](../Lab2%20-%20watsonx%20Orchestrate%20/)

---

## System Requirements

### Minimum Requirements

- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+, Fedora 35+, etc.)
- **RAM**: 8 GB minimum, 16 GB recommended
- **Disk Space**: 5 GB free space
- **Internet**: Stable broadband connection
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

### Software Requirements

- **Python**: 3.11 or later
- **VS Code**: Latest version
- **Git**: For cloning repositories (optional but recommended)
- **Terminal**: Command-line access

---

## Troubleshooting

### Common Issues

**Issue**: Python version too old

**Solution**: Follow the Python installation steps in [Environment Setup](environment-setup.md#install-python-311)

---

**Issue**: Bob can't access MCP servers

**Solution**: 
1. Verify `.bob/mcp.json` exists and is properly formatted
2. Check that `uvx` is installed
3. Restart VS Code
4. See [MCP Configuration](environment-setup.md#configure-mcp-servers)

---

**Issue**: ADK can't connect to watsonx Orchestrate

**Solution**:
1. Verify API key is correct
2. Check service instance URL
3. Ensure service is provisioned and running
4. See [Troubleshooting Guide](watsonx-orchestrate-signup.md#troubleshooting)

---

## Getting Help

If you encounter issues:

1. **Check the Troubleshooting sections** in each guide
2. **Review the official documentation**:
   - [watsonx Orchestrate ADK Docs](https://developer.watson-orchestrate.ibm.com)
   - [IBM Bob Documentation](https://www.ibm.com/products/bob)
3. **Contact IBM Support** for service-related issues
4. **Check IBM Developer** for tutorials and community support

---

## Additional Resources

### Documentation

- [watsonx Orchestrate Product Page](https://www.ibm.com/products/watsonx-orchestrate)
- [IBM Cloud Documentation](https://cloud.ibm.com/docs)
- [Python Documentation](https://docs.python.org/3/)
- [VS Code Documentation](https://code.visualstudio.com/docs)

### Tutorials

- [IBM Developer Tutorials](https://developer.ibm.com/tutorials/)
- [watsonx Orchestrate Getting Started](https://developer.watson-orchestrate.ibm.com/getting_started/what_is)
- [Building Your First Agent](https://developer.watson-orchestrate.ibm.com/tutorials/first_agent)

### Community

- [IBM Developer Community](https://developer.ibm.com/community/)
- [Stack Overflow - IBM watsonx](https://stackoverflow.com/questions/tagged/ibm-watsonx)

---

## Next Steps

Once you've completed both setup guides:

✅ **You're ready to start the lab!**

🚀 [Begin Lab 2: Build Agentic Workflows with watsonx Orchestrate](../)

---

**Happy Learning!** 🎓