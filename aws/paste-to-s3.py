import os
import boto3
import logging
import argparse
import datetime


def create_s3_client():
    """
    Creates an S3 client.

    :return: boto3 S3 client object
    """
    
    try:
      s3_client = boto3.client("s3")
      return s3_client
    except Exception as e:
      raise Exception(e)


def setup_logging():
    """
    Set up logging for the program. Print INFO messages to console and save all messages to /tmp/paste-to-s3.log file.

    :return: logger
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create console handler and set level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # create file handler and set level to INFO
    file_handler = logging.FileHandler("/tmp/paste-to-s3.log")
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger

def create_bucket_if_not_exists(bucket_name):
    """
    Creates an S3 bucket with the given name if it does not already exist.

    :param bucket_name: str, name of the bucket to create
    :return: None
    """
    s3_client = create_s3_client()

    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logging.info(f"Bucket {bucket_name} already exists.")
    except:
        try:
          s3_client.create_bucket(Bucket=bucket_name)
          logging.info(f"Bucket {bucket_name} created.")
        except Exception as e:
          raise Exception(e)

    # Set the bucket policy to delete objects older than 1 year
    lifecycle_config = {
        "Rules": [
            {
                "Expiration": {"Days": 365},
                "Status": "Enabled",
                "NoncurrentVersionExpiration": {"NoncurrentDays": 365},
                "Filter": {"Prefix": ""},
                "ID": "Delete objects older than 1 year",
                "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7},
            }
        ]
    }

    s3_client.put_bucket_lifecycle_configuration(Bucket=bucket_name, LifecycleConfiguration=lifecycle_config)
    logger.info(f"Bucket {bucket_name} lifecycle policy set.")


def upload_file_to_s3(filename, bucket_name):
    """
    Uploads the file to S3 and returns a pre-signed URL for viewing the file.

    :param filename: str, name of the file to upload
    :param bucket_name: str, name of the bucket to upload the file to
    :return: str, pre-signed URL for viewing the file
    """
    s3_client = create_s3_client()

    # Append ISO 8601 date to the uploaded file name so it stays unique if the same file is uploaded again.
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    object_key = f"{timestamp}-{filename}"

    # Upload the file to S3
    try:
      with open(filename, "rb") as f:
          s3_client.upload_fileobj(f, bucket_name, object_key)

      # Generate a pre-signed URL for viewing the file
      url = s3_client.generate_presigned_url(
          "get_object",
          Params={"Bucket": bucket_name, "Key": object_key},
          ExpiresIn=0,
          HttpMethod="GET",
      )

    except Exception as e:
      raise Exception(e)

    logger.info(f"File {filename} uploaded to {bucket_name} as {object_key}.")
    return url


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Uploads a file to S3 and generates a pre-signed URL.')
    parser.add_argument('-f', '--file', type=str, help='The path of the file to upload')
    args = parser.parse_args()

    logger = setup_logging()

    # setup bucket
    bucket_name = 'code-pastes'
    create_bucket_if_not_exists(bucket_name)
    
    # Upload file
    logger.info(f"uploading {args.file} to S3")
    presigned_url = upload_file_to_s3(bucket_name, file_path)
    logger.info(presigned_url)
