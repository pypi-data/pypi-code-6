import re


def block(text=""):
    """
    Substitute emails and phone number with dummies

    example:

    text = "So please send me an email at name@domain.com, thanks!"

    result: 'So please send me an email at xxxx@xxxxx.xxx, thanks!'

    text = "So please call me at 333-333-3333, thanks!'"

    result: 'So please call me at xxx-xxx-xxxx, thanks!'

    format recognized:

    Emails:

    name@domain.com
    name(at)domain.com
    name at domain.com

    Phone numbers:

    333-333-3333
    3333333333
    333 333 3333
    333 333-3333
    333333-3333
    333-3333333

    """
    email = re.compile(r'\w+(@|at| at |\(at\))[a-zA-Z_]+?\.[a-zA-Z]{2,3}')
    phone = re.compile(r'\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})')
    text = email.sub("xxxx@xxxxx.xxx", text)
    text = phone.sub("xxx-xxx-xxxx", text)
    return text