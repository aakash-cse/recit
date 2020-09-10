from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import smtplib
import ssl
from extra import write_log, get_password

sender_email = "testrecruitathon@gmail.com"


def email_content(ip, mail):
    write_log('\nMail System triggered')
    receiver_email = mail
    message = MIMEMultipart("alternative")

    message["From"] = sender_email
    message["To"] = receiver_email
    print('mail program', ip, mail)
    if ip == 1:
        # Create the plain-text and HTML version of your message
        message["Subject"] = 'Preview Mail'
        text = """\
        Hi,
        This is a preview mail"""
        html = """\
        <html>
        <body>
            <p>Hi,<br>
            This is a preview mail<br>
            </p>
        </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)
        write_log('Preview mail template loaded')
    #Mailing template to call for interview
    elif ip == 2:
        # Create the plain-text and HTML version of your message
        message["Subject"] = 'Interview Mail'
        text = """\
        Hi,
        This is a Interview mail"""
        html = """\
        <html>
        <body>
            <p>Hi,<br>
            This is a Interview mail<br>
            </p>
        </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)
        write_log('Interview mail template loaded')

    elif ip == 3:
        message['Subject'] = "Recruitathon Log File"
        log_file = r"Extras\logfile.txt"
        attachment = open(log_file, 'rb')
        obj = MIMEBase('application', 'octet-stream')
        obj.set_payload((attachment).read())
        encoders.encode_base64(obj)
        obj.add_header('Content-Disposition',
                       "attachment; filename= "+log_file)
        message.attach(obj)
        write_log('Log data sent to admin')

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            pass_wd = get_password()
            server.login(sender_email, pass_wd)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        print('mail sent')
        write_log('Mail Server logged in successfully ! \nMailSent')
    except:
        write_log('Mail Server login failed')
        print('mail failed')
    return
