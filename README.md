# DocuRAG - Docusign Extension Application for Maestro Workflow
## Description
This is half an extension and standalone application designed for Docusign platform. This application can be installed and used in Docusign Maestro Workflow.

## Overwiew
In the world, where people and industries cooperate with each other based on documents, contracts, agreements, etc., it becomes very crucial to process all the data in documents and make decisions quickly and effectively. Thus, this application solves this problem by integrating RAG into Docusign platform for document QA.
Signers of documents can now easily QA documents using AI such as Google's Gemini Pro model. The following sections will explain the technical aspects and how to use this application. 

## Diagram
### Figure 1: Authorization flowchart of the application.
<div align=center><img src="https://github.com/Rahman2001/DocuRAG/blob/main/resources/DocuRAG%20oauth%20flowchart.drawio.svg"/></div> </br>

### Figure 2: Application's functional diagram.
<div align=center><img src="https://github.com/Rahman2001/DocuRAG/blob/main/resources/DocuRAG%20flowchart.drawio.svg"/></div>

## Setup
### Google Cloud API 
First of all, sign up for Google Cloud and make sure you have credits to use Vertex AI. If you don't have it, you can sign up for 300$ free credits to Google Cloud in which Vertex AI and many services will be accessible. 
### Google Cloud OAuth
Make sure you have enabled "OAuth consent screen" located in "APIs & Services" section of Google Cloud. After enabling it, go to "Credentials" section and create OAuth Client ID. Add a URI in "Authorized redirect URIs" field (URI: <code>https://demo.services.docusign.net/act-gateway/v1.0/oauth/callback</code>). Also, add test users' email addresses. 
### PyPi dependencies
Clone this repository and execute the following command: 
```bash
cd DocuRAG
pip3 install -r requirements.txt
```
