FROM python:3.11

WORKDIR /app
COPY requirements/ requirements
 
RUN pip install -r requirements/api.txt
RUN pip install -r requirements/dev.txt

COPY . .

CMD ["python", "src/main.py"]