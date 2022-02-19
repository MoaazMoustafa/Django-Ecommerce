from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import UserRegisterationForm
from .token import account_activation_token


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
            return HttpResponse('registered succesfully and activation sent')
        else:
            return render(request, 'account/registeration/register.html', {'form': registerForm})
    registerForm = UserRegisterationForm()
    return render(request, 'account/registeration/register.html', {'form': registerForm})
