"""
A flask based web application that listens to
printing requests and serves them
"""
import thread

import usb
import flask
from flask import request, render_template, redirect, url_for
from gevent.wsgi import WSGIServer
from escpos import printer

from config import CONFIG

# A threadsafe lock to prevent two requests printing simultaneously
print_lock = thread.allocate_lock()


app = flask.Flask(__name__)


@app.template_filter('isSameDevice')
def same_device(dev1, dev2):
    """
    Compares the two given devices and finds if they are the same
    """
    if (dev1 is None) or (dev2 is None):
        return False
    return (
        (dev1.idVendor == dev2.idVendor) and
        (dev1.idProduct == dev2.idProduct) and
        (dev1.address == dev2.address)
    )


@app.route('/')
def home():
    return render_template('home.html')


def get_devices(only_printers=False):
    """
    Return all the devices
    """
    kwargs = {}
    if only_printers:
        kwargs['bDeviceClass'] = 7

    devices = []
    for device in usb.core.find(find_all=True, **kwargs):
        try:
            device.product, device.manufacturer
        except usb.USBError:
            pass
        else:
            devices.append(device)
    return devices


def get_current_printer():
    """
    Return the printer currently attached to
    """
    return usb.core.find(
        idVendor=CONFIG['vendor'],
        idProduct=CONFIG['product']
    )


@app.route('/admin')
def administration():
    """
    An Administration Page
    """
    devices = get_devices(request.args.get('printers', 0, type=int))
    return render_template(
        'administration.html',
        devices=devices,
        current_printer=get_current_printer(),
    )


@app.route('/set_printer/<int:vendor>/<int:product>')
def set_printer(vendor, product):
    """
    Set the printer now and forever
    """
    CONFIG['vendor'] = vendor
    CONFIG['product'] = product
    CONFIG.save()

    return redirect(url_for('administration'))


@app.route('/test-kit', methods=['get', 'post'])
def test_kit():
    device = get_current_printer()

    if request.method == 'POST':
        with print_lock:
            p = printer.Usb(
                device.idVendor, device.idProduct, CONFIG['interface']
            )
            instruction = request.form['instruction']

            assert instruction in ('cut', 'text')

            if instruction == 'cut':
                p.cut()
            elif instruction == 'text':
                p.text(request.form['text'])

    return render_template('test-kit.html', current_printer=device)


@app.route('/print', methods=['post'])
def print_handler():
    """
    A Handler that receives the ESC/POS code in the body expected as json
    with an attribute called content and encoded in base64.

    The content is sent as such to the printer, so any cut instructions must
    be part of the content.

    Expected json body in POST:

    {
        'content': '<base 64 encoded ESC/POS instructions>'
    }
    """
    device = get_current_printer()
    if device is None:
        return 'Printer Not Connected', 502

    content = request.json['content'].decode('base64')
    with print_lock:
        p = printer.Usb(device.idVendor, device.idProduct, CONFIG['interface'])
        p._raw(content)
    return 'ok'


if __name__ == '__main__':
    CONFIG.parse()

    local_ip = CONFIG['address']
    port = CONFIG['port']
    http_server = WSGIServer((local_ip, port), app)
    http_server.serve_forever()
