from django.db.models.related import RelatedObject
from django.db.models.fields import Field
from django.db.models.fields.related import ManyToManyRel, ForeignRelatedObjectsDescriptor, ManyToManyField
from django.utils.encoding import smart_unicode


class ReverseForeignRelation(ManyToManyField):
    """Provides an accessor to reverse foreign key related objects"""

    def __init__(self, to, field_name, **kwargs):
        kwargs['verbose_name'] = kwargs.get('verbose_name', None)
        kwargs['rel'] = ManyToManyRel(to,
                            related_name='+',
                            symmetrical=False,
                            limit_choices_to=kwargs.pop('limit_choices_to', None),
                            through=None)
        self.field_name = field_name

        kwargs['blank'] = True
        kwargs['editable'] = True
        kwargs['serialize'] = False
        Field.__init__(self, **kwargs)

    # def get_choices_default(self):
    #     return Field.get_choices(self, include_blank=False)
    #
    # def value_to_string(self, obj):
    #     qs = getattr(obj, self.name).all()
    #     return smart_unicode([instance._get_pk_val() for instance in qs])

    def m2m_db_table(self):
        return self.rel.to._meta.db_table

    def m2m_column_name(self):
        return self.field_name

    def m2m_reverse_name(self):
        return self.rel.to._meta.pk.column

    def m2m_target_field_name(self):
        return self.model._meta.pk.name

    def m2m_reverse_target_field_name(self):
        return self.rel.to._meta.pk.name

    def contribute_to_class(self, cls, name):
        self.model = cls
        super(ManyToManyField, self).contribute_to_class(cls, name)

        # Save a reference to which model this class is on for future use

        # Add the descriptor for the m2m relation
        field = self.rel.to._meta.get_field(self.field_name)
        setattr(cls, self.name, ForeignRelatedObjectsDescriptor(
            RelatedObject(cls, self.rel.to, field)))

    def contribute_to_related_class(self, cls, related):
        pass

    # def set_attributes_from_rel(self):
    #     pass

    def get_internal_type(self):
        return "ManyToManyField"

    # def db_type(self, connection):
    #     # Since we're simulating a ManyToManyField, in effect, best return the
    #     # same db_type as well.
    #     return None

    def formfield(self, **kwargs):
        from cropduster.models import Thumb
        from cropduster.forms import CropDusterThumbFormField

        kwargs.update({
            'form_class': CropDusterThumbFormField,
            'queryset': Thumb.objects.none(),
        })
        return super(ManyToManyField, self).formfield(**kwargs)
