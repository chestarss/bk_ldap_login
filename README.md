
# 蓝鲸系统对接企业内部LDAP认证


## 根据【木讷大叔爱运维】的文章整理，
[https://mp.weixin.qq.com/s?__biz=MzA4ODQwMDg1NQ==&mid=2247483660&idx=1&sn=f29959e62448bd8569d6f8e6cfcfdbaf&chksm=902bf7b4a75c7ea22bcbe0f3b3501526151451002fac848b7d48c1961d0e9022bb33aa9f1725&mpshare=1&scene=23&srcid=&sharer_sharetime=1583551575316&sharer_shareid=5d7a84a63006a403569777456f05a0b4#rd](原文链接)

## 安装依赖
``` shell script
# 中控机
cd /data/install
grep paas install.config  查看paas在哪台机器

# paas login所在机器
workon open_paas-login
pip install ldap3
# 一定要是在open_paas-login这个虚拟环境下，否则ldap会找不到

cd /data/bkce/open_paas/login/ee_login
git clone <该项目的链接>
ln -s bk_ldap_login/enterprise_ldap .
```

## 在enterprise_ldap目录下增加ladp配置
新建 secret.py
``` python
# -*- coding: utf-8 -*-
# 根据自己的配置改成对应的，主要LDAP_BASE, 是ldap用户的全路径的后缀，比如ou=users,dc=test,dc=cn
LDAP_HOST = '10.90.10.123'
LDAP_PORT = 389
LDAP_USER_BASE = 'dc=test,dc=cn'
```

## 编辑 settings_login.py
先备份cp settings_login.py settings_login.py.bak
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

### ldap_utils.py 中的中文用户名根据自己ldap中的字段修改设置

## 重启paas-login
验证是否登录成功

## Debug
在secret.py中增加
DEBUG=True
记得调试成功后关闭debug