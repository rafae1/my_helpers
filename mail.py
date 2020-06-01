import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiofiles
import aiosmtplib
from aiosmtplib.errors import SMTPServerDisconnected

# dict для smtp клиентов,
# т.к. может быть письмо отправлено с разных почтовых ящиков,
# один почтовый ящик - один клиент
smtp = {}
conf = {"host": "", "port": "", "tls": "", "timeout": "", "use_starttls": ""}


async def send_email(to, subject, body, html_body=None, from_email=None,
                     from_password=None,
                     cc=None, bcc=None, files=None):
    files = files or []
    # если не переданы ящик и пароль, с которого отправлять письмо,
    # то берем из конфига
    email = from_email or conf['email']
    password = from_password or conf['password']
    # иницилизируем клиента, если еще такого нет
    if not smtp.get(email):
        smtp[email] = aiosmtplib.SMTP(hostname=conf['host'], port=conf['port'],
                                      use_tls=conf['tls'],
                                      timeout=conf['timeout'])

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = ', '.join(to) if isinstance(to, list) else to
    if cc:
        msg['Cc'] = ', '.join(cc) if isinstance(cc, list) else cc
    if bcc:
        msg['Bcc'] = ', '.join(bcc) if isinstance(bcc, list) else bcc

    msg.attach(MIMEText(body, 'plain'))
    if html_body:
        msg.attach(MIMEText(html_body, 'html'))

    for filename in files:
        async with aiofiles.open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(await attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(filename)}",
        )
        msg.attach(part)
    try:
        await smtp[email].send_message(msg)
    except SMTPServerDisconnected:
        await smtp[email].connect()
        if conf.get('use_starttls'):
            await smtp[email].starttls()
        await smtp[email].login(email, password)
        await smtp[email].send_message(msg)
