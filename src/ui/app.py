
import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000/query"


st.set_page_config(
    page_title="Technical Documentation RAG Assistant",
    page_icon="📚",
    layout="centered"
)


st.title("📚 Technical Documentation RAG Assistant")

st.caption(
    "Ask questions about Python, LangChain and FastAPI "
    "based on the technical documentation."
)


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous conversation
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):

            with st.expander("View Sources"):

                for source in message["sources"]:
                    st.write(source)


# Chat input
question = st.chat_input("Ask a technical question...")


if question:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)


    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Searching documentation and generating answer..."):

            try:

                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=60
                )

                response.raise_for_status()

                result = response.json()

                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)

                if sources:

                    with st.expander("View Sources"):

                        for source in sources:
                            st.write(source)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    }
                )


            except requests.exceptions.ConnectionError:

                error_message = (
                    "Unable to connect to the RAG backend. "
                    "Please ensure the FastAPI server is running."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    }
                )


            except requests.exceptions.Timeout:

                error_message = (
                    "The request timed out. "
                    "Please try again."
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    }
                )


            except requests.exceptions.HTTPError as e:

                error_message = (
                    f"The API returned an HTTP error: {e}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    }
                )


            except Exception as e:

                error_message = (
                    f"An unexpected error occurred: {e}"
                )

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                        "sources": []
                    }
                )
