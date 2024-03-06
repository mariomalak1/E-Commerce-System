from project.settings import EMAIL_HOST_USER

def resetPasswordSendMail(resetCode, user_):
    title = "Password Reset Request"
    body = f"Security code to reset your password is \n {resetCode} \n " \
           "If you Don't make the request, then simply ignore this email and no change will be made"
    user_.email_user(title, body, from_email=EMAIL_HOST_USER)
