from naman.core.models import VLan
from django.core.exceptions import ImproperlyConfigured


def assign_provisioning_vlan(machine):
  
    print("Entering assign_provisioning_vlan")
    prov_vlans = VLan.objects.filter(provisioning_purpose=True)
    if prov_vlans.count() == 0:
        raise ImproperlyConfigured("Missing provisioning vlans")

    for vlan in prov_vlans:
        try:
            machine.get_vlanconfig().append_vlan(vlan)
            return
        except VLan.NoFreeIPError:
            continue

    raise VLan.NoFreeIPError("No free IPs at any provisioning vlan")
    
  
def assign_backup_vlan(machine):
    #logging.basicConfig(level=logging.DEBUG)
    print("Entering assign_backup_vlan")
    for vlan in machine.environment.backup_vlans.all().order_by('name'):
        try:
            machine.get_vlanconfig().append_vlan(vlan)
            return
        except VLan.NoFreeIPError:
            continue
    raise VLan.NoFreeIPError("No free IPs at any backup vlan")


def assign_management_vlan(machine):
    print("Entering management vlan")
    man_vlans = VLan.objects.filter(management_purpose=True)
    if man_vlans.count() == 0:
        raise ImproperlyConfigured("Missing management vlans")

    for vlan in man_vlans:
        try:
            machine.get_vlanconfig().append_vlan(vlan)
            return
        except VLan.NoFreeIPError:
            continue

    raise VLan.NoFreeIPError("No free IPs at any management vlan")


def assign_dmz_based_on_project(machine):
    print("Entering dmz based on project vlan")
    #if machine.dmz_located:
    project = machine
    if project is None or project.dmz is None:
        raise ImproperlyConfigured(
            "DMZ located machine must belong to a project which has dmz vlan assing")
    machine.get_vlan_config().append_vlan(project.dmz)
        
        
def assign_service_vlan_based_on_project(machine):
    print("Entering service vlan based on project")
    project = machine.project
    for vlan in project.service_vlans.all().order_by('name'):
        try:
            machine.get_vlanconfig().append_vlan(vlan)
            return
        except VLan.NoFreeIPError:
            continue
    
def assign_general_purpose_service_vlan(machine):
    print("General purpose service vlan")
    for vlan in machine.environment.service_vlans.all().order_by('name'):
        #print "trying service vlan with: %s" % vlan
        try:
            machine.get_vlanconfig().append_vlan(vlan)
            return
        except VLan.NoFreeIPError:
            continue

    #raise VLan.NoFreeIPError("Can't assign free IP for service vlan")
mappings = [
    assign_backup_vlan,
    assign_management_vlan,
    assign_provisioning_vlan,
    assign_dmz_based_on_project,
    assign_service_vlan_based_on_project,
    assign_general_purpose_service_vlan,
   
    ]