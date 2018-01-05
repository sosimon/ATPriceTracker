FROM tiangolo/uwsgi-nginx-flask:python3.6

# copy requirements.txt
COPY ./app/requirements.txt /tmp/

# upgrade pip and install requirements
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

# copy app code
COPY ./app /app
