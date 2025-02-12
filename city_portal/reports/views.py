from django.shortcuts import render

def home(request):
    return render(request, 'reports/index.html')

def register(request):
    return render(request, 'reports/register.html')

def login_view(request):
    return render(request, 'reports/login.html')
def profile(request):
    return render(request, 'reports/profile.html')
def add_order(request):
    return render(request, 'reports/add_order.html')