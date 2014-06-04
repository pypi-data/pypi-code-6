import tasks


def validate_manifest(data, validator, error):
	import os.path
	schema_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'manifest-schema.json'))
	validator(data, schema_path)


def resolve_tasks(taskset, manifest):
	taskset.add(tasks.InstallSaltDependencies)
	taskset.add(tasks.BootstrapSaltMinion)
	if 'grains' in manifest.plugins['salt']:
		taskset.add(tasks.SetSaltGrains)
