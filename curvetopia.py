import numpy as np
import svgwrite
import cairosvg

colours = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#FFB833', '#8D33FF', '#33FFB3']

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

def fit_bezier_to_polyline(XY):
    n = len(XY)
    P1, P2, P3, P4 = XY[0], XY[n//3], XY[2*n//3], XY[-1]
    return np.array([P1, P2, P3, P4])

def polyline_to_bezier(path_XYs):
    bezier_curves = []
    for XYs in path_XYs:
        bezier_path = []
        for XY in XYs:
            bezier_curve = fit_bezier_to_polyline(XY)
            bezier_path.append(bezier_curve)
        bezier_curves.append(bezier_path)
    return bezier_curves

def bezier_to_svg(bezier_curves, svg_path):
    W, H = 0, 0
    for bezier_path in bezier_curves:
        for bezier_curve in bezier_path:
            W, H = max(W, np.max(bezier_curve[:, 0])), max(H, np.max(bezier_curve[:, 1]))
    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)

    dwg = svgwrite.Drawing(svg_path, profile='tiny', size=(W, H))

    for i, bezier_path in enumerate(bezier_curves):
        path_str = ""
        for bezier_curve in bezier_path:
            path_str += f"M {bezier_curve[0, 0]},{bezier_curve[0, 1]} "
            path_str += f"C {bezier_curve[1, 0]},{bezier_curve[1, 1]} {bezier_curve[2, 0]},{bezier_curve[2, 1]} {bezier_curve[3, 0]},{bezier_curve[3, 1]} "

        dwg.add(dwg.path(d=path_str, stroke=colours[i % len(colours)], fill='none', stroke_width=3))

    dwg.save()

    png_path = svg_path.replace('.svg', '_new.png')
    fact = max(1, 1024 // min(H, W))
    cairosvg.svg2png(url=svg_path, write_to=png_path, parent_width=W, parent_height=H,
                     output_width=fact*W, output_height=fact*H, background_color='white')
    return png_path

def main(csv_path, output_svg_path):

    path_XYs = read_csv(csv_path)

    bezier_curves = polyline_to_bezier(path_XYs)

    bezier_to_svg(bezier_curves, output_svg_path)

csv_file_path = 'frag0.csv'
svg_file_path = 'outputfile_path.svg'
main(csv_file_path, svg_file_path)
