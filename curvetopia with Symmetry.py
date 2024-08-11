import numpy as np
import matplotlib.pyplot as plt
import svgwrite
import cairosvg
from scipy.interpolate import splprep, splev
from scipy.spatial import ConvexHull

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []

    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []

        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)

        path_XYs.append(XYs)

    return path_XYs

def save_original_image(paths_XYs, save_path='original.png'):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))

    for XYs in paths_XYs:
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], color='black', linewidth=2)

    ax.set_aspect('equal')
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close()

def plot(paths_XYs, save_path=None):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))

    colours = ['#FFFF00']  # Use yellow color as in the provided image

    for i, XYs in enumerate(paths_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)

    ax.set_aspect('equal')
    plt.axis('off')
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    
    plt.close()

def detect_open_shape(XY):
    return not np.allclose(XY[0], XY[-1])

def close_shape(XY):
    if detect_open_shape(XY):
        XY = np.vstack([XY, XY[0]])  # Close the shape by adding the first point at the end
    return XY

def is_symmetric(XY, tolerance=1e-2):
    # Check for reflection symmetry
    centroid = np.mean(XY, axis=0)
    reflection_lines = []
    
    for angle in np.linspace(0, np.pi, 180):
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)
        
        # Reflect points over the line
        reflected_points = np.copy(XY)
        reflected_points[:, 0] = cos_angle * (XY[:, 0] - centroid[0]) + sin_angle * (XY[:, 1] - centroid[1]) + centroid[0]
        reflected_points[:, 1] = -sin_angle * (XY[:, 0] - centroid[0]) + cos_angle * (XY[:, 1] - centroid[1]) + centroid[1]
        
        distances = np.sqrt(np.sum((reflected_points - XY)**2, axis=1))
        if np.all(distances < tolerance):
            reflection_lines.append(angle)
    
    return len(reflection_lines) > 0

def fit_bezier_curve(XY, num_points=100):
    tck, _ = splprep([XY[:, 0], XY[:, 1]], s=0)
    u_fine = np.linspace(0, 1, num_points)
    x_fine, y_fine = splev(u_fine, tck)
    return np.column_stack((x_fine, y_fine))

def polylines2svg(paths_XYs, svg_path):
    W, H = 0, 0
    for path_XYs in paths_XYs:
        for XY in path_XYs:
            W, H = max(W, np.max(XY[:, 0])), max(H, np.max(XY[:, 1]))

    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)
    dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges')

    group = dwg.g()
    for i, path in enumerate(paths_XYs):
        path_data = []
        c = '#FFFF00'  # Use yellow color
        for XY in path:
            path_data.append(("M", (XY[0, 0], XY[0, 1])))
            for j in range(1, len(XY)):
                path_data.append(("L", (XY[j, 0], XY[j, 1])))
            if not np.allclose(XY[0], XY[-1]):
                path_data.append(("L", (XY[0, 0], XY[0, 1])))  # Close the path
        group.add(dwg.path(d=path_data, fill='none', stroke=c, stroke_width=2))

    dwg.add(group)
    dwg.save()

    png_path = svg_path.replace('.svg', '.png')
    fact = max(1, 1024 // min(H, W))
    cairosvg.svg2png(url=svg_path, write_to=png_path, parent_width=W, parent_height=H,
                     output_width=fact*W, output_height=fact*H, background_color='white')

def main():
    # Replace with your CSV file path
    csv_path = 'frag2.csv'  
    paths_XYs = read_csv(csv_path)
    
    # Save and display original image
    save_original_image(paths_XYs, save_path='original_image.png')
    
    # Process each shape
    for i, path_XYs in enumerate(paths_XYs):
        for j, XY in enumerate(path_XYs):
            XY = close_shape(XY)  # Ensure the shape is closed
            if is_symmetric(XY):  # Check if the shape is symmetric
                XY = fit_bezier_curve(XY)  # Fit Bezier curve if symmetric
            paths_XYs[i][j] = XY

    # Beautify and save the final image
    plot(paths_XYs, save_path='beautified_image.png')

    # Convert to SVG and Export
    svg_path = 'output.svg'
    polylines2svg(paths_XYs, svg_path)

if _name_ == "_main_":
    main()