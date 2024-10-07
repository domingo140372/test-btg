
#from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_sms(to_phone, message):
    pass
    """
    PARA PODER HABILITAR ESTA FUNCION SE NECESITA 
    UNA CUENTA EN UN SERVICIO DE ENVIO DE SMS COMO TWILO 
    POR LO TANTO LA DEJO COMENTADA PARA QUE EL DESARROLADOR DECIDA
    EN UN FUTURO COMO HABILITARLA

    try:
        client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        message = client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=to_phone
        )
        return "SMS enviado con éxito"
    except Exception as e:
        return f"Error al enviar el SMS: {e}"
 """


def send_email(to_email, subject, body):
    """
    para hacer efectivo el envio de emails
    por favor configure las variables de entorno
    en el archivo .env 
    """
    try:

        # Configura el servidor SMTP
        server = smtplib.SMTP(os.getenv("EMAIL_HOST"), os.getenv("EMAIL_PORT"))
        server.starttls()
        server.login(os.getenv("EMAIL_HOST_USER"), os.getenv("EMAIL_HOST_PASSWORD"))

        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL_HOST_USER")
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Enviar el correo
        server.sendmail(os.getenv("EMAIL_HOST_USER"), to_email, msg.as_string())
        server.quit()
        return "Correo enviado con éxito"
    except Exception as e:
        return f"Error al enviar el correo: {e}"
    