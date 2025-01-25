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
### Credentials
Here, we need to to do two thigns; first, download our credentials of Google OAuth Client in "Credentials" section which will be in <code>.json</code> format. Let's name it as <code>OAUTH_CLIENT_CREDENTIALS.json</code> to refer to it later.
```json
{
  "web":
  {
    "client_id":"....",
    "project_id":"....",
    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
    "token_uri":"https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
    "client_secret":"...."
  }
}
```
Save the downloaded file in project root location (i.e. <code>./DocuRAG</code>); second, we need to fill our <code>credentials.py</code> with required data <i>(instructions are commented)</i>. </br><strong>Note:</strong> It is required to get a password for your email to use in your application for testing purposes. For more details, visit the link: [Support Google](https://support.google.com/mail/answer/185833?hl=en)
### Database
Finally, our database needs to be configured for the application. Simply, install <strong>MongoDB</strong> in your computer and create a database called <strong>"docurag-db"</strong> and collection with a name <strong>"appointment"</strong>. 

## Run 
After completing all the tasks above, we can run our application using two <code>.py</code> files, such as <code>api.py</code> and <code>llm_ui.py</code>.
