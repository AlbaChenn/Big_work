# 登录账号权限校验，统一验证路由请求
from django.shortcuts import render


# admin权限校验
def admin_auth(func):
    def validate(*args, **kwargs):
        request = args[0]
        role = request.session.get("role")
        # 非管理员用户，跳转到无权限页面，
        if role != 1:
            request.session.clear()
            return render(request, "login.html")
        return func(*args, **kwargs)

    return validate


# 用户必须登录权限
def login_in(func):
    def validate(*args, **kwargs):
        request = args[0]
        role = request.session.get("role")
        # 非管理员用户，跳转到无权限页面，
        if not role:
            request.session.clear()
            return render(request, "login.html")
        return func(*args, **kwargs)

    return validate
