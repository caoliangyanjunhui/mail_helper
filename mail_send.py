# encoding: UTF-8
import smtplib
from email.mime.text import MIMEText


class MailSend(object):
	"""docstring for MailSend"""
	def __init__(self, host, user, password, postfix):
		super(MailSend, self).__init__()
		self.__host = host
		self.__user = user
		self.__password = password
		self.__postfix = postfix


	def send(self, to_list, subject, content):
		me = self.__user + '<' + self.__user + '@' + self.__postfix + '>'
		msg = MIMEText(content, 'plain', 'UTF-8')
		msg['Subject'] = subject
		msg['From'] = me
		msg['To'] = ';'.join(to_list)
		print '========', msg['To'], '==========='

		try:
			s = smtplib.SMTP()
			s.set_debuglevel(1)
			s.connect(self.__host)
			s.login(self.__user, self.__password)
			s.sendmail(me, to_list, msg.as_string())
			s.close()
		except Exception, e:
			print 'send mail failed, from:%s, to:%s, error:%s' % (self.__user, str(to_list), e)


HOST = 'smtp.163.com'
USER = 'python_mail_test'
PASSWORD = 'python'
POSTFIX = '163.com'

def main():
	mail_send = MailSend(HOST, USER, PASSWORD, POSTFIX)
	mail_send.send(('python_mail_test@163.com',), '发送测试', '这是一封测试邮件')

if __name__ == '__main__':
	main()