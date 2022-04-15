from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Ваш ник на сервере')
    email_field = forms.EmailField(label='Почта', required=False)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль на сервере')


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_again = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_again = cleaned_data.get("new_password_again")

        if len(new_password) < 8:
            self.add_error('new_password', 'Парль должен быть не меньше 8 символов')
        elif new_password_again != new_password:
            self.add_error('new_password_again', 'Пароли не совпадают')


class ForgetPasswordForm(forms.Form):
    username = forms.CharField(label='Ваш ник на сервере')


class RecoveryPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_again = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_again = cleaned_data.get("new_password_again")

        if len(new_password) < 8:
            self.add_error('new_password', 'Парль должен быть не меньше 8 символов')
        elif new_password_again != new_password:
            self.add_error('new_password_again', 'Пароли не совпадают')


class ChangeEmailForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    email_field = forms.EmailField(label='Почта', required=True)


class DonateTicketForm(forms.Form):
    email_field = forms.EmailField(label='Почта')
    promo = forms.CharField(label='Ник друга или промокод', required=False)


class DonateTicketFormForm(forms.Form):
    username = forms.CharField(label='Ваш ник на сервере')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль на сервере')


class Application1Form(forms.Form):
    username = forms.CharField(label='Ваш ник на сервере')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль на сервере')


class Application2Form(forms.Form):
    data1 = forms.CharField(label='Как вы узнали о нашем сервере?')
    data2 = forms.Textarea(attrs={'cols': '40', 'rows': '4'})
    data3 = forms.Textarea(attrs={'cols': '40', 'rows': '2'})
    data4 = forms.Textarea(attrs={'cols': '40', 'rows': '2'})
    data5 = forms.Textarea(attrs={'cols': '40', 'rows': '2'})
