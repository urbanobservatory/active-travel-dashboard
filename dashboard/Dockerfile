FROM python:3.9
RUN pip install dash pandas plotly python-dotenv requests numpy dash-bootstrap-components gunicorn
ADD code/ /code/
WORKDIR /code/
CMD python3 app.py & gunicorn --bind 0.0.0.0:80  app:server