FROM python:3 as base

# copy source code
RUN git clone https://github.com/hampta/gamebanana2discord.git
WORKDIR /gamebanana2discord

# install dependencies
RUN pip install -r requirements.txt

# start app
CMD ["python", "main.py"]