# Use a imagem base Python
FROM python:3.8
COPY /app .
EXPOSE 80
ENTRYPOINT ["python", "Server/server.py"]
