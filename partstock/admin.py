from django.contrib import admin
from .models import Part, StockMovement, MovementItem 

admin.site.register(Part)
admin.site.register(StockMovement)
admin.site.register(MovementItem)
