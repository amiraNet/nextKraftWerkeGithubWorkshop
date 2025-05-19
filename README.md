# Virtual Power Plant Dashboard App (Updated)

This project combines a FastAPI backend (Virtual Power Plant API) with a Streamlit frontend (Interactive Dashboard).

## Prerequisites

- Python 3.10+
- (Optional) Docker & Docker Compose

## Installation & Run

1. **Create & activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate     # macOS/Linux
   # or on Windows PowerShell:
   # .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**:
   ```bash
   python3 -m pip install --upgrade pip
   python3 -m pip install -r requirements.txt
   ```

3. **Run the FastAPI backend**:
   ```bash
   uvicorn vpp.main:app --reload --app-dir src
   ```

4. **In a new terminal**, **run the Streamlit dashboard**:
   ```bash
   streamlit run app.py
   ```

5. **Access**:
   - API docs: http://127.0.0.1:8000/docs
   - Dashboard: http://127.0.0.1:8501

