FROM python:3.9
RUN pip install dash pandas plotly python-dotenv requests numpy dash-bootstrap-components gunicorn
ADD code/ /code/
WORKDIR /code/
ENV PYTHONUNBUFFERED=1

CMD python3 app.py