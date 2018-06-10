from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignInForm, SignUpForm, ChangeProfileForm


def signin_fbv(request):
    if request.method == "POST":
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('post:list')
        else:
            form.add_error(None, '아이디나 비밀번호가 잘못되었습니다.')

    else:
        form = SignInForm()

    context = {
        'form': form,
    }

    return render(request, 'member/signin_p.html', context)


def signup_fbv(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            return redirect('post:list')
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup_p.html', context)


@login_required
def profile_fbv(request):
    context = {

    }
    return render(request, 'member/profile.html', context)


@login_required
def change_profile_fbv(request):
    if request.method == 'POST':
        form = ChangeProfileForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            form.save()
            return redirect('member:profile')
    else:
        form = ChangeProfileForm(
            instance=request.user
        )
    context = {
        'form': form,
    }
    return render(request, 'member/change_profile.html', context)


def signout_fbv(request):
    logout(request)
    return redirect('member:signin')
