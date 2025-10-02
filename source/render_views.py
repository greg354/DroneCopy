import trimesh
import pyrender
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def align_model_by_bounding_box(mesh):
    extents = mesh.extents  # [width_x, height_y, depth_z]

    # Sort axes by size: longest is front↔back, middle is left↔right, shortest is bottom↔top
    sorted_axes = np.argsort(extents)[::-1]

    # Map those to canonical axes
    # 0: X, 1: Y, 2: Z
    # Let's say we want:
    # - longest → Z (front-back)
    # - middle → X (left-right)
    # - shortest → Y (bottom-top)

    target_axes = [2, 0, 1]  # Map from sorted to desired

    # Build rotation matrix from current → target
    R = np.zeros((3, 3))
    for i, axis in enumerate(sorted_axes):
        R[target_axes[i], axis] = 1.0

    transform = np.eye(4)
    transform[:3, :3] = R
    mesh.apply_transform(transform)

def render_view(mesh, camera_pose, view_name, output_folder):
    scene = pyrender.Scene(bg_color=[200, 200, 200, 255])  # Light gray background

    # Support materials (for GLB texture realism)
    render_mesh = pyrender.Mesh.from_trimesh(mesh, smooth=False)
    scene.add(render_mesh)

    camera = pyrender.OrthographicCamera(xmag=0.5, ymag=0.5)
    scene.add(camera, pose=camera_pose)

    light = pyrender.DirectionalLight(color=np.ones(3), intensity=4.0)
    scene.add(light, pose=camera_pose)

    r = pyrender.OffscreenRenderer(800, 600)
    color, _ = r.render(scene)
    r.delete()

    output_path = output_folder / f"{view_name}.png"
    plt.imsave(str(output_path), color)

def get_pose(view):
    poses = {
        "front":  [0, 0, 5],     # Z+ is front bumper
        "back":   [0, 0, -5],    # Z- is rear
        "left":   [-5, 0, 0],    # X- is left side
        "right":  [5, 0, 0],     # X+ is right side
        "top":    [0, 5, 0],     # Y+ is top (looking down)
    }
    ups = {
        "front":  [0, 1, 0],
        "back":   [0, 1, 0],
        "left":   [0, 1, 0],
        "right":  [0, 1, 0],
        "top":    [0, 0, -1],  # Looking from above (Y+), Z- is up
    }
    eye = np.array(poses[view], dtype=np.float64)
    up = np.array(ups[view], dtype=np.float64)
    target = np.array([0, 0, 0], dtype=np.float64)

    return look_at(eye, target, up)

def look_at(eye, target, up):
    eye = np.array(eye, dtype=np.float64)
    target = np.array(target, dtype=np.float64)
    up = np.array(up, dtype=np.float64)

    z = eye - target
    z /= np.linalg.norm(z)

    x = np.cross(up, z)
    if np.linalg.norm(x) < 1e-6:
        # Up vector is parallel to z — fix by using alternative up
        up = np.array([0, 1, 0], dtype=np.float64) if not np.allclose(up, [0, 1, 0]) else np.array([1, 0, 0], dtype=np.float64)
        x = np.cross(up, z)
    x /= np.linalg.norm(x)

    y = np.cross(z, x)

    m = np.eye(4, dtype=np.float64)
    m[0:3, 0] = x
    m[0:3, 1] = y
    m[0:3, 2] = z
    m[0:3, 3] = eye
    return m

if __name__ == "__main__":
    # Setup paths
    root = Path(__file__).resolve().parent.parent
    model_path = root / "data" / "processed" / "generic_sedan_car.glb"
    output_folder = root / "data" / "renders"
    output_folder.mkdir(parents=True, exist_ok=True)

    # Load mesh, normalize scale and center it
    loaded = trimesh.load(model_path, force='scene')
    if isinstance(loaded, trimesh.Scene):
        mesh = trimesh.util.concatenate(loaded.dump())  # preserve materials
    else:
        mesh = loaded

    mesh.apply_translation(-mesh.centroid)
    mesh.apply_scale(1.0 / mesh.scale)  # normalize to unit cube
    align_model_by_bounding_box(mesh)

    for view in ["front", "back", "left", "right", "top"]:
        pose = get_pose(view)
        render_view(mesh, pose, view, output_folder)

    print("✅ All 2D views rendered to /data/renders")
