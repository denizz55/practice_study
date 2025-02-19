from django.urls import path
from reports.views import (
    index, register, login_view, profile,
    add_order, user_logout, admin_profile, delete_application, reject_application
)

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('add_order/', add_order, name='add_order'),
    path('logout/', user_logout, name='logout'),
    path('admin_profile/', admin_profile, name='admin_profile'),
    path('delete_application/<int:application_id>/', delete_application, name='delete_application'),
    path('reject_application/<int:application_id>/', reject_application, name='reject_application'),
]