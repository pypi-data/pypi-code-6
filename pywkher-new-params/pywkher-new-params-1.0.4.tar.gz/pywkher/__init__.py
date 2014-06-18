from os import chmod, environ, path as os_path
from subprocess import call as call_subprocess
from tempfile import NamedTemporaryFile


def generate_pdf(html='', url='', cmd=None, chmod=False, args=['-q']):
    # Validate input
    if not html and not url:
        raise ValueError('Must pass HTML or specify a URL')
    if html and url:
        raise ValueError('Must pass HTML or specify a URL, not both')

    wkhtmltopdf_default = (
            os_path.abspath(os_path.split(__file__)[0]) +
            '/bin/wkhtmltopdf-heroku')

    if chmod:
        # Make sure wkhtmltopdf-heroku is executable
        chmod(wkhtmltopdf_default, 0755)

    if cmd is None:
        # Reference command
        wkhtmltopdf_cmd = environ.get('WKHTMLTOPDF_CMD', wkhtmltopdf_default)
    else:
        wkhtmltopdf_cmd = cmd

    # Set up return file
    pdf_file = NamedTemporaryFile(suffix='.pdf')

    if html:
        # Save the HTML to a temp file
        html_file = NamedTemporaryFile(suffix='.html', bufsize=0)
        html_file.write(html)

        # wkhtmltopdf
        call_subprocess([wkhtmltopdf_cmd] + args + [html_file.name, pdf_file.name])

        # Clean up
        html_file.close()
    else:
        # wkhtmltopdf, using URL
        call_subprocess([wkhtmltopdf_cmd] + args + [url, pdf_file.name])

    return pdf_file
