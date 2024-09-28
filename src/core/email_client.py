import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from src.config.logging import logger


class SendGridEmailClient:

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.sender = "fiuba.tpp.notificaciones@gmail.com"
        self.name = 'FIUBA Trabajo Profesional'

    def _get_api_client(self):
        if self.api_key is None:
            raise Exception("No api key provided")
        return sendgrid.SendGridAPIClient(api_key=self.api_key)

    def _log_response(self, response):
        if response.status_code == 202:
            logger.info("Email send successfully")
        else:
            logger.info(
                f"Sendgrid send email had a problem, the response code status is: {response.status_code}"
            )
    
    def send_mail(self, mail: Mail):
        sg = self._get_api_client()
        
        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()
        response = sg.client.mail.send.post(request_body=mail_json)
        return response

    def send_email(self, to: str, subject: str, body: str):
        from_email = Email(self.sender, name= self.name)
        to_email = To(to)
        content = Content("text/plain", body)
        mail = Mail(from_email, to_email, subject, content)

        response = self.send_mail(mail)
        self._log_response(response)
        return response.status_code

    def send_emails(self, to: list[str], subject: str, body: str):
        from_email = Email(self.sender, name= self.name)
        to_emails = [To(user) for user in to]
        content = Content("text/plain", body)
        mail = Mail(from_email, to_emails, subject, content)

        response = self.send_mail(mail)
        self._log_response(response)
        return response.status_code
