"""
Utilities
=========
"""

__all__ = ['create_doi', 'verify_sftp', 'generate_metadata_page',
           'upload_data', 'update_gmaps_json']

import os
import subprocess
import datetime
import re
import time
import json

import pysftp


def create_doi(username, password, shoulder, creator, publisher, site, acq_date, acq_time):
    """
    This function works with ezid.py to create a basic DOI for a SynthSet on
    EcosynthData

    :param string shoulder: (e.g. doi:10.5072/FK2)
    """
    try:
        dirname = os.path.dirname(os.path.realpath(__file__))
        ezid_filepath = os.path.join(dirname, "ezid.py")

        proc = subprocess.Popen([
            "python", ezid_filepath, (username + ":" + password), "mint", shoulder,
            "datacite.creator", creator,
            "datacite.title", ("SynthSet for " + site + " Acquired " + str(acq_date) + " " + str(acq_time)),
            "datacite.publisher", publisher,
            "datacite.publicationyear", str(datetime.date.today().year),
            "datacite.resourcetype", "Dataset"
            ], stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()

        if lines[0].split()[0].startswith("success:"):
            return lines[0].split()[1]

        else:
            return None

    except:
        pass


def verify_sftp(sftp_ip, sftp_user, sftp_pw):
    """
    Checks that credential successfully connect to FTP server and
    fetches new post ID based on current list of sub-directories

    :param string sftp_ip:
    :param string sftp_user:
    :param string sftp_pw:

    :return: synth_id (returns None if cannot connect)
    :rtype: int

    | **Example**
    |
    | **Notes**
    |
    """
    try:
        sftp = pysftp.Connection(sftp_ip, username=sftp_user, password=sftp_pw)
        #ftp = FTP(host=ftp_ip, user=ftp_user, passwd=ftp_pw)

        #ls = ftp.nlst()
        sftp.cwd('.')
        ls = sftp.listdir()

        if 'EcosynthData' in ls:
            sftp.chdir('EcosynthData')
        elif 'home' in ls:
            sftp.chdir('home')
        elif 'web' in ls:
            sftp.chdir('web/EcosynthData')
        ls = sftp.listdir()
        ls = sorted(ls, key=_sort_numerically)

        if 'index.html' not in ls:
            print 'index.html not found, adding site html'
            # Upload EcosynthData html/css here
            dirname = os.path.dirname(os.path.realpath(__file__))
            site_html_filepath = os.path.join(dirname, "html/site_html")
            sftp.put_r(site_html_filepath, sftp.getcwd())

        count = 1
        for name in ls:
            if not name.isdigit():
                break
            else:
                count += 1

        sftp.close()

        return count

    except:
        return None


def _sort_numerically(string_list):
    r = re.compile('(\d+)')
    reg_list = r.split(string_list)
    return [int(name) if name.isdigit() else name for name in reg_list]


def generate_metadata_page(synth_id, ov_author, ov_organization, ov_doi, acq_site, acq_lat, acq_lon, acq_date, acq_time, gen_cv_type, gen_cv_version, notes, img_file, ply_file, out_file, ecobrowser_ply_file):
    """
    Creates a new metadata page based on inputs

    :param string ov_author:
    :param string ov_organization:
    :param string ov_doi:
    :param string acq_site:
    :param string acq_lat:
    :param string acq_lon:
    :param string acq_date:
    :param string acq_time:
    :param string gen_cv_type:
    :param string gen_cv_version:
    :param string notes:
    :param file img_file:
    :param file ply_file:
    :param file out_file:
    :param file ecobrowser_ply_file:

    :return: metadata_html
    :rtype: string

    | **Example**
    |
    | **Notes**
    |
    """

    synthset_content = ""

    dirname = os.path.dirname(os.path.realpath(__file__))
    html_filepath = os.path.join(dirname, "html")
    html_header = open(os.path.join(html_filepath, "synthset_header.html"), 'r')
    #html_footer = open(os.path.join(html_filepath, "synthset_footer.html"), 'r')

    synthset_content += html_header.read()

    if img_file:
        synthset_content += (
            '<a class="btn btn-primary" href="./img.zip" download="img.zip">\
            Download Images (zip)</a>  ')

    if out_file:
        synthset_content += (
            '<a class="btn btn-primary" href="./bundle.out" download="bundle.out">\
            Download Bundle File (out)</a>  ')

    if ply_file:
        synthset_content += (
            '<a class="btn btn-primary" href="./sparse.ply" download="sparse.ply">\
            Download Point Cloud (ply)</a>  ')

    '''
    if ecobrowser_ply_file:
        synthset_content += (
            '<a class="btn btn-primary" href="3dvis.ecosynth.org/?table=%s">\
            Download Images (zip)</a>  ' % str(synth_id))
    '''

    synthset_content += '<meta id="post_id" content=2 /><div class="synthset-data"><br><div class="col-md-6">'

    synthset_content += '<table class="table"><tr><th class="col-md-2">Field</th><th class="col-md-4">Value</th></tr>'

    if ov_author:
        synthset_content += (
            "<tr><td>Author</td> <td>%s</td></tr>" % ov_author)

    if ov_organization:
        synthset_content += (
            "<tr><td>Organization</td> <td>%s</td></tr>" % ov_organization)

    if ov_doi:
        synthset_content += (
            "<tr><td>DOI</td> <td>%s</td></tr>" % ov_doi)

    synthset_content += (
        "<tr><td>Date Uploaded</td> <td>%s</td></tr>" % time.strftime("%Y-%m-%d"))

    if acq_site:
        synthset_content += (
            "<tr><td>Acquisition Site</td> <td>%s</td></tr>" % acq_site)

    if acq_lat and acq_lon:
        synthset_content += (
            "<tr><td>Lat / Lon</td> <td>%s / %s</td></tr>" % (acq_lat, acq_lon))

    if acq_date:
        synthset_content += (
            "<tr><td>Date Acquired</td> <td>%s</td></tr>" % acq_date)

    if acq_time:
        synthset_content += (
            "<tr><td>Time Acquired</td> <td>%s</td></tr>" % acq_time)

    if gen_cv_type:
        synthset_content += (
            "<tr><td>SfM Program Type</td> <td>%s</td></tr>" % gen_cv_type)

    if gen_cv_version:
        synthset_content += (
            "<tr><td>SfM Program Version</td> <td>%s</td></tr>" % gen_cv_version)

    if notes:
        synthset_content += (
            "<tr><td>Notes</td> <td>%s</td></tr>" % notes)

    synthset_content = synthset_content + '''</table></div>
    <div class="col-md-6"><div id="map_canvas" style="padding: 10; border:10px; height:400px; width=100%"></div></div>
</body></div>
<script src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/js/bootstrap.min.js"></script>
<script src="//cdnjs.cloudflare.com/ajax/libs/moment.js/2.5.1/moment-with-langs.min.js"></script>
<script>
function flask_moment_render(elem) {
    $(elem).text(eval('moment("' + $(elem).data('timestamp') + '").' + $(elem).data('format') + ';'));
    $(elem).removeClass('flask-moment');
}
function flask_moment_render_all() {
    $('.flask-moment').each(function() {
        flask_moment_render(this);
        if ($(this).data('refresh')) {
            (function(elem, interval) { setInterval(function() { flask_moment_render(elem) }, interval); })(this, $(this).data('refresh'));
        }
    })
}
$(document).ready(function() {
    flask_moment_render_all();
});
</script>


<!-- Google Maps API: Currently Only Used in Index -->
<script
  src="https://maps.googleapis.com/maps/api/js?v=3.exp">
</script>

<script>
    function initialize() {

        var lat = ''' + str(acq_lat) + ''';
        var lon = ''' + str(acq_lon) + ''';
        var latLng = new google.maps.LatLng(lat,lon);

        var mapOptions = {
          zoom: 12,
          center: latLng,
          mapTypeId: google.maps.MapTypeId.TERRAIN
        };

        var map = new google.maps.Map(document.getElementById('map_canvas'),
            mapOptions);

        var infowindow = new google.maps.InfoWindow();

        var fill = ("<b>Site</b>:" + "''' + str(acq_site) + '''" + "<br>"
        + "<b>Author</b>: " + "''' + str(ov_author) + '''" + "<br>"
        + "<b>Organization</b>: " + "''' + str(ov_organization) + '''" + "<br>"
        + "<b>Date</b>: " + "''' + str(acq_date) + '''" + "<br>");

        var marker = new google.maps.Marker({
            position: latLng, 
            fill: fill, 
            map: map,
        });

        google.maps.event.addListener(marker, 'click', (function() {
            infowindow.setContent(marker.fill);
            infowindow.open(map, marker);
        }));
    }
</script>
</body>
</html>
    '''

    html_header.close()

    return synthset_content


def upload_data(sftp_ip, sftp_user, sftp_pw, synth_id, metadata_page, image_file, ply_file, out_file):
    """
    Connects be to sftp server, creates new dataset folder, and uploads new
    dataset.

    :param string sftp_ip:
    :param string sftp_user:
    :param string sftp_pw:
    :param int synth_id:
    :param string metadata_page:
    :param file image_file:
    :param file ply_file:
    :param file out_file:

    | **Example**
    |
    | **Notes**
    |
    """
    # Connect
    sftp = pysftp.Connection(sftp_ip, username=sftp_user, password=sftp_pw)
    sftp.cwd('.')

    # Switch into base directory
    if 'EcosynthData' in sftp.listdir():
        sftp.chdir('EcosynthData')
    elif 'home' in sftp.listdir():
        sftp.chdir('home')
    elif 'web' in ls:
        sftp.chdir('web/EcosynthData')

    sftp.cwd('.')

    # Make new directory and change into it
    metadata_dir = os.path.join(sftp.getcwd(), str(synth_id))
    if str(synth_id) not in sftp.listdir():
        sftp.mkdir(str(synth_id))
    sftp.chdir(metadata_dir)

    # Upload Data

    index_file = open(os.path.join(os.getcwd(), 'temp_index.html'), 'w')
    index_file.write(metadata_page)
    index_file.close()
    '''
    command_string = 'echo "%s" > %s/index.html' % (
        metadata_page.replace('"', '\\"'), metadata_dir)
    #    re.escape(metadata_page), metadata_dir)
    sftp.execute(command_string)
    '''
    index_file = open(os.path.join(os.getcwd(), 'temp_index.html'), 'r')

    f = sftp.open(os.path.join(metadata_dir, 'index.html'), mode='w')
    f.write(index_file.read())
    f.close()

    os.remove(os.path.join(os.getcwd(), 'temp_index.html'))

    if image_file:
        f = sftp.open(os.path.join(metadata_dir, 'img.zip'), mode='w')
        f.write(image_file.read())
        f.close()
    if ply_file:
        f = sftp.open(os.path.join(metadata_dir, 'sparse.ply'), mode='w')
        f.write(ply_file.read())
        f.close()
    if out_file:
        f = sftp.open(os.path.join(metadata_dir, 'bundle.out'), mode='w')
        f.write(out_file.read())
        f.close()

    sftp.close()


def update_gmaps_json(sftp_ip, sftp_user, sftp_pw, synth_id, acq_lat, acq_lon, acq_site, ov_author):
    """
    Appends metadata to a file that is used for Google Maps on
    the front page of the website

    :param string sftp_ip:
    :param string sftp_user:
    :param string sftp_pw:
    :param int synth_id:
    :param string acq_lat:
    :param string acq_lon:
    :param string acq_site:
    :param string ov_author:

    | **Example**
    |
    | **Notes**
    |
    """
    try:
        # Create string
        json_object = json.dumps({
            "acq_lat": acq_lat,
            "acq_lon": acq_lon,
            "acq_site": acq_site,
            "ov_author": ov_author,
            "id": synth_id
            })

        command_string = 'echo "%s" >> map_objects.txt' % (
            json_object.replace('"', '\\"'))

        # Connect
        sftp = pysftp.Connection(sftp_ip, username=sftp_user, password=sftp_pw)

        # Switch into base directory
        ls = sftp.listdir()
        if 'EcosynthData' in ls:
            sftp.chdir('EcosynthData')
        elif 'home' in ls:
            sftp.chdir('home')

        # Append string to file
        sftp.execute(command_string)

        sftp.close()
    except:
        pass
