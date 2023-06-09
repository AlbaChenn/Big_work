# Generated by Django 4.1 on 2023-06-05 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Goods",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=20, verbose_name="商品编号")),
                ("name", models.CharField(max_length=20, verbose_name="商品名称")),
                ("price", models.FloatField(verbose_name="商品价格")),
                ("stock", models.IntegerField(verbose_name="库存数量")),
                ("pic", models.CharField(max_length=200, verbose_name="商品图片")),
                (
                    "goods_type",
                    models.CharField(
                        choices=[
                            ("model01", "美食"),
                            ("model02", "缝补衣物"),
                            ("model03", "五金"),
                            ("model04", "开锁"),
                            ("model05", "居家日用"),
                            ("model06", "菜市场"),
                        ],
                        max_length=20,
                        verbose_name="商品类别",
                    ),
                ),
                ("unit", models.CharField(max_length=10, verbose_name="单位")),
                ("title", models.CharField(max_length=255, verbose_name="标题")),
                ("detail", models.CharField(max_length=2048, verbose_name="详情简介")),
                ("click_num", models.IntegerField(default=0, verbose_name="浏览量")),
                ("create_time", models.DateTimeField(null=True, verbose_name="创建时间")),
                ("write_time", models.DateTimeField(null=True, verbose_name="修改时间")),
            ],
            options={
                "verbose_name": "Goods",
                "verbose_name_plural": "商品管理",
                "db_table": "t_goods",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order_no", models.CharField(max_length=64, verbose_name="订单交易编号")),
                ("order_amount", models.IntegerField(default=0, verbose_name="订单金额")),
                (
                    "discount_amount",
                    models.IntegerField(default=0, verbose_name="折扣金额"),
                ),
                ("pay_amount", models.IntegerField(default=0, verbose_name="支付金额")),
                ("pay_time", models.DateTimeField(null=True, verbose_name="支付时间")),
                (
                    "pay_mode",
                    models.IntegerField(
                        choices=[(1, "货到付款"), (2, "微信支付"), (3, "支付宝支付"), (4, "银行卡支付")],
                        default=0,
                        verbose_name="支付方式",
                    ),
                ),
                (
                    "pay_status",
                    models.IntegerField(
                        choices=[
                            (1, "待支付"),
                            (2, "已支付"),
                            (3, "已退款"),
                            (4, "已取消"),
                            (5, "申请退款"),
                        ],
                        default=0,
                        verbose_name="支付状态",
                    ),
                ),
                ("receive_name", models.CharField(max_length=20, verbose_name="收件人")),
                ("receive_phone", models.CharField(max_length=11, verbose_name="手机号码")),
                ("receive_addr", models.CharField(max_length=128, verbose_name="详细地址")),
                ("postcode", models.CharField(max_length=10, verbose_name="邮编")),
                ("create_time", models.DateTimeField(null=True, verbose_name="创建时间")),
                ("write_time", models.DateTimeField(null=True, verbose_name="修改时间")),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "用户订单",
                "db_table": "t_order",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=32, verbose_name="用户名")),
                ("password", models.CharField(max_length=128, verbose_name="密码")),
                (
                    "role",
                    models.IntegerField(
                        choices=[(1, "管理员"), (2, "普通用户")], verbose_name="角色"
                    ),
                ),
                ("email", models.CharField(max_length=32, verbose_name="邮箱")),
                ("create_time", models.DateTimeField(null=True, verbose_name="创建时间")),
                ("write_time", models.DateTimeField(null=True, verbose_name="修改时间")),
                ("last_login", models.DateTimeField(null=True, verbose_name="最后登录时间")),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "用户管理",
                "db_table": "t_user",
            },
        ),
        migrations.CreateModel(
            name="UserBrowse",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("browse_time", models.DateTimeField(verbose_name="浏览时间")),
                (
                    "goods",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.goods",
                        verbose_name="所属商品",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.user",
                        verbose_name="所属用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "UserBrowse",
                "verbose_name_plural": "浏览商品",
                "db_table": "t_user_browse",
            },
        ),
        migrations.CreateModel(
            name="UserAddr",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("receive_name", models.CharField(max_length=20, verbose_name="收件人")),
                ("receive_phone", models.CharField(max_length=11, verbose_name="手机号码")),
                ("receive_addr", models.CharField(max_length=128, verbose_name="详细地址")),
                ("postcode", models.CharField(max_length=10, verbose_name="邮编")),
                ("create_time", models.DateTimeField(null=True, verbose_name="创建时间")),
                ("write_time", models.DateTimeField(null=True, verbose_name="修改时间")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.user",
                        verbose_name="所属用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "UserAddr",
                "verbose_name_plural": "用户地址",
                "db_table": "t_user_addr",
            },
        ),
        migrations.CreateModel(
            name="OrderDetail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("buy_num", models.IntegerField(verbose_name="购买数量")),
                ("goods_price", models.FloatField(verbose_name="产品单价")),
                (
                    "goods",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.goods",
                        verbose_name="所属商品",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.order",
                        verbose_name="所属订单",
                    ),
                ),
            ],
            options={
                "verbose_name": "OrderDetail",
                "verbose_name_plural": "用户订单详情",
                "db_table": "t_order_detail",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="app.user",
                verbose_name="所属用户",
            ),
        ),
    ]
