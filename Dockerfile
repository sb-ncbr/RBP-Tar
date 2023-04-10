FROM python:3.10-alpine

# upgrade pip
RUN pip install --upgrade pip

# get curl for healthchecks
RUN apk add curl

# permissions and nonroot user for tightened security
RUN adduser -D 1000 -u 1000
RUN mkdir /home/app/ && chown -R 1000:1000 /home/app
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R 1000:1000 /var/log/flask-app
WORKDIR /home/app
USER 1000

# copy all the files to the container
COPY --chown=1000:1000 . .

# venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN export FLASK_APP=app.py
RUN pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 5000

CMD ["python", "app.py"]
