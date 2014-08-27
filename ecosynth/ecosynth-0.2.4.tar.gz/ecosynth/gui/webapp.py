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
from ecosynth import share

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

    try:
        dense_ply_file = request.files.get('dense_ply_file')
    except:
        dense_ply_file = None

    output_dir_name = request.forms.get('output_dir_name')
    if output_dir_name == "":
        output_dir_name = "outputs"
    print output_dir_name
    output_dir_path = os.path.join(os.getcwd(), output_dir_name)
    print output_dir_path

    if not os.path.isdir(output_dir_path):
        os.mkdir(output_dir_path)

    # Data Processing
    gps_filepath_out = os.path.join(output_dir_path, 'gps_file.txt')
    cam_filepath_out = os.path.join(output_dir_path, 'geo_camera_array.txt')
    ply_filepath_out = os.path.join(output_dir_path, 'geo_filtered_sparse.ply')
    txt_filepath_out = os.path.join(output_dir_path, 'xyzrgb_array.txt')
    eco_ply_filepath_out = os.path.join(
        output_dir_path, 'ecobrowser_ready.ply')
    params_filepath_out = os.path.join(output_dir_path, 'params.txt')
    quality_metrics_filepath_out = os.path.join(
        output_dir_path, 'quality_metrics.txt')
    if dense_ply_file:
        dense_ply_filepath_out = os.path.join(
            output_dir_path, 'geo_filtered_dense.ply')

    gps_file_out = open(gps_filepath_out, 'w')
    cam_file_out = open(cam_filepath_out, 'w')
    ply_file_out = open(ply_filepath_out, 'w')
    txt_file_out = open(txt_filepath_out, 'w')
    eco_ply_file_out = open(eco_ply_filepath_out, 'w')
    params_file_out = open(params_filepath_out, 'w')
    quality_metrics_file_out = open(quality_metrics_filepath_out, 'w')
    dense_ply_file_out = None
    dense_data = None
    if dense_ply_file:
        dense_ply_file_out = open(dense_ply_filepath_out, 'w')
        dense_data = dense_ply_file.file

    cr_object = pp.run.standard_pipeline(
        out_file.file,
        log_file.file,
        msl_float,
        outputs_filepath=output_dir_path,
        cams_geo_file=cam_file_out,
        ply_file=ply_file_out,
        points_txt_file=txt_file_out,
        gps_file=gps_file_out,
        logger_file=quality_metrics_file_out,
        ecobrowser_ply_file=eco_ply_file_out,
        helm_params_file=params_file_out,
        dense_ply_file_in=dense_data,
        dense_ply_file_out=dense_ply_file_out
        )

    gps_file_out.close()
    cam_file_out.close()
    ply_file_out.close()
    txt_file_out.close()
    params_file_out.close()
    if dense_ply_file:
        dense_ply_file_out.close()

    # Analysis
    color_raster = cr_object.get_color_raster()
    q95_raster = cr_object.get_Q95_elevation_raster()
    point_density_raster = cr_object.get_point_density_raster()
    max_elev_raster = cr_object.get_max_elevation_raster()
    mean_elev_raster = cr_object.get_mean_elevation_raster()
    median_elev_raster = cr_object.get_median_elevation_raster()

    color_filepath_out = os.path.join(output_dir_path, 'color.tiff')
    q95_filepath_out = os.path.join(output_dir_path, 'q95.asc')
    pd_filepath_out = os.path.join(output_dir_path, 'point_density.asc')
    max_elev_filepath_out = os.path.join(output_dir_path, 'max_elevation.asc')
    mean_elev_filepath_out = os.path.join(
        output_dir_path, 'mean_elevation.asc')
    median_elev_filepath_out = os.path.join(
        output_dir_path, 'median_elevation.asc')

    #color_file = open(color_filepath_out, 'w')
    q95_file = open(q95_filepath_out, 'w')
    pd_file = open(pd_filepath_out, 'w')
    max_elev_file = open(max_elev_filepath_out, 'w')
    mean_elev_file = open(mean_elev_filepath_out, 'w')
    median_elev_file = open(median_elev_filepath_out, 'w')

    aoi = cr_object.get_aoi()
    pp.io.save_image(color_filepath_out, color_raster, aoi)
    pp.io.save_ascii_raster(q95_file, q95_raster, aoi[0], aoi[2])
    pp.io.save_ascii_raster(pd_file, point_density_raster, aoi[0], aoi[2])
    pp.io.save_ascii_raster(max_elev_file, max_elev_raster, aoi[0], aoi[2])
    pp.io.save_ascii_raster(mean_elev_file, mean_elev_raster, aoi[0], aoi[2])
    pp.io.save_ascii_raster(
        median_elev_file, median_elev_raster, aoi[0], aoi[2])

    #color_file.close()
    q95_file.close()
    pd_file.close()
    max_elev_file.close()
    mean_elev_file.close()
    median_elev_file.close()

    return ("Processing Complete <br><br> Output Directory Path: " + str(output_dir_path))


@route('/Ecosynth/Sharing', method="GET")
def send_sharing_form():
    f = open(os.path.join(directory, "static/html/share_form.html"))
    return f


@route('/Ecosynth/Sharing', method="POST")
def run_sharing():
    # FTP IP Address - ftp_ip
    # FTP User - ftp_user
    # FTP Password - ftp_pw
    # MySQL IP Address - mysql_ip
    # MySQL User - mysql_user
    # MySQL Password - mysql_pw
    # EZID User - ezid_user
    # EZID Password - ezid_pw
    # EZID Shoulder - ezid_shoulder
    # --------
    # Author - ov_author
    # Organization - ov_organization
    # Acquisition Site - acq_site
    # Latitude - acq_lat
    # Longitude - acq_lon
    # Acquisition Date - acq_date
    # Acquisition Time - acq_time
    # SfM Program Type - gen_cv_type
    # SfM Program Version - gen_cv_version
    # Images (ZIP) - img_zip
    # Point Cloud (PLY) - ply
    # EcosynthBrowser PLY - ecobrowser_ply
    # () Viewable Cloud (boolean) - viewable_cloud - detect from inputs
    # Bundle (OUT) - out
    # Notes - notes

    # Fetch Inputs
    sftp_ip = request.forms.get('sftp_ip')
    sftp_user = request.forms.get('sftp_user')
    sftp_pw = request.forms.get('sftp_pw')
    #mysql_ip = request.forms.get('mysql_ip')
    #mysql_user = request.forms.get('mysql_user')
    #mysql_pw = request.forms.get('mysql_pw')
    ezid_user = request.forms.get('ezid_user')
    ezid_pw = request.forms.get('ezid_pw')
    ezid_shoulder = request.forms.get('ezid_shoulder')
    #### Site Information ###
    ov_author = request.forms.get('ov_author')
    ov_organization = request.forms.get('ov_organization')
    acq_site = request.forms.get('acq_site')
    acq_lat = request.forms.get('acq_lat')
    acq_lon = request.forms.get('acq_lon')
    acq_date = request.forms.get('acq_date')
    acq_time = request.forms.get('acq_time')
    gen_cv_type = request.forms.get('gen_cv_type')
    gen_cv_version = request.forms.get('gen_cv_version')
    notes = request.forms.get('notes')

    #### Debugging
    print "ezid_user", ezid_user
    print "ezid_pw", ezid_pw
    print "ezid_shoulder", ezid_shoulder
    print "ov_author", ov_author
    print "ov_organization", ov_organization
    print "acq_site", acq_site
    print "acq_date", acq_date
    print "acq_time", acq_time

    # Log into FTP, fetch highest-numbered sub-directory
    synth_id = share.verify_sftp(sftp_ip, sftp_user, sftp_pw)
    if synth_id is None:
        return "Could not connect to SFTP server. Check SFTP Credentials"
    else:
        print 'Successfully connected to SFTP server'
        print 'New Synth ID:', synth_id

    ### Files ###
    img_zip = request.files.get('img_zip')
    try:
        img_zip_file = img_zip.file
    except:
        img_zip_file = None

    ply = request.files.get('ply')
    try:
        ply_file = ply.file
    except:
        ply_file = None

    out = request.files.get('out')
    try:
        out_file = out.file
    except:
        out_file = None

    ecobrowser_ply = request.files.get('ecobrowser_ply')
    try:
        ecobrowser_ply_file = ecobrowser_ply.file
    except:
        ecobrowser_ply_file = None

    # Check that mysql password works
    #share.verify_mysql(mysql_ip, mysql_user, mysql_pw)

    # Create DOI
    ov_doi = None
    if (ezid_user is not '') and (ezid_pw is not '') and (ezid_shoulder is not ''):
        try:
            ov_doi = share.create_doi(
                ezid_user,
                ezid_pw,
                ezid_shoulder,
                ov_author,
                ov_organization,
                acq_site,
                acq_date,
                acq_time
            )
            print "DOI Generated:", ov_doi
        except:
            return "Could not process DOI. Check EZID Credentials"

    # Generate metadata page
    try:
        metadata_page = share.generate_metadata_page(
            synth_id=synth_id,
            ov_author=ov_author,
            ov_organization=ov_organization,
            ov_doi=ov_doi,
            acq_site=acq_site,
            acq_lat=acq_lat,
            acq_lon=acq_lon,
            acq_date=acq_date,
            acq_time=acq_time,
            gen_cv_type=gen_cv_type,
            gen_cv_version=gen_cv_version,
            notes=notes,
            img_file=img_zip_file,
            ply_file=ply_file,
            out_file=out_file,
            ecobrowser_ply_file=ecobrowser_ply_file
            )
    except:
        return "Error generating metadata HTML page"

    # FTP --> create directory structure
    # FTP --> upload data
    try:
        share.upload_data(
            sftp_ip,
            sftp_user,
            sftp_pw,
            synth_id,
            metadata_page,
            img_zip_file,
            ply_file,
            out_file
            )
    except:
        return "Error uploading data"

    '''
    # MySQL --> Process and Upload EcosynthBrowser PLY
    #share.upload_ecobrowser(
    #    mysql_ip,
    #    mysql_user,
    #    mysql_pw,
    #    ecobrowser_ply
    #    )
    '''
    # SFTP --> Update Google Maps File (Append to file, and have php script
        # format?) acq_lat, acq_lon, acq_site, ov_author, synth_id
    try:
        share.update_gmaps_json(
            sftp_ip,
            sftp_user,
            sftp_pw,
            synth_id,
            acq_lat,
            acq_lon,
            acq_site,
            ov_author
            )
    except:
        return "Error updating file for Google Maps"

    return "Data processed and uploaded successfully."


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
