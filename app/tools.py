import datetime
import hashlib


# 分页，每页条数
PAGE_SIZE = 5

# 购物车Session KEY
SESSION_USER_CART = "SESSION_USER_CART:%s"

GOODS_TYPE = [('model01', '美食'), ('model02', '缝补衣物'), ('model03', '五金'), ('model04', '开锁'), ('model05', '居家日用'),
              ('model06', '菜市场')]

PAY_MODE = [(1, "货到付款"), (2, "微信支付"), (3, "支付宝支付"), (4, "银行卡支付")]

PAY_STATUS = [(1, "待支付"), (2, "已支付"), (3, "已退款"), (4, "已取消"), (5, "申请退款")]


def set_password(password):
    """
    密码md5加密，算法单次md5
    :param password: 传入的密码
    :return: 加密后的密码
    """

    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    return str(password)


def get_now_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    pwd = "admin"
    rtpwd = set_password(pwd)
    print(rtpwd)
