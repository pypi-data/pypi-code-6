from dragline.http import Request
from dragline.htmlparser import HtmlParser
import argparse
from lxml.html import open_in_browser


def start_python_console(namespace=None, noipython=False, banner=''):
    """Start Python console binded to the given namespace. If IPython is
    available, an IPython console will be started instead, unless `noipython`
    is True. Also, tab completion will be used on Unix systems.
    """
    if namespace is None:
        namespace = {}

    try:
        try:  # use IPython if available
            if noipython:
                raise ImportError()
            try:
                try:
                    from IPython.terminal import embed
                except ImportError:
                    from IPython.frontend.terminal import embed
                sh = embed.InteractiveShellEmbed(banner1=banner)
            except ImportError:
                from IPython.Shell import IPShellEmbed
                sh = IPShellEmbed(banner=banner)
            sh(global_ns={}, local_ns=namespace)
        except ImportError:
            import code
            try:  # readline module is only available on unix systems
                import readline
            except ImportError:
                pass
            else:
                import rlcompleter
                readline.parse_and_bind("tab:complete")
            code.interact(banner=banner, local=namespace)
    except SystemExit:  # raised when using exit() in python code.interact
        pass


def shelp():
    repr_data = {k: repr(v) for k, v in data.iteritems()}
    intro = """\n[d] Available Dragline objects:
    [d]   parser                 %(parser)s
    [d]   request                %(request)s
    [d]   response               %(response)s
    [d] Useful shortcuts: ## Override methods in Cmd object ##
    [d]   shelp()                Shell help (print this help)
    [d]   fetch(req_or_url)      Fetch request (or URL) and update local objects
    [d]   view(response=None)    View response in a browser\n\n""" % repr_data
    print(intro)


def fetch(req_or_url):
    global data
    if isinstance(req_or_url, Request):
        data["request"] = req_or_url
    else:
        data["request"] = Request(req_or_url)
    data["response"] = data["request"].send()
    data["parser"] = HtmlParser(data["response"])
    shelp()


def view(response=None):
    if response is None:
        global data
        response = data["response"]
    open_in_browser(HtmlParser(response), 'utf-8')

data = {}
data["fetch"] = fetch
data["view"] = view
data["shelp"] = shelp
data["Request"] = Request


def execute():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url', action='store', default='', help='url')
    url = (parser.parse_args()).url
    fetch(url)
    start_python_console(data)


if __name__ == "__main__":
    execute()

