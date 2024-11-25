# AI-powered-data-querying

📖 Overview

This app demonstrates the power of Gemini's Function Calling capabilities, enabling users to query and understand their BigQuery databases using natural language. Forget complex SQL syntax – interact with your data conversationally.

Function Calling in Gemini lets developers create a description of a function in their code, then pass that description to a language model in a request. The response from the model includes the name of a function that matches the description and the arguments to call it with.

Try using the demo app now! (App Link expires on Dec 5, 2024)
 https://sql-talk-ai-csv-280048506091.us-central1.run.app/

![Screenshot 2024-11-25 at 11 11 02 AM](https://github.com/user-attachments/assets/0eedc0d1-7fc6-42fd-be60-8f93d864db31)

[Watch the video](./streamlit-app-2024-11-21-02-11-49.webm)



# Key features include:

1. Function calling to handle queries.
2. Generative AI for intuitive data summarization.
3. Integration with Vertex AI for seamless processing.

# 🎯 Features

1. Query Tabular Data: Use natural language to perform SQL-like queries.
2. Generative Summarization: Summarize datasets with simple prompts.
3. Customizable Workflow: Extend the querying logic for specific datasets and use cases.

# 🚀 Getting Started
Prerequisites

1. Google Cloud account.
2. Vertex AI, Cloud Run, and BigQuery enabled in your Google Cloud project.
3. Python (3.8 or above).
4. Basic knowledge of SQL, Vertex AI, Streamlit, and Cloud Run.

# Deploy to Cloud Run

Ensure you have Docker installed and authenticated with Google Cloud:

    gcloud auth configure-docker

Build the Docker image:

    gcloud builds submit --tag gcr.io/<PROJECT_ID>/ai-powered-data-querying

When deploying this app to Cloud Run, a best practice is to create a service account to attach the following roles to, which are the permissions required for the app to read data from BigQuery, run BigQuery jobs, and use resources in Vertex AI:

1. BigQuery Data Viewer (roles/bigquery.dataViewer)
2. BigQuery Job User (roles/bigquery.jobUser)
3. Vertex AI User (roles/aiplatform.user)
        
To deploy this app to Cloud Run, run the following command to have the app built with Cloud Build and deployed to Cloud Run, replacing the service-account and project values with your own values, similar to:

      gcloud run deploy sql-talk-ai-csv --allow-unauthenticated --region us-central1 --service-account SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com --source .

# Access the Application

After deployment, you’ll receive a URL for the application. Open the URL to interact with your Streamlit-powered frontend that enables intuitive querying and summarization of BigQuery datasets.

https://sql-talk-ai-csv-280048506091.us-central1.run.app/

# 🧩 Frontend (Streamlit)

The Streamlit frontend provides an intuitive user interface for:

    1. Querying BigQuery datasets with natural language.
    2. Visualizing summarized data in real time.
    3. Customizing prompts and queries to suit business needs.

References:

https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/function-calling





