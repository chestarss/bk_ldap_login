# -*- coding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend
from .ldap_utils import SearchLdap
from django.contrib.auth import get_user_model
from bkaccount.constants import RoleCodeEnum
from common.log import logger

class ldapbackend(ModelBackend):
  def authenticate(self, **credentials):
    username = credentials.get('username')
    password = credentials.get('password')

    if username and password:
      logger.info("username: %s,password: %s" % (username,password))
      #当登录账号为admin时，直接在蓝鲸验证，不走ldap认证
      if username == 'admin':
        logger.info(u'用户为admin，直接蓝鲸验证')
        return super(ldapbackend, self).authenticate(username=username, password=password)
      else:
        ldapinfo = SearchLdap()
        resp = ldapinfo.get_user_info(username=username, password=password)
        #如果ldap中存在此用户
        if resp["result"] == "success":
          # 获取用户类 Model（即对应用户表）
          user_model = get_user_model()
          try:
            user = user_model.objects.get(username=username)
          except user_model.DoesNotExist:
            # 创建 User 对象
            user = user_model.objects.create_user(username)
            # 获取用户信息，只在第一次创建时设置，已经存在不更新
            chname = resp['data']['chname']
            phone = resp['data']['mobile']
            email = resp['data']['email']
            user.chname = chname
            user.phone = phone
            user.email = email
            user.save()
            # 设置新增用户角色为普通管理员
            logger.info(u'新建用户：%s 权限：%s' % (chname, u'普通用户'))
            result, message = user_model.objects.modify_user_role(username, RoleCodeEnum.STAFF)
          return user
        else:
          return None
    else:
      return None