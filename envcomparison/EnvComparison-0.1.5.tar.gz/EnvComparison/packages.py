


def get_packages():
    packages = {}
    for line in o.run_command('dpkg -l'):
        parts = line.split()
        if parts[0] == 'ii':
            packages[parts[1]] = parts[2]
    return packages











