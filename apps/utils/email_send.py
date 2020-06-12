from django.core.mail import send_mail
from random import Random
from users.models import EmailVerifyRecord


# code是一个随机的字符串
def random_str(random_length=8):
    code = ""
    str1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random = Random()
    for i in range(random_length):
        code += str1[random.randint(0, len(str1) - 1)]
    return code


def send_register_email(email,send_type="register"):
    #发送邮件之前，先保存到数据库，以方便查询链接是否存在
    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    email_record.email = email
    email_record.send_type = send_type
    #code
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    # 生成随机的code放入链接
    email_record.code = code
    email_record.save()

    #定义邮件的标题、内容
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "在线教育注册激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)
        send_status = send_mail(email_title,email_body,"1419517126@qq.com",[email])
        if send_status:
            pass
    elif send_type == "forget":
        email_title = "在线教育找回密码链接"
        email_body = "请点击下面的链接找回你的密码：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title, email_body, "1419517126@qq.com", [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = "在线教育--修改验证码"
        email_body = "你的邮箱验证码为{0}".format(code)
        # 使用Django内置函数完成邮件发送，主题，邮件主体，发送邮箱，接受者列表，返回一个状态信息
        send_status = send_mail(email_title, email_body, "1419517126@qq.com", [email])
        if send_status:
            pass