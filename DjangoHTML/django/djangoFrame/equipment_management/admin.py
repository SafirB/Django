from django.contrib import admin
from .models import Item
from .models import Reservation

# Register your models here.

admin.site.register(Item)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'date', 'time', 'status')
    list_filter = ('status',)
    actions = ['approve_reservations', 'deny_reservations']

    def approve_reservations(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected reservations have been approved.")
    approve_reservations.short_description = "Approve selected reservations"

    def deny_reservations(self, request, queryset):
        queryset.update(status='denied')
        self.message_user(request, "Selected reservations have been denied.")
    deny_reservations.short_description = "Deny selected reservations"