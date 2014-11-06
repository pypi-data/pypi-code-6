from babel.bin.base import *
import requests_futures.sessions

# Make request
session = requests_futures.sessions.FuturesSession()
if args.MESSAGE: r = session.post(args.TO, args.MESSAGE)
else: r = session.get(args.TO)

# Print reply
if args.reply: print(r.result().text)