FROM python:3.6

WORKDIR /usr/src/app

COPY code/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./code/main.py" ]