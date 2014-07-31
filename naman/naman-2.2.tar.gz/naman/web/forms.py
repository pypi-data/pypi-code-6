from naman.core.models import Machine, Iface, VLanConfig, ConflictingIP, Service
from django.forms import ModelForm


class VLanConfigForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VLanConfigForm, self).__init__(*args, **kwargs)
        self.fields["machine"].widget.attrs = {"style": "display:none"}
        for name, f in self.fields.items():
           # f.widget.attrs = {'required': 'true'}

            f.widget.attrs['placeholder'] = "%s ..." % f.label
            if f.widget.__class__.__name__ != "CheckboxInput":
                f.widget.attrs["class"] = "form-control"

    class Meta:
        model = VLanConfig
        exclude = "vlans"


class ConflictingIPForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConflictingIPForm, self).__init__(*args, **kwargs)
        for name, f in self.fields.items():
           # f.widget.attrs = {'required': 'true'}

            f.widget.attrs['placeholder'] = "%s ..." % f.label
            if f.widget.__class__.__name__ != "CheckboxInput":
                f.widget.attrs["class"] = "form-control"
    class Meta:
        model = ConflictingIP



class MachineForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MachineForm, self).__init__(*args, **kwargs)
        for name, f in self.fields.items():
           # f.widget.attrs = {'required': 'true'}
            f.widget.attrs['placeholder'] = "%s ..." % f.label
            if f.widget.__class__.__name__ != "CheckboxInput":
                f.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(MachineForm, self).clean()
        hostname = cleaned_data.get("hostname")
        mtype = cleaned_data.get("mtype")
        role = cleaned_data.get("role")
        env = cleaned_data.get("environment")
        os = cleaned_data.get("operating_system")

        if hostname in (None, ""):
            if mtype is None or not mtype.auto_name:
                self._errors["mtype"] = self.error_class(
                    ["Hostname must be filled if mtype is not auto_named"])
                try:
                    del cleaned_data["mtype"]
                except KeyError:
                    pass

            if role is None:
                self._errors["role"] = self.error_class(
                    ["Role must be filled if hostname is empty"]
                )
                try:
                    del cleaned_data["role"]
                except KeyError:
                    pass

            if env is None:
                self._errors["environment"] = self.error_class(
                    ["Environment must be filled if hostname is empty"]
                )
                try:
                    del cleaned_data["environment"]
                except KeyError:
                    pass

            if os is None:
                self._errors["operating_system"] = self.error_class(
                    ["Operating system must be filled if hostname is empty"]
                )
                try:
                    del cleaned_data["operating_system"]
                except KeyError:
                    pass

        return cleaned_data

    class Meta:
        model = Machine


class IfaceByMachineForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IfaceByMachineForm, self).__init__(*args, **kwargs)
        #self.fields["machines"].choices = Iface.objects.filter(id)
        #self.fields["machines"].widget.attrs = {"style": "display:none"}
        for name, f in self.fields.items():
           # f.widget.attrs = {'required': 'true'}
            f.widget.attrs['placeholder'] = "%s ..." % f.label
            if f.widget.__class__.__name__ != "CheckboxInput":
                f.widget.attrs["class"] = "form-control"

    class Meta:
        model = Iface
        fields = ("machines", "ip", "dhcp", "vlan", "comments" )


class ServiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)

        for name, f in self.fields.items():
            print name
           # f.widget.attrs = {'required': 'true'}
            f.widget.attrs['placeholder'] = "%s ..." % f.label
            if f.widget.__class__.__name__ != "CheckboxInput":
                f.widget.attrs["class"] = "form-control"

    class Meta:
        model = Service
        fields = ('name', 'iface', 'description')



class IfaceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IfaceForm, self).__init__(*args, **kwargs)
        self.fields["mask"].widget.attrs = {"disabled": ""}
        for name, f in self.fields.items():
           # f.widget.attrs = {'required': 'true'}
            f.widget.attrs['placeholder'] = "%s ..." % f.label
            if f.widget.__class__.__name__ != "CheckboxInput":
                f.widget.attrs["class"] = "form-control"

    class Meta:
        model = Iface


class IfaceShortForm(IfaceForm):
    class Meta:
        model = Iface
        exclude = ("nat", "gw", "mask", "name", "comments", "nat", "virtual", )
