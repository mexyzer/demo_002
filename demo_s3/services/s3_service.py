import base64
from datetime import datetime
from odoo import models, fields, api
import boto3
from odoo.exceptions import UserError
from io import BytesIO


class S3Service:

    @staticmethod
    def _get_s3_client(env):
        params = {
            'endpoint_url': env['ir.config_parameter'].sudo().get_param('demo_s3.endpoint_url'),
            'aws_access_key_id': env['ir.config_parameter'].sudo().get_param('demo_s3.access_key_id'),
            'aws_secret_access_key': env['ir.config_parameter'].sudo().get_param('demo_s3.secret_access_key'),
            'region_name': env['ir.config_parameter'].sudo().get_param('demo_s3.region'),
        }
        return boto3.client('s3', **params)

    @staticmethod
    def _get_default_bucket_name(env):
        return env['ir.config_parameter'].sudo().get_param('demo_s3.bucket')

    @staticmethod
    def _get_cdn_file_url(env, file_name):
        public_cdn_url = env['ir.config_parameter'].sudo().get_param('demo_s3.public_cdn_url')
        return f"{public_cdn_url}/{file_name}"

    @staticmethod
    def sanitize_file_name(file_name):
        file_name = file_name.lower().replace(' ', '_')

        if '.' in file_name:
            parts = file_name.split('.')
            base_name = '_'.join(parts[:-1])  # Join all parts except the last one with underscores
            ext = parts[-1]  # Last part as the extension
        else:
            base_name = file_name
            ext = ''

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        unique_file_name = f"{base_name}_{timestamp}.{ext}" if ext else f"{base_name}_{timestamp}"

        return unique_file_name

    @staticmethod
    def upload_file(env, file_name, file_data):
        s3 = S3Service._get_s3_client(env)
        bucket_name = S3Service._get_default_bucket_name(env)

        # unique_file_name = S3Service._sanitize_file_name(file_name)

        try:
            if isinstance(file_data, str):
                file_data = base64.b64decode(file_data)

            file_stream = BytesIO(file_data)

            s3.upload_fileobj(file_stream, bucket_name, file_name, ExtraArgs={'ACL': 'public-read'})

            file_url = S3Service._get_cdn_file_url(env, file_name)

            return file_url

        except Exception as e:
            raise UserError(f"Failed to upload file {file_name} to S3: {str(e)}")

    @staticmethod
    def download_file(env, object_name, file_name):
        s3 = S3Service._get_s3_client(env)
        bucket_name = S3Service._get_default_bucket_name(env)

        try:
            s3.download_file(bucket_name, object_name, file_name)
        except Exception as e:
            raise UserError(f"Failed to download file {file_name} from S3: {str(e)}")
        return True

    @staticmethod
    def delete_file(env, filename):
        s3 = S3Service._get_s3_client(env)
        bucket_name = S3Service._get_default_bucket_name(env)

        try:
            s3.delete_object(Bucket=bucket_name, Key=filename)
        except Exception as e:
            raise UserError(f"Failed to delete file {filename} from S3: {str(e)}")
        return True
