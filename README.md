# AI-powered-data-querying
AI-powered tool to translate natural language queries into actionable SQL and deliver user-friendly results. (App Link expires on Dec 5, 2024)


    https://sql-talk-ai-csv-280048506091.us-central1.run.app/

📖 Overview

This project demonstrates how to leverage Vertex AI for querying tabular datasets using generative AI and function calling. The goal is to simplify data exploration and enable users to interact with their data conversationally.

Key features include:

    1. Function calling to handle queries.
    2. Generative AI for intuitive data summarization.
    3. Integration with Vertex AI for seamless processing.

🎯 Features

    1. Query Tabular Data: Use natural language to perform SQL-like queries.
    2. Generative Summarization: Summarize datasets with simple prompts.
    3. Customizable Workflow: Extend the querying logic for specific datasets and use cases.

🚀 Getting Started
Prerequisites

    1. Google Cloud account.
    2. Vertex AI, Cloud Run, and BigQuery enabled in your Google Cloud project.
    3. Python (3.8 or above).
    4. Basic knowledge of SQL, Vertex AI, Streamlit, and Cloud Run.

Setup Instructions

1. Clone the Repository

        git clone https://github.com/yourusername/ai-powered-data-querying.git
        cd ai-powered-data-querying

2. Install Dependencies

        pip install -r requirements.txt

3. Set Up Google Cloud Authentication

Download your service account key from the Google Cloud Console.
Set the GOOGLE_APPLICATION_CREDENTIALS environment variable:

        export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-key.json"

4. Connect to BigQuery

Ensure your dataset is uploaded to BigQuery. You can create a new dataset and table using the BigQuery console or CLI:

        bq mk --dataset <PROJECT_ID>:<DATASET_NAME>
        bq load --source_format=CSV <PROJECT_ID>:<DATASET_NAME>.<TABLE_NAME> path/to/your-data.csv

5. Prepare for Deployment

Update the Dockerfile to include both the backend (querying logic) and Streamlit frontend:

        FROM python:3.8-slim
    
        WORKDIR /app
    
        COPY . /app
    
        RUN pip install -r requirements.txt
    
        CMD ["streamlit", "run", "src/frontend.py", "--server.port=8080", "--server.enableCORS=false"]



6. Deploy to Cloud Run

Ensure you have Docker installed and authenticated with Google Cloud:

    gcloud auth configure-docker

Build the Docker image:

    gcloud builds submit --tag gcr.io/<PROJECT_ID>/ai-powered-data-querying

Deploy to Cloud Run:

        gcloud run deploy ai-powered-data-querying \
          --image gcr.io/<PROJECT_ID>/ai-powered-data-querying \
          --platform managed \
          --region <REGION> \
          --allow-unauthenticated

7. Access the Application

    After deployment, you’ll receive a URL for the application. Open the URL to interact with your Streamlit-powered frontend that enables intuitive querying and summarization of BigQuery datasets.

   

🧩 Frontend (Streamlit)

The Streamlit frontend provides an intuitive user interface for:

    1. Querying BigQuery datasets with natural language.
    2. Visualizing summarized data in real time.
    3. Customizing prompts and queries to suit business needs.




