# AI-powered-data-querying

📖 Overview

This app demonstrates the power of Gemini's Function Calling capabilities, enabling users to query and understand their BigQuery databases using natural language. Forget complex SQL syntax – interact with your data conversationally.

Function Calling in Gemini lets developers create a description of a function in their code, then pass that description to a language model in a request. The response from the model includes the name of a function that matches the description and the arguments to call it with.

Try using the demo app now! (App Link expires on Dec 5, 2024)
 https://sql-talk-ai-csv-280048506091.us-central1.run.app/

![Screenshot 2024-11-25 at 11 11 02 AM](https://github.com/user-attachments/assets/0eedc0d1-7fc6-42fd-be60-8f93d864db31)

# 🎯 Key features include:

1. Function calling to handle queries.
2. Generative AI for intuitive data summarization.
3. Integration with Vertex AI for seamless processing.


# 🚀 Getting Started

**Prerequisites**

1. A Google Cloud project with billing enabled
2. A BigQuery dataset (used synthetic data (airlinebookings), created using faker library)
3. APIs for Vertex AI, BigQuery, BigQuery Data Transfer, and Cloud Run enabled
4. Python (3.8 or above).
5. Familiarity with Python and SQL concepts

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





