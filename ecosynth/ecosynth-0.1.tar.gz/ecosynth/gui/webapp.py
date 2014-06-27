import os
import webbrowser

from bottle import route
from bottle import run
from bottle import template
from bottle import static_file
from bottle import redirect
from bottle import request

from bottle import SimpleTemplate

from ecosynth import postprocess as pp

directory = os.path.dirname(__file__)


@route('/hello/<name>')
def example(name):
    return template('<b>You have reached the {{name}} page</b>!', name=name)


@route('/')
def toIndex():
    redirect('/Ecosynth/')


@route('/Ecosynth/')
def index():
    f = open(
        os.path.join(directory, "static/html/index.html"))
    return f


@route('/Ecosynth/Acquisition')
def acquisition():
    pass


@route('/Ecosynth/Generation')
def generation():
    pass


@route('/Ecosynth/PostProcessing', method="GET")
def send_postprocessing_form():
    f = open(
        os.path.join(directory, "static/html/postprocess_form.html"))

    return f


@route('/Ecosynth/PostProcessing', method="POST")
def run_postprocessing():

    # Fetch Inputs
    out_file = request.files.get('out_file')
    log_file = request.files.get('log_file')

    try:
        msl_float = float(request.forms.get('msl_float'))
    except:
        print "Error: could not parse msl_float value"
        print "msl_float set to 0.0"
        msl_float = 0.0

    output_dir_name = request.forms.get('output_dir_name')
    print output_dir_name
    output_dir_path = os.path.join(os.getcwd(), output_dir_name)
    print output_dir_path

    if not os.path.isdir(output_dir_path):
        os.mkdir(output_dir_path)

    # Data Processing
    gps_filepath_out = os.path.join(output_dir_path, 'gps_file.txt')
    cam_filepath_out = os.path.join(output_dir_path, 'geo_camera_array.txt')
    ply_filepath_out = os.path.join(output_dir_path, 'geo_filtered.ply')
    txt_filepath_out = os.path.join(output_dir_path, 'xyzrgb_array.txt')
    params_filepath_out = os.path.join(output_dir_path, 'params.txt')
    quality_metrics_filepath_out = os.path.join(output_dir_path, 'quality_metrics.txt')

    gps_file_out = open(gps_filepath_out, 'w')
    cam_file_out = open(cam_filepath_out, 'w')
    ply_file_out = open(ply_filepath_out, 'w')
    txt_file_out = open(txt_filepath_out, 'w')
    params_file_out = open(params_filepath_out, 'w')
    quality_metrics_file_out = open(quality_metrics_filepath_out, 'w')

    cr_object = pp.postprocess.run(
        out_file.file, log_file.file, msl_float, cams_geo_file=cam_file_out, ply_file=ply_file_out, points_txt_file=txt_file_out, gps_file=gps_file_out, logger_file=quality_metrics_file_out, helm_params_file=params_file_out)

    gps_file_out.close()
    cam_file_out.close()
    ply_file_out.close()
    txt_file_out.close()
    params_file_out.close()

    # Analysis
    color_raster = cr_object.get_color_raster()
    q95_raster = cr_object.get_Q95_elevation_raster()
    point_density_raster = cr_object.get_point_density_raster()

    color_filepath_out = os.path.join(output_dir_path, 'color.png')
    q95_filepath_out = os.path.join(output_dir_path, 'q95.png')
    pd_filepath_out = os.path.join(output_dir_path, 'point_density.png')

    color_file = open(color_filepath_out, 'w')
    q95_file = open(q95_filepath_out, 'w')
    pd_file = open(pd_filepath_out, 'w')

    cr_object.plot_raster_colors(
        color_raster, title="Color Raster", png_file=color_file)
    cr_object.plot_raster_heatmap(
        q95_raster, title="Q95 Raster", png_file=q95_file)
    cr_object.plot_raster_heatmap(
        point_density_raster, title="Point Density Raster", png_file=pd_file)

    color_file.close()
    q95_file.close()
    pd_file.close()

    return ("Processing Complete <br><br> Output Directory Path: " + str(output_dir_path))


@route('/Ecosynth/Sharing')
def sharing():
    f = open("form.html")
    return f


@route('/Ecosynth/static/<filepath:path>')
def server_static(filepath):
    root = os.path.join(directory, "static")
    return static_file(filepath, root=root)


def launch():
    url = "http://localhost:8081/Ecosynth/"
    webbrowser.open(url)

    run(host='localhost', port=8081, debug=True)


if __name__ == "__main__":
    run(host='localhost', port=8081, debug=True)
