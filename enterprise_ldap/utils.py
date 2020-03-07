# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from common.log import logger

class CustomLoginForm(AuthenticationForm):
  """
  重写AuthenticationForm类，用于自定义登录custom_login
  """
  def clean(self):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')
    if username and password:
      self.user_cache = authenticate(username=username,
                                     password=password)
      if self.user_cache is None:
        raise forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )
      else:
        super(CustomLoginForm, self).confirm_login_allowed(self.user_cache)

    return self.cleaned_data