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
    # Preview resumes by HR

    receiver_email = mail

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    if ip == 1:
        # Create the plain-text and HTML version of your message
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
        file = "Extras\logfile.txt"
        attachment = open(file, 'rb')

        obj = MIMEBase('application', 'octet-stream')
        obj.set_payload((attachment).read())
        encoders.encode_base64(obj)
        obj.add_header('Content-Disposition', "attachment; filename= "+file)
        message.attach(obj)

        write_log('Log data sent to admin')

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, get_password())
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        write_log('Mail Server logged in successfully ! \nMailSent')
    except:
        write_log('Mail Server login failed')

    return
