# Agentic AI-Based Student Assistant

## 1. Project Overview

Agentic AI-Based Student Assistant is an intelligent student-support application developed using Python, a Large Language Model (LLM), and tool calling.

The system is designed to:

- Understand natural-language requests
- Determine whether a tool is required
- Select the appropriate tool
- Execute the required operation
- Use the tool result
- Generate a clear final response

Unlike a conventional program that follows fixed conditions for every request, this system allows the LLM to decide which available tool should be used based on the user's query.

This demonstrates the fundamental concept of **Agentic AI**, where an AI system can understand a task, decide what action is required, and use available tools to complete it.

---

## 2. Objectives

The main objectives of this project are:

- To develop a simple Agentic AI system using an LLM.
- To enable automatic selection of appropriate tools based on user requests.
- To perform mathematical calculations using a calculator tool.
- To retrieve student department information.
- To retrieve student attendance information.
- To provide normal LLM-based responses for general questions.
- To handle unavailable student information without generating incorrect data.

---

## 3. Technologies Used

- **Python**
- **Groq API**
- **Large Language Model (LLM)**
- **Function Calling / Tool Calling**
- **Python Dictionary**
- **GitHub**
- **python-dotenv**

---

## 4. System Architecture

The system follows a simple agentic workflow:

```text
User Request
     ↓
LLM Understands the Request
     ↓
LLM Decides Whether a Tool is Required
     ↓
Selects the Appropriate Tool
     ↓
Tool Executes the Required Operation
     ↓
Tool Result is Returned to the LLM
     ↓
LLM Generates the Final Response
```

The LLM is responsible for understanding the user's intention and automatically selecting the appropriate tool. The selected tool performs the required operation, and its result is provided back to the LLM for generating the final response.

---

## 5. Available Tools

### Calculator Tool

The Calculator tool performs basic arithmetic operations including:

- Addition
- Subtraction
- Multiplication
- Division
- Percentage calculations

**Example:**

```text
Calculate 250 * 15 / 100
```

**Expected result:**

```text
37.5
```

### Student Information Tool

The Student Information tool retrieves information about a student, including their department.

**Example:**

```text
What department does Arun belong to?
```

**Expected result:**

```text
Arun is from CSE department.
```

### Attendance Tool

The Attendance tool retrieves the attendance percentage of a student.

**Example:**

```text
What is Priya's attendance?
```

**Expected result:**

```text
Priya's attendance is 91%.
```

---

## 6. Student Database

The project currently uses a Python dictionary to store sample student information.

| Student | Department | Attendance |
|---------|------------|------------|
| Arun | CSE | 82% |
| Priya | AI | 91% |

If a student is not available in the database, the system informs the user instead of guessing the information.

---

## 7. Agentic Decision Making

The key feature of this project is **automatic tool selection**.

For example:

| User Request | Agent Decision | Tool |
|--------------|----------------|------|
| Calculate 250 * 15 / 100 | Perform calculation | Calculator |
| What department does Arun belong to? | Retrieve department | Student Information |
| What is Priya's attendance? | Retrieve attendance | Attendance |
| What is Python? | Answer using LLM | No tool |

The system uses automatic tool selection through the LLM rather than relying only on manually written conditions for each type of question.

This allows the LLM to decide whether a tool is necessary and which tool should be used.

---

## 8. Project Structure

```text
agentic-ai-student-assistant/
│
├── agent.py
├── main.py
└── README.md
```

### main.py

The `main.py` file:

- Initializes the Groq client
- Loads environment variables
- Accepts user input
- Runs the agent
- Displays the tool execution information
- Displays the final response

### agent.py

The `agent.py` file contains:

- System instructions
- Student data
- Available tool definitions
- Calculator implementation
- Student information function
- Attendance function
- Tool execution logic
- Main agent workflow

---

## 9. Installation and Execution

### Step 1: Install Required Packages

Install the required Python packages using:

```bash
python3 -m pip install groq python-dotenv
```

### Step 2: Configure the API Key

Create a `.env` file in the project directory and add:

```text
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

**Note:** Do not upload the `.env` file to GitHub.

### Step 3: Run the Application

Run the application using:

```bash
python3 main.py
```

The user can then interact with the Student Assistant through the terminal.

---

## 10. Test Cases

The system can be tested using the following requests.

### Test 1: Calculator

**Input:**

```text
Calculate 250 * 15 / 100
```

**Expected result:**

```text
37.5
```

### Test 2: Student Department

**Input:**

```text
What department does Arun belong to?
```

**Expected result:**

```text
Arun is from CSE department.
```

### Test 3: Student Attendance

**Input:**

```text
What is Priya's attendance?
```

**Expected result:**

```text
Priya's attendance is 91%.
```

### Test 4: General Question

**Input:**

```text
What is Python?
```

**Expected result:**

A normal LLM-generated explanation without unnecessary use of student tools.

### Test 5: Student Not Found

**Input:**

```text
What is Rahul's attendance?
```

**Expected result:**

The system informs the user that Rahul was not found in the student database.

---

## 11. Security

The Groq API key is stored in a `.env` file and must not be uploaded to GitHub.

The `.gitignore` file is used to prevent sensitive files and unnecessary Python cache files from being committed.

Example:

```text
.env
__pycache__/
*.pyc
venv/
.venv/
```

---

## 12. Future Enhancements

The system can be extended by adding:

- More student records
- Marks and grade information
- Timetable details
- Course information
- Database integration
- Web-based interface
- Additional student-support tools
- More advanced AI agent capabilities

---

## 13. Conclusion

The Agentic AI-Based Student Assistant demonstrates the practical use of Large Language Models with tool calling.

The system understands user requests, determines whether a tool is required, selects the appropriate tool, executes the required operation, processes the tool result, and generates a final response.

This project provides a simple and practical demonstration of:

- Agentic AI
- LLM-based decision making
- Function calling
- Tool selection
- Python-based tool execution

It demonstrates how AI agents can be used to build intelligent student-support applications.

---

## 14. Author

**Lina Snowlin**  
B.Tech Artificial Intelligence and Data Science
