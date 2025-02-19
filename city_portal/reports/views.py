from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ReportForm, CategoryForm
from .models import Report, Category
from django.contrib import messages

def index(request):
    # Получаем последние 4 решенные заявки
    resolved_reports = Report.objects.filter(status='resolved').order_by('-created_at')[:4]
    # Получаем общее количество решенных заявок
    total_resolved = Report.objects.filter(status='resolved').count()
    
    return render(request, 'reports/index.html', {
        'resolved_reports': resolved_reports,
        'total_resolved': total_resolved
    })

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически входим после регистрации
            return redirect("profile")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "reports/register.html", {"form": form})  # Убедись, что путь правильный

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
            if user.is_staff:  # Если пользователь админ
                return redirect("admin_profile")
            else:  # Если обычный пользователь
                return redirect("profile")
        else:
            print("Ошибка: неверные имя пользователя или пароль")
            messages.error(request, "Неверное имя пользователя или пароль")
    
    return render(request, "reports/login.html")

# Выход пользователя
def user_logout(request):
    logout(request)
    return redirect("index")

# Декоратор для проверки прав администратора
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, "Доступ запрещен. Требуются права администратора.")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper

# Личный кабинет пользователя
@login_required
def profile(request):
    if request.user.is_staff:
        return redirect('admin_profile')

    reports = Report.objects.filter(user=request.user)

    status_new = request.GET.get('status_new')
    status_resolved = request.GET.get('status_resolved')
    sort_by_date = request.GET.get('sort_by_date')

    if status_new:
        reports = reports.filter(status='pending')
    if status_resolved:
        reports = reports.filter(status='resolved')

    if sort_by_date:
        reports = reports.order_by('-created_at')
    else:
        reports = reports.order_by('created_at')

    return render(request, 'reports/profile.html', {
        'user_reports': reports,
        'user_info': request.user,
    })

# Личный кабинет администратора
@admin_required
def admin_profile(request):
    if request.method == "POST":
        if 'add_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                messages.success(request, 'Новая категория успешно создана!')
                return redirect('admin_profile')
        else:
            report_id = request.POST.get('report_id')
            action = request.POST.get('action')
            
            if report_id and action:
                report = Report.objects.get(id=report_id)
                
                # Маппинг действий на статусы
                status_mapping = {
                    'approve': 'approved',
                    'reject': 'rejected',
                    'in_progress': 'in_progress',
                    'resolved': 'resolved'
                }
                
                if action in status_mapping:
                    # Если отмечаем как решенную, требуем фото "после"
                    if action == 'resolved':
                        if 'image_after' in request.FILES:
                            report.image_after = request.FILES['image_after']
                        else:
                            messages.error(request, 'Необходимо загрузить фото "после" решения проблемы')
                            return redirect('admin_profile')
                    
                    report.status = status_mapping[action]
                    report.save()
                    messages.success(request, f'Статус заявки "{report.title}" обновлен на {report.get_status_display()}')
    
    # Получаем все заявки для админа
    all_problems = Report.objects.all().order_by('-created_at')
    # Создаем пустую форму для категории
    category_form = CategoryForm()
    # Получаем все существующие категории
    categories = Category.objects.all().order_by('name')
    
    return render(request, 'reports/admin_profile.html', {
        'all_problems': all_problems,
        'user': request.user,
        'category_form': category_form,
        'categories': categories
    })

# Создание заявки
@login_required
def add_order(request):
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.status = 'pending'
            report.save()
            messages.success(request, "Заявка успешно создана и отправлена на рассмотрение")
            return redirect("profile")
    else:
        form = ReportForm()
    
    return render(request, "reports/add_order.html", {"form": form})

# Удаление заявки
@login_required
def delete_application(request, application_id):
    report = get_object_or_404(Report, id=application_id)
    report.delete()
    return redirect('profile')

# Отклонение заявки
@login_required
def reject_application(request, application_id):
    report = get_object_or_404(Report, id=application_id)
    if request.method == "POST":
        rejection_reason = request.POST.get('rejection_reason')
        if rejection_reason:
            report.status = 'rejected'
            report.rejection_reason = rejection_reason
            report.save()
            messages.success(request, 'Заявка успешно отклонена.')
        return redirect('profile')
    return render(request, 'reports/reject_application.html', {'report': report})