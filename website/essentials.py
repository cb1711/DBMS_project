import datetime
import smtplib
from email.mime.text import MIMEText



def isEmailID(id):
	parts=id.split('@')
	if(len(parts)==2):
		rem=parts[1].split('.')
		if(len(rem)>1):
			return True
		else:
			return False
	else:
		return False

def mail(user,message,subject):
	msg = MIMEText(message)
	msg['Subject'] = subject
	msg['From'] = 'iitbhu.counselling@gmail.com'
	msg['To'] = str(user)
	try:
		#socket.setdefaulttimeout(120)
		s = smtplib.SMTP('smtp.gmail.com',587)
		s.ehlo()
		s.starttls()
		s.login('iitbhu.counselling@gmail.com','counsel@iitbhu')
		s.sendmail('iitbhu.counselling@gmail.com', str(user), msg.as_string())
		s.quit()
		return True
	except:
		return False
def dateConvert(periodStart):
	periodStart=periodStart.split('-')
	startY=periodStart[0]
	startM=periodStart[1]
	startD=periodStart[2]
	startDate=datetime.date(int(startY),int(startM),int(startD))
	return startDate
