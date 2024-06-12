from pathlib import Path
from argparse import ArgumentParser
import torch
import trimesh
from mini_dust3r.api import OptimizedResult, inferece_dust3r
from mini_dust3r.model import AsymmetricCroCo3DStereo

def save_as_glb(mesh: trimesh.Trimesh, file_path: Path):
    """
    Save a 3D mesh as a .glb file.
    """
    mesh.export(file_path, file_type='glb')

def main(image_dir: Path):
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
    mesh_file_path = Path("world/optimized_result_mesh.glb")
    point_cloud_file_path = Path("world/optimized_result_point_cloud.glb")
    
    # Save the mesh
    save_as_glb(optimized_results.mesh, mesh_file_path)
    
    # Save the point cloud as a mesh (trimesh can handle point clouds similarly)
    point_cloud_mesh = trimesh.Trimesh(vertices=optimized_results.point_cloud.vertices,
                                       vertex_colors=optimized_results.point_cloud.colors)
    save_as_glb(point_cloud_mesh, point_cloud_file_path)

if __name__ == "__main__":
    # Parse the command line arguments
    parser = ArgumentParser(description="mini-dust3r demo script")
    parser.add_argument("--image-dir", type=Path, help="Directory containing images to process", required=True)
    args = parser.parse_args()
    
    # Call the main function with the provided image directory
    main(args.image_dir)
