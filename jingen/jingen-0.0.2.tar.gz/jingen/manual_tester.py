from jingen import TemplateHandler

template_file = "mock.template"
# vars_source = {
#     "test_var": "manual_tester_test_value"
# }
vars_source = "tests/resources/mock_vars.py"
output_file = "tests/resources/manual_test_result.file"
templates_dir = "tests/resources/"
make_file = True
verbose = True

i = TemplateHandler(
    template_file=template_file,
    vars_source=vars_source,
    output_file=output_file,
    templates_dir=templates_dir,
    make_file=make_file,
    verbose=verbose)
output = i.generate()

print output
