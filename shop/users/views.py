from pyexpat.errors import messages
from typing import Self
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from product.models import RecentlyViewedProducts
from users.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from users.forms import UserLoginForm
from .forms import UserEditForm, UserRegisterForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from users.mixins import UserIsNotAuthenticated
from django.contrib.auth.decorators import login_required

from email.message import EmailMessage
import smtplib


User = get_user_model()


class UserLoginView(LoginView):
    
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = "Login"


class UserRegisterView(UserIsNotAuthenticated, CreateView):
   
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # відправка листів з токеном
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('confirm_email', kwargs={
                                      'uidb64': uid, 'token': token})
        current_site = f"localhost:8000/"

        from_email = 'Confirmation of Registration <confirmationofregistration@ukr.net>'
        to_email = [user.email]
        message_body = f'Follw this link to activate your account: http://{current_site}{activation_url}'

        msg = EmailMessage()
        msg['From'] = from_email
        msg['To'] = to_email
        msg.set_content(message_body)

        server = smtplib.SMTP_SSL('smtp.ukr.net', 2525)
        server.login("confirmationofregistration@ukr.net", "RxFucyKX5nqimoOk")
        server.send_message(msg)

        server.quit()

        return redirect('email_confirmation_sent')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Activation email sent'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        
        user.is_verified_email = True
        user.save()
        
        context = super().get_context_data(**kwargs)
        context['title'] = 'Your email has been activated.'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Your email doesn't activated."
        return context

@login_required
def logout_view(request):
    RecentlyViewedProducts.objects.all().delete()
    print("they should have been already deleted!!!!!!!!!!!")
    logout(request)
    return render(request, 'users/logout.html')


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():        
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
          
    else:
        form = UserLoginForm(request)

    context = {'form': form}
    return render(request, 'login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})
