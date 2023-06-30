FROM python:3.9
RUN pip install dash pandas plotly python-dotenv requests numpy dash-bootstrap-components boto3
ADD code/ /code/
WORKDIR /code/
CMD python3 -u get_video_counts_and_locations.py