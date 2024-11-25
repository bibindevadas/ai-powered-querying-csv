
import time

from google.cloud import bigquery
import streamlit as st
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import numpy as np
import pandas as pd
import io

BIGQUERY_DATASET_ID = "airline_bookings"

list_datasets_func = FunctionDeclaration(
    name="list_datasets",
    description="Get a list of datasets that will help answer the user's question",
    parameters={
        "type": "object",
        "properties": {},
    },
)

list_tables_func = FunctionDeclaration(
    name="list_tables",
    description="List tables in a dataset that will help answer the user's question",
    parameters={
        "type": "object",
        "properties": {
            "dataset_id": {
                "type": "string",
                "description": "Dataset ID to fetch tables from.",
            }
        },
        "required": [
            "dataset_id",
        ],
    },
)

get_table_func = FunctionDeclaration(
    name="get_table",
    description="Get information about a table, including the description, schema, and number of rows that will help answer the user's question. Always use the fully qualified dataset and table names.",
    parameters={
        "type": "object",
        "properties": {
            "table_id": {
                "type": "string",
                "description": "Fully qualified ID of the table to get information about",
            }
        },
        "required": [
            "table_id",
        ],
    },
)

sql_query_func = FunctionDeclaration(
    name="sql_query",
    description="Get information from data in BigQuery using SQL queries",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "SQL query on a single line that will help give quantitative answers to the user's question when run on a BigQuery dataset and table. In the SQL query, always use the fully qualified dataset and table names.",
            }
        },
        "required": [
            "query",
        ],
    },
)

sql_query_tool = Tool(
    function_declarations=[
        list_datasets_func,
        list_tables_func,
        get_table_func,
        sql_query_func,
    ],
)

model = GenerativeModel(
    "gemini-1.5-pro",
    generation_config={"temperature": 0},
    tools=[sql_query_tool],
)

st.set_page_config(
    page_title="AI Powered Data Query Interface",
    page_icon="vertex-ai.png",
    layout="wide",
)

col1, col2 = st.columns([8, 1])
with col1:
    st.title("AI Powered Data Querying")
with col2:
    st.image("vertex-ai.png")

st.subheader("Powered by Function Calling in Gemini")


with st.expander("Sample prompts", expanded=True):
    st.write(
        """
        - What kind of information is in this database?
        - How many bookings were made by customers in the 25-34 age group, grouped by state and airline?
        - Show the average ticket price for international flights grouped by airline.
        - How many customers booked more than 3 times in the last 3 months?
        - Compare ticket prices for business and economy classes.
    """
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"].replace("$", r"\$"))  # noqa: W605
        try:
            with st.expander("Function calls, parameters, and responses"):
                st.markdown(message["backend_details"])
        except KeyError:
            pass

if prompt := st.chat_input("Ask me about information in the database..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        chat = model.start_chat()
        client = bigquery.Client()

        prompt += """
                            You are a highly skilled data analyst specializing in airline booking data. Your task is to accurately answer user queries about this data, stored in a BigQuery database. **Prioritize result dont just return SQL query**
                            
                            #### Dataset Details:
                            **Dataset Name**: `airline_bookings`
                            **Tables**:
                            1. `customer_profiles`: CustomerID, AgeGroup, Gender, FrequentFlyer, State, City.
                            2. `airline_bookings`: BookingID, CustomerID, Airline, Destination, BookingDate, FlightType, TicketPrice, Class, BookingChannel, AffinityIndex.


                            **Here's an example of a user query:**

                            > "What are the top 5 destinations for customers aged 25-34?"

                            **Here's how you would respond:**

                            Top 5 Destinations for Customers Aged 25-34
                            | Destination | Total Bookings |
                            |---|---|
                            | London | 1234 |
                            | Paris | 987 |
                            | Tokyo | 876 |
                            | New York | 765 |
                            | Sydney | 654 |
                            
                            Now, here's the user's query:

                            [User's query]


                            Please provide:

                            1. The query results in a clear format (e.g., tables, lists, or visualizations)
                            2. A concise explanation of the results
                            3. Any relevant insights or observations
                            
                            **Important Considerations:**

                            1. Dataset: Always fully qualify table names with their dataset name in SQL queries. For example, use `airline_bookings.airline_bookings` instead of `airline_bookings`. Dont use any public dataset.
                            2. Data Accuracy: Ensure the accuracy of your SQL queries and the correctness of the results. 
                            3. Clarity and Conciseness: Present your response in a clear and concise manner, avoiding unnecessary details.
                            4. User-Friendliness: Tailor your response to the user's level of technical expertise. e.g., tables, lists, or visualizations.
                            
                            
                            **Additional Notes:**
                            1. The following columns exist in **both tables**: `AgeGroup`, `Gender`, `FrequentFlyer`, `State`, and `City`. Always qualify these column names with the table name or alias in the query.
                                   - Use `cp` for `customer_profiles` (e.g., `cp.State`, `cp.AgeGroup`).
                                   - Use `abd` for `airline_bookings_data` (e.g., `abd.State`, `abd.AgeGroup`).
                            2. When joining the tables, you can use `CustomerID` as the key for the join.
                            3. Ensure the generated SQL queries are free of ambiguity and fully qualify columns, especially in SELECT, WHERE, GROUP BY, and ORDER BY clauses.
                            4. For GROUP BY queries, explicitly use the fully qualified column name in the GROUP BY clause.
                            5.The `FrequentFlyer` column is of type `BOOL`. Treat `'Yes'` as `TRUE` and `'No'` as `FALSE`. 
If the column is `STRING`, use `'Yes'` and `'No'` as is.
                            6. If the result is not tabular (e.g., a single string message or an error), skip the download logic and display only the response

                            
                            By following these guidelines, you can provide accurate, informative, and user-friendly responses.

            """

        try:
            response = chat.send_message(prompt)
            response = response.candidates[0].content.parts[0]

            print(response)

            api_requests_and_responses = []
            backend_details = ""

            function_calling_in_process = True
            while function_calling_in_process:
                try:
                    params = {}
                    for key, value in response.function_call.args.items():
                        params[key] = value

                    print(response.function_call.name)
                    print(params)

                    if response.function_call.name == "list_datasets":
                        api_response = client.list_datasets()
                        api_response = BIGQUERY_DATASET_ID
                        api_requests_and_responses.append(
                            [response.function_call.name, params, api_response]
                        )

                    if response.function_call.name == "list_tables":
                        api_response = client.list_tables(params["dataset_id"])
                        api_response = str([table.table_id for table in api_response])
                        api_requests_and_responses.append(
                            [response.function_call.name, params, api_response]
                        )

                    if response.function_call.name == "get_table":
                        api_response = client.get_table(params["table_id"])
                        api_response = api_response.to_api_repr()
                        api_requests_and_responses.append(
                            [
                                response.function_call.name,
                                params,
                                [
                                    str(api_response.get("description", "")),
                                    str(
                                        [
                                            column["name"]
                                            for column in api_response["schema"][
                                                "fields"
                                            ]
                                        ]
                                    ),
                                ],
                            ]
                        )
                        api_response = str(api_response)

                    if response.function_call.name == "sql_query":
                        job_config = bigquery.QueryJobConfig(
                            maximum_bytes_billed=100000000
                        )  # Data limit per query job
                        try:
                            cleaned_query = (
                                params["query"]
                                .replace("\\n", " ")
                                .replace("\n", "")
                                .replace("\\", "")
                            )
                            query_job = client.query(
                                cleaned_query, job_config=job_config
                            )
                            api_response = query_job.result()
                            # Convert the response into a list of rows
                            rows = list(api_response)

                            if rows:
                                # Extract column information
                                column_names = rows[0].keys() if isinstance(rows[0], bigquery.Row) else []
                                num_columns = len(column_names)

                                # Case 1: Non-tabular data (≤10 rows or very few columns)
                                if len(rows) <= 10 or num_columns <= 1:
                                    
                                    api_response = str([dict(row) for row in rows])
                                    api_response = api_response.replace("\\", "").replace("\n", "")
                                    api_requests_and_responses.append([response.function_call.name, params, api_response])

                                # Case 2: Tabular data (>10 rows and ≥2 columns)
                                else:
                                    # Convert rows into a DataFrame
                                    result_data = pd.DataFrame([dict(row) for row in rows])

                                    # Display the DataFrame in Streamlit
                                    st.write("### Query Results", result_data)
                                    
                                    # Create a CSV file in memory for download
                                    csv_buffer = io.StringIO()
                                    result_data.to_csv(csv_buffer, index=False)
                                    csv_data = csv_buffer.getvalue()

                                    # Add a download button for the CSV file
                                    st.download_button(
                                        label="Download Results as CSV",
                                        data=csv_data,
                                        file_name="query_results.csv",
                                        mime="text/csv"
                                    )

                                    # Generate key observations (e.g., insights from the data)
                                    #st.write("### Observations:")
                                    try:
                                        api_response = str([dict(row) for row in rows])
                                        api_response = api_response.replace("\\", "").replace("\n", "")
                                        api_requests_and_responses.append([response.function_call.name, params, api_response])

                                    except Exception as obs_error:
                                        st.warning(f"Could not generate detailed observations. Error: {obs_error}")
                                        
                                    # Update api_response to keep data consistency
                                    api_response = result_data.to_json(orient="records")
                            else:
                                # If no rows or columns, revert to original handling
                                api_response = str([dict(row) for row in rows])
                                api_response = api_response.replace("\\", "").replace("\n", "")
                                api_requests_and_responses.append([response.function_call.name, params, api_response])
                        except Exception as e:
                            error_message = f"""
                            We're having trouble running this SQL query. This
                            could be due to an invalid query or the structure of
                            the data. Try rephrasing your question to help the
                            model generate a valid query. Details:

                            {str(e)}"""
                            st.error(error_message)
                            api_response = error_message
                            api_requests_and_responses.append(
                                [response.function_call.name, params, api_response]
                            )
                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": error_message,
                                }
                            )

                    print(api_response)

                    response = chat.send_message(
                        Part.from_function_response(
                            name=response.function_call.name,
                            response={
                                "content": api_response,
                            },
                        ),
                    )
                    response = response.candidates[0].content.parts[0]

                    backend_details += "- Function call:\n"
                    backend_details += (
                        "   - Function name: ```"
                        + str(api_requests_and_responses[-1][0])
                        + "```"
                    )
                    backend_details += "\n\n"
                    backend_details += (
                        "   - Function parameters: ```"
                        + str(api_requests_and_responses[-1][1])
                        + "```"
                    )
                    backend_details += "\n\n"
                    backend_details += (
                        "   - API response: ```"
                        + str(api_requests_and_responses[-1][2])
                        + "```"
                    )
                    backend_details += "\n\n"
                    with message_placeholder.container():
                        st.markdown(backend_details)

                except AttributeError:
                    function_calling_in_process = False

            time.sleep(3)

            full_response = response.text
            with message_placeholder.container():
                st.markdown(full_response.replace("$", r"\$"))  # noqa: W605
                with st.expander("Function calls, parameters, and responses:"):
                    st.markdown(backend_details)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                    "backend_details": backend_details,
                }
            )
        except Exception as e:
            print(e)
            error_message = f"""
                Something went wrong! We encountered an unexpected error while
                trying to process your request. Please try rephrasing your
                question. Details:

                {str(e)}"""
            st.error(error_message)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )
