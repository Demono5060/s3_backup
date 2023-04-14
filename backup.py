import boto3
from botocore.client import BaseClient
from config import *
import subprocess


def delete_old_backups(s3client: BaseClient) -> None:
    '''
    :param s3client: s3 client, need to call s3 api functions
    '''
    for service in SERVICES:
        backups = s3client.list_objects(Bucket=service.get('bucket')).get('Contents')
        if len(backups) > BACKUPS_SIZE:
            s3.delete_object(Bucket=service.get('bucket'), Key=backups[-1].get('Key'))


def create_backups() -> None:
    for service in SERVICES:
        try:
            command = service.get('command').replace('{BUFFER_PATH}', BUFFER_PATH).replace('{NAME}', service.get('name'))
            subprocess.call(command, shell=True)
            if LOGS:
                LOG_FILE.write(f'[{DATETIME}] {service.get("name")} backup successfully created \n')

        except subprocess.CalledProcessError as error:
            if LOGS:
                LOG_FILE.write(f'[{DATETIME}] Error while making {service.get("name")}: {error} \n')


def upload_backups(s3client: BaseClient) -> None:
    """
    :param s3client: s3 client, need to call s3 api functions
    """
    for service in SERVICES:
        try:
            s3client.upload_file(BUFFER_PATH+service.get('name'), service.get('bucket'),
                                 service.get('bucket_path')+service.get('name'))
            subprocess.call(f'rm {BUFFER_PATH+service.get("name")}', shell=True)
        except subprocess.CalledProcessError as error:
            if LOGS:
                LOG_FILE.write(f'[{DATETIME}] Error while making {service.get("name")}: {error} \n')


if __name__ == '__main__':
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    create_backups()
    upload_backups(s3)
    delete_old_backups(s3)
