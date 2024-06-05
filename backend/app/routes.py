from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import boto3
import os

# Create a Blueprint for routes
upload_bp = Blueprint('upload', __name__)

# Configure AWS credentials
AWS_ACCESS_KEY_ID = 'YOUR_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_ACCESS_KEY'
S3_BUCKET_NAME = 'YOUR_S3_BUCKET_NAME'

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


@upload_bp.route('/upload', methods=['POST'])
def upload_files():
    # Check if files were uploaded
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files found'}), 400

    files = request.files.getlist('files[]')

    uploaded_files = []
    for file in files:
        # Generate a unique filename
        filename = secure_filename(file.filename)
        # Save file to a temporary location
        file_path = os.path.join('app/static', filename)
        file.save(file_path)

        # Upload file to S3
        s3_key = f'uploads/{filename}'
        s3_client.upload_file(file_path, S3_BUCKET_NAME, s3_key)

        # Add uploaded file details to the list
        uploaded_files.append({
            'filename': filename,
            'url': f'https://{S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}'
        })

    return jsonify({'files': uploaded_files}), 200
