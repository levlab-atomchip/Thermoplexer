# def email_warning(self, tcname, temp):
import smtplib
tcname = 'tctest'
temp = 250
maxtemp = 200

sender = 'thermoplexer@stanford.edu'
receivers = ['rwturner@stanford.edu']

message = '''From: From Thermoplexer <thermoplexer@stanford.edu>
To: To Human <ACM>
Subject: Overheating Warning!!

The thermocouple labeled '%s' has reached a temperature of %d!

The maximum acceptable temperature is %d.

Love,
Thermoplexer
'''%(tcname, temp, maxtemp)

smtpObj = smtplib.SMTP('smtp-unencrypted.stanford.edu', 25)
# smtpObj.login('rwturner@stanford.edu','twywapfi')
# smtpObj.starttls()
# smtpObj.sendmail(sender, receivers, message)         
print("Successfully sent email")
# except SMTPException:
   # print("Error: unable to send email")
# smtpObj.quit()

# import os
# import smtplib
# import mimetypes
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email.mime.text import MIMEText
# from email.mime.audio import MIMEAudio
# from email.mime.image import MIMEImage
# from email.encoders import encode_base64
# def sendMail(subject, text, *attachmentFilePaths):
    # gmailUser = 'blevlab@gmail.com'
    # gmailPassword = 'atomchip'
    # recipient = 'rwturner17@gmail.com'
    # msg = MIMEMultipart()
    # msg['From'] = gmailUser
    # msg['To'] = recipient
    # msg['Subject'] = subject
    # msg.attach(MIMEText(text))
    # for attachmentFilePath in attachmentFilePaths:
        # msg.attach(getAttachment(attachmentFilePath))
    # mailServer = smtplib.SMTP('aspmx.l.google.com', 25)
    # mailServer.ehlo()
    # mailServer.starttls()
    # mailServer.ehlo()
    # mailServer.login(gmailUser, gmailPassword)
    # mailServer.sendmail(gmailUser, recipient, msg.as_string())
    # mailServer.close()
    # print('Sent email to %s' % recipient)
# def getAttachment(attachmentFilePath):
    # contentType, encoding = mimetypes.guess_type(attachmentFilePath)
    # if contentType is None or encoding is not None:
        # contentType = 'application/octet-stream'
        # mainType, subType = contentType.split('/', 1)
        # file = open(attachmentFilePath, 'rb')
    # if mainType == 'text':
        # attachment = MIMEText(file.read())
    # elif mainType == 'message':
        # attachment = email.message_from_file(file)
    # elif mainType == 'image':
        # attachment = MIMEImage(file.read(),_subType=subType)
    # elif mainType == 'audio':
        # attachment = MIMEAudio(file.read(),_subType=subType)
    # else:
        # attachment = MIMEBase(mainType, subType)
    # attachment.set_payload(file.read())
    # encode_base64(attachment)
    # file.close()
    # attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachmentFilePath))
    # return attachment

if __name__ == "__main__":
    sendMail('test tplx email', message)