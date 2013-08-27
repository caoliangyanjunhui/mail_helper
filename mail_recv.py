import poplib, email, string, os

class MailRecv(object):
	"""docstring for MailRecv"""
	def __init__(self, host, username, password, store_path):
		super(MailRecv, self).__init__()
		self.__pop = poplib.POP3(host)
		self.__pop.set_debuglevel(1)
		self.__pop.user(username)
		self.__pop.pass_(password)
		self.__path = store_path

	def __get_filename(self, original_fname):
		arr = original_fname.split('?')
		print 'arr:', arr
		fname_arr = arr[3].split('.')
		print 'fname_arr:', fname_arr
		fname = ''
		tmp = fname_arr[0].split('=')
		for i in range(1,len(tmp)):
			fname += chr(string.atoi(tmp[i],16))
		return '.'.join((fname.decode(arr[1]), fname_arr[1]))

	def __save_file(self, dir_name, filename, idx, content):
		try:
			self.__path = os.path.join(self.__path, str(idx))
			if not os.path.exists(self.__path):
				os.makedirs(self.__path)
			print 'path:', self.__path
			fp = open(os.path.join(self.__path, filename), 'wb')
			fp.write(content)
			fp.close()
		except Exception, e:
			print 'Save file:%s error: %s' % (filename, e)	

	def recv(self):
		ret = self.__pop.stat()
		print ret[0]
		for i in range(1, ret[0] + 1):
			mlist = self.__pop.top(i, 0)
			print 'line:', len(mlist[1])
		print ret
		print self.__pop.list()

		for i in range(1, ret[0] + 1):
			hdr, msg, octet = self.__pop.retr(i)
			#print 'hdr:',hdr
			#print 'msg',msg
			#print 'octet',octet

			mail = email.message_from_string(string.join(msg,'\n'))
			endcode_type = email.Header.decode_header(mail['subject'])[0][1]
			print email.Header.decode_header(mail['subject'])[0][0].decode(endcode_type)
			for part in mail.walk():
				print 'content type:', part.get_content_type()
				if part.get_content_maintype() == 'multipart':
					continue
				if part['Content-Disposition'] is None:
					print('no content dispo')
					continue
				filename = part.get_filename()
				if not filename: 
					filename = 'test.txt'
				else:
					filename = self.__get_filename(filename)
				self.__save_file(self.__path, filename, i, part.get_payload(decode=1))
		self.__pop.quit()

'''
				self.__save_file(self.__path, filename, i, part.get_payload(decode=1))

				try:
					fp = open(os.path.join(self.__path, filename), 'wb')
					fp.write(part.get_payload(decode=1))
					fp.close()
				except Exception, e:
					print 'Save file:%s error: %s' % (filename, e)	
'''
		

host = 'pop3.163.com'
username = 'python_mail_test@163.com'
password = 'python'
file_path = '.'

def main():
	mail_recv = MailRecv(host, username, password, file_path)
	mail_recv.recv()

if __name__ == '__main__':
	main()
