# -*- coding: utf-8 -*-

from django.db import models
import datetime
from app import tools


# 用户表（管理员和普通用户）
class User(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=128, verbose_name="密码")
    role = models.IntegerField(verbose_name="角色", choices=[(1, '管理员'), (2, '普通用户')])
    email = models.CharField(max_length=32, verbose_name="邮箱")
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)
    write_time = models.DateTimeField(verbose_name="修改时间", null=True)
    last_login = models.DateTimeField(verbose_name="最后登录时间", null=True)

    class Meta:
        db_table = "t_user"
        verbose_name = "User"
        verbose_name_plural = "用户管理"

    def save(self, *args, **kwargs):
        self.write_time = datetime.datetime.now()
        super().save(*args, **kwargs)


# 用户收货地址
class UserAddr(models.Model):
    user = models.ForeignKey(User, verbose_name="所属用户", on_delete=models.CASCADE)  # 外键
    receive_name = models.CharField(max_length=20, verbose_name="收件人")
    receive_phone = models.CharField(max_length=11, verbose_name="手机号码")
    receive_addr = models.CharField(max_length=128, verbose_name="详细地址")
    postcode = models.CharField(max_length=10, verbose_name="邮编")
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)
    write_time = models.DateTimeField(verbose_name="修改时间", null=True)
    
    class Meta:
        db_table = "t_user_addr"
        verbose_name = "UserAddr"
        verbose_name_plural = "用户地址"

    def save(self, *args, **kwargs):
        self.write_time = datetime.datetime.now()
        super().save(*args, **kwargs)


# 商品类
class Goods(models.Model):
    code = models.CharField(max_length=20, verbose_name='商品编号')
    name = models.CharField(max_length=20, verbose_name="商品名称")
    price = models.FloatField(verbose_name='商品价格')
    stock = models.IntegerField(verbose_name='库存数量')
    pic = models.CharField(max_length=200, verbose_name='商品图片')  # 保存图片路径
    goods_type = models.CharField(max_length=20, verbose_name="商品类别", choices=tools.GOODS_TYPE)
    unit = models.CharField(max_length=10, verbose_name="单位")
    title = models.CharField(max_length=255, verbose_name="标题")
    detail = models.CharField(max_length=2048, verbose_name="详情简介")
    click_num = models.IntegerField(verbose_name='浏览量', default=0)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True)
    write_time = models.DateTimeField(verbose_name="修改时间", null=True)

    class Meta:
        db_table = "t_goods"
        verbose_name = "Goods"
        verbose_name_plural = "商品管理"

    def save(self, *args, **kwargs):
        self.write_time = datetime.datetime.now()
        super().save(*args, **kwargs)


# 用户浏览过的商品
class UserBrowse(models.Model):
    user = models.ForeignKey(User, verbose_name="所属用户", on_delete=models.CASCADE)  # 外键
    goods = models.ForeignKey(Goods, verbose_name="所属商品", on_delete=models.CASCADE)  # 外键
    browse_time = models.DateTimeField(verbose_name="浏览时间")

    class Meta:
        db_table = "t_user_browse"
        verbose_name = "UserBrowse"
        verbose_name_plural = "浏览商品"


# 订单表

# 订单表
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="所属用户", on_delete=models.CASCADE)  # 外键

    order_no = models.CharField(max_length=64, verbose_name="订单交易编号")
    order_amount = models.FloatField(verbose_name='订单金额', default=0)
    discount_amount = models.FloatField(verbose_name='折扣金额', default=0)
    pay_amount = models.FloatField(verbose_name='支付金额', default=0)
    pay_time = models.DateTimeField(verbose_name='支付时间', null=True)
    pay_mode = models.IntegerField(verbose_name='支付方式', default=0, choices=tools.PAY_MODE)
    pay_status = models.IntegerField(verbose_name='支付状态', default=0, choices=tools.PAY_STATUS)

    receive_name = models.CharField(max_length=20, verbose_name="收件人")
    receive_phone = models.CharField(max_length=11, verbose_name="手机号码")
    receive_addr = models.CharField(max_length=128, verbose_name="详细地址")
    postcode = models.CharField(max_length=10, verbose_name="邮编")

    create_time = models.DateTimeField(verbose_name="创建时间", null=True)
    write_time = models.DateTimeField(verbose_name="修改时间", null=True)

    class Meta:
        db_table = "t_order"
        verbose_name = "Order"
        verbose_name_plural = "用户订单"

    def save(self, *args, **kwargs):
        self.write_time = datetime.datetime.now()
        super().save(*args, **kwargs)


# 订单-详情表
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name="所属订单", on_delete=models.CASCADE)  # 外键
    goods = models.ForeignKey(Goods, verbose_name="所属商品", on_delete=models.CASCADE)  # 外键
    buy_num = models.IntegerField(verbose_name='购买数量')
    goods_price = models.FloatField(verbose_name='产品单价')

    class Meta:
        db_table = "t_order_detail"
        verbose_name = "OrderDetail"
        verbose_name_plural = "用户订单详情"
