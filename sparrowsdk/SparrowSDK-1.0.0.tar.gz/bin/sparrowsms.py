#!/usr/bin/env python
import argparse

from sparrowsms.pushclient import PushClient

def main():

    parser = argparse.ArgumentParser(description='Sparrow PushClient command line interface.')
    parser.add_argument('-c', '--clientid', type=str, dest="client_id", required=True, help="Client Id of the login parameters.")
    parser.add_argument('-u', '--username', type=str, dest="username", required=True, help="Username of the login parameters.")
    parser.add_argument('-p', '--password', type=str, dest="password", required=True, help="Password of the login parameters.")
    parser.add_argument('-i', '--intent', dest="intent", required=True, choices=["sms", "credits", "topup", "simulate"], help="Intent to execute.")
    parser.add_argument('-m', '--message', type=str, dest="message", help="Message to send.")
    parser.add_argument('-d', '--destination', dest="destination", nargs='*', help="Message to send.")
    parser.add_argument('-U', '--unicode', dest="unicode", default='False', choices=['True', 'False', 'Auto'], help="Unicode flag for sending unicode messages.")
    parser.add_argument('-s', '--shortcode', type=str, dest="shortcode", help="Shortcode if multiple shortcodes are assigned.")
    parser.add_argument('-I', '--identity', type=str, dest="identity", help="Identity if multiple identities are assigned.")
    parser.add_argument('-S', '--subaccount', type=str, dest="subaccount", help="Subaccount param for reporting purposes only.")
    parser.add_argument('-t', '--tag', type=str, dest="tag", help="Tag param for reporting purposes only.")
    parser.add_argument('-a', '--amount', type=str, dest="amount", help="Amount to request for topup.")

    args = parser.parse_args()

    pushclient = PushClient(client_id=args.client_id, username=args.username, password=args.password)
    if args.intent == 'credits':
        response = pushclient.credit_status()
    elif args.intent == 'topup':
        response = pushclient.request_topup(amount=args.amount)
    elif args.intent == 'simulate':
        pushclient.parse_kwargs(**vars(args))
        response = pushclient.simulate()
    else:
        response = pushclient.send(**vars(args))
    print response

if __name__ == '__main__':
    main()