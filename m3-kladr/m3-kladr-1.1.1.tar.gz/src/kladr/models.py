#coding:utf-8

from django.db import models

class KladrGeo(models.Model):
    '''
    Справочник КЛАДР
    '''
    parent = models.ForeignKey('KladrGeo', null=True, blank=True)
    name = models.CharField(max_length=40, db_index = True)
    socr = models.CharField(max_length=10, db_index = True)
    code = models.CharField(max_length=13, db_index = True)
    zipcode = models.CharField(max_length=6)
    gni = models.CharField(max_length=4)
    uno = models.CharField(max_length=4)
    okato = models.CharField(max_length=11)
    status = models.CharField(max_length=1)
    level = models.IntegerField(null=True, blank=True)
    
    def display_name(self):
        if self.parent:
            return self.socr+" "+self.name+" / "+self.parent.display_name()
        else:
            return self.socr+" "+self.name
    display_name.json_encode = True
    
    def addr_name(self):
        # наименование в формате текстового адреса
        curr = self
        res = None
        while curr:
            if res:
                res = curr.socr+" "+curr.name+", "+res
            else:
                res = curr.socr+" "+curr.name
            curr = curr.parent
        return res
    addr_name.json_encode = True
    
class KladrStreet(models.Model):
    '''
    Справочник КЛАДР (улицы)
    ''' 
    parent = models.ForeignKey('KladrGeo', null=True, blank=True)
    name = models.CharField(max_length=40, db_index = True)
    socr = models.CharField(max_length=10, db_index = True)
    code = models.CharField(max_length=17, db_index = True)
    zipcode = models.CharField(max_length=6)
    gni = models.CharField(max_length=4)
    uno = models.CharField(max_length=4)
    okato = models.CharField(max_length=11)
    
    def display_name(self):
        if self.parent:
            return self.socr+" "+self.name+" / "+self.parent.name
        else:
            return self.socr+" "+self.name
    display_name.json_encode = True