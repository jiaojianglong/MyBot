FROM python:3.5

COPY ./requirements /usr/local/bin/MyBot/requirements
WORKDIR /usr/local/bin/MyBot
RUN pip install -r requirements -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./chat_bot /usr/local/bin/MyBot/chat_bot
COPY ./data /usr/local/bin/MyBot/data

CMD ["python", "./chat_bot/start.py"]