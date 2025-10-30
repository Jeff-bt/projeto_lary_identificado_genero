streamlit run interface.py

.venv\Scripts\activate #windowns
source .venv/bin/activate #linux

uv install --system .

fastapi dev summarize_fastapi.py
