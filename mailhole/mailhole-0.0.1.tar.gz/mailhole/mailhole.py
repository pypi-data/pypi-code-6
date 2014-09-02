#!/usr/bin/env python


import asyncore
import argparse
import ConfigParser
import email
import json
import os
import threading
import SimpleHTTPServer
import SocketServer
import logging as log

from smtpd import SMTPServer


class MailHoleSMTP(SMTPServer):
    def __init__(self, localaddr, remoteaddr, maildir):
        SMTPServer.__init__(self, localaddr, remoteaddr)
        self.maildir = maildir

    def process_message(self, peer, mailfrom, rcpttos, data):
        msg = email.message_from_string(data)
        subject = self.compile_subject(msg)
        body = self.get_body(msg)
        headers = self.get_headers(msg)
        mail_data = {
            'from': mailfrom, 'to': rcpttos, 'headers': headers, 'body': body
        }
        log.debug(mail_data)
        mail_file = '{}__{}'.format(subject, '_'.join(rcpttos)).lower()
        with open('{}/{}'.format(self.maildir, mail_file), 'w') as f:
            f.write(json.dumps(mail_data))

    def compile_subject(self, message):
        original_subject = message.get('Subject')
        if original_subject:
            subject = original_subject.replace(' ', '_')
        else:
            subject = '__NOSUBJECT'
        return subject

    def get_headers(self, message):
        headers = {}
        for header in message.items():
            headers[header[0]] = header[1]
        return headers

    def get_body(self, message):
        body = []
        if message.is_multipart():
            for msg_part in message:
                body.append(msg_part.get_payload(decode=True))
        else:
            body.append(message.get_payload(decode=True))
        return body


def run_smtp(host, port, maildir):
    MailHoleSMTP((host, port), None, maildir)
    try:
        log.info('SMTP server listening on {}:{}'.format(host, port))
        asyncore.loop()
    except Exception, e:
        log.debug(e)
        pass


def run_http(host, port, maildir):
    try:
        os.chdir(maildir)
        handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer((host, port), handler)
        log.info('HTTP server listening on {}:{}'.format(host, port))
        httpd.serve_forever()
    except Exception, e:
        log.debug(e)
        pass


def main():
    default_host = '127.0.0.1'
    default_port_smtp = 4025
    default_port_http = 4080
    default_maildir = os.getcwd()

    config_dict = {
        'smtp_host': default_host, 'smtp_port': default_port_smtp,
        'http_host': default_host, 'http_port': default_port_http,
        'maildir': default_maildir, 'log_file': None
    }

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='Default behavior is to listen on 127.0.0.1:4025 for SMTP'
               'connections and 127.0.0.1:4080 for HTTP connetctions, '
               'write email files into current directory and log to STDOUT. '
               'All of these settings can be overridden with the options '
               'above. Also a configuration file can be specified that '
               'must contain all the above options.'
    )

    parser.add_argument('-m', '--smtp_host', default=default_host,
                        help='SMTP server host')
    parser.add_argument('-p', '--smtp_port', default=default_port_smtp,
                        help='SMTP server port')
    parser.add_argument('-t', '--http_host', default=default_host,
                        help='HTTP server host')
    parser.add_argument('-q', '--http_port', default=default_port_http,
                        help='HTTP server port')
    parser.add_argument('-d', '--maildir', default=default_maildir,
                        help='Directory where emails are stored')
    parser.add_argument('-l', '--log_file', default=None,
                        help='Log file')
    parser.add_argument('-c', '--config_file',
                        help='Config file path')

    args = parser.parse_args()

    config_dict['smtp_host'] = args.smtp_host
    config_dict['smtp_port'] = args.smtp_port
    config_dict['http_host'] = args.http_host
    config_dict['http_port'] = args.http_port
    config_dict['maildir'] = args.maildir
    config_dict['log_file'] = args.log_file

    if args.config_file:
        if os.path.isfile(args.config_file):
            config = ConfigParser.RawConfigParser(config_dict,
                                                  allow_no_value=True)
            config.read(args.config_file)

            parsed_config = {
                'smtp_host': config.get('DEFAULT', 'smtp_host'),
                'smtp_port': config.getint('DEFAULT', 'smtp_port'),
                'http_host': config.get('DEFAULT', 'http_host'),
                'http_port': config.getint('DEFAULT', 'http_port'),
                'maildir': config.get('DEFAULT', 'maildir'),
                'log_file': config.get('DEFAULT', 'log_file')
            }

            for key, value in parsed_config.iteritems():
                if value:
                    config_dict[key] = value

    log.basicConfig(filename=config_dict['log_file'],
                    format='[%(asctime)s]: %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d, %H:%M:%S',
                    level=log.DEBUG)

    smtp_thread = threading.Thread(target=run_smtp,
                                   args=(
                                       config_dict['smtp_host'],
                                       config_dict['smtp_port'],
                                       config_dict['maildir']
                                   ))
    http_thread = threading.Thread(target=run_http,
                                   args=(
                                       config_dict['http_host'],
                                       config_dict['http_port'],
                                       config_dict['maildir']
                                   ))
    smtp_thread.daemon = True
    http_thread.daemon = True
    smtp_thread.start()
    http_thread.start()

    while smtp_thread.is_alive():
        smtp_thread.join(1)
    while http_thread.is_alive():
        http_thread.join(1)


if __name__ == '__main__':
    exit(main())
