# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import time
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


# 首页
def index(request):
    goods_type_list = tools.GOODS_TYPE
    home_goods_list = []
    for goods_type in goods_type_list:
        goods_list = Goods.objects.filter(goods_type=goods_type[0])[:4]
        home_goods_list.append({
            "goods_type_name": goods_type[1],
            "goods_type_id": goods_type[0],
            "goods_list": goods_list
        })

    return render(request, "index.html", {"goods_type_list": goods_type_list, "home_goods_list": home_goods_list})


# 商品分类列表
def list(request):
    goods_type = request.GET.get("type") or ""
    search_keyword = request.GET.get("search_keyword") or ""
    page_num = int(request.GET.get("page_num", 1) or 1)

    stat_index = (page_num - 1) * tools.PAGE_SIZE
    end_index = stat_index + tools.PAGE_SIZE

    # 商品列表(分页查询)
    if search_keyword:
        goods_list = Goods.objects.filter(name__icontains=search_keyword).order_by("-click_num")[stat_index:end_index]
    elif goods_type:
        goods_list = Goods.objects.filter(goods_type=goods_type).order_by("-click_num")[stat_index:end_index]
    else:
        goods_list = Goods.objects.all().order_by("-click_num")[stat_index:end_index]

    # 商品分类
    goods_type_list = tools.GOODS_TYPE
    # 商品分类名
    goods_type_name = dict(goods_type_list).get(goods_type)
    # 新品推荐（返回两条同类别商品）
    if goods_type:
        new_goods_list = Goods.objects.filter(goods_type=goods_type).order_by("-create_time")[:2]
    else:
        new_goods_list = Goods.objects.all().order_by("-create_time")[:2]

    context = {"new_goods_list": new_goods_list, "goods_list": goods_list, "goods_type_list": goods_type_list,
               "goods_type_name": goods_type_name, "page_num": page_num, "search_keyword": search_keyword,
               "type": goods_type}

    return render(request, "list.html", context=context)


# 商品详情
def detail(request):
    gid = request.GET.get("gid")
    goods = Goods.objects.get(id=gid)
    # 商品浏览量+1
    goods.click_num += 1
    goods.save()

    # 判断用户如果已经登录，则加入用户最近浏览商品
    userid = request.session.get("userid") or 0
    if userid:
        user = User.objects.get(id=userid)
        ubs = UserBrowse.objects.filter(user=user, goods=goods)
        browse_time = tools.get_now_time()
        if not ubs:
            ub = UserBrowse(user=user, goods=goods, browse_time=browse_time)
            ub.save()
        else:
            ub = ubs[0]
            ub.browse_time = browse_time
            ub.save()

    # 新品推荐（返回两条同类别商品）
    new_goods_list = Goods.objects.exclude(id=goods.id).filter(goods_type=goods.goods_type).order_by("-create_time")[:2]
    # 商品分类
    goods_type_list = tools.GOODS_TYPE

    goods_type_name = dict(goods_type_list).get(goods.goods_type)

    context = {"goods_info": goods, "new_goods_list": new_goods_list, "goods_type_list": goods_type_list,
               "goods_type_name": goods_type_name}

    return render(request, "detail.html", context=context)


# 计算购物车商品件数
def calc_cart_goods(request):
    userid = request.session.get("userid") or 0
    key = tools.SESSION_USER_CART % userid
    user_cart_info = request.session.get(key) or {}
    mycart_num = 0
    for num in user_cart_info.values():
        mycart_num += num
    request.session["mycart_num"] = mycart_num


# 我的购物车
@login_in
def cart(request):
    valid, user = get_login_user(request)
    if not valid:
        return user

    key = tools.SESSION_USER_CART % user.id
    user_cart_info = request.session.get(key) or {}
    goods_list = []
    goods_total_amount = 0
    goods_total_num = 0
    if user_cart_info:
        goods_ids = [goods_id for goods_id in user_cart_info.keys()]
        goods_list = Goods.objects.filter(id__in=goods_ids)
        for goods_info in goods_list:
            buy_num = user_cart_info.get(str(goods_info.id))
            total_amount = round(goods_info.price * buy_num, 2)

            goods_total_amount += total_amount
            goods_total_num += buy_num

            goods_info.__setattr__("buy_num", buy_num)
            goods_info.__setattr__("total_amount", total_amount)

    return render(request, "cart.html", {"goods_list": goods_list, "goods_total_amount": goods_total_amount,
                                         "goods_total_num": goods_total_num})


# 加到购物车
@login_in
def add_cart(request):
    valid, user = get_login_user(request)
    if not valid:
        return user

    gid = request.POST.get("gid")
    buy_num = int(request.POST.get("gcount"))

    key = tools.SESSION_USER_CART % user.id
    user_cart_info = request.session.get(key) or {}

    if gid in user_cart_info:
        user_cart_info[gid] += buy_num
    else:
        user_cart_info[gid] = buy_num

    # 更新购物车缓存
    request.session[key] = user_cart_info

    calc_cart_goods(request)

    # 跳转到我的购物车
    return HttpResponseRedirect("/app/cart/")


# 删除购物车商品
@login_in
def del_cart(request):
    valid, user = get_login_user(request)
    if not valid:
        return user

    gid = request.GET.get("gid")
    key = tools.SESSION_USER_CART % user.id
    user_cart_info = request.session.get(key) or {}
    user_cart_info.pop(gid, "")
    # 更新购物车缓存
    request.session[key] = user_cart_info

    calc_cart_goods(request)

    # 跳转到我的购物车
    return HttpResponseRedirect("/app/cart/")


# 修改购物车商品数量
def update_cart(request):
    valid, user = get_login_user(request)
    if not valid:
        return user

    gid = request.POST.get("gid")
    buy_num = int(request.POST.get("gcount"))

    key = tools.SESSION_USER_CART % user.id
    user_cart_info = request.session.get(key) or {}

    user_cart_info[gid] = buy_num
    # 更新购物车缓存
    request.session[key] = user_cart_info

    calc_cart_goods(request)

    # 跳转到我的购物车
    return HttpResponseRedirect("/app/cart/")


# 立即购买
@login_in
def buy_now(request):
    valid, user = get_login_user(request)
    if not valid:
        return user

    gid = request.POST.get("gid")
    buy_num = request.POST.get("gcount")
    goods_info = Goods.objects.get(id=gid)

    total_amount = round(int(buy_num) * goods_info.price, 2)
    goods_info.__setattr__("buy_num", buy_num)
    goods_info.__setattr__("goods_amount", total_amount)

    addr_list = UserAddr.objects.filter(user=user)
    if addr_list:
        addr = addr_list[0]
        show_addr = f"{addr.receive_addr} ({addr.receive_name} 收) {addr.receive_phone}"
    else:
        # 无地址，先跳转到编辑地址
        return HttpResponseRedirect("/app/site/")

    freight = 12  # 运费
    order_info = {"buy_num": buy_num, "total_amount": total_amount, "freight": 12, "pay_amount": freight + total_amount}

    # 用于提交的信息
    order_detail_info = {f"{gid}": buy_num}

    context = {"addr": addr, "show_addr": show_addr, "order_goods_list": [goods_info], "order_info": order_info,
               "order_detail_info": json.dumps(order_detail_info), "source": "buy_now"}
    return render(request, "place_order.html", context=context)


# 下单页面
@login_in
def place_order(request):
    valid, user = get_login_user(request)
    if not valid:
        return user
    addr_list = UserAddr.objects.filter(user=user)
    if addr_list:
        addr = addr_list[0]
        show_addr = f"{addr.receive_addr} ({addr.receive_name} 收) {addr.receive_phone}"
    else:
        # 无地址，先跳转到编辑地址
        return HttpResponseRedirect("/app/site/")

    # 购物车中的商品
    key = tools.SESSION_USER_CART % user.id
    user_cart_info = request.session.get(key) or {}
    if not user_cart_info:
        # 无商品，点击：去结算，重新跳转到购物车列表
        return HttpResponseRedirect("/app/cart/")

    order_goods_list = []
    goods_total_amount = 0
    goods_total_num = 0
    order_detail_info = {}  # 用于提交的信息

    goods_ids = [goods_id for goods_id in user_cart_info.keys()]
    goods_list = Goods.objects.filter(id__in=goods_ids)
    for goods_info in goods_list:
        buy_num = user_cart_info.get(str(goods_info.id))
        goods_amount = round(goods_info.price * buy_num, 2)

        goods_total_amount += goods_amount
        goods_total_num += buy_num

        goods_info.__setattr__("buy_num", buy_num)
        goods_info.__setattr__("goods_amount", goods_amount)

        order_goods_list.append(goods_info)

        order_detail_info[str(goods_info.id)] = buy_num

    freight = 12  # 运费
    order_info = {"buy_num": goods_total_num, "total_amount": goods_total_amount, "freight": 12,
                  "pay_amount": freight + goods_total_amount}
    context = {"addr": addr, "show_addr": show_addr, "order_goods_list": order_goods_list, "order_info": order_info,
               "order_detail_info": json.dumps(order_detail_info), "source": "cart"}
    return render(request, "place_order.html", context=context)


# 提交订单支付
@login_in
def submit_order(request):
    valid, user = get_login_user(request)
    if not valid:
        return user

    pay_mode = request.POST.get("pay_mode")
    order_detail_info = request.POST.get("order_detail_info")
    order_detail_info = json.loads(order_detail_info)

    addr = UserAddr.objects.filter(user=user)[0]

    # 计算订单金额
    cache_detail_list = []
    order_amount = 0
    for gid in order_detail_info.keys():
        goods = Goods.objects.get(id=gid)
        buy_num = int(order_detail_info[gid])
        order_amount += round(goods.price * buy_num, 2)

        order_detail = OrderDetail(goods=goods, buy_num=buy_num, goods_price=goods.price)
        cache_detail_list.append(order_detail)

    pay_amount = order_amount +12  # 加上运费？
    # 创建订单 (时间戳）
    order_no = int(time.time())
    pay_status = 1
    discount_amount = 0
    pay_time = tools.get_now_time()
    create_time = tools.get_now_time()
    order = Order(user=user, order_no=order_no, receive_name=addr.receive_name, receive_phone=addr.receive_phone,
                  receive_addr=addr.receive_addr, postcode=addr.postcode, pay_status=pay_status, pay_mode=pay_mode,
                  order_amount=order_amount, discount_amount=discount_amount, pay_amount=pay_amount, pay_time=pay_time,
                  create_time=create_time)
    order.save()

    # 保存订单商品详情
    for order_detail in cache_detail_list:
        order_detail.order = order
        order_detail.save()

    # 判断来源
    source = request.POST.get("source")
    if source == "cart":
        key = tools.SESSION_USER_CART % user.id
        user_cart_info = request.session.get(key) or {}
        for goods_id in order_detail_info.keys():
            user_cart_info.pop(goods_id, "")
        request.session[key] = user_cart_info

        calc_cart_goods(request)

    # 跳转到订单列表
    return HttpResponseRedirect("/app/order/")


# 去付款
@login_in
def pay_order(request):
    valid, user = get_login_user(request)
    if not valid:
        return user

    order_id = request.GET.get("order_id")
    order = Order.objects.get(id=order_id)
    order.pay_status = 2
    order.save()

    # 跳转到订单列表
    return HttpResponseRedirect("/app/order/")
