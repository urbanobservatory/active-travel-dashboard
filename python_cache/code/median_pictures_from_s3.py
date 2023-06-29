import boto3
import os
import pandas as pd
import cv2
from dotenv import load_dotenv
load_dotenv()

local_folder = os.getenv('img_folder')  # where do you want downloaded images to go

BLOB_NAME = os.getenv('BLOB_NAME')
BLOB_ID = os.getenv('BLOB_ID')
BLOB_PWD = os.getenv('BLOB_PWD')

class Bucket():
    def __init__(self, BLOB_ID, BLOB_PWD, BLOB_NAME):
        self.s3 = boto3.resource('s3', aws_access_key_id=BLOB_ID, aws_secret_access_key=BLOB_PWD)
        self.bucket_name = BLOB_NAME
        self.update_s3_contents()

    def update_s3_contents(self):
        bucket =self.s3.Bucket(self.bucket_name)
        self.current_list_of_all_files_on_s3 = [my_bucket_object.key for my_bucket_object in bucket.objects.filter(Prefix="median/")]

    def download_from_s3(self, src, dst):
        self.s3.Bucket(self.bucket_name).download_file(src,dst)


bucket = Bucket(BLOB_ID, BLOB_PWD, BLOB_NAME)  # initialise session
median_images = bucket.current_list_of_all_files_on_s3  # list of available files

def get_images():
    df = pd.read_csv('location_coordinates.csv')
    locations = df['location'].tolist()

    for location in locations:
        try:
            matching = [i for i in median_images if location in i]
            print(matching[-1])
            bucket.download_from_s3(matching[-1], os.path.join(local_folder, os.path.basename(location+'.jpg')))
        except:
            continue

    for filename in os.listdir(local_folder):
        if '.jpg' in filename:
            img = cv2.imread(local_folder+filename)
            img = cv2.resize(img, (0,0), fx=0.2, fy=0.2)
            cv2.imwrite(local_folder+filename, img)


if __name__ == '__main__':
    # TODO: Get images with timestamp attached to name.
    # Delete images older than available data collected
    # Set a time to collect new images each day (9am?), or if images have not
    # already been collected for that day.
    # Run as its own containerised service.
    get_images()
    

# WARNING! images, although they are 'median' from 5-10sec,
# can still contain recognizable personal features, so please
# apply blurring or resize them down


