from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ReportForm
from .models import Report
from django.contrib import messages

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

# Регистрация пользователя
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Перенаправление после успешной регистрации
    else:
        form = CustomUserCreationForm()
    
    return render(request, "reports/register.html", {"form": form})  # ✅ Убедись, что путь правильный

# Авторизация пользователя
def login_view(request):
    print(f"Метод запроса: {request.method}")  
    if request.method == "POST":
        print(f"POST-данные: {request.POST}")  

        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"Введённые данные: {username}, {password}")

        user = authenticate(request, username=username, password=password)
        print(f"Результат authenticate(): {user}")  # ДОЛЖНО выводить пользователя!

        if user:
            login(request, user)
            print("Пользователь вошел!")
            return redirect("profile")
        else:
            print("Ошибка: неверные имя пользователя или пароль")
            messages.error(request, "Неверное имя пользователя или пароль")
    
    return render(request, "reports/login.html")

# Выход пользователя
def user_logout(request):
    logout(request)
    return redirect("index")

# Личный кабинет пользователя
@login_required
def profile(request):
    reports = Report.objects.filter(user=request.user)
    return render(request, "reports/profile.html", {"reports": reports})

# Создание заявки
@login_required
def add_order(request):
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect("profile")
    else:
        form = ReportForm()
    return render(request, "reports/add_order.html", {"form": form})
