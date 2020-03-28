from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import logout
from grp.forms import RegisterForm, ProfileForm, CicleForm
from django.contrib import messages
from grp.models import Profile, Cicle
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/profile")
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)


class HomeView(TemplateView):
    template_name = "home.html"


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                if User.objects.filter(
                        username=form.cleaned_data['username']).exists():
                    messages.error(request,
                                   u"Пользователь с таким именем уже есть, "
                                   u"введите новое имя"
                                   )
                    return redirect("/register")
                elif User.objects.filter(
                        email=form.cleaned_data['email']).exists():
                    messages.error(request,
                                   u"Пользователь с таким email уже есть, "
                                   u"введите новый email "
                                   )
                    return redirect("/register")
                self.create_new_user(form)
                messages.success(request, u"Вы успешно зарегистрировались!")
                return redirect("/login")

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def create_new_user(self, form):
        email = None
        if 'email' in form.cleaned_data:
            email = form.cleaned_data['email']
        User.objects.create_user(form.cleaned_data['username'],
                                 email, form.cleaned_data['password']
                                 )


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect(reverse("edit_profile"))
        form = CicleForm()
        if request.method == 'POST':
            form = CicleForm(request.POST)
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                messages.success(request, u"Ваш новый цикл добавлен")
                return redirect("/profile")
            else:
                messages.error(request, u"Произошла непредвиденная ошибка")
                return redirect("/profile")
        return render(request, self.template_name,
                      {'selected_user': request.user,
                       'cicle_form': form
                       }
                      )

    def get_profile(self, user):
        try:
            return user.profile
        except AttributeError:
            return None


@login_required
def all_cicles(request):

    cicle = Cicle.objects.filter(user=request.user)
    return render(request, "adder.html", {'cicles': cicle})


class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES,
                               instance=self.get_profile(request.user)
                               )
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                messages.success(request, u"Профиль успешно обновлен!")
                return redirect("/profile")
        return render(request, self.template_name, {'form': form})

    def get_profile(self, user):
        try:
            return user.profile
        except AttributeError:
            return None


def delete(request, id):
    try:
        cicle = Cicle.objects.get(id=id)
        cicle.delete()
        messages.error(request, u"Цикл успешно удален")
        return redirect("/profile/adder")
    except Cicle.DoesNotExist:
        messages.error(request, u"Цикл не найден")
        return redirect("/adder")


def correct(request, id):
    try:
        form = CicleForm(request.POST)
        if request.method == "POST":
            cicle = Cicle.objects.get(id=id)
            cicle.last_cicle_first_date = datetime.strptime(
                request.POST.get("last_cicle_first_date"), '%d/%m/%Y').date()
            cicle.last_cicle_last_date = datetime.strptime(
                request.POST.get("last_cicle_last_date"), '%d/%m/%Y').date()
            cicle.save()
            messages.success(request, u"Цикл успешно обновлен")
            return redirect("/profile/adder")
        else:
            return render(request, "cicles/correct.html", {"cicle_form": form})
    except Cicle.DoesNotExist:
        messages.error(request, u"Цикл не найден")
        return redirect("/adder")
