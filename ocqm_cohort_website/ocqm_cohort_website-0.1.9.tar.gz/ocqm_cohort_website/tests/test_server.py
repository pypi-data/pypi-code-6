from .. import server


def test_get_http_server(temp_directory):

    # tests if the imports for python 2/3 are correct
    assert server.get_http_server(temp_directory, 8000)
