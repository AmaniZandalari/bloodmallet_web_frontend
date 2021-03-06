# -*- coding: utf-8 -*-

import logging


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from general_website.models.account import User
from general_website.models.simulation import Simulation
from general_website.models.world_of_warcraft import SimulationType
from general_website.models.world_of_warcraft import WowSpec

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from crispy_forms.bootstrap import FieldWithButtons, StrictButton

logger = logging.getLogger(__name__)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. 254 characters or fewer.'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class UserLoginForm(AuthenticationForm):
    pass


class UserUpdateForm(PasswordChangeForm):
    """Settings form for the user to update his own profile.
    """
    pass


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ()


class SimulationCreationForm(forms.ModelForm):
    dynamic_delete = forms.BooleanField(required=False, label=_(
        "Auto-remove oldest chart"), help_text=_(
        "If your slots are filled, enabling this checkbox will auto-remove the oldest chart to free up a slot."),
    )

    class Meta:
        model = Simulation
        fields = (
            'name',
            'wow_spec',
            'simulation_type',
            'fight_style',
            'custom_profile',
        )

    def __init__(self, *args, **kwargs):
        super(SimulationCreationForm, self).__init__(*args, **kwargs)
        self.fields['simulation_type'].queryset = SimulationType.objects.filter(
            is_deleted=False
        ).order_by(
            'name'
        )
        self.fields['wow_spec'].queryset = WowSpec.objects.order_by(
            'wow_class__tokenized_name', 'tokenized_name'
        )

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('name'), css_class='col-12 col-md-6'),
                Div(Field('wow_spec'), css_class='col-12 col-md-6'),
                css_class='row'
            ),
            Div(
                Div(Field('simulation_type'), css_class='col-12 col-md-6'),
                Div(Field('fight_style'), css_class='col-12 col-md-6'),
                css_class='row'
            ),
            Div(Div(Field('custom_profile', placeholder=_(
                "Paste your /simc output into this element."
            )), css_class='col-12'), css_class='row'),
            Div(Div(Field('dynamic_delete'), css_class='col-12'), css_class='row'),
            StrictButton(
                _("Create Chart"),
                type='submit',
                css_class="btn btn-primary",
            )
        )

    def clean_custom_profile(self):
        data = self.cleaned_data['custom_profile']

        return data[:10000]
