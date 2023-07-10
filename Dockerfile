FROM python:3.11.2-alpine3.17

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY resolv.conf /etc/resolv.conf

COPY . .

CMD ["python", "Praccforces.py"]

