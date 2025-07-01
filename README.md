Here's a template for your Bank Bot project 👇

# 🏦 FinBot 360

This is an AI-powered chatbot built using Django and LangChain.  
It can answer banking-related queries like:
- Account balance
- Loan policies
- Branch locator
- Document guidance
- Complaint/ticket registration
And also it answer's knowledge base Questions also

---

## 🚀 Features

- ✅ Chat with AI using LangChain and LLM
- ✅ Uses PDF documents for real banking data (RAG)
- ✅ Persistent memory using `chat_memory.json`
- ✅ Built with Python and Django

---

## 📁 Project Structure

gemini_chatbot_project/
│
├── chatbot/
│   ├── __pycache__/
│   ├── bank_docs/
│   ├── migrations/
│   ├── templates/
│   │   └── index.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── llm_config.py
│   ├── models.py
│   ├── rag_tools.py
│   ├── tests.py
│   ├── tools.py
│   ├── views.py
│
├── gemini_chatbot_project/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── .env
├── .gitignore
├── chat_memory.json
├── db.sqlite3
├── manage.py
├── README.md
├── requirements.txt


---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
    git clone https://github.com/surendrakunchanapalli/FinBot_360.git
    cd gemini_chatbot_project

2. Create and activate virtual environment

    python -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On Mac/Linux

3. Install dependencies

    pip install -r requirements.txt

4. Run the project

    python manage.py runserver

📄 Example PDF Files Used

    bank_terms.pdf
    These are loaded and used for RAG-based responses.

👨‍💻 Author
    Surendra Kunchanapalli
    Python Developer Intern
    MBA Finance Graduate

📜 License
This project is for educational and demo purposes only.

