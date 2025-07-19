## 🚀 How to Use This App

Follow these steps to set up and run the RAG-based MCQ Generator on your local machine:

---

### ✅ Step 1: Run Ollama (LLM Engine)
Make sure [Ollama](https://ollama.com/) is installed and running locally on your Windows system.

```bash
ollama run llama3
```

### ✅ Step 2: Create a Conda Environment

```bash
conda create -n rag_env python=3.10
conda activate rag_env
```

### ✅ Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### ✅ Step 4: Run the Streamlit App

```bash
streamlit run app.py
```

### ✅ Step 5: Upload Documents

Upload one or more documents (`.pdf`, `.docx`, `.pptx`, or `.txt`) through the web interface.

### ✅ Step 6: Enter a Prompt

> Generate 15 MCQs with A, B, C, D options and highlight the correct answer.

### 👤 Author
Developed by **Muhammad Hassan Saboor**

### ThankYou 
