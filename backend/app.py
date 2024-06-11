from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config
import os

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
CORS(app)

s3_client = Config.create_s3_client()

def get_presign_url(filename):
    try:
        if not filename:
            return jsonify({'error': 'No filename is found!'}), 400
        
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': Config.S3_BUCKET_NAME,
                'Key': filename,
                'ResponseContentDisposition': 'attachment; filename=' + filename    
            },
            ExpiresIn=3600
        )
        return response
    except Exception as e:
        return str(e), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'})

@app.route('/healthcheck', methods=['GET'])
def health_check():
    return jsonify({'message': 'OK!'})

@app.route('/get-image', methods=['GET'])
def get_image():
    filename = request.args.get('filename')
    print("filename", filename)
    return get_presign_url(filename)

@app.route('/get-models', methods=['GET'])
def get_all_models():
    try:
        response = s3_client.list_objects_v2(
            Bucket=Config.S3_BUCKET_NAME,
            Prefix='output/'
        )
        files = []
        for obj in response.get('Contents', []):
            key = obj.get('Key')
            if key.endswith('.glb'):
                files.append(key)
        return jsonify(files)
    except Exception as e:
        return str(e), 500
    
def upload_to_s3(file, filename):
    try:
        s3_client.upload_fileobj(
            file,
            Config.S3_BUCKET_NAME,
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

    for file in files:
        filename = secure_filename(file.filename)
        upload_to_s3(file, filename)

    return jsonify({'message': 'OK'}), 200

# Serve the Vue.js application
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
