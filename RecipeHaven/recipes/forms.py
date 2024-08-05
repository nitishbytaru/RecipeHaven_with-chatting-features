from django import forms
from .models import Recipe, Review
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class EditProfileForm(UserChangeForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), required=False
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "placeholder": "Enter Comment here",
                    "class": "form-control w-100",
                    "style": "height: 110px;",
                }
            ),
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "category",
            "ingredients",
            "steps_to_cook",
            "photo",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Name",
                    "class": "form-control",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter description here",
                    "class": "form-control w-100",
                    "style": "height: 110px;",
                }
            ),
            "ingredients": forms.Textarea(
                attrs={
                    "placeholder": "Enter Ingredients here",
                    "class": "form-control w-100",
                    "style": "height: 160px;",
                }
            ),
            "steps_to_cook": forms.Textarea(
                attrs={"placeholder": "Enter Steps here", "class": "form-control w-100"}
            ),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
