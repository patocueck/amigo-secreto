import random
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]
flow = InstalledAppFlow.from_client_secrets_file('creds.json', SCOPES)
creds = flow.run_local_server(port=0)

# (nombre, grupoFamiliar, email)
people = [
    ('persona01',   'G1',   'persona01@email.com'),
    ('persona02',   'G1',   'persona02@email.com'),
    
    ('persona03',   'G2',   'persona03@email.com'),
    ('persona04',   'G2',   'persona04@email.com'),
    
    ('persona05',   'G3',   'persona05@email.com'),
    ('persona06',   'G3',   'persona06@email.com'),
    ('persona07',   'G3',   'persona07@email.com')
]

amigos = list(people)


service = build('gmail', 'v1', credentials=creds)

ok = False
while not ok:
    random.shuffle(amigos)
    for p, a in zip(people, amigos):
        if p == a: #si se encuentra el mismo, ordena de nuevo
            break
        elif p[1] == a[1]: #si encuentra otro pero del mismo grupo familiar, ordena de nuevo
            break
    else:
        ok = True
            
else:
    for p, a in zip(people, amigos):
        #print ('%s (%s): %s (%s)' % (p[0], p[1], a[0], a[1]))
        body = """
        <html>
          <body>
            <p>Hola <b>persona !</b></p><p> Tu regalo de amigo secreto es para: <b>destinatario</b></p>
            </br>
            
            <p>Recuerda que el valor del regalo es de $30.000</p>
            <p>La entrega es el día X de Diciembre</p>
          </body>
        </html>
        """
        body = body.replace('persona', p[0])
        body = body.replace('destinatario', a[0])
        message = MIMEText(body, 'html')
        message['subject'] = 'Amigo secreto de los Zuñiga'
        message['to'] = p[2]
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        try:
            message = (service.users().messages().send(userId="me", body=create_message).execute())
            print(F'sent message to {message} Message Id: {message["id"]}')
        except HTTPError as error:
            print(F'An error occurred: {error}')
            message = None