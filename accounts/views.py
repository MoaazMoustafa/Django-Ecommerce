from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import login, logout
from .forms import UserEditForm, UserRegisterationForm
from .token import account_activation_token
from .models import User
from django.urls import reverse


def signup(request):
    if request.method == 'POST':
        registerForm = UserRegisterationForm(data=request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registeration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')
        else:
            return render(request, 'account/registeration/register.html', {'form': registerForm})
    registerForm = UserRegisterationForm()
    return render(request, 'account/registeration/register.html', {'form': registerForm})


@login_required
def dashboard(request):
    return render(request, 'account/user/dashboard.html')


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registeration/activation_invalid.html')


@login_required
def profile_edit(request):
    if request.method == "POST":
        registerForm = UserEditForm(instance=request.user, data=request.POST)
        if registerForm.is_valid():
            registerForm.save()
            return redirect('account:dashboard')
        else:
            print('registerform not valid 🌹🌹🌹🌹')
            print(registerForm)
            return render(request, 'account/user/edit_details.html', {'user_form': registerForm})
    else:
        registerForm = UserEditForm(instance=request.user)
    return render(request, 'account/user/edit_details.html', {'user_form': registerForm})


@login_required
def profile_delete(request):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        user.is_active = False
        user.save()
        logout(request)
    return redirect('account:delete_confirmation')
