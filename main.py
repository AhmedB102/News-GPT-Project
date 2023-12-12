import imaplib
import email
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

import assistant_upload
import assistant_chat

import logging

# Configure logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Load environment variables
load_dotenv()

def send_email(to_addr, subject, body, is_html=False):
    # Sender email details loaded from environment variables
    from_addr = os.getenv('EMAIL')
    smtp_user = from_addr
    smtp_pass = os.getenv("EMAIL_PASSWORD")
    smtp_server = "smtp-mail.outlook.com"
    smtp_port = 587  # For starttls

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = from_addr
    message['To'] = to_addr
    message['Subject'] = subject

    # The body of the email
    if is_html:
        message.attach(MIMEText(body, 'html'))
    else:
        message.attach(MIMEText(body, 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP(smtp_server, smtp_port)  # use outlook with tls
    session.starttls()  # enable security
    session.login(smtp_user, smtp_pass)  # login with mail_id and password

    text = message.as_string()
    session.sendmail(from_addr, to_addr, text)
    session.quit()
    print(f'Mail Sent to {to_addr}')



def check_email_and_process():
    # Your email credentials
    username = os.getenv('EMAIL')
    password = os.getenv("EMAIL_PASSWORD")

    # Create an IMAP4 class with SSL 
    imap = imaplib.IMAP4_SSL("imap-mail.outlook.com")
    imap.login(username, password)

    # Select the mailbox you want to check, typically INBOX
    imap.select('INBOX')

    # Search for specific emails with the given subject
    subject = 'Sudan News Sweep'
    status, messages = imap.search(None, '(SUBJECT "' + subject + '")')
    mail_ids = [int(mail_id) for mail_id in messages[0].split()]
    mail_ids.sort(reverse=True)  # Sort the email ids in descending order

    email_content = ''
    if mail_ids:
        # Fetch the email by ID
        status, msg_data = imap.fetch(str(mail_ids[0]), '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                if msg.is_multipart():
                    for part in msg.walk():
                        content_disposition = str(part.get("Content-Disposition"))
                        if "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename and filename.endswith(".pdf"):
                                filepath = f"{filename}"
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                # Now you can call your main function with the downloaded PDF
                                assistant_upload.process_pdf_and_update_assistant(filepath)
                                email_content = assistant_chat.run_open_ai()
                                break  # Assumes only one PDF attachment is of interest

    # Close the mailbox
    imap.close()
    # Log out from the server
    imap.logout()

    return email_content

def markdown_to_html(text):
    # Replace markdown bold with HTML bold
    text = text.replace('**', '<b>').replace('**', '</b>')
    return text

def main():
    # Check the email for new updates and process them
    email_content = check_email_and_process()

    # Send the processed content via email
    if email_content:
        recipient = "abc@gmail.com"
        email_subject = "Sudan News Update"
        send_email(recipient, email_subject, email_content, is_html=False)
    else:
        print("No new Sudan News Sweep email found or no content to send.")


# Run the main function
if __name__ == "__main__":
    main()
