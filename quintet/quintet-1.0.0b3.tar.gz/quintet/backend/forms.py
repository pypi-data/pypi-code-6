from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_bootstrap_markdown.widgets import MarkdownInput
from django_bootstrap_typeahead.fields import MultipleTypeaheadField
from django_password_strength.widgets import PasswordStrengthInput
from ..models import Profile, Section, Role, Tag


def build_tag(value):
    tag, _ = Tag.objects.get_or_create(
        slug=slugify(value),
        defaults={'title': value}
    )
    return tag


class PostForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Post Title'
        })
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        empty_label='Section',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control input-lg'
        })
    )
    markdown = forms.CharField(
        required=False,
        widget=MarkdownInput(image_control=True)
    )
    tags = MultipleTypeaheadField(
        queryset=Tag.objects.all(),
        builder=build_tag,
        required=False
    )


class PageForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control input-lg',
            'placeholder': 'Post Title'
        })
    )
    markdown = forms.CharField(
        required=False,
        widget=MarkdownInput(image_control=True)
    )


def build_role(value):
    role, _ = Role.objects.get_or_create(
        slug=slugify(value),
        defaults={'title': value}
    )
    return role


class AddContributorForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label='User',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    role = MultipleTypeaheadField(
        queryset=Role.objects.all(),
        builder=build_role
    )


class EditContributorForm(forms.Form):
    role = MultipleTypeaheadField(
        queryset=Role.objects.all(),
        builder=build_role
    )


class AddReviewerForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label='User',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Comment...',
            'rows': '5',
            'style': 'resize:vertical;',
        })
    )
    excerpt = forms.CharField(required=False, widget=forms.HiddenInput)


class SettingsForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    twitter = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Twitter',
        })
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'resize:vertical;',
            'rows': '5',
        })
    )


class AddUserForm(SettingsForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )

    def save(self, request=None):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )

        profile = Profile(
            user=user,
            twitter=self.cleaned_data['twitter'],
            bio=self.cleaned_data['bio']
        )
        profile.save()

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }

        from_email = None
        subject = 'New account details for %s' % site_name
        email = loader.render_to_string('registration/new_user_email.html', c)
        html_email = None

        send_mail(
            subject,
            email,
            from_email,
            [user.email],
            html_message=html_email
        )


class ChangePhotoForm(forms.Form):
    photo = forms.ImageField()


class PermissionForm(forms.Form):
    add_post = forms.BooleanField(required=False)
    change_post = forms.BooleanField(required=False)
    delete_post = forms.BooleanField(required=False)
    publish_post = forms.BooleanField(required=False)
    add_page = forms.BooleanField(required=False)
    change_page = forms.BooleanField(required=False)
    delete_page = forms.BooleanField(required=False)
    publish_page = forms.BooleanField(required=False)
    add_section = forms.BooleanField(required=False)
    delete_section = forms.BooleanField(required=False)
    add_user = forms.BooleanField(required=False)
    change_user = forms.BooleanField(required=False)
    delete_user = forms.BooleanField(required=False)
    set_perms = forms.BooleanField(required=False)


class SectionForm(forms.Form):
    section = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Section Name'
        })
    )


class SetPasswordFormWithMeter(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"), widget=PasswordStrengthInput())
