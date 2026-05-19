# Build agentic workflows with watsonx Orchestrate and IBM Bob

*A hands-on guide to automate invoice processing with AI-powered workflows using IBM Bob to generate code, tools, and configuration for watsonx Orchestrate*

**By** Allen Chan, Ahmed Azraq, Syeda Ameena Begum  
**Published:** 09 February 2026 · IBM Developer  
**Source:** [developer.ibm.com](https://developer.ibm.com/tutorials/build-programmatic-agentic-workflows-watsonx-orchestrate-bob/)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Step 1 – Configure Access to watsonx Orchestrate MCP Servers](#step-1--configure-access-to-watsonx-orchestrate-mcp-servers)
- [Step 2 – Install the watsonx Orchestrate ADK Extension](#step-2--install-the-watsonx-orchestrate-adk-extension)
- [Step 3 – Create a Bob Rule for watsonx Orchestrate Development Best Practices](#step-3--create-a-bob-rule-for-watsonx-orchestrate-development-best-practices)
- [Step 4 – Create the Implementation Plan and Agent Design](#step-4--create-the-implementation-plan-and-agent-design)
- [Step 5 – Implement the Agent and the Agentic Workflow](#step-5--implement-the-agent-and-the-agentic-workflow)
- [Step 6 – Deploy the Agentic Workflow and the Agent](#step-6--deploy-the-agentic-workflow-and-the-agent)
- [Step 7 – Verify the Agent in watsonx Orchestrate](#step-7--verify-the-agent-in-watsonx-orchestrate)
- [Summary and Next Steps](#summary-and-next-steps)

---

## Overview

Building intelligent, automation-ready agentic workflows often means connecting together tools, schemas, and logic across multiple systems. That work can be powerful, but it also becomes repetitive and slow. This tutorial shows you how to use **IBM Bob** as your AI development partner to remove that friction and help you build a fully programmatic agentic workflow for watsonx Orchestrate.

You use IBM Bob to generate the complete project structure in code. Bob creates the extraction schema, builds a multi-step document processing workflow, validates outputs, and assembles a native agent that uses the Groq GPT-OSS 120B model. You also deploy the agent and agentic workflow using the watsonx Orchestrate Agent Development Kit (ADK).

In this tutorial, you learn how agentic workflows support structured reasoning, tool orchestration, and automated decision making. You also see how these capabilities apply to enterprise-grade document-processing scenarios such as extracting structured fields from airline invoices.

![watsonx Orchestrate – Open Agentic Framework](images/01-architecture-diagram.png)

IBM watsonx Orchestrate (wxO) is an open and hybrid enterprise platform for agentic AI. It offers first-class multi-agent orchestration capabilities, integrated end-to-end security and governance, and observability capabilities for AI agents.

![Agent development modes overview](images/02-architecture-table.png)

The platform also offers multiple agent development tools: a low-code agent builder, pro-code development using the wxO Agent Development Kit (ADK), and integrated Langflow AI Builder.

Instead of configuring components in the UI, developers can use the ADK to code all components, including agentic workflows — combining document processing, validation rules, schemas, and deployment steps in a repeatable, production-ready way.

---

## Architecture

You build an agentic workflow that extracts structured data from airline invoices. This workflow removes manual data entry and improves processing efficiency.

The following figure created using Bob shows this architecture:

![Invoice processing agentic workflow – architecture diagram](images/03-architecture-flow.png)

1. The user uploads an invoice document as a PDF or image file.
2. The **expense_report_agent** on watsonx Orchestrate receives the document and starts the processing workflow, and it uses `groq/openai/gpt-oss-120b` as an LLM for the agent reasoning.
3. The **Invoice Processing Flow** retrieves the key-value pair (KVP) schema.
4. The KVP schema returns the list of fields that the system must extract.
5. The **Extract Structured Data** component processes the invoice using the schema.
6. The **Structured JSON Output** contains all extracted invoice data.
7. The agent sends the formatted results to the user, and the agentic workflow can continue to process the expense.

---

## Prerequisites

- **IBM Bob installed.** Sign up for [IBM Bob free trial](https://bob.ibm.com/trial).
- **Python version 3.12, or later** installed on your system.
- **uv installed.** See [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).
- **watsonx Orchestrate access.** Complete the [wxO – Bob environment setup guide](Prerequisites/environment-setup.md) to prepare your environment.

---

## Step 1 – Configure Access to watsonx Orchestrate MCP Servers

> **Note:** If you have already completed the [env setup instructions.pdf](env%20setup%20instructions%20.pdf) guide, you can **skip this step** as your MCP servers are already configured.

Configure Bob to access the following watsonx Orchestrate MCP servers:

- **watsonx Orchestrate ADK Docs**: Provides a tool that queries the [watsonx Orchestrate ADK developer documentation](https://developer.watson-orchestrate.ibm.com/). This gives Bob the context that is needed to understand how all watsonx Orchestrate ADK features work.
- **watsonx Orchestrate ADK**: Give Bob direct access to all commands in the [watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com/). This allows Bob to create, import, or list agents, tools, MCP toolkits, knowledge bases, and connections. Bob can also export agents and Python tools into your workspace.

### Manual Configuration Approach

To configure access, complete the following steps:

1. Open the IBM Bob IDE.
2. Go to **File > Open Folder**.
3. Click **New Folder**, name the folder `wxo-agentic-workflow`, and then click **Open**.
4. Create a new folder named `.bob` to store all Bob-related configuration files.
5. Create a new file named `mcp.json` to store the MCP server settings, and enter your working directory in the `WXO_MCP_WORKING_DIRECTORY` field.

```json
{
  "mcpServers": {
    "watsonx-orchestrate-adk-docs": {
      "command": "uvx",
      "args": [
        "mcp-proxy",
        "--transport",
        "streamablehttp",
        "https://developer.watson-orchestrate.ibm.com/mcp"
      ]
    },
    "watsonx-orchestrate-adk": {
      "command": "uvx",
      "args": [
        "ibm-watsonx-orchestrate-mcp-server"
      ],
      "env": {
        "WXO_MCP_WORKING_DIRECTORY": "/absolute/path/to/project",
        "WXO_MCP_DEBUG": ""
      },
      "timeout": 300
    }
  }
}
```

![Bob IDE showing MCP server configuration in mcp.json file](images/04-mcp-json-config.png)

### Bob Marketplace Approach (Optional)

Alternatively, complete the following steps to configure Bob to access the watsonx Orchestrate MCP servers:

1. In the right pane, click **... > MCP Servers**.

2. Search for **watsonx Orchestrate**.

3. Click **Install** on **watsonx Orchestrate ADK Docs**. Choose the installation scope (current project or global), then click **Install**.

   > **Important:** Make sure Python and uv are installed in your system before you continue.

4. Click **Install** on **watsonx Orchestrate ADK**.
   - Set the installation scope to **Project**.
   - Set the installation method to **Latest ADK Version**.
   - Enter the absolute path of your project directory in **Current Project Working Directory**.
   - Click **Install**.

5. Both MCP servers must now be marked as healthy. Close the Settings page to continue.

---

## Step 2 – Install the watsonx Orchestrate ADK Extension

> **Note:** If you have already completed the [env setup instructions.pdf](env%20setup%20instructions%20.pdf) guide, you can **skip this step** as the ADK extension is already installed and configured.

Install the watsonx Orchestrate ADK extension that enables the development and deployment of agents and tools in Bob.

**Steps:**

1. Click **Manage** in the lower-left pane, then select **Extensions**.

2. Search for **watsonx Orchestrate ADK** and click **Install**.

3. Create a Python virtual environment:
   - Press **CMD+Shift+P** (Mac) or **Ctrl+Shift+P** (Windows/Linux).
   - Select **Python: Create Environment...**
   - Select **venv**.
   - Choose **Python 3.12**.
   - Rename the virtual environment folder from `.venv` to `venv`.

4. A new tile with watsonx logo appears in the left sidebar. Click the tile, then click **Initialize Workspace**.

![Initialize Workspace in the watsonx extension](images/18-initialize-workspace.png)

5. In the **Environment Manager**, configure access to your watsonx Orchestrate environment:
   - Click **Add +**
   - Enter a name for the environment
   - Provide the service instance URL for your watsonx Orchestrate environment
   - Click **Submit**

   > **Alternative:** You can use your local watsonx Orchestrate Developer Edition environment. Make sure your local Developer Edition environment is running before you activate it.

![Environment Manager showing active environment](images/19-environment-manager.png)

6. Select the environment and click **Activate**. Enter your API key when you are prompted.

   > **Tip:** You can store your credentials in a `.env` file for easier management. Copy the `.env.example` file to `.env` and fill in your actual values:
   > ```bash
   > cp .env.example .env
   > ```
   > Then edit `.env` with your watsonx Orchestrate API key and service URL.

![API key prompt](images/20-api-key-prompt.png)

7. When the environment becomes active, Bob shows all the agents and tools that exist in that environment.

---

## Step 3 – Create a Bob Rule for watsonx Orchestrate Development Best Practices

Create a Bob rule that captures best practices for development work with watsonx Orchestrate ADK. Bob rules apply across all Bob modes and ensures that Bob follows correct patterns when planning tasks, writing code, or using advanced features. This rule gives Bob:

- Clear semantics about watsonx Orchestrate agents
- Examples of correct ADK usage
- Standard flow patterns
- Expected CLI operations
- Constraints and rules specific to watsonx Orchestrate

This rule improves accuracy and keeps Bob aligned with approved ADK constructs.

This rule improves accuracy and keeps Bob aligned with approved ADK patterns. It provides a focused version of the implementation guidance without requiring Bob to process the full documentation, which adds unnecessary context. This smaller rule set gives Bob clearer guidance, supports consistent reasoning, and reduces the chance of incorrect output.

Using Bob rules that point to the implementation guide, together with the MCP documentation, gives Bob a stable foundation for planning and coding. The rules capture the best practices, patterns, and examples that Bob should follow across projects. The MCP documentation provides the official commands and configuration details when Bob needs exact syntax. This approach keeps Bob aligned with expected practices while still allowing it to request full documentation only when deeper technical details are needed. Using both together reduces confusion, lowers context load, and avoids incorrect assumptions.

The guidance is separated into two files: a reference guide and a rules file. [`wxo-implementation-guide.md`](wxo-implementation-guide.md) is a detailed implementation guide that Bob can request when more context is needed. You see an approval prompt when this happens. [`wxo-development.md`](.bob/rules/wxo-development.md) (saved in `.bob/rules/`) is a concise, always-on rule that Bob automatically applies across all modes. This rule has access to both the implementation guide and the watsonx Orchestrate documentation MCP server. This structure keeps the active rule context small while giving Bob access to complete, curated information whenever necessary.

| File | Purpose |
|------|---------|
| [`wxo-implementation-guide.md`](wxo-implementation-guide.md) (root) | Comprehensive reference guide Bob reads on demand |
| [`.bob/rules/wxo-development.md`](.bob/rules/wxo-development.md) | Concise always-on rule applied automatically across all modes |

**Steps:**

1. Save the [`wxo-implementation-guide.md`](wxo-implementation-guide.md) to the root directory of your workspace with the same name.

2. Create a `rules` directory in the `.bob` folder. This directory stores all rules that Bob must follow in this workspace.

3. Create a new file named [`wxo-development.md`](.bob/rules/wxo-development.md) in `.bob/rules/`. Copy and paste the content from GitHub to your `wxo-development.md` file and save it.

![wxo-development.md rule file in Bob IDE](images/05-bob-rule-wxo-development.png)

---

## Step 4 – Create the Implementation Plan and Agent Design

Provide Bob the agent requirements. Bob then creates the task plan and generates the agent architecture design.

In this step and the next step, you give Bob the prompts needed to create the implementation plan and the code. The quality of your prompts affects the quality of Bob's output. Be specific, use clear language, and include examples when you can. You can also use the prompt-enhancement feature to add more context and structure.

After Bob creates the implementation plan, review it carefully to ensure it matches your requirements, your expected functions, and your overall solution design.

> **Tip:** Be specific and clear in your prompts. Use the **enhance prompt** feature to improve your query with additional context and structure.

**Steps:**

1. Make sure you are in **Plan** mode, and keep **auto-approve turned off** so you can review each step and confirm that it matches your goals.

2. Provide Bob with the following agent requirements and instructions:

![Plan mode with agent requirements entered](images/06-plan-mode-prompt.png)

```text
Create a watsonx Orchestrate agent that will help a user create an expense report:

The agent will use a flow that:
1. Accept an uploaded document file
2. Extracts the expense fields below validated with KVP schema.
3. Return the output in structured JSON format

Required Fields to Extract:
  Invoice Information:
    - Invoice Date
    - Transaction Mode (e.g., Credit Card, Bank Transfer, Cash)
  Airline and Passenger Information (If airline invoice):
    - Airline Name / Passenger Name / Ticket Number / Ticket Date / Flight Details
  Hotel Information (If accommodation invoice):
    - Hotel Name / Customer Name / City
  Fee Information:
    - Base Fare / Charges / Taxes (with breakdown) / Total Amount / Currency
```

![Agent requirements submitted to Bob](images/07-bob-prompt-sent.png)

3. Based on the Bob rule, Bob requests access to read [`wxo-implementation-guide.md`](wxo-implementation-guide.md) so it can follow the best practices. Bob may also request access to other files if needed. Click **Approve**.

![Bob requests access to implementation guide](images/08-bob-approve-file.png)

4. Bob then requests access to [watsonx Orchestrate ADK documentation](https://developer.watson-orchestrate.ibm.com/) MCP server to gather more context. Bob shares the task list afterward. Review the task list and click **Approve**.

![Bob task list ready for approval](images/09-bob-task-list.png)

5. Bob may ask questions about the structure. Choose the answers that match the **simple approach**. Your questions may differ from the example, so select the options that fit this tutorial. For this tutorial, choose one flow, use the default models, include only the import script, and use the SaaS version.

![Bob clarification questions](images/10-bob-clarification.png)

6. Bob generates the implementation plan, the architecture design, and the workflow design. If Bob asks you to switch to code mode, **ignore the request** and continue to the next step.

![Bob implementation plan complete](images/11-bob-plan-complete.png)

7. Switch to **Ask** mode and ask Bob: *"Show me the workflow diagram"*. To view the Mermaid diagram, you may need to install the **Mermaid** extension.

![Expense Extraction Flow – workflow diagram](images/12-workflow-diagram.png)

---

## Step 5 – Implement the Agent and the Agentic Workflow

Ask Bob to generate the code and the configuration needed to build the agent. Bob creates an agent, creates the invoice processing flow, generates the OCR and extraction tools, defines the schemas and steps, and assembles the workflow according to watsonx Orchestrate implementation rules.

> **Important:** Make sure to review the generated code carefully to confirm that it matches your intended functions and your requirements.

**Steps:**

1. Switch to **Advanced** mode so that Bob can access the two watsonx Orchestrate MCP servers.

2. Give Bob the instructions to create the agent, then review the plan and click **Approve**.

![Advanced mode – implementation plan approved](images/13-advanced-mode-implement.png)

```text
Implement the approved plan and follow the below instructions:

Requirements:
  1. Create a native agent with this specific LLM model: groq/openai/gpt-oss-120b
  2. Build a document processing flow using docproc node.
  3. Define a KVP schema for the fields I need to extract.
  4. For simplicity include the KVP schema inline in the flow file.
  5. Ensure all imports are relative (using dot notation).

Important Implementation Details:
  - Use plain functions for schema helpers (no @tool decorator).
  - Use relative imports in all Python files.
  - Keep the flow simple with just a docproc node.
  - Use native agent type for better document handling.
  - Use JSON output format (not file reference).
```

3. Bob creates checkpoints so that you can roll back to earlier versions if needed. Bob then creates the flow. Review the code and continue.

![Bob creates the expense extraction flow](images/14-bob-creates-flow.png)

4. Bob creates the agent YAML file with the agent configuration.

![Bob creates agent YAML configuration](images/15-bob-creates-agent-yaml.png)

5. Bob creates a script to import the workflow and the agent to watsonx Orchestrate.

![Bob creates the import-all.sh deployment script](images/16-bob-creates-import-script.png)

6. Bob creates a test script and documentation.

![Bob creates test script and README documentation](images/17-bob-creates-docs.png)

7. Bob verifies and confirms that the implementation is complete.

---

## Step 6 – Deploy the Agentic Workflow and the Agent

Ask Bob to deploy the agentic workflow tool and agent YAML file by importing the script that Bob created in the previous step.

**Steps:**

1. Click the **watsonx tile** on the left sidebar.

2. In the **Environment Manager**, reactivate your watsonx Orchestrate environment:
   
   **Why reactivate?** Although you configured this environment in Step 2, the watsonx Orchestrate ADK extension requires an active authenticated session to deploy agents and workflows. Reactivating ensures Bob has the necessary permissions to execute deployment commands.
   
   - Select your environment from the list
   - Click **Activate**
   - Enter your API key when prompted (this authenticates the ADK CLI tools)
   
   The environment status will change to "Active" with a green indicator once authentication succeeds.

   > **Note:** If you are using the watsonx Orchestrate Developer Edition, make sure your local environment is running before you continue.
   
   > **Tip:** Your API key is stored securely in a `.env` file in your workspace. See the `.env.example` file for the required format.

3. Give Bob the following deployment instruction:

```text
Run the import script to deploy the flow and agent to my watsonx Orchestrate
environment. If orchestrate command line is not installed, install
ibm-watsonx-orchestrate with pip.
```

![Bob receives the deployment instruction](images/21-bob-deploy-instruction.png)

4. Bob runs the import script to deploy the workflow and the agent.

![Bob runs the import script – flow and agent deployed](images/22-bob-runs-import.png)

---

## Step 7 – Verify the Agent in watsonx Orchestrate

Confirm that the agentic workflow created by Bob works correctly in watsonx Orchestrate. You log in, check the agent configuration, and run a simple test to ensure that the agent can extract invoice details.

**Steps:**

1. Log in to watsonx Orchestrate:
   - **Local environment:** Run `orchestrate chat start` in your workspace terminal. UI at `http://localhost:3000/chat-lite`
   - **IBM Cloud SaaS:** Log in to IBM Cloud → Resource list → AI/Machine Learning → Watson Orchestrate

![IBM Cloud resource list – finding the watsonx Orchestrate service](images/23-ibmcloud-resource-list.png)

![Launch watsonx Orchestrate from IBM Cloud](images/24-wxo-launch-button.png)

2. Go to **Manage Agents** and search for the agent named `expense_report_agent` created by Bob.

![Manage Agents – searching for expense_report_agent](images/25-manage-agents-search.png)

3. Confirm that the agentic workflow is attached to the agent and that the agent uses the **Groq-GPT-OSS 120B** model.

![Agent configuration – workflow attached and LLM model confirmed](images/26-agent-config.png)

4. Test the agent by typing: *"Extract my invoices details from flight.pdf"*. The agent prompts you to upload the PDF. Upload the sample PDF from the `sample-pdfs/` folder and click **Send**.

![Testing the agent with a PDF invoice upload](images/27-test-agent-upload.png)

5. The agent returns all extracted invoice details in structured JSON format with a human-readable summary.

![Agent returns extracted invoice data in structured JSON](images/28-agent-json-result.png)

---

## Summary and Next Steps

This tutorial showed how Bob automates the complete process of building and deploying agentic workflows for watsonx Orchestrate. You created specialized watsonx Orchestrate development rules to guide Bob with the best practices. Bob generated the implementation plan, the document-processing flow with an inline KVP schema, the agent configuration using the specified LLM model, the documentation with Mermaid diagrams, and the deployment scripts.

Bob acted as a developer partner by applying detailed knowledge of watsonx Orchestrate patterns. Bob structured the project using ADK conventions, added the correct tools and agents directories, applied the document-processing pattern, and configured the semantic field extraction.

Bob then deployed the agentic workflow and agent in watsonx Orchestrate following the defined Bob rules. Bob improved quality and consistency by enforcing standard patterns, generating clear documentation, and managing the entire deployment lifecycle from ADK installation to environment activation and tool import.

![Bob summary – all 10 tasks completed successfully](images/29-bob-all-tasks-complete.png)

### Completed Tasks

| Task | Description |
|------|-------------|
| ✓ Project Structure | Created complete directory structure with all necessary folders |
| ✓ Document Processing Flow | Implemented flow with inline KVP schema for expense extraction |
| ✓ Native Agent Configuration | Created agent using `groq/openai/gpt-oss-120b` LLM |
| ✓ Deployment Script | Created executable `import-all.sh` for easy deployment |
| ✓ Testing Script | Created `flow_main.py` for programmatic testing |
| ✓ Documentation | Created comprehensive README with architecture and workflow diagrams |
| ✓ Python Package Structure | Added all necessary `__init__.py` files |
| ✓ ADK Installation | Installed `ibm-watsonx-orchestrate` package |
| ✓ Flow Deployment | Successfully deployed `expense_extraction_flow` tool |
| ✓ Agent Deployment | Successfully deployed `expense_report_agent` |

### Related Resources

- [Using IBM Bob to build watsonx Orchestrate agents and MCP tools](https://developer.ibm.com/tutorials/build-agents-mcp-tools-watsonx-orchestrate-using-bob/)
- [Beginner's guide to multi-agent orchestration with watsonx Orchestrate](https://developer.ibm.com/articles/multi-agent-orchestration-watsonx-orchestrate/)
- [Try watsonx Orchestrate free trial](https://www.ibm.com/account/reg/us-en/signup?formid=urx-52753)

### Acknowledgments

The authors Allen Chan, Ahmed Azraq, and Syeda Ameena deeply appreciate the support of Jukka Juselius for the guidance on reviewing and contributing to this tutorial.

This tutorial was produced as part of the IBM Open Innovation Community initiative: Agentic AI (AI for Developers and Ecosystem).

---

*This tutorial was published on IBM Developer · developer.ibm.com · © IBM Corporation 2026*
