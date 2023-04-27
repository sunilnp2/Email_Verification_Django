from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from myapp.forms import UserRegistrationForm, UserLoginForm
# from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.contrib.auth.forms import  AuthenticationForm
from django.shortcuts import render
from django.contrib import auth 
# Create your views here.

from django.views import View

def home(request):
    return render(request, 'index.html')

# def signup(request):
#     return render(request, 'signup.html')




def activate(request, uidb64, token):
    User = User()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('homepage')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("profile.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

from myapp.models import User

# register
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            User.email_verify=False
            user.save()
            messages.success(request, "You are registered successfully")
            activateEmail(request, user, form.cleaned_data.get('email')) 
            return redirect('/')

    else:
        form = UserRegistrationForm()

    return render(request,"signup.html",{'form': form})


def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")


def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
            user = auth.authenticate(username = username, password = password)
            if user is not None :
                login(request, user)
                messages.success(request, f"Hello <b>{user.email}</b>! You have been logged in")
                return redirect("myapp:home")
            

    form = AuthenticationForm()

    return render(request,"login.html",context={"form": form}
        )
