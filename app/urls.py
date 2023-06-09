from django.urls import path

from app.views import user_views
from app.views import goods_views


app_name = 'app'

urlpatterns = [
    # 注册、登录
    path('login/', user_views.login, name='login'),
    path('logout/', user_views.logout, name='logout'),
    path('register/', user_views.register, name='register'),

    path('center/', user_views.center, name='center'),

    path('cart/', goods_views.cart, name='cart'),
    path('add_cart/', goods_views.add_cart, name='add_cart'),
    path('del_cart/', goods_views.del_cart, name='del_cart'),
    path('update_cart/', goods_views.update_cart, name='update_cart'),

    path('order/', user_views.order, name='order'),

    path('buy_now/', goods_views.buy_now, name='buy_now'),
    path('place_order/', goods_views.place_order, name='place_order'),
    path('submit_order/', goods_views.submit_order, name='submit_order'),
    path('pay_order/', goods_views.pay_order, name='pay_order'),

    path('site/', user_views.site, name='site'),
    path('update_site/', user_views.update_site, name='update_site'),

    # 首页
    path('index/', goods_views.index, name='index'),
    path('list/', goods_views.list, name='list'),
    path('detail/', goods_views.detail, name='detail'),

]
