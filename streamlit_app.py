import streamlit as st
import requests
import json

st.title("NetOps Agentic Co-Pilot Frontend")

st.markdown("""
This application allows you to submit a network alert log (in JSON format) to the
NetOps Agentic Co-Pilot backend for diagnosis and remediation planning.
""")

# Input for API Key
api_key = st.text_input("Enter your API Key", type="password")

st.subheader("Submit Network Log")
network_log_input = st.text_area("Paste Network Log JSON here:", height=300,
                                 value="""{
    "timestamp": "2026-06-15T10:30:00Z",
    "device_id": "router-123",
    "error_code": "BGP-4-NOCONN",
    "description": "BGP peer 192.168.1.1 is down. Route flapping detected."
}""")

if st.button("Diagnose"):
    if not api_key:
        st.error("Please enter an API Key.")
    else:
        try:
            log_data = json.loads(network_log_input)
            headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
            # Assuming the FastAPI backend is running locally at http://localhost:8000
            # For deployment, this URL would change to your deployed service URL
            response = requests.post("http://localhost:8000/diagnose", headers=headers, json=log_data)

            if response.status_code == 200:
                st.success("Diagnosis Complete!")
                st.json(response.json())
            else:
                st.error(f"Error during diagnosis: {response.status_code} - {response.text}")
        except json.JSONDecodeError:
            st.error("Invalid JSON format in network log. Please check your input.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend. Please ensure the FastAPI application is running.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
