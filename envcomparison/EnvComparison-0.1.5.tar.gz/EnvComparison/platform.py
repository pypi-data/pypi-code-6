








def get_platform_name():
    for line, ecode in o.run_command('cat /etc/lsb-release'):
        if 'DISTRIB_ID' in line:
            return line.split("=")[1].lower().replace('\n','')






