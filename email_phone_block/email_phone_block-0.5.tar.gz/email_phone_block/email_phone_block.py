import re


def filter_email(text):
    email = re.compile(r'\w+(@|at| at |\(at\))[a-zA-Z_]+?\.[a-zA-Z]{2,3}')
    return email.sub("xxxx@xxxxx.xxx", text)


def filter_phone(text):
    phone = re.compile(r'\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})')
    return phone.sub("xxx-xxx-xxxx", text)


def filter_email_phone(text):
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

    text = filter_email(text)
    text = filter_phone(text)
    return text

# Legacy
block = filter_email_phone