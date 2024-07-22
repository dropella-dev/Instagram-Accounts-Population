from instagrapi import Client


cl = Client()
cl.__setattr__('device_id', 'android-8ad80b61e790ed47')
signup = cl.signup('eatmoregetfat4370','mathematics4370','hassamrajpoot100@gmail.com','','babluman437')
print(signup)
#create_account = cl.accounts_create('eatmoregetfat4370','mathematics4370','hassamrajpoot100@gmail.com','','babluman437')
# cl.send_confirm_email()
# cl.send_confirm_phone_number()
# cl.send_verify_email()
# cl.check_email()
# cl.check_confirmation_code()
# cl.get_signup_config()
# cl.signup()
# cl.accounts_create()
#'android-8ad80b61e790ed47'