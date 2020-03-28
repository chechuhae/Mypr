from grp.models import Profile, Cicle
from django import forms
from .widgets import BootstrapDateTimePickerInput


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label=u"Имя пользователя")
    email = forms.EmailField(label=u"Email", required=False)
    password = forms.CharField(label=u"Пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=u"Подтвердите пароль",
                                       widget=forms.PasswordInput
                                       )

    def is_valid(self):
        valid = super(RegisterForm, self).is_valid()
        if self.cleaned_data['password'] !=\
                self.cleaned_data['password_confirm']:
            self.add_error("password_confirm", u"Пароли не совпадают")
            return False
        return valid


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'] = forms.DateTimeField(
            input_formats=['%d/%m/%Y'],
            widget=BootstrapDateTimePickerInput()
        )


class CicleForm(forms.ModelForm):
    class Meta:
        model = Cicle
        exclude = ['user', 'created']

    def __init__(self, *args, **kwargs):
        super(CicleForm, self).__init__(*args, **kwargs)
        self.fields['last_cicle_first_date'] = forms.DateTimeField(
            input_formats=['%d/%m/%Y'],
            widget=BootstrapDateTimePickerInput(),
            label=u"Начало последнего цикла"
        )
        self.fields['last_cicle_last_date'] = forms.DateTimeField(
            input_formats=['%d/%m/%Y'],
            widget=BootstrapDateTimePickerInput(),
            label=u"Конец последнего цикла"
        )
