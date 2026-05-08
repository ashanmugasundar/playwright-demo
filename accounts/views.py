from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .forms import RegisterForm, UserManageForm
from .serializers import UserSerializer
from functools import wraps
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
import csv
from .permissions import IsStaffOrReadOnly


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped


def register_view(request):
    if request.user.is_authenticated:
        return redirect('users_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users_list')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def users_list(request):
    users = User.objects.order_by('id').all()
    return render(request, 'accounts/users_list.html', {'users': users})


@login_required
@staff_required
def user_add(request):
    if request.method == 'POST':
        form = UserManageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created.')
            return redirect('users_list')
    else:
        form = UserManageForm()
    return render(request, 'accounts/user_form.html', {'form': form, 'mode': 'add'})


@login_required
@staff_required
def user_edit(request, user_id: int):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserManageForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated.')
            return redirect('users_list')
    else:
        form = UserManageForm(instance=user)
    return render(request, 'accounts/user_form.html', {'form': form, 'mode': 'edit', 'target_user': user})


class UserViewSetOld(viewsets.ModelViewSet):
    queryset = User.objects.order_by('id').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('id').all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffOrReadOnly]


@staff_required
def users_export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(["id", "username", "email", "is_active", "is_staff"])

    for u in User.objects.order_by("id").all():
        writer.writerow([u.id, u.username, u.email, u.is_active, u.is_staff])

    return response
