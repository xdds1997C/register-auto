import requests
import io
import sys
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
email = ''
passwd = ''
loginurl = 'https://freemycloud.cc/auth/login'
userurl='https://freemycloud.cc/user'
def sendemail(text):
	mail_host='smtp.gmail.com'
	mail_user=''
	mail_passwd=''
	sender=''
	receiver=['']

	message=MIMEText(text,'plain','utf-8')
	message['Subject']='闪电签到'
	message['From']=sender
	message['To']=receiver[0]

	try:
		smtpObj=smtplib.SMTP_SSL('smtp.gmail.com',465)
		#smtpObj.set_debuglevel(1)
		#smtpObj.ehlo()
		#smtpObj.starttls()
		smtpObj.login(sender,mail_passwd)
		smtpObj.sendmail(sender,receiver,message.as_string())
		smtpObj.quit()
		print('success')
	except smtplib.SMTPException as e:
		print('error',e)

def main():
	s = requests.Session()
	loginparams = {'email': email, 'passwd': passwd}
	r = s.get(loginurl)
	send_text=time.asctime(time.localtime(time.time()))
	if r.status_code is not 200:
		send_text+='网页无法请求，请查看网站是否正常'
		return 0
	r=s.post(loginurl,data=loginparams)
	
	r.encoding = 'utf-8'

	checkinurl='https://freemycloud.cc/user/checkin'
	r=s.post(checkinurl)
	r=s.get(userurl)
	soup = BeautifulSoup(r.text, 'html.parser') 
	state = soup.select('a[class="btn kt-subheader__btn-secondary disabled"]')
	if state:
		if '已签到' in state[0].text:
			send_text+=',今日已签到成功,'
		else:
			send_text+=',今日未签到成功,'

	script=soup.select('h4[class="m-b-0"]')

	send_text=send_text+"剩余流量："+script[2].text
	print(send_text)
	sendemail(send_text)
	
if __name__ == '__main__':
	main()