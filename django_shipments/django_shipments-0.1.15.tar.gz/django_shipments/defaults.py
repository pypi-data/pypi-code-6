from django.utils.translation import ugettext as _

from mezzanine.conf import register_setting

register_setting(
	name="UPS_CREDENTIALS",
	description="UPS credentials: username, password, \
		access license, shipper number",
	editable=False,
)

register_setting(
	name="UPS_SHIPMENT_ORIGIN",
	description="Address of the origin of the package",
	editable=False,
)