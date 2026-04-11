FROM python:3.14-slim

COPY requirements.txt .
RUN pip install -r requirements.txt --root-user-action=ignore

COPY *.py .
CMD ["flask", "--app=api-server", "run", "--host=0.0.0.0"]
