# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from .models import Examiner

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

# class ExaminerRegisterForm(forms.ModelForm):
#     class Meta:
#         model = Examiner
#         fields = ['examiner_id']

# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username', 'email']

# class ExaminerUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Examiner
#         fields = ['examiner_id']