from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .forms import RegisterForm, UserManageForm
from .serializers import UserSerializer


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('id').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
