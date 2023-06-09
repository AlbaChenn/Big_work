# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import traceback

from app import tools
from app.models import User, Goods, UserAddr, Order, OrderDetail, UserBrowse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.authorization import login_in


def get_login_user(request):
    try:
        userid = request.session.get("userid") or 0
        user = User.objects.get(id=userid)
        return True, user
    except:
        return False, render(request, "login.html")


# 登录
def login(request):
    page_name = "login.html"

    if request.method == "GET":
        return render(request, page_name)

    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)

        if not username:
            return render(request, page_name, {"username_error": "请输入用户名", "username": username})
        if not password:
            return render(request, page_name, {"password_error": "请输入密码", "username": username})

        try:
            objs = User.objects.filter(username=username)
            if objs:
                obj = objs[0]
                encrypt_pwd = tools.set_password(password)
                if encrypt_pwd == obj.password:
                    request.session["username"] = obj.username
                    request.session["userid"] = obj.id
                    request.session["role"] = obj.role
                    # 更新登录时间
                    obj.last_login = datetime.datetime.now()
                    obj.save()
                    # 跳转到首页
                    return HttpResponseRedirect("/app/index/")
                else:
                    return render(request, page_name, {"password_error": "登录密码错误", "username": username})
            else:
                return render(request, page_name, {"username_error": "用户名不存在", "username": username})
        except:
            traceback.print_exc()
            return render(request, page_name, {"username_error": "登录异常"})


# 退出登录
def logout(request):
    """
    :param request:
    :return:
    """
    request.session.clear()
    return HttpResponseRedirect("/app/login/")


# 注册
def register(request):
    page_name = "register.html"

    if request.method == "GET":
        return render(request, page_name)

    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        samepwd = request.POST.get("samepwd", None)
        email = request.POST.get("email", None)

        if not username:
            return render(request, page_name, {"username_error": "用户名不能为空"})
        if not password:
            return render(request, page_name, {"password_error": "密码不能为空", "username": username})
        if not samepwd:
            return render(request, page_name, {"samepwd_error": "密码不能为空", "username": username})
        if password != samepwd:
            return render(request, page_name,
                          {"password_error": "密码不一致", "samepwd_error": "密码不一致", "username": username})
        if not email:
            return render(request, page_name, {"email_error": "邮箱不能为空", "username": username})

        objs = User.objects.filter(username=username)
        if objs:
            return render(request, page_name, {"username_error": "用户名已被注册，请换个用户名"})
        user = User()
        user.username = username
        user.password = tools.set_password(password)
        user.role = 2  # 注册普通用户
        user.email = email
        user.create_time = tools.get_now_time()
        user.save()
        # 跳转到首页
        return HttpResponseRedirect("/app/index/")


# 个人中心
@login_in
def center(request):
    valid, user = get_login_user(request)
    if not valid:
        return user
    # 用户信息
    user_info = {"username": user.username, "phone": "尚未设置", "addr": "尚未设置"}
    addr_list = UserAddr.objects.filter(user=user)
    if addr_list:
        addr = addr_list[0]
        user_info["phone"] = addr.receive_phone
        user_info["addr"] = addr.receive_addr

    # 最近浏览的商品（只取前5个）
    goods_list = []
    browse_list = UserBrowse.objects.filter(user=user).order_by("-browse_time")[:5]
    goods_ids = [b.goods.id for b in browse_list]
    if goods_ids:
        src_goods_list = Goods.objects.filter(id__in=goods_ids)
        for sort_gid in goods_ids:
            for src_goods in src_goods_list:
                if src_goods.id == sort_gid:
                    goods_list.append(src_goods)
                    break
    return render(request, "user_center_info.html", {"user_info": user_info, "goods_list": goods_list})


# 我的订单
@login_in
def order(request):
    valid, user = get_login_user(request)
    if not valid:
        return user

    pay_status_dict = dict(tools.PAY_STATUS)
    pay_mode_dict = dict(tools.PAY_MODE)
    user_order_list = Order.objects.filter(user=user).order_by("-create_time")
    for order in user_order_list:
        pay_status_desc = pay_status_dict.get(order.pay_status) or order.pay_status
        order.__setattr__("pay_status_desc", pay_status_desc)

        pay_mode_desc = pay_mode_dict.get(order.pay_mode) or order.pay_mode
        order.__setattr__("pay_mode_desc", pay_mode_desc)

        # 订单-商品 详情
        order_detail_list = []
        detail_list = OrderDetail.objects.filter(order=order)
        for detail in detail_list:
            order_detail_list.append({
                "goods_name": detail.goods.name,
                "goods_pic": detail.goods.pic,
                "goods_unic": detail.goods.unit,
                "goods_buy_num": detail.buy_num,
                "goods_price": detail.goods_price,
                "goods_amount": round(detail.buy_num * detail.goods_price, 2),
            })

        order.__setattr__("order_detail_list", order_detail_list)

    return render(request, "user_center_order.html", {"user_order_list": user_order_list})


# 我的地址
@login_in
def site(request):
    valid, user = get_login_user(request)
    if not valid:
        return user
    addr_info = {"receive_name": "尚未设置", "receive_phone": "尚未设置", "receive_addr": "尚未设置", "postcode": "尚未设置"}
    addr_list = UserAddr.objects.filter(user=user)
    if addr_list:
        addr = addr_list[0]
        if addr.receive_name:
            addr_info["receive_name"] = addr.receive_name
        if addr.receive_phone:
            addr_info["receive_phone"] = addr.receive_phone
        if addr.receive_addr:
            addr_info["receive_addr"] = addr.receive_addr
        if addr.postcode:
            addr_info["postcode"] = addr.postcode

    edit_form = request.session.pop("edit_addr_form", {})

    return render(request, "user_center_site.html", {"addr_info": addr_info, "edit_form": edit_form})


# 修改地址
@login_in
def update_site(request):
    valid, user = get_login_user(request)
    if not valid:
        return user

    if request.method == "POST":
        edit_form = {
            "receive_name": request.POST.get("receive_name"),
            "receive_addr": request.POST.get("receive_addr"),
            "postcode": request.POST.get("postcode"),
            "receive_phone": request.POST.get("receive_phone")
        }
        valid = True
        if not edit_form.get("receive_name"):
            edit_form["receive_name_error"] = "请输入收件人"
            valid = False
        if not edit_form.get("receive_addr"):
            edit_form["receive_addr_error"] = "请输入详细地址"
            valid = False
        if not edit_form.get("postcode"):
            edit_form["postcode_error"] = "请输入邮编"
            valid = False
        if not edit_form.get("receive_phone"):
            edit_form["receive_phone_error"] = "请输入手机"
            valid = False

        if valid:
            addr_list = UserAddr.objects.filter(user=user)
            if addr_list:
                addr = addr_list[0]
                addr.receive_name = edit_form["receive_name"]
                addr.receive_addr = edit_form["receive_addr"]
                addr.receive_phone = edit_form["receive_phone"]
                addr.postcode = edit_form["postcode"]
                addr.save()
            else:
                addr = UserAddr(user=user, receive_name=edit_form["receive_name"],
                                receive_phone=edit_form["receive_phone"], receive_addr=edit_form["receive_addr"],
                                postcode=edit_form["postcode"])
                addr.save()
        else:
            request.session["edit_addr_form"] = edit_form

    return HttpResponseRedirect("/app/site/")
