# !/usr/bin/env python
#
# Author: Paul D. Eden <paul@benchline.org>
# Created: 2014-08-15
"""
Parses a miredot-generated REST web service tree.
"""
from string import Template

import benchline.args


TEST_TREE = ("- authorization\n"
             "  - / GET\n"
             "  - {personId} POST DELETE\n"
             "  - all\n"
             "    - / PUT\n"
             "- calendar\n"
             "  - {beginDate}/{endDate} GET")


class RestClass(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def __repr__(self):
        return self.file_name + ":" + str(self.methods)

    file_name = ""
    methods = []


class RestMethod(object):
    def __init__(self, name, path, method, params):
        self.class_name = name
        self.path = path
        self.http_method = method
        self.params = params

    def __repr__(self):
        """
        >>> RestMethod("testing", "/", "GET", ['personId'])
        GET testing/{personId}
        >>> RestMethod("testing", "", "DELETE", ['personId'])
        DELETE testing/{personId}
        >>> RestMethod("testing", "all", "POST", ['personId'])
        POST testing/all/{personId}
        >>> RestMethod("testing", "all", "GET", ['a','beeTree'])
        GET testing/all/{a}/{beeTree}
        >>> RestMethod("testing2", "all", "PUT", [])
        PUT testing2/all
        """
        if len(self.params):
            params = "/" + "{" + "}/{".join(self.params) + "}"
        else:
            params = ""

        result = self.http_method + " "
        if self.path in ["/", ""]:
            result += self.class_name
        else:
            result += "/".join([self.class_name, self.path])
        result += params
        return result

    class_name = ""
    path = ""
    http_method = ""
    params = []


def split_method_line(line, prefix=""):
    """
    >>> split_method_line('- {bd}/{ed} GET POST')
    ['{bd}/{ed}', 'GET', 'POST']
    >>> split_method_line('- {bd}/{ed} GET POST', 'prefix')
    ['prefix/{bd}/{ed}', 'GET', 'POST']
    >>> split_method_line('- / GET', 'peter')
    ['peter', 'GET']

    :param line:
    :param prefix:
    :return:
    """
    items = right_side(line).split()
    if prefix:
        items[0] = "/".join([prefix, items[0]])
    while items[0].endswith("/") and items[0] != "/":
        items[0] = items[0][:-1]
    return items


def rest_method_factory(file_name, items):
    """
    >>> rest_method_factory("testing", ["{bd}/{ed}", "GET", "POST"])
    [GET testing/{bd}/{ed}, POST testing/{bd}/{ed}]
    >>> rest_method_factory("testing", ["/", "DELETE"])
    [DELETE testing]

    :param file_name:
    :param items:
    :return:
    """

    def one_rest_method(method):
        return RestMethod(file_name, path_without_params(items[0]), method, get_params_from_path(items[0]))

    return map(one_rest_method, items[1:])  # make a new RestMethod for each GET PUT POST or DELETE in the method_line


def parse_tree(lines):
    """
    >>> parse_tree(TEST_TREE.splitlines())
    [authorization:[GET authorization, POST authorization/{personId}, DELETE authorization/{personId}, PUT authorization/all, GET calendar/{beginDate}/{endDate}]]

    :param lines:string
    :return:list of RestMethod objects
    """
    classes = []
    current_class = None
    saved_path_prefix = ""
    for line in lines:
        if line.startswith("-"):  # '- authorization'
            if current_class:  # Only needed the first time through
                classes.append(current_class)
            current_class = RestClass(right_side(line))
            saved_path_prefix = ""
        else:
            if is_method_line(line):
                map(current_class.methods.append,
                    rest_method_factory(current_class.file_name, split_method_line(line, saved_path_prefix)))
            else:
                saved_path_prefix = right_side(line)
    return classes


def path_without_params(path_str):
    """
    >>> path_without_params("all")
    'all'
    >>> path_without_params("/")
    '/'
    >>> path_without_params("{personId}")
    '/'
    >>> path_without_params("{beginDate}/{endDate}")
    '/'

    :param path_str:
    :return:str
    """
    if path_str.startswith("{") or path_str == "/":
        return '/'
    else:
        return path_str


def is_method_line(line):
    """
    >>> is_method_line("/ GET")
    True
    >>> is_method_line("{personId} POST")
    True
    >>> is_method_line("all")
    False
    >>> is_method_line("{beginDate}/{endDate} GET POST DELETE PUT")
    True

    :param line:string
    :return:bool
    """
    return any(method in line for method in "GET PUT POST DELETE".split())


def get_params_from_path(path):
    """
    >>> get_params_from_path("/")
    []
    >>> get_params_from_path("{personId}")
    ['personId']
    >>> get_params_from_path("{beginDate}/{endDate}")
    ['beginDate', 'endDate']
    >>> get_params_from_path("all")
    []

    :param path:
    :return:
    """
    if path.startswith("{"):
        return map(lambda x: camel_case(x.replace("{", "").replace("}", "")), filter(None, path.split("/")))
    else:
        return []


def right_side(line):
    """
    Gets the right side of a line with a -
    >>> right_side("- testing")
    'testing'
    >>> right_side("  - all")
    'all'
    >>> right_side("    - {personId} GET")
    '{personId} GET'

    :param line:str
    :return:str
    """
    return line.split("- ")[1]


def name_from_rest_method(rest_method):
    """
    >>> rest_method = RestMethod("testing", "/", "GET", [])
    >>> name_from_rest_method(rest_method)
    'getTesting'
    >>> rest_method = RestMethod("testing", "all", "GET", ['personId'])
    >>> name_from_rest_method(rest_method)
    'getTestingAllByPersonId'
    >>> rest_method = RestMethod("testing", "", "GET", ['name', 'personId'])
    >>> name_from_rest_method(rest_method)
    'getTestingByNameAndPersonId'
    >>> rest_method = RestMethod("testing", "/", "PUT", ['personId'])
    >>> name_from_rest_method(rest_method)
    'updateTestingByPersonId'
    >>> rest_method = RestMethod("testing", "/", "POST", [])
    >>> name_from_rest_method(rest_method)
    'createTesting'
    >>> rest_method = RestMethod("test_ing", "paul", "DELETE", ['controlDate'])
    >>> name_from_rest_method(rest_method)
    'deleteTestIngPaulByControlDate'

    :param rest_method:
    :return:
    """
    mapping = {"GET": "get", "POST": "create", "PUT": "update", "DELETE": "delete"}
    part2 = "".join(map(lambda x: upper_first_letter(camel_case(x)),
                        filter(lambda x: x not in ["/", ""], [rest_method.class_name, rest_method.path])))
    result = mapping[rest_method.http_method] + part2
    if not rest_method.params:
        return result
    return result + "By" + "And".join(
        map(upper_first_letter, rest_method.params))


def read_tree(file_name):
    return open(file_name).read().splitlines()


def lower_first_letter(some_str):
    """
    >>> lower_first_letter("Paul")
    'paul'
    >>> lower_first_letter("PAUL")
    'pAUL'
    >>> lower_first_letter(None)
    ''
    >>> lower_first_letter('')
    ''
    >>> lower_first_letter('paul')
    'paul'

    :param some_str:
    :return:str
    """
    return some_str[:1].lower() + some_str[1:] if some_str else ''


def upper_first_letter(some_str):
    """
    >>> upper_first_letter("Paul")
    'Paul'
    >>> upper_first_letter("PAUL")
    'PAUL'
    >>> upper_first_letter(None)
    ''
    >>> upper_first_letter('')
    ''
    >>> upper_first_letter('paul')
    'Paul'

    :param some_str:
    :return:str
    """
    return some_str[:1].upper() + some_str[1:] if some_str else ''


def camel_case(some_str):
    """
    >>> camel_case("paul_eden")
    'paulEden'
    >>> camel_case("personId")
    'personId'
    >>> camel_case("Paul eden")
    'paulEden'
    >>> camel_case("paul-Eden")
    'paulEden'

    :param some_str:
    :return:some_str in camelCase
    """
    if not any(delimiter in some_str for delimiter in " ,-,_".split(",")):
        return some_str
    return lower_first_letter(''.join(some_str.replace("_", " ").replace("-", " ").title().replace(" ", "")))


def gen_param_list(params):
    """
    >>> gen_param_list(["personId", "name"])
    '$personId, $name'
    >>> gen_param_list([])
    ''

    :param params:
    :return:
    """
    return ", ".join(map(lambda x: "$" + x, params))


def gen_params_for_path(params):
    """
    >>> gen_params_for_path(["personId", "name"])
    '$personId . "/" . $name'
    >>> gen_params_for_path(["adminNoteId"])
    '$adminNoteId'
    >>> gen_params_for_path([])
    ''

    :param params:
    :return:
    """
    return ' . "/" . '.join(map(lambda x: "$" + x, params))


def get_path_from_rest_method(rm):
    """
    >>> get_path_from_rest_method(RestMethod("testing", "/", "GET", ['adminNoteId']))
    '"testing/" . $adminNoteId'
    >>> get_path_from_rest_method(RestMethod("testing", "/", "GET", ['adminNoteId', 'paul']))
    '"testing/" . $adminNoteId . "/" . $paul'
    >>> get_path_from_rest_method(RestMethod("testing", "/", "GET", []))
    '"testing"'

    :param rm:
    :return:
    """
    return "\"" + rm.class_name + (rm.path + "\" . " if rm.params else "\"") + gen_params_for_path(rm.params)


def generate_method_code(rest_method):
    """
    >>> rest_method = RestMethod("testing", "/", "GET", ['adminNoteId'])
    >>> generate_method_code(rest_method).startswith('public function getTestingByAdminNoteId($adminNoteId) {')
    True
    >>> rest_method = RestMethod("admin_note", "/", "POST", [])
    >>> generate_method_code(rest_method).startswith("public function createAdminNote(array $adminNote) {")
    True
    >>> rest_method = RestMethod("admin_note", "/", "PUT", [])
    >>> generate_method_code(rest_method).startswith("public function updateAdminNote(array $adminNote) {")
    True
    >>> rest_method = RestMethod("admin_note", "/", "DELETE", [])
    >>> generate_method_code(rest_method).startswith("public function deleteAdminNote(array $adminNote) {")
    True

    :param rest_method:RestMethod
    :return:string
    """
    method_name = name_from_rest_method(rest_method)
    params = gen_param_list(rest_method.params)
    path = get_path_from_rest_method(rest_method)
    param = "$" + camel_case(rest_method.class_name)
    result = ""
    if rest_method.http_method == "GET":
        template_str = ('public function $method_name($params) {\n'
                        '    $response = $this->http->get($path, array());\n'
                        '    return json_decode($response->getBody());\n'
                        '}')
        result = Template(template_str).safe_substitute(method_name=method_name, path=path, params=params)
    elif rest_method.http_method == "POST":
        template_str = ('public function $method_name(array $param) {\n'
                        '    $response = $this->http->post($path, array("Content-Type: application/json"),\n'
                        '        json_encode($param));\n'
                        '    return json_decode($response->getBody());\n'
                        '}')
        result = Template(template_str).safe_substitute(method_name=method_name, path=path, param=param)
    elif rest_method.http_method == "PUT":
        template_str = ('public function $method_name(array $param) {\n'
                        '    $this->http->put($path, array("Content-Type: application/json"),\n'
                        '        json_encode($param));\n'
                        '}')
        result = Template(template_str).safe_substitute(method_name=method_name, path=path, param=param)
    elif rest_method.http_method == "DELETE":
        template_str = ('public function $method_name(array $param) {\n'
                        '    $this->http->delete($path, array("Content-Type: application/json"),\n'
                        '        json_encode($param));\n'
                        '}')
        result = Template(template_str).safe_substitute(method_name=method_name, path=path, param=param)

    return result


def generate_test_method_code(rest_method):
    """
    >>> rest_method = RestMethod("testing", "/", "GET", ['adminNoteId'])
    >>> generate_test_method_code(rest_method).startswith('public function')
    True

    :param rest_method:
    :return:
    """
    return ""


def rest_class_to_ws_file_contents(rest_class):
    """
    :param rest_class:RestClass
    :return:string
    """
    template_str = ("<?php\n"
                    "\n"
                    "namespace clients;\n"
                    "\n"
                    "use CONFIG;\n"
                    "\n"
                    'require_once(__DIR__ . "/../config.php");\n'
                    'require_once(__DIR__ . "/util/http.php");\n'
                    "\n"
                    "class $class_name {\n"
                    "\n"
                    "    private $http;\n"
                    "\n"
                    "    function __construct() {\n"
                    '    $this->http = new util\http(CONFIG::$URL_ROOT . "/$class_name");\n'
                    "    }\n"
                    "\n"
                    "    $functions\n"
                    "}\n")
    template = Template(template_str)
    return template.safe_substitute(class_name=rest_class.file_name,
                                    functions="\n\n".join(map(generate_method_code, rest_class.methods)))


def rest_class_to_test_file_contents(rest_class):
    """
    >>> rest_class_to_test_file_contents("")
    something

    :param rest_class:
    :return:
    """
    # todo make this be for tests, right now it's a copy of the class file
    template_str = ("<?php\n"
                    "\n"
                    "namespace clients;\n"
                    "\n"
                    "use CONFIG;\n"
                    "\n"
                    'require_once(__DIR__ . "/../config.php");\n'
                    'require_once(__DIR__ . "/util/http.php");\n'
                    "\n"
                    "class $class_name {\n"
                    "\n"
                    "    private $http;\n"
                    "\n"
                    "    function __construct() {\n"
                    '    $this->http = new util\http(CONFIG::$URL_ROOT . "/$class_name");\n'
                    "    }\n"
                    "\n"
                    "    $functions\n"
                    "}\n")
    template = Template(template_str)
    return template.safe_substitute(class_name=rest_class.file_name,
                                    functions="\n\n".join(map(generate_test_method_code, rest_class.methods)))


def write_file(file_name, file_contents):
    with open(file_name, 'w') as f:
        f.write(file_contents)


def write_class_to_files(rest_class):
    """
    writes files on disk
    assumes we are at the root of the PHP project and it has a src/clients and tests/clients directories

    :param rest_class:RestClass
    :return:void
    """

    write_file("src/clients/" + rest_class.file_name + ".php", rest_class_to_ws_file_contents(rest_class))
    # TODO uncomment this when done
    # write_file("tests/clients/" + rest_class.file_name + ".php", rest_class_to_test_file_contents(rest_class))


def write_tree_to_files(tree):
    map(write_class_to_files, tree)


def validate_args(parser, options, args):
    assert options
    if len(args) < 1:
        parser.error("The first positional argument must be the file tree to parse.")


def main():
    parser = benchline.args.make_parser(usage="usage: %%prog [options] tree_file\n%s" % __doc__)
    options, args = benchline.args.triage(parser, validate_args=validate_args)
    tree = parse_tree(read_tree(args[0]))
    write_tree_to_files(tree)


if __name__ == "__main__":
    main()
