FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard/streamlit/app.py dashboard/streamlit/app.py

EXPOSE 8501

CMD ["streamlit", "run", "dashboard/streamlit/app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
