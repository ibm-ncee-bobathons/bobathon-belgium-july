# Lab 2: Build Agentic Workflows with IBM Bob and watsonx Orchestrate

## Overview

This lab demonstrates how to use **IBM Bob** as an AI development partner to programmatically build and deploy agentic workflows on **watsonx Orchestrate**. You'll create an automated invoice-processing agent that extracts structured data from documents without manual coding.

### What You'll Build

An **Expense Report Agent** that:
- Accepts uploaded invoice documents (PDF/images)
- Extracts structured data using AI-powered document processing
- Validates outputs against a key-value pair (KVP) schema
- Returns formatted JSON results

### Key Technologies

- **IBM Bob**: AI-powered development assistant
- **watsonx Orchestrate (wxO)**: Enterprise agentic AI platform
- **wxO Agent Development Kit (ADK)**: Pro-code development tools
- **Model Context Protocol (MCP)**: Enables Bob to access wxO tools and documentation

## Learning Objectives

By completing this lab, you will:

1. Configure Bob with watsonx Orchestrate MCP servers
2. Create Bob rules for development best practices
3. Use Bob's Plan mode to design agent architecture
4. Generate complete agent implementations using Bob's Advanced mode
5. Deploy agentic workflows and agents to watsonx Orchestrate
6. Test and verify agent functionality

## Architecture

The invoice processing workflow follows this flow:

```
User Upload → Expense Report Agent → Invoice Processing Flow → 
Extract Structured Data → Validate with KVP Schema → Return JSON Output
```

**Key Components:**
- **LLM Model**: `groq/openai/gpt-oss-120b`
- **Processing**: Document processing with KVP schema validation
- **Output**: Structured JSON with invoice details

**Extracted Fields:**
- Invoice Information (date, transaction mode)
- Airline/Passenger Information (name, ticket, flight details)
- Hotel Information (name, customer, city)
- Fee Information (base fare, charges, taxes, total, currency)

## Prerequisites

**⚠️ Important**: Complete these setup guides before starting this lab:

### Access Options

Choose the option that applies to you:

#### Option 1: Self-Paced Learning (Free Trial)

For individual learners using the watsonx Orchestrate free trial:

1. **[Environment Setup Guide](Prerequisites/environment-setup.md)** (~30-45 min)
   - ✅ Python 3.11+ installed
   - ✅ IBM Bob IDE extension installed in VS Code
   - ✅ watsonx Orchestrate ADK installed
   - ✅ MCP servers configured

2. **[watsonx Orchestrate Free Trial Signup](Prerequisites/watsonx-orchestrate-signup.md)** (~10-15 min)
   - ✅ Free trial account created
   - ✅ watsonx Orchestrate instance provisioned
   - ✅ API credentials generated
   - ✅ ADK environment configured and activated

**👉 [Start with Prerequisites →](Prerequisites/)**

#### Option 2: Using TechZone (Alternative)

If the free trial isn't available in your region or doesn't work for you:

**Prerequisites:**
1. **[Create Your IBMid First](ibmid-registration.md)** (~5 min) - **Required before instructor can provide access**
   - ✅ IBMid created and verified
   - ✅ Email address confirmed
   - ✅ Ready to receive TechZone details

**Then:**
2. **Provide your IBMid to your instructor**
   - Share your IBMid (email address) with the instructor
   - Instructor will provision TechZone environment for you

3. **Receive TechZone details from instructor**
   - Environment URL and access credentials
   - Connection instructions
   - Workshop-specific setup guidance

4. **Follow instructor-provided instructions** to access your TechZone environment

**👉 [IBMid Registration Guide →](ibmid-registration.md)**

> **Important**: You MUST create your IBMid BEFORE the instructor can provide TechZone access. IBM employees already have an IBMid and can skip step 1.

### Quick Verification

Before proceeding, verify your setup:

```bash
# Check Python version
python --version  # Should be 3.11+

# Check ADK installation
orchestrate --version

# Check active environment
orchestrate env info
```

## Lab Structure

### Files Included

- **wxo-bob-lab.md**: Complete step-by-step tutorial (336 lines)
- **images/**: 29 screenshots documenting each step
  - Architecture diagrams (01-03)
  - Configuration examples (04-05)
  - Bob interaction screenshots (06-22)
  - Deployment and verification (23-29)

### Tutorial Sections

1. **Overview**: Introduction to watsonx Orchestrate and agent development
2. **Architecture**: System design and workflow explanation
3. **Prerequisites**: Required setup and tools
4. **MCP Configuration**: Connect Bob to wxO servers (optional)
5. **Bob Rules**: Create development best practices
6. **Plan Creation**: Design agent architecture with Bob
7. **Implementation**: Generate code and configuration
8. **Deployment**: Import workflow and agent to wxO
9. **Verification**: Test the agent functionality
10. **Summary**: Review completed tasks and next steps

## Key Concepts

### Bob Modes

- **Plan Mode**: Create implementation plans and architecture designs
- **Advanced Mode**: Access MCP servers for code generation
- **Ask Mode**: Query Bob for information and diagrams

### Development Approach

This lab uses a **pro-code approach** with the wxO ADK, offering:
- Complete control over agent behavior
- Repeatable, version-controlled deployments
- Production-ready code generation
- Integration with CI/CD pipelines

### Bob Rules

Bob rules ensure consistent development practices:
- **wxo-implementation-guide.md**: Comprehensive reference (root directory)
- **.bob/rules/wxo-development.md**: Always-on concise rules

## Expected Outcomes

After completing this lab, you will have:

✅ A fully functional expense report agent deployed to watsonx Orchestrate  
✅ A document processing flow with KVP schema validation  
✅ Deployment scripts for automated imports  
✅ Test scripts for programmatic verification  
✅ Complete documentation with architecture diagrams  

## Time Estimate

- **Setup**: 15-20 minutes
- **Implementation**: 30-40 minutes
- **Testing**: 10-15 minutes
- **Total**: ~60-75 minutes

## Tips for Success

1. **Be Specific**: Provide clear, detailed prompts to Bob
2. **Review Code**: Always review Bob's generated code before approval
3. **Use Checkpoints**: Bob creates rollback points during implementation
4. **Follow Best Practices**: Let Bob rules guide the development process
5. **Test Thoroughly**: Verify agent functionality with sample invoices

## Related Resources

- [Using IBM Bob to build watsonx Orchestrate agents and MCP tools](https://developer.ibm.com/tutorials/build-agents-mcp-tools-watsonx-orchestrate-using-bob/)
- [Beginner's guide to multi-agent orchestration with watsonx Orchestrate](https://developer.ibm.com/articles/multi-agent-orchestration-watsonx-orchestrate/)
- [Try watsonx Orchestrate free trial](https://www.ibm.com/account/reg/us-en/signup?formid=urx-52753)
- [watsonx Orchestrate ADK Documentation](https://developer.watson-orchestrate.ibm.com)

## Authors

- Allen Chan
- Ahmed Azraq
- Syeda Ameena Begum

**Published**: February 9, 2026  
**Source**: [IBM Developer](https://developer.ibm.com/tutorials/build-programmatic-agentic-workflows-watsonx-orchestrate-bob/)

---

## Getting Started

To begin this lab, open **[wxo-bob-lab.md](wxo-bob-lab.md)** and follow the step-by-step instructions. Each section includes detailed explanations and screenshots to guide you through the process.

**[🚀 Start the Lab Now →](wxo-bob-lab.md)**

**Happy Building! 🚀**