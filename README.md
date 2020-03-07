
## 安装依赖

workon open_paas-login
pip install ldap3
一定要是在open_paas-login这个虚拟环境下，否则ldap会找不到

中控机
cd /data/bkce/open_paas/login/ee_login

## 增加ladp配置
新建 secret.py
``` python
LDAP_HOST = '10.90.10.123'
LDAP_PORT = 389
LDAP_BASE = 'dc=test,dc=cn'
```

## 编辑 settings_login.py

``` python
# -*- coding: utf-8 -*-
# 蓝鲸登录方式：bk_login
# 自定义登录方式：custom_login

#LOGIN_TYPE = 'bk_login'
LOGIN_TYPE = 'custom_login'

# 默认bk_login，无需设置其他配置

###########################
# 自定义登录 custom_login   #
###########################
# 配置自定义登录请求和登录回调的响应函数, 如：CUSTOM_LOGIN_VIEW = 'ee_official_login.oauth.google.views.login'
CUSTOM_LOGIN_VIEW = 'ee_login.enterprise_ldap.views.login'
# 配置自定义验证是否登录的认证函数, 如：CUSTOM_AUTHENTICATION_BACKEND = 'ee_official_login.oauth.google.backends.OauthBackend'
CUSTOM_AUTHENTICATION_BACKEND = 'ee_login.enterprise_ldap.backends.ldapbackend'
```