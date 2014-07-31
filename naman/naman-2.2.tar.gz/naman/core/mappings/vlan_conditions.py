

def environment(machine):
    
    env = machine.environment.to_pypelib()
    print("Environment: %s" % env)
    return env


def project(machine):
    return machine.project.to_pypelib()


def role_needs_backup(machine):
    does = "1" if machine.role.needs_backup_vlan else "0"
    print("role_needs_backup: %s" % does)
    return does
    
    
def needs_backup(machine):
    does = "1" if machine.get_vlanconfig().needs_backup else "0"
    print("vlan_config needs backup: %s" % does)
    return does

    
def dmz_located(machine):
    does = "1" if machine.dmz_located else "0"
    print("machine dmz located: %s" % does)
    return does


def needs_management(machine):
    does = "1" if machine.get_vlanconfig().needs_management else "0"
    print("Vlan_config needs management: %s" % does)
    return does

    
mappings = [
    environment,
    project,
    role_needs_backup,
    dmz_located,
    needs_management,
    needs_backup,
   ]