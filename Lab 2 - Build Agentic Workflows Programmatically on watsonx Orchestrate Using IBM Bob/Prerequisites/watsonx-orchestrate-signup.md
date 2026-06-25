# watsonx Orchestrate Free Trial Signup and Configuration

Quick guide for signing up for the watsonx Orchestrate free trial and configuring your environment for agent development.

## Table of Contents

1. [Overview](#overview)
2. [Sign Up for watsonx Orchestrate Free Trial](#sign-up-for-watsonx-orchestrate-free-trial)
3. [Access watsonx Orchestrate](#access-watsonx-orchestrate)
4. [Generate API Credentials](#generate-api-credentials)
5. [Configure ADK Environment](#configure-adk-environment)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)
8. [Additional Resources](#additional-resources)

---

## Overview

This guide walks you through:

- Signing up for watsonx Orchestrate free trial
- Accessing your watsonx Orchestrate instance
- Generating API credentials
- Configuring the ADK to connect to your instance

**Estimated Time**: 10-15 minutes

**Prerequisites**:
- ✅ Completed [Environment Setup Guide](environment-setup.md)
- ✅ Valid email address

---

## Sign Up for watsonx Orchestrate Free Trial

### Step 1: Access Free Trial Registration

1. **Visit the Free Trial Page**
   - Go to: **[https://www.ibm.com/account/reg/us-en/signup?formid=urx-52753](https://www.ibm.com/account/reg/us-en/signup?formid=urx-52753)**

2. **Complete Registration Form**
   - Enter your business email address
   - Fill in your personal information:
     - First and last name
     - Company name
     - Country/Region
     - Phone number
   - Create a password (must meet security requirements)

3. **Accept Terms**
   - Review the IBM Terms and Conditions
   - Check the acceptance box
   - Optionally subscribe to IBM communications

4. **Submit Registration**
   - Click "Continue" or "Create account"
   - Check your email for verification link
   - Click the verification link to activate your account

### Step 2: Complete Trial Setup

1. **Sign In**
   - After email verification, you'll be redirected to sign in
   - Use your email and password

2. **Trial Provisioning**
   - The system will automatically provision your watsonx Orchestrate instance
   - This typically takes 2-5 minutes
   - You'll receive an email when your instance is ready

3. **Access Confirmation**
   - Once provisioned, you'll see your watsonx Orchestrate dashboard
   - Your free trial is now active!

### Trial Details

**What's Included:**
- Full access to watsonx Orchestrate features
- Ability to create and deploy AI agents
- Access to Agent Development Kit (ADK)
- Community support

**Trial Duration:**
- Check the trial terms for current duration (typically 30-60 days)
- No credit card required for trial

**Trial Limitations:**
- Usage limits may apply (check trial terms)
- Some enterprise features may be restricted

---

## Access watsonx Orchestrate

### Step 1: Access Your Instance

1. **Check Your Email**
   - Look for the welcome email from IBM watsonx Orchestrate
   - The email contains your instance access link

2. **Click the Access Link**
   - Click the "Launch watsonx Orchestrate" link in the email
   - Or use the direct URL provided in your trial confirmation

3. **Sign In**
   - Use the email and password you created during registration
   - You'll be taken to your watsonx Orchestrate dashboard

### Step 2: First-Time Setup

1. **Complete Initial Setup** (if prompted)
   - Accept terms of service
   - Configure basic preferences
   - Complete any welcome tutorials (optional)

2. **Explore the Dashboard**
   - Familiarize yourself with the interface
   - You're now ready to generate API credentials

---

## Generate API Credentials

API credentials are required to connect the ADK to your watsonx Orchestrate instance.

### Step 1: Access API Details

1. **Open watsonx Orchestrate**
   - Launch your watsonx Orchestrate instance (see previous section)

2. **Open Settings**
   - Click your user icon in the top-right corner
   - Select "Settings" from the dropdown menu

3. **Navigate to API Details**
   - Click on the "API details" tab
   - You'll see your service instance URL

### Step 2: Copy Service Instance URL

1. **Locate Service Instance URL**
   - In the API details tab, find the "Service instance URL" field
   - Example format: `https://us-south.ml.cloud.ibm.com/ml/v1/...`

2. **Copy the URL**
   - Click the copy icon next to the URL
   - Or manually select and copy the entire URL
   - **Save this URL** - you'll need it for ADK configuration

### Step 3: Generate API Key

1. **Click "Generate API key" Button**
   - In the API details tab
   - Click the "Generate API key" button

2. **Create API Key**
   - You may be prompted to create an API key name
   - Enter a descriptive name (e.g., "wxo-adk-bobathon-labs")
   - Add a description (optional, e.g., "API key for ADK development in Bobathon labs")
   - Click "Create" or "Generate"

3. **Copy and Save API Key**
   - **IMPORTANT**: The API key is shown only once
   - Click "Copy" to copy the key
   - **Save it securely** in a password manager or secure note
   - You cannot retrieve this key later
   - If lost, you'll need to generate a new one

### Important Notes About API Keys

⚠️ **Security Best Practices**:
- Never commit API keys to version control
- Don't share API keys in public channels
- Store keys in secure password managers
- Rotate keys periodically
- Delete unused keys

⚠️ **Key Limitations**:
- Keys cannot be edited or retrieved after creation
- Deleted keys cannot be recovered
- Check your trial terms for any API key limits

---

## Configure ADK Environment

Now configure the ADK to connect to your watsonx Orchestrate instance.

**📄 For detailed ADK environment configuration instructions, please refer to:**

**[env_setup_instructions.md](../env_setup_instructions.md)**

This PDF contains the complete, authoritative guide for configuring the ADK environment with your watsonx Orchestrate instance.

### Quick Summary

You'll need:
- The service instance URL you copied earlier
- The API key you generated
- To run the `orchestrate env add` command as detailed in the PDF

---

## Troubleshooting

### Issue: "Invalid API Key"

**Symptoms**: Authentication fails when adding environment

**Solutions**:
1. Verify you copied the complete API key
2. Check for extra spaces or characters
3. Generate a new API key and try again
4. Ensure you're using the API key from watsonx Orchestrate Settings > API details

### Issue: "Cannot Connect to Service"

**Symptoms**: ADK can't reach the service instance

**Solutions**:
1. Verify the service instance URL is correct
2. Check your internet connection
3. Ensure the service is provisioned and running
4. Try accessing watsonx Orchestrate in a browser first

### Issue: "Environment Not Found"

**Symptoms**: `orchestrate env list` shows no environments

**Solutions**:
- Re-add the environment following the instructions in the [env_setup_instructions.md](../env_setup_instructions.md)

### Issue: "Wrong Authentication Type"

**Symptoms**: Connection fails with authentication error

**Solutions**:
- For watsonx Orchestrate free trial: Use `--type ibm_iam`
- If auto-detection fails, explicitly specify the type

### Issue: "API Key Limit Reached"

**Symptoms**: Cannot generate new API key

**Solutions**:
1. Delete unused API keys from Settings > API details
2. Check your trial terms for API key limits
3. Reuse existing keys if possible

---

## Next Steps

✅ **watsonx Orchestrate Setup Complete!**

You're now ready to start building agents:

1. 🚀 [Start Lab 2: Build Agentic Workflows](../)
2. 📖 Review [watsonx Orchestrate ADK Documentation](https://developer.watson-orchestrate.ibm.com)
3. 🎓 Explore [IBM Developer Tutorials](https://developer.ibm.com/tutorials/)

---

## Additional Resources

- [watsonx Orchestrate Product Page](https://www.ibm.com/products/watsonx-orchestrate)
- [watsonx Orchestrate Free Trial](https://www.ibm.com/account/reg/us-en/signup?formid=urx-52753)
- [watsonx Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com)
- [ADK CLI Reference](https://developer.watson-orchestrate.ibm.com/cli/overview)
- [IBM Developer](https://developer.ibm.com)

---

**Need Help?** Contact IBM Support or refer to the [official documentation](https://developer.watson-orchestrate.ibm.com).