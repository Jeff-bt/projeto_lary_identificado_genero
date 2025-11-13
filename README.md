streamlit run interface.py

.venv\Scripts\activate #windowns
source .venv/bin/activate #linux

uv pip install --system . --no-cache-dir

fastapi dev summarize_fastapi.py
