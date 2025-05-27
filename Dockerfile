
FROM python:3.10-slim

WORKDIR /app

COPY . /app
RUN pip install --upgrade pip && pip install transformers matplotlib fpdf

EXPOSE 8080

CMD ["python3", "yggdrasil/yggdrasil_alpha.py"]
