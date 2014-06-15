"""
DB Utils
=========

Il modulo fornisce database utilities per i models

-------------

.. autofunction:: clone

"""
from django.db import transaction

@transaction.commit_manually
def clone(obj):
    """Crea un'istanza di un modello con i valori di un'altra instanza esistente (tranne l'id), comprese
    le relazioni m2m e fk.
    
    :param obj: instanza modello
    """
    try:
        obj_new = obj.__class__()
        obj_new.__dict__.update(obj.__dict__)
        obj_new.pk = None
        obj_new.save()
        # foreignkey
        for related in obj._meta.get_all_related_objects():
            setattr(obj_new, related.get_accessor_name(), getattr(obj, related.get_accessor_name()).all())
        obj_new.save()
        # many-to-many
        for m2m_field in obj._meta.many_to_many:
            setattr(obj_new, m2m_field.attname, getattr(obj, m2m_field.attname).all())
            #setattr(obj_new, m2m_field.attname, getattr(obj, m2m_field.attname).all())
        obj_new.save()
        transaction.commit()
        return (obj_new, True)
    except Exception, e:
        transaction.rollback()
        return (e, False)
