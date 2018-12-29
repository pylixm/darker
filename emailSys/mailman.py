#encoding:utf-8
from email.mime.multipart import MIMEMultipart

import smtplib
from email.mime.text import MIMEText
from django.db.backends.dummy.base import ignore
import traceback


class Email(object):
    def __init__(self,smtp_server,mail_user,login_passwd):
        self.mail_user = mail_user
        try:
            self.s = smtplib.SMTP()
            self.s.connect(smtp_server)
            self.s.login(mail_user,login_passwd)
        except Exception,e:
            print "E-mail login faild : %s " %traceback.format_exc()
    
    def send(self,send_to_list,subject,body):
        if not isinstance(subject,unicode):
            subject = unicode(subject)
        if not isinstance(body,unicode):
            body = unicode(body)
        content = MIMEText(body,'plain','utf-8')
        content['Subject'] = subject
        content['From'] = ''
        content['To'] =   ';'.join(send_to_list)
      
        content["Accept-Language"]="zh-CN"
        content["Accept-Charset"]="ISO-8859-1,utf-8"
        print 'Sending email to:', content['To']
        try:
            self.s.sendmail(self.mail_user, send_to_list, content.as_string())
            self.s.close()
        except Exception,e:
            print "E-mail send mess faild : %s " %traceback.format_exc()

    def send_as_html(self, send_to_list, subject, body):
        """
        使用邮件模板发送
        :param send_to_list:
        :param subject:
        :param body:
        :return:
        """
        if not isinstance(subject,unicode):
            subject = unicode(subject)
        if not isinstance(body,unicode):
            body = unicode(body)

        content = MIMEMultipart('alternative')
        body_attach = MIMEText(body,'html','utf-8')
        content['Subject'] = subject
        content['From'] = ''
        content['To'] =   ';'.join(send_to_list)

        content.attach(body_attach)
        content["Accept-Language"]="zh-CN"
        content["Accept-Charset"]="ISO-8859-1,utf-8"
        print 'Sending email to:', content['To']
        try:
            self.s.sendmail(self.mail_user, send_to_list, content.as_string())
            self.s.close()
        except Exception,e:
            print "E-mail send mess faild : %s " %traceback.format_exc()


def send_mail(send_to_list,subject,body):
    send_smtp = ""
    send_user = ""
    send_pass = ""
    mail_obj = Email(send_smtp,send_user,send_pass)
    mail_obj.send(send_to_list,subject,body)

def send_html_mail(send_to_list,subject,body):
    send_smtp = ""
    send_user = ""
    send_pass = ""
    mail_obj = Email(send_smtp,send_user,send_pass)
    mail_obj.send_as_html(send_to_list, subject, body)


if __name__ == '__main__':
    send_mail(['pyli.xm@gmail.com'],'Test email 3', 'You are the loser! yes ,you.')      
