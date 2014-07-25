class SimpleCaptcher():
    def __init__(self):
        pass

    def process_captcha(self, url, sid, callback):
        print('\n\n__________________Simple process captcha__________________')
        key = input("Open url: {URL} \n"
                    "Enter captcha key:\n".format(URL=url))
        if key:
            callback(sid, key)
