from urlparse import urlparse

DOCKER_ENV_PREFIX = 'ENV'
DOCKER_PORT_PREFIX = 'PORT'


def process_variable_for_docker(key, value, type_name, index, variable_name,
                                docker_info):
    docker_info = docker_info or {
        "hostname": "%s_%s" % (type_name.lower(), index),
        "env": {}
    }

    # Parse the port variable
    # For now this is the only "PORT" variable we should parse the others don't
    # really make much sense
    if variable_name == DOCKER_PORT_PREFIX:
        parsed_url = urlparse(value)

        docker_info['ip'] = parsed_url.hostname

    # Parse an env variable
    if variable_name.startswith(DOCKER_ENV_PREFIX):
        env_variable_name = variable_name[len(DOCKER_ENV_PREFIX + 1):]
        docker_info['env'][env_variable_name] = value

    return docker_info


def process_env(type_names_to_process, env, process_docker=False):
    # Collect all the data
    working_storage = dict()
    for key, value in env.iteritems():

        for type_name in type_names_to_process:
            if key.startswith(type_name):
                # Parse the key like so
                # TYPE_NAME_INDEX#_ENVIRONMENT_VARIABLE
                key_without_prefix = key[len(type_name) + 1:]

                split_key_without_prefix = key_without_prefix.split('_')

                index = int(split_key_without_prefix[0])

                variable_name = "_".join(split_key_without_prefix[1:])

                # Initialize the storage with defaults
                type_storage = working_storage.get(type_name, {})
                index_storage = type_storage.get(index, {"_index": index})

                index_storage[variable_name] = value

                # If we enable docker parsing mode parse the SERVER_PORT
                # variables created during linking. Works on docker 1.2.x
                if process_docker:
                    docker_info = index_storage.get('docker', None)
                    docker_info = process_variable_for_docker(
                        key,
                        value,
                        type_name,
                        index,
                        variable_name,
                        docker_info
                    )
                    index_storage['docker'] = docker_info

                # Save the storage
                type_storage[index] = index_storage
                working_storage[type_name] = type_storage

    env_copy = env.copy()
    env_copy.update(_generate_context_object(type_names_to_process,
                                             working_storage))
    return env_copy


def _generate_context_object(type_names_to_process, working_storage):
    # Render the collected data into a context
    context_object = {}

    for type_name in type_names_to_process:
        context_object_type_data = []

        working_storage_type_data = working_storage.get(type_name, {})

        for index, index_data in working_storage_type_data.iteritems():
            context_object_type_data.append(index_data)

        # Create a pluralized name of the type
        type_plural_name = "%sS" % type_name
        if type_name.endswith('S'):
            type_plural_name = "%sES" % type_name

        sorted_context_object_type_data = sorted(context_object_type_data,
                                                 key=lambda obj: obj['_index'])

        context_object[type_plural_name] = sorted_context_object_type_data

        # duplicate the context data into it's lower cased name so it can be
        # accessed that way
        context_object[type_plural_name.lower()] = context_object_type_data

    return context_object
