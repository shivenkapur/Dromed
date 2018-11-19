from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from db.models import Users
from random import randint

def get_random(x):
    startRandom = 10**(x-1)
    endRandom = (10**x)-1
    return randint(startRandom, endRandom)



def main():
	users = Users.objects.all()
	for user in users:
		if not user.token:
			token = hex(get_random(32)).split('x')[-1]
			user.token = token
			user.save()
			send_mail('Token', str(token), user.emailID, [user.emailID], fail_silently=False)
			print('hi')


if __name__ == '__main__':
    main()