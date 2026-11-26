# --------------------------------------------------
# RETRIEVAL THRESHOLD EVALUATION DATASET
# --------------------------------------------------

TEST_QUESTIONS = [

    # --------------------------------------------------
    # PYTHON - QUERY VARIATIONS
    # --------------------------------------------------

    {
        "id": "Q1",
        "question": "What is Python?",
        "expected": "in_scope"
    },
    {
        "id": "Q2",
        "question": "what is Python",
        "expected": "in_scope"
    },
    {
        "id": "Q3",
        "question": "what is python",
        "expected": "in_scope"
    },
    {
        "id": "Q4",
        "question": "What is PYTHON?",
        "expected": "in_scope"
    },
    {
        "id": "Q5",
        "question": "Explain Python",
        "expected": "in_scope"
    },
    {
        "id": "Q6",
        "question": "Tell me about Python",
        "expected": "in_scope"
    },
    {
        "id": "Q7",
        "question": "Python programming language",
        "expected": "in_scope"
    },
    {
        "id": "Q8",
        "question": "Can you explain what Python is?",
        "expected": "in_scope"
    },

    # --------------------------------------------------
    # PYTHON FUNCTIONS
    # --------------------------------------------------

    {
        "id": "Q9",
        "question": "What are Python functions?",
        "expected": "in_scope"
    },
    {
        "id": "Q10",
        "question": "Explain functions in Python",
        "expected": "in_scope"
    },

    # --------------------------------------------------
    # PYTHON OOP
    # --------------------------------------------------

    {
        "id": "Q11",
        "question": "What is object-oriented programming in Python?",
        "expected": "in_scope"
    },
    {
        "id": "Q12",
        "question": "Explain OOP in Python",
        "expected": "in_scope"
    },

    # --------------------------------------------------
    # PYTHON DATA STRUCTURES
    # --------------------------------------------------

    {
        "id": "Q13",
        "question": "What are Python data structures?",
        "expected": "in_scope"
    },
    {
        "id": "Q14",
        "question": "Explain data structures in Python",
        "expected": "in_scope"
    },

    # --------------------------------------------------
    # FASTAPI
    # --------------------------------------------------

    {
        "id": "Q15",
        "question": "What is FastAPI?",
        "expected": "in_scope"
    },
    {
        "id": "Q16",
        "question": "Explain FastAPI",
        "expected": "in_scope"
    },
    {
        "id": "Q17",
        "question": "What can I build using FastAPI?",
        "expected": "in_scope"
    },

    # --------------------------------------------------
    # FASTAPI DEPENDENCY INJECTION
    # --------------------------------------------------

    {
        "id": "Q18",
        "question": "How does dependency injection work in FastAPI?",
        "expected": "in_scope"
    },
    {
        "id": "Q19",
        "question": "Explain dependency injection in FastAPI",
        "expected": "in_scope"
    },

    # --------------------------------------------------
    # PYTHON MODULES
    # --------------------------------------------------

    {
        "id": "Q20",
        "question": "What are Python modules?",
        "expected": "in_scope"
    },
    {
        "id": "Q21",
        "question": "Explain Python modules",
        "expected": "in_scope"
    },

    # --------------------------------------------------
    # PYTHON EXCEPTIONS
    # --------------------------------------------------

    {
        "id": "Q22",
        "question": "How do Python exceptions work?",
        "expected": "in_scope"
    },
    {
        "id": "Q23",
        "question": "Explain exception handling in Python",
        "expected": "in_scope"
    },

    # --------------------------------------------------
    # OUT-OF-SCOPE QUESTIONS
    # --------------------------------------------------

    {
        "id": "Q24",
        "question": "Who is the president of France?",
        "expected": "out_of_scope"
    },
    {
        "id": "Q25",
        "question": "What is the capital of Brazil?",
        "expected": "out_of_scope"
    },
    {
        "id": "Q26",
        "question": "Who won the FIFA World Cup in 2018?",
        "expected": "out_of_scope"
    },
    {
        "id": "Q27",
        "question": "What is the population of Japan?",
        "expected": "out_of_scope"
    },
    {
        "id": "Q28",
        "question": "Who invented the telephone?",
        "expected": "out_of_scope"
    },
    {
        "id": "Q29",
        "question": "What is the boiling point of water?",
        "expected": "out_of_scope"
    },
    {
        "id": "Q30",
        "question": "What is the stock price of Apple today?",
        "expected": "out_of_scope"
    },
]