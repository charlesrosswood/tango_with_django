from rango.models import SiteUser
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django.settings")

sresult_dict = SiteUser.create(first_name='Charles', last_name='Wood', email='charles.ross.wood@gmail.com', username='chazrwood', password='1')

print result_dict