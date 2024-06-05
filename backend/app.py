# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)



@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'})

# @app.route('/upload-images', methods=['POST'])
# def upload_images():
#     print("triggerd")
#     return jsonify({'message': 'Hello, World!'})

@app.route('/get-image', methods=['GET'])
def get_image():
    filename = request.args.get('filename')
    print("filename", filename)
    return get_presign_url(filename)




def get_presign_url(filename):
    try:
        if not filename:
            return jsonify({'error': 'No filename is found!'}), 400
        
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': S3_BUCKET_NAME,
                'Key': filename,
                'ResponseContentDisposition': 'attachment; filename=' + filename
            },
            ExpiresIn=3600
        )
        return response
    except Exception as e:
        return str(e)
    
def upload_to_s3(file, filename):
    try:
        s3_client.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            filename
        )
        return file.filename
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files are found!'}), 400

    files = request.files.getlist('files')
    file_urls = []
    
    print("len(files)", len(files))

    for file in files:
        filename = secure_filename(file.filename)
        upload_to_s3(file, filename)

    return jsonify({'message': 'OK'}), 200

if __name__ == '__main__':
    app.run(debug=True)
