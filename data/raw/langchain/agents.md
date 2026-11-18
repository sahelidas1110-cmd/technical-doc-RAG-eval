# Agents in LangChain

## 1. What Is an AI Agent?

An AI agent is a system that uses a language model to decide how to accomplish a task.

Unlike a traditional LLM application that follows a fixed sequence of operations, an agent can dynamically decide which actions to take based on the user's request and the information it receives.

An agent can:

- Understand a user's request.
- Decide whether additional information is required.
- Select an appropriate tool.
- Call external APIs or services.
- Process tool results.
- Decide whether another action is necessary.
- Generate a final response.

An agent combines an LLM with tools, instructions, and an execution mechanism.

## 2. Why Do We Need AI Agents?

Consider a user asking:

"Find the total cost of 15 products if each product costs ₹250, and explain the calculation."

A traditional LLM might calculate the result directly.

However, consider a more complex request:

"Check the inventory, calculate the total order value, and prepare an order summary."

This task may require:

1. Checking inventory using an API.
2. Retrieving product prices from a database.
3. Calculating the total.
4. Preparing a summary.

An AI agent can decide which tools are needed and execute the required operations.

Agents are useful when a task requires multiple steps, external information, or interaction with different systems.

## 3. How Does an AI Agent Work?

A typical agent follows an iterative process.

1. Receive the user's request.
2. Send the request and available tool descriptions to the LLM.
3. The LLM decides whether to answer directly or request a tool.
4. If a tool is requested, the agent runtime executes it.
5. The tool result is returned to the LLM.
6. The LLM evaluates the result and decides what to do next.
7. The process continues until the agent produces a final response or reaches an execution limit.

### Agent Execution Flow

```text id="9zv3gk"
             User Request
                  |
                  v
             AI Agent
                  |
                  v
              LLM Model
                  |
                  v
          Decide Next Action
                  |
             +----+----+
             |         |
             v         v
        Call Tool   Direct Answer
             |
             v
       Execute Tool
             |
             v
        Tool Result
             |
             v
          LLM Model
             |
             v
        Final Answer
```

The agent can repeat the tool-calling cycle when additional actions are required.

This is commonly called the **agent loop**.

## 4. What Are Tools in LangChain?

Tools are functions that an AI agent can use to interact with external systems or perform specific operations.

Examples include:

- Calculator functions.
- Weather APIs.
- Database queries.
- Web searches.
- File operations.
- Python execution.
- Internal company APIs.
- Document retrieval.

A tool provides the agent with a capability that the LLM does not directly perform by itself.

For example, an LLM can decide that it needs current inventory information, but a database tool is required to retrieve the actual inventory.

### Components of a Tool

A LangChain tool generally has:

1. A name.
2. A description.
3. Input parameters.
4. An implementation.
5. A return value.

The tool description is important because the LLM uses it to understand when the tool should be selected.

## 5. Creating Tools Using the `@tool` Decorator

LangChain provides the `@tool` decorator to convert Python functions into tools.

Example:

```python id="x4wz2n"
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b
```

Here:

- `multiply` is the tool name.
- `a` and `b` are input parameters.
- The function performs multiplication.
- The docstring describes what the tool does.

The function's type hints and description help LangChain construct the tool schema.

### Invoke the Tool Directly

A tool can be invoked independently of an agent.

```python id="1v2w5p"
result = multiply.invoke({
    "a": 10,
    "b": 5
})

print(result)
```

Output:

```text id="g82l5q"
50
```

This is useful for testing a tool before integrating it into an agent.

## 6. Creating an Agent in LangChain

LangChain provides the `create_agent` API for creating agents.

The agent is configured with:

- A language model.
- A collection of tools.
- Optional system instructions.

### Example: Calculator Agent

**Step 1: Install Dependencies**

Your existing project already includes `langchain` and `langchain-openai`.

If you are using a separate environment, install them with:

```powershell id="7x3cba"
uv add langchain
uv add langchain-openai
```

**Step 2: Import Libraries**

```python id="f0m3vg"
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
```

**Step 3: Define a Tool**

```python id="z7ndx8"
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b
```

**Step 4: Initialize the LLM**

```python id="5y9u6k"
llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)
```

**Step 5: Create the Agent**

```python id="a8q2w6"
agent = create_agent(
    model=llm,
    tools=[multiply],
    system_prompt="You are a helpful mathematical assistant."
)
```

**Step 6: Invoke the Agent**

```python id="6v3f2j"
result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is 25 multiplied by 16?"
        }
    ]
})

print(result["messages"][-1].content)
```

The model can decide to call the multiplication tool, receive its result, and provide the final answer.

The agent manages the tool-calling cycle.

The exact response may include intermediate messages in addition to the final response.

## 7. Understanding Tool Calling

Tool calling is the mechanism through which an LLM requests the execution of a tool.

The LLM does not necessarily execute the Python function itself.

Instead, it produces a structured tool-call request containing information such as:

- Tool name.
- Arguments.
- Tool-call ID.

The application or agent runtime executes the requested tool and sends the result back to the model.

### Tool Calling Workflow

```text id="9p0xq4"
             User Question
                   |
                   v
               LLM Model
                   |
                   v
           Tool Call Requested
                   |
                   v
           Application Runtime
                   |
                   v
              Execute Tool
                   |
                   v
              Tool Result
                   |
                   v
               LLM Model
                   |
                   v
              Final Answer
```

Tool calling is also known as function calling in many LLM platforms.

The model must support tool calling for this workflow to operate.

## 8. Binding Tools to a Chat Model

LangChain supports binding tools directly to compatible chat models using `bind_tools()`.

This exposes the available tool definitions to the model.

Example:

```python id="3j9r0a"
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

model_with_tools = llm.bind_tools([multiply])

response = model_with_tools.invoke(
    "Calculate 12 multiplied by 8."
)

print(response.tool_calls)
```

The model may return a structured tool call similar to:

```python id="p8w6x2"
[
    {
        "name": "multiply",
        "args": {
            "a": 12,
            "b": 8
        },
        "id": "call_example"
    }
]
```

This demonstrates that the model has requested a tool call.

**Important distinction:** `bind_tools()` makes tools available to the model. It does not, by itself, execute the requested Python functions. The application must execute the tool calls and return their results, or use an agent runtime that manages this process.

## 9. Types of Tools

An agent can use different kinds of tools depending on the application.

### 9.1 Built-in Tools

Some integrations provide ready-made tools for common tasks.

Examples:

- Search tools.
- Database tools.
- File-management tools.
- API tools.

### 9.2 Custom Python Tools

Developers can create tools using Python functions.

Example:

```python id="c4z0pr"
from langchain.tools import tool

@tool
def calculate_discount(price: float, discount: float) -> float:
    """Calculate the discounted price."""
    return price - (price * discount / 100)
```

### 9.3 API-Based Tools

A tool can call an external API to retrieve information or perform an action.

Example:

```python id="q2g5s8"
import requests
from langchain.tools import tool

@tool
def get_user_details(user_id: int) -> str:
    """Retrieve user details using the user ID."""

    response = requests.get(
        f"https://example.com/api/users/{user_id}",
        timeout=10
    )

    response.raise_for_status()

    return response.text
```

This is an illustrative example. A real implementation should use an authorized API, validate responses, handle errors, and protect credentials.

### 9.4 Database Tools

A database tool can retrieve information from a database.

For example:

- Find customer details.
- Retrieve order history.
- Check product inventory.
- Calculate sales summaries.

Database tools should enforce access controls and restrict which operations the agent can perform.

### 9.5 Retrieval Tools

An agent can also use a retriever as a tool.

For example, a technical documentation search tool can retrieve relevant information from Chroma.

This allows an agent to access a knowledge base when necessary.

## 10. Agent vs Traditional RAG Chain

An important distinction exists between a traditional RAG pipeline and an AI agent.

### Traditional RAG

A traditional RAG application generally follows a predefined workflow.

```text id="q6j5kx"
User Query
    |
    v
Retriever
    |
    v
Context Builder
    |
    v
Prompt
    |
    v
LLM
    |
    v
Answer
```

The retrieval process is usually executed according to the application's predefined logic.

### Agent-Based Application

An agent can decide whether retrieval is necessary and which tool to use.

```text id="c9n4rw"
User Query
    |
    v
    Agent
      |
      v
     LLM
      |
      v
 Select Action
      |
   +--+------+
   |         |
   v         v
Retriever  Calculator
   |         |
   v         v
 Results   Results
   |         |
   +----+----+
        |
        v
       LLM
        |
        v
      Answer
```

### Comparison

| Feature | Traditional RAG | AI Agent |
|---|---|---|
| Workflow | Mostly predefined | Can be dynamically selected |
| Retrieval | Usually part of the fixed pipeline | Can be one of several available tools |
| Tool usage | Limited or explicitly wired | Can select tools based on the task |
| Multiple steps | Usually application-controlled | Can involve iterative decisions |
| Complexity | Generally simpler | Generally more complex |
| Predictability | More predictable | Requires additional control and testing |

Traditional RAG is often sufficient for document question answering.

An agent is useful when the task requires decisions, multiple tools, or dynamic workflows.

An agent is not automatically better than a traditional RAG chain. The architecture should match the problem.

## 11. RAG Agent

A RAG agent combines document retrieval with agent-based decision-making.

Instead of retrieving documents for every query using a fixed sequence, the agent can decide when to search the knowledge base.

For example, an employee asks:

"According to the company policy, how many days of leave are available, and what is the difference between casual leave and earned leave?"

The agent might:

1. Search the policy knowledge base.
2. Retrieve information about casual leave.
3. Retrieve information about earned leave.
4. Compare the retrieved information.
5. Generate a combined answer with sources.

A RAG agent can also use other tools when required.

Example tools:

- `search_company_policy`
- `search_employee_handbook`
- `calculate_leave_balance`

This can make the application more flexible than a simple fixed retrieval pipeline.

However, tool selection and answer quality must be evaluated carefully.

## 12. Agent Memory and Conversation State

An agent may need information from earlier interactions to complete a task.

For example:

User: "Find the price of a laptop."

Agent: "Which laptop are you interested in?"

User: "A laptop with 16 GB RAM."

The agent needs the previous conversation to understand what the user means.

It is useful to distinguish two concepts:

### 12.1 Conversation State

Conversation state contains information associated with an ongoing interaction.

It may include:

- Previous messages.
- Tool results.
- Intermediate steps.
- Current task information.

### 12.2 Long-Term Memory

Long-term memory allows relevant information to be stored and retrieved across separate interactions or sessions.

For example:

- User preferences.
- Frequently used settings.
- Previous project information.

Conversation state and long-term memory are not the same thing.

A conversation can retain its messages without having a separate long-term memory system.

In LangChain's current agent architecture, state and persistence are closely related to LangGraph.

## 13. Tool Selection and Agent Reasoning

An agent uses the model's reasoning capabilities to select an appropriate action.

For example:

User request:

"Find the total price of five laptops costing ₹45,000 each."

Available tools:

- `search_product_price`
- `multiply`
- `get_weather`

The agent should recognize that the multiplication tool is relevant.

It does not need to call the weather tool.

Tool descriptions and input schemas help the model choose the correct tool and provide its arguments.

However, tool selection is not guaranteed to be correct.

Developers should validate tool inputs, restrict permissions, and handle unexpected tool calls.

## 14. Multi-Step and Multi-Tool Agents

Some tasks require more than one tool.

Example:

"Find the current price of a product, calculate the price after a 10% discount, and prepare a summary."

Possible execution:

1. Call a product-search tool.
2. Retrieve the product price.
3. Call a discount-calculation tool.
4. Calculate the discounted price.
5. Generate a summary.

The output of one tool may become the input to another tool.

This is an example of multi-step tool orchestration.

The agent decides which actions to perform based on the task and intermediate results.

## 15. Human-in-the-Loop Agents

Some agent actions should require human approval.

For example:

- Sending an email.
- Deleting files.
- Making a financial transaction.
- Updating production data.
- Publishing content.

A human-in-the-loop workflow pauses execution before a sensitive action and requests approval.

### Example Workflow

```text id="w4m6n1"
        User Request
             |
             v
          Agent
             |
             v
       Select Tool
             |
             v
      Approval Required?
             |
        +----+----+
        |         |
       Yes        No
        |         |
        v         v
   Human Review  Execute
        |
     +--+--+
     |     |
   Approve Reject
     |     |
     v     v
  Execute Stop
```

LangGraph provides mechanisms such as interrupts and state persistence for implementing human-in-the-loop workflows.

Human approval is especially important when an agent can perform actions that have external consequences.

## 16. Agent Safety and Security

Agents can be powerful because they can interact with external systems.

This also creates security risks.

Important considerations include:

### 16.1 Tool Permissions

Give each tool only the permissions it needs.

For example, a document-search tool should not automatically have permission to delete documents.

### 16.2 Input Validation

Validate all tool arguments.

Do not assume that arguments generated by an LLM are correct.

### 16.3 Prompt Injection

An external document or webpage may contain malicious instructions.

Retrieved content should be treated as untrusted data, not as instructions that can override system policies.

### 16.4 Sensitive Operations

Require explicit approval for high-impact actions.

### 16.5 API Credentials

Store API keys securely in environment variables or a secrets manager.

Never expose credentials in prompts, logs, or source code.

### 16.6 Execution Limits

Set appropriate limits for:

- Number of tool calls.
- Execution time.
- Maximum iterations.
- Token consumption.
- API usage.

These controls help prevent runaway execution and unexpected costs.

## 17. Agent Evaluation

An agent should be evaluated beyond whether it produces a good final answer.

It is important to measure how well it performs the intermediate actions required to complete a task.

Useful evaluation dimensions include:

### 17.1 Task Completion

Did the agent successfully complete the requested task?

### 17.2 Tool Selection Accuracy

Did the agent select the appropriate tool?

### 17.3 Tool Argument Accuracy

Did it provide valid arguments to the tool?

### 17.4 Tool Execution Success

Did the tools execute successfully?

### 17.5 Final Answer Quality

Was the final response correct, relevant, and complete?

### 17.6 Safety

Did the agent respect permissions and approval requirements?

For more complex applications, evaluate the complete execution trace rather than looking only at the final response.

LangSmith can help trace agent execution, inspect tool calls, and evaluate runs.

## 18. LangChain Agents and LangGraph

LangChain provides high-level agent APIs, while LangGraph provides lower-level orchestration capabilities.

LangChain's current agent implementations use LangGraph primitives.

LangGraph is useful when developers need more control over:

- Workflow state.
- Execution steps.
- Conditional routing.
- Loops.
- Checkpointing.
- Persistence.
- Human approval.
- Multi-agent orchestration.

### LangChain Agent vs Custom LangGraph Workflow

| LangChain Agent | Custom LangGraph Workflow |
|---|---|
| Higher-level agent interface | Lower-level workflow control |
| Faster to get started | More customization |
| Suitable for common tool-using agents | Suitable for complex stateful workflows |
| Agent loop is managed by the framework | Developer defines graph behavior |
| Less orchestration code initially | More explicit workflow design |

Choose a high-level agent when its behavior meets the requirements.

Use a custom LangGraph workflow when the application needs more explicit control over execution.

## 19. Agent Use Cases

AI agents can be used in many practical applications.

### 19.1 Customer Support Agent

Possible tools:

- Search customer records.
- Retrieve order status.
- Check refund policies.
- Create support tickets.

### 19.2 Research Agent

Possible tools:

- Web search.
- Read documents.
- Extract information.
- Summarize research.

### 19.3 Data Analysis Agent

Possible tools:

- Query databases.
- Execute approved Python code.
- Generate charts.
- Prepare reports.

### 19.4 HR Assistant

Possible tools:

- Search HR policies.
- Retrieve leave information.
- Calculate leave balances.
- Create HR requests.

### 19.5 Developer Assistant

Possible tools:

- Search technical documentation.
- Inspect source files.
- Run tests in a controlled environment.
- Explain errors.

The usefulness of an agent depends on the quality of its tools, instructions, and execution controls.

## 20. Common Problems When Building Agents

### Problem 1: Incorrect Tool Selection

**Cause:** The tool descriptions are unclear or multiple tools have overlapping purposes.

**Possible improvements:**

- Use descriptive tool names.
- Write clear docstrings.
- Provide well-defined input schemas.
- Avoid unnecessary tools.

### Problem 2: Invalid Tool Arguments

**Cause:** The model generates arguments that do not match the tool schema.

**Possible improvements:**

- Use type hints.
- Use Pydantic validation.
- Validate inputs before execution.
- Return useful error messages.

### Problem 3: Repeated Tool Calls

**Cause:** The agent does not obtain the information it needs or fails to recognize completion.

**Possible improvements:**

- Improve system instructions.
- Set execution limits.
- Inspect execution traces.
- Return clear tool results.

### Problem 4: Incorrect Final Answers

**Cause:** Tool results may be incomplete, incorrect, or misunderstood.

**Possible improvements:**

- Validate tool output.
- Preserve source information.
- Add verification steps.
- Evaluate final answers against expected results.

### Problem 5: High API Costs

**Cause:** Agents may make multiple model and tool calls for a single request.

**Possible improvements:**

- Limit unnecessary tool calls.
- Use appropriate models.
- Cache repeatable results.
- Set execution limits.
- Monitor token usage.

## 21. Best Practices

1. Build tools with clear names and descriptions.
2. Use structured input schemas.
3. Give agents only the tools they need.
4. Validate every tool argument.
5. Keep tool functions focused on a single responsibility.
6. Handle tool failures gracefully.
7. Set appropriate execution limits.
8. Require human approval for sensitive actions.
9. Treat retrieved documents and external content as untrusted input.
10. Trace tool calls and intermediate steps.
11. Evaluate tool selection separately from final answer quality.
12. Prefer a simple deterministic workflow when an agent is unnecessary.
13. Use LangGraph when more explicit orchestration and state control are required.

## 22. Summary

An AI agent uses an LLM to decide how to complete a task by selecting and invoking tools.

Important concepts include:

- Agents.
- Tools.
- The `@tool` decorator.
- Tool calling.
- `bind_tools()`.
- `create_agent()`.
- Agent execution loops.
- Multi-tool orchestration.
- Conversation state.
- Human-in-the-loop workflows.
- Agent evaluation.
- LangGraph integration.

Traditional RAG applications generally follow a predefined retrieval workflow, whereas agents can dynamically decide whether to retrieve information or use other tools.

Agents are useful for tasks that require multiple actions and decisions, but they introduce additional complexity and security considerations.

## References

- LangChain Agents: https://docs.langchain.com/oss/python/langchain/agents
- LangChain Learn: https://docs.langchain.com/oss/python/learn
- LangChain Tools: https://docs.langchain.com/oss/python/langchain/tools
- LangChain RAG Agent Tutorial: https://docs.langchain.com/oss/python/langchain/rag
- LangGraph Documentation: https://docs.langchain.com/oss/python/langgraph/overview
- LangChain Core Tool Reference: https://reference.langchain.com/python/langchain-core/tools/
- LangSmith Documentation: https://docs.langchain.com/langsmith/home