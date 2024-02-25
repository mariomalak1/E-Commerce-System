from django.core.paginator import Paginator

from project.settings import EMAIL_HOST_USER

def resetPasswordSendMail(resetCode, user_):
    title = "Password Reset Request"
    body = f"Security code to reset your password is \n {resetCode} \n " \
           "If you Don't make the request, then simply ignore this email and no change will be made"
    user_.email_user(title, body, from_email=EMAIL_HOST_USER)


# function that take paginator and try to get the required page number and per-page number
def getDataFromPaginator(request, objectsNeedToPaginate) -> "required_page, per_page, paginator":
    try:
        required_page = request.GET.get("page", 1)
        per_page = request.GET.get("perPage", 10)

        paginator = Paginator(objectsNeedToPaginate, per_page)

        if int(required_page) > paginator.num_pages:
            required_page = paginator.num_pages
        elif int(required_page) < 1:
            required_page = 1
        else:
            required_page = int(required_page)
        return (required_page, per_page, paginator)
    except:
        return None