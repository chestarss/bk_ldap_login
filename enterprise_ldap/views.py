# -*- coding: utf-8 -*-

from django.http.response import HttpResponse
from bkaccount.accounts import Account
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from .utils import CustomLoginForm

def login(request, template_name='login/login.html',
    authentication_form=CustomLoginForm,
    current_app=None, extra_context=None):
  """
  登录处理，
  """
  account = Account()

  # 获取用户实际请求的 URL, 目前 account.REDIRECT_FIELD_NAME = 'c_url'
  redirect_to = request.GET.get(account.REDIRECT_FIELD_NAME, '')
  # 获取用户实际访问的蓝鲸应用
  app_id = request.GET.get('app_id', '')
  redirect_field_name = account.REDIRECT_FIELD_NAME

  if request.method == 'POST':
    #通过自定义表单CustomLoginForm实现登录验证
    form = authentication_form(request, data=request.POST)
    if form.is_valid():
      #验证通过跳转
      return account.login_success_response(request, form, redirect_to, app_id)
  else:
    form = authentication_form(request)

  current_site = get_current_site(request)
  context = {
    'form': form,
    redirect_field_name: redirect_to,
    'site': current_site,
    'site_name': current_site.name,
    'app_id': app_id,
  }
  if extra_context is not None:
    context.update(extra_context)
  if current_app is not None:
    request.current_app = current_app
  response = TemplateResponse(request, template_name, context)
  response = account.set_bk_token_invalid(request, response)
  return response