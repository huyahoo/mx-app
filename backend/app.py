from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config
import os
import torch
import trimesh
from pathlib import Path
from mini_dust3r.api import OptimizedResult, inferece_dust3r
from mini_dust3r.model import AsymmetricCroCo3DStereo

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

@app.route('/api/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/healthcheck', methods=['GET'])
def health_check():
    return jsonify({'message': 'OK!'})

@app.route('/api/get-image', methods=['GET'])
def get_image():
    filename = request.args.get('filename')
    return get_presign_url(filename)

@app.route('/api/get-models', methods=['GET'])
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
                files.append({
                    'key': key,
                    'last_modified': obj.get('LastModified')
                })

        # Sort files by last modified time in descending order
        files.sort(key=lambda x: x['last_modified'], reverse=True)
        sorted_files = [file['key'] for file in files]
        
        return jsonify(sorted_files)
    except Exception as e:
        return str(e), 500

def upload_to_s3(file, filename):
    try:
        s3_client.upload_fileobj(
            file,
            Config.S3_BUCKET_NAME,
            filename
        )
        return filename
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def save_as_glb(mesh: trimesh.Trimesh, file_path: Path):
    """
    Save a 3D mesh as a .glb file.
    """
    mesh.export(file_path, file_type='glb')

def run_inference_and_upload(image_dir: Path, output_filename: str):
    # Determine the device to use for inference
    if torch.backends.mps.is_available():
        device = "mps"
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    
    # Load the pre-trained model and move it to the appropriate device
    model = AsymmetricCroCo3DStereo.from_pretrained("naver/DUSt3R_ViTLarge_BaseDecoder_512_dpt").to(device)
    
    # Perform inference and get the optimized results
    optimized_results: OptimizedResult = inferece_dust3r(
        image_dir_or_list=image_dir,
        model=model,
        device=device,
        batch_size=1,
    )
    
    # Save the optimized results as .glb files
    mesh_file_path = Path(f"/tmp/{output_filename}")
    
    # Save the mesh
    save_as_glb(optimized_results.mesh, mesh_file_path)
    
    # Upload the .glb file to S3
    with open(mesh_file_path, "rb") as file:
        upload_to_s3(file, f"output/{output_filename}")

@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files are found!'}), 400

    if 'objectName' not in request.form:
        return jsonify({'error': 'No object name found!'}), 400

    files = request.files.getlist('files')
    object_name = request.form['objectName']

    # Use a directory in /tmp for temporary storage
    image_dir = Path("/tmp/uploaded_images")
    image_dir.mkdir(parents=True, exist_ok=True)

    # Clear the directory before saving new files
    for file_path in image_dir.iterdir():
        file_path.unlink()

    for file in files:
        filename = secure_filename(file.filename)
        # upload_to_s3(file, filename)
        
        file_path = image_dir / filename
        file.save(file_path)

    # Run inference and upload results to S3
    run_inference_and_upload(image_dir, f"{object_name}.glb")

    # Clean up uploaded files
    for file_path in image_dir.iterdir():
        file_path.unlink()
    image_dir.rmdir()

    return jsonify({'message': 'OK'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
