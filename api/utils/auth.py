from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from api import models



class Authentication(BaseAuthentication):

    def authenticate(self, request):
        """
        用户认证
        :param request:
        :return:
        """
        # print(request.method)
        # 判断请求方式
        if request.method == "GET":
            token = request.query_params.get('token')
        else:
            token = request.data.get('token')

        # print('auth',token)
        token_obj = models.Token.objects.filter(token=token).first()
        if not token_obj:
            # 认证失败
            raise AuthenticationFailed({'code':1008,'error':'认证失败'})
        # 认证成功
        # return (token_obj.user,token_obj)
        return (token_obj.user,token_obj)