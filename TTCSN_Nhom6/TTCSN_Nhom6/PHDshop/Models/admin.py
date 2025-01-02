from django.contrib import admin
from .models import *

# Registering Admin model
admin.site.register(Admin)


# Registering Address model
admin.site.register(Address)


# Registering Promotion model
admin.site.register(Promotion)


# Registering Contact model
admin.site.register(Contact)


# Registering ProductPromotion model
admin.site.register(GoodPromotion)
