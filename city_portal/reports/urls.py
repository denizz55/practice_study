from django.urls import path
from . import views  
from reports.views import home, register, login_view, profile, add_order, user_logout
urlpatterns = [
    path('', home, name='index'),
    path('register/', register, name='register'),  
    path('login/', login_view, name='login'),
    path("logout/", user_logout, name="logout"),  
    path('profile/', profile, name='profile'),
    path('add_order/', add_order, name='add_order'),
]