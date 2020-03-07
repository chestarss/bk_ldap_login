# -*- coding: utf-8 -*-

from ldap3 import Connection, Server, SUBTREE
from common.log import logger
from secret import LDAP_BASE, LDAP_HOST, LDAP_PORT

class SearchLdap:
  host = LDAP_HOST
  port = LDAP_PORT
  ldap_base = LDAP_BASE
  def get_user_info(self, **kwargs):

    username = kwargs.get("username")
    password = kwargs.get("password")

    ldap_user = 'cn='+username+','+self.ldap_base

    try:
      #与ldap建立连接
      s = Server(host=self.host, port=self.port, use_ssl=False, get_info='ALL', connect_timeout=5)
      #bind打开连接
      c = Connection(
              s,
              user=ldap_user,
              password=password,
              auto_bind='NONE',
              version=3,
              authentication='SIMPLE',
              client_strategy='SYNC',
              auto_referrals=True,
              check_names=True,
              read_only=True,
              lazy=False,
              raise_exceptions=False)

      c.bind()
      logger.info(c.result)
      #认证正确-success 不正确-invalidCredentials
      if c.result['description'] == 'success':
        res = c.search(search_base=self.ldap_base, search_filter = "(cn="+username+")", search_scope = SUBTREE, attributes = ['cn', 'mobile', 'mail'], paged_size = 5)
        if res:
          attr_dict = c.response[0]["attributes"]
          chname = attr_dict['givenName'][0]
          email = attr_dict['mail'][0]
          mobile = attr_dict['mobile'][0]
          data = {
            'username': "%s" % username,
            'password': "%s" % password,
            'chname': "%s" % chname,
            'email': "%s" % email,
            'mobile' : "%s" % mobile,
          }
          logger.info(u'ldap成功匹配用户')
          result = {
            'result': "success",
            'message':'验证成功',
            'data':data
          }
        else:
          logger.info(u'ldap无此用户信息')
          result = {
            'result': "null",
            'message':'result is null'
          }
        #关闭连接
        c.unbind()
      else:
        logger.info(u"用户认证失败")
        result = {
          'result': "auth_failure",
          'message': "user auth failure"
        }

    except Exception as e:
      logger.info(u'ldap连接出错: %s' % e)
      result = {
        'result': 'conn_error',
        'message': "connect error"
      }

    return result