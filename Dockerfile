FROM python:3 as base

# copy source code
COPY . .

# install dependencies
RUN pip install -r requirements.txt

# start app
CMD ["python", "main.py"]