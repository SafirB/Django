#Edited By Everyone

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .views import signup
from .views import reports_view
from .views import dashboard_view
from .views import delete_reservation
from .views import view_inventory
from .views import manage_account
from .views import equipment_usage_history_view
from django.urls import path, reverse_lazy


app_name = "equipment_management"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='equipment_management/login.html',redirect_authenticated_user=False), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='equipment_management:login'), name='logout'),
    path('', RedirectView.as_view(url='products/', permanent=True)),
    path('signup/', signup, name='signup'),
    path('reserve/<int:item_id>/', views.create_reservation, name='create_reservation'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('products/', views.product_list, name='product_list'),
    path('reports/', reports_view, name='reports'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('view_inventory/', view_inventory, name='view_inventory'),
    path('manage_account/', manage_account, name='manage_account'),
    path('change-password/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('equipment_management:manage_account')), name='change_password'),
    path('equipment-usage-history/', equipment_usage_history_view, name='equipment_usage_history'),

]