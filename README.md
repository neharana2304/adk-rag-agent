**Agentic RAG Framework for Log Analytics**
Overview
This project demonstrates a Retrieval-Augmented Generation (RAG) framework built with Google ADK and Vertex AI embeddings to enable natural language querying and analysis of cybersecurity logs.
Designed specifically for cybersecurity teams—particularly those focused on CIAM/IAM workflows—this framework allows ingestion of structured log files (e.g., JSON logs from authentication systems, audit trails) and analytics through natural language queries.

Key Features
Dynamic Corpus Creation
Ingest log files from Google Drive into multiple independent corpora representing different datasets (e.g., Okta logs, privileged access events).

Agent-Orchestrated Queries
Use Google ADK agents to coordinate document retrieval and prompt execution, enabling natural language queries over the data.

Vertex AI Embeddings
Leverages Vertex AI’s embedding models for efficient vector similarity search across large-scale logs.

No SIEM Required
Lightweight alternative for log analytics, root cause analysis, and threat hunting—no heavy SIEM infrastructure required.

CIAM/IAM Focus
Tailored for analyzing authentication events, access logs, policy changes, and detecting suspicious patterns.

Use Cases
Analyzing failed MFA attempts and authentication anomalies.
Detecting privilege escalation or unusual access patterns.
Conducting access review audits based on historical logs.
Investigating policy misconfigurations through natural language queries.
Accelerating threat detection workflows with lightweight AI-powered analytics.
Vertex AI RAG Agent with Google ADK
This repository contains a Google Agent Development Kit (ADK) implementation of a Retrieval Augmented Generation (RAG) agent using Google Cloud Vertex AI.

Features
Query document corpora with natural language questions
List available document corpora
Create new document corpora
Add new documents to existing corpora
Get detailed information about specific corpora
Delete corpora when they're no longer needed
Prerequisites
Google Cloud account with billing enabled
Google Cloud project with Vertex AI API enabled
Appropriate access to create and manage Vertex AI resources
Python 3.9+ environment

Setting Up Google Cloud Authentication
Install Google Cloud CLI
Google Cloud SDK Installation Guide

Initialize the Google Cloud CLI

bash
gcloud init
Set up Application Default Credentials

bash
gcloud auth application-default login
This will open a browser window for authentication and store credentials in:
~/.config/gcloud/application_default_credentials.json

Verify Authentication

bash
gcloud auth list
gcloud config list
Enable Required APIs

bash
gcloud services enable aiplatform.googleapis.com
Installation
Set up a virtual environment

bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Install Dependencies

bash
pip install -r requirements.txt
Using the Agent
The agent provides the following functionality through its tools:

1. Query Documents
Ask questions and get answers from your document corpus
Automatically retrieves relevant information from the specified corpus
Generates informative responses based on the retrieved content
2. List Corpora
Shows all available document corpora in your project
Displays corpus names and basic information
3. Create Corpus
Create a new empty document corpus with a custom name
Sets up the corpus with recommended embedding model configuration
4. Add New Data
Add documents to existing corpora or create new ones
Supports Google Drive URLs and GCS (Google Cloud Storage) paths
Automatically creates new corpora if they don't exist
5. Get Corpus Information
Provides detailed information about a specific corpus
Shows document count, file metadata, and creation time
6. Delete Corpus
Removes corpora that are no longer needed
Requires confirmation to prevent accidental deletion
Troubleshooting
Authentication Problems

Run gcloud auth application-default login again
Check if your service account has the necessary permissions
API Errors

Ensure the Vertex AI API is enabled: gcloud services enable aiplatform.googleapis.com
Verify your project has billing enabled
Quota Issues

Check your Google Cloud Console for any quota limitations
Request quota increases if needed
Missing Dependencies

Ensure all requirements are installed: pip install -r requirements.txt
Additional Resources
Vertex AI RAG Documentation
Google Agent Development Kit (ADK) Documentation
Google Cloud Authentication Guide
