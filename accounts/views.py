from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import SecurityAnswers

# Create your views here.
def signup(request):
    template_data = {}
    template_data['title'] = 'Create an Account'

    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['username'] = form.cleaned_data['username']
            return redirect('accounts.security')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

def security(request):
    template_data = {}
    template_data['title'] = 'Set Up Security Questions'
    if request.method == 'GET':
        return render(request, 'accounts/security.html', {'template_data': template_data})
    elif request.method == 'POST':
        username = request.session['username']
        try:
            user = User.objects.get(username = username)
            security = SecurityAnswers(user = user)
            security.securityAnswer1 = request.POST['securityAnswer1']
            security.securityAnswer2 = request.POST['securityAnswer2']
            security.save()
            return redirect('accounts.login')
        except:
            return render(request, 'accounts/security.html', {'template_data': template_data})
    else:
        return render(request, 'accounts/security.html', {'template_data': template_data})

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'Your username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def reset(request):
    template_data = {}
    template_data['title'] = 'Reset Password'
    if request.method == 'GET':
        return render(request, 'accounts/reset.html', {'template_data': template_data})
    elif request.method == 'POST':
        try:
            user = User.objects.get(username = request.POST['username'])
            security = SecurityAnswers.objects.get(user = user)
        except:
            template_data['error'] = 'No user found.'
            return render(request, 'accounts/reset.html', {'template_data': template_data})
        if user is not None:
            securityAnswer1 = request.POST.get('securityAnswer1')
            securityAnswer2 = request.POST.get('securityAnswer2')
            if security.securityAnswer1 != securityAnswer1:
                template_data['error'] = 'Incorrect security answer.'
                return render(request, 'accounts/reset.html', {'template_data': template_data})
            if security.securityAnswer2 != securityAnswer2:
                template_data['error'] = 'Incorrect security answer.'
                return render(request, 'accounts/reset.html', {'template_data': template_data})
            user.set_password(request.POST['newpassword'])
            user.save()
            return redirect('accounts.login')
        else:
            template_data['error'] = 'Problem with username.'
            return render(request, 'accounts/reset.html', {'template_data': template_data})
    else:
        return render(request, 'accounts/reset.html', {'template_data': template_data})
