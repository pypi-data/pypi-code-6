from jingen import Jingen

template_file = "mock.template"
vars_source = "tests/resources/mock_vars.py"
# alternatively, can be a dict:
# vars_source = {
#     "test_var": "manual_tester_test_value"
# }
output_file = "tests/resources/manual_test_result.file"
template_dir = "tests/resources/"
make_file = True

i = Jingen(
    template_file=template_file,
    vars_source=vars_source,
    output_file=output_file,
    template_dir=template_dir,
    make_file=make_file)
output = i.generate()

print output
