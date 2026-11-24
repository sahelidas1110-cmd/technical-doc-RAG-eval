# Phase 7: Streamlit Frontend

## 1. Objective

Develop a user-friendly web interface for the Technical Documentation RAG Assistant using Streamlit.

The frontend communicates with the FastAPI backend through HTTP requests. It does not directly invoke the RAG pipeline or interact with the vector database.

## 2. Architecture

The application follows a frontend-backend architecture:

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **RAG Pipeline:** Retrieval, context construction, prompt generation and LLM response
- **Vector Database:** Chroma
- **LLM:** OpenAI GPT-4.1-mini

### Request Flow

1. User enters a question in the Streamlit interface.
2. Streamlit sends an HTTP POST request to the FastAPI `/query` endpoint.
3. FastAPI invokes the RAG pipeline.
4. Relevant documents are retrieved from the vector database.
5. Retrieved context is passed to the LLM.
6. The LLM generates a grounded response.
7. FastAPI returns the answer and source information.
8. Streamlit displays the answer and retrieved sources.

## 3. Technologies Used

- Streamlit
- Requests
- FastAPI
- Python
- LangChain
- Chroma
- OpenAI

## 4. Frontend Implementation

The frontend was implemented in:

`src/ui/app.py`

Key functionalities implemented:

- Chat-based user interface using `st.chat_input()`.
- Conversation display using `st.chat_message()`.
- Persistent chat history within the Streamlit session using `st.session_state`.
- HTTP communication with the FastAPI backend using the Requests library.
- Loading indicator during response generation.
- Source display through expandable sections.
- Error handling for connection failures, request timeouts, HTTP errors and unexpected exceptions.

## 5. Backend Integration

The Streamlit frontend communicates with the FastAPI endpoint:

`POST http://127.0.0.1:8000/query`

The question is sent as a JSON payload:

```json
{
  "question": "What is dependency injection in FastAPI?"
}
```

The backend returns the generated answer and source information, which are displayed by the frontend.

## 6. Testing and Validation

The frontend was tested with multiple questions.

### Test Cases

| Test | Expected Behavior | Status |
|---|---|---|
| Answerable question | Generate a relevant answer from the knowledge base | Passed |
| Source display | Display retrieved sources through View Sources | Passed |
| Unanswerable question | Appropriately abstain when information is unavailable | Passed |
| Chat history | Maintain previous questions and answers within the session | Passed |

All four frontend functionality tests were successfully verified.

## 7. Error Handling

The frontend handles the following scenarios:

- Backend connection failure
- Request timeout
- HTTP errors returned by the backend
- Unexpected errors

User-friendly error messages are displayed in the interface.

## 8. Application Execution

### Start the FastAPI backend

```powershell
python -m uvicorn src.api.main:app --reload
```

### Start the Streamlit frontend

```powershell
python -m streamlit run src/ui/app.py
```

The Streamlit application is accessible through the local browser.

## 9. Outcome

A functional chat-based web interface was successfully developed and integrated with the FastAPI backend.

The frontend supports question answering, source transparency, abstention for unsupported queries, conversation history and basic error handling.

The RAG assistant is now accessible through a web interface rather than requiring users to interact directly with Python code or API endpoints.