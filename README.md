# Agentic RAG Framework for Log Analytics

## Overview

This project demonstrates a Retrieval-Augmented Generation (RAG) framework built with Google ADK and Vertex AI embeddings to enable natural language querying and analysis of cybersecurity logs.

Designed specifically for cybersecurity teams—particularly those focused on CIAM/IAM workflows—this framework allows ingestion of structured log files (e.g., JSON logs from authentication systems, audit trails) and analytics through natural language queries.

---

## Key Features

- **Dynamic Corpus Creation**  
  Ingest log files from Google Drive into multiple independent corpora representing different datasets (e.g., Okta logs, privileged access events).

- **Agent-Orchestrated Queries**  
  Use Google ADK agents to coordinate document retrieval and prompt execution, enabling natural language queries over the data.

- **Vertex AI Embeddings**  
  Leverages Vertex AI’s embedding models for efficient vector similarity search across large-scale logs.

- **No SIEM Required**  
  Lightweight alternative for log analytics, root cause analysis, and threat hunting—no heavy SIEM infrastructure required.

- **CIAM/IAM Focus**  
  Tailored for analyzing authentication events, access logs, policy changes, and detecting suspicious patterns.

---

## Use Cases

- Analyzing failed MFA attempts and authentication anomalies.
- Detecting privilege escalation or unusual access patterns.
- Conducting access review audits based on historical logs.
- Investigating policy misconfigurations through natural language queries.
- Accelerating threat detection workflows with lightweight AI-powered analytics.

---

## Vertex AI RAG Agent with Google ADK

This repository contains a Google Agent Development Kit (ADK) implementation of a Retrieval Augmented Generation (RAG) agent using Google Cloud Vertex AI.

### Features

- Query document corpora with natural language questions
- List available document corpora
- Create new document corpora
- Add new documents to existing corpora
- Get detailed information about specific corpora
- Delete corpora when they're no longer needed

---

## Prerequisites

- Google Cloud account with billing enabled
- Google Cloud project with Vertex AI API enabled
- Appropriate access to create and manage Vertex AI resources
- Python 3.9+ environment

---

## Setting Up Google Cloud Authentication

1. **Install Google Cloud CLI**  
   [Google Cloud SDK Installation Guide](https://cloud.google.com/sdk/docs/install)

2. **Initialize the Google Cloud CLI**
   ```bash
   gcloud init
