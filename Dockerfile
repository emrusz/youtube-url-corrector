FROM python:3.11.6

WORKDIR /usr/src/units

COPY requirements.txt .
RUN pip install -r requirements.com

COPY bot.py .

CMD ["python", "bot.py"]
