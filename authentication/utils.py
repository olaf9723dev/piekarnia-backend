from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.conf import settings


def send_activation_email(user, request, password):  # TODO add lang after english prepared
    # if lang == 'pl':
    email_subject = f'Resetowanie hasła {settings.APP_NAME}'
    email_body = render_to_string('password_reset.html', {
        'user': user,
        'password': password
    })

    send_mail(
        email_subject,
        '',
        None,  # TODO setting.EMAIL_FROM
        [user.email],
        fail_silently=False,
        html_message=email_body
    )
# elif lang == 'en':
#     email_subject = 'Dent-X password reset'
#     email_body = render_to_string('temp_password_en.html', {
#         'user': user,
#         'password': password
#     })
#
#     send_mail(
#         email_subject,
#         '',
#         None,
#         [user.email],
#         fail_silently=False,
#         html_message=email_body
#     )
