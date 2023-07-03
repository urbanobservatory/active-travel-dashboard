FROM python:3.9
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN pip3 install dash pandas plotly python-dotenv requests numpy dash-bootstrap-components boto3 opencv-python
ADD code/ /code/
WORKDIR /code/
CMD python3 -u get_video_counts_and_locations.py