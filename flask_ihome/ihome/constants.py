# coding: utf-8

# 图片验证码redis有效期
IMAGE_CODE_REDIS_EXPIRES = 180

# 短信验证码redis有效期
SMS_CODE_REDIS_EXPIRES = 300

# 短信验证码redis有效期
SEND_SMS_CODE_INTERVAL = 60

# 账号密码错误尝试次数
LOGIN_ERROR_MAX_TIMES = 5

# 保存错误次数的有效期
LOGIN_ERROR_FORBID_TIME = 600

# 七牛域名
QINIU_URL_DOMAIN = 'http://pwflymlov.bkt.clouddn.com/'

# 城区信息缓存时间, 单位：秒
AREA_INFO_REDIS_CACHE_EXPIRES = 7200

# 首页订单最多的数据的条数
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的Redis缓存时间，单位:秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面数据Redis缓存时间，单位:秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 7200

# 房屋列表页面每页数据容量
HOUSE_LIST_PAGE_CAPACITY = 2

# 房屋列表页面页数缓存时间，单位:秒
HOUES_LIST_PAGE_REDIS_CACHE_EXPIRES = 7200

# 支付宝对接需要变动的参数
ALIPAY_APPID="2016092800614150"     # 应用id

ALIPAY_DEBUG=True     # 真实环境False，模拟环境True，

ALIPAY_RETURN_URL="http://127.0.0.1:5000/payComplete.html"    # 支付宝返回的return_url地址

ALIPAY_PAY_URL='https://openapi.alipaydev.com/gateway.do?'  # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string,真实环境去掉dev

