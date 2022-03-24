from flask import Flask
from flask import render_template,request
import json

app = Flask(__name__)


import smtplib, ssl

smtp_server = "smtp.mail.ru"
port = 587  # For starttls
sender_email = "9x02@mail.ru"
password = "jZzwWNZBYmUDZYLwbq9z"



config = []
with open('config.json', 'r') as f:
    config = json.loads(f.read())
cost_1 = config['cost_1_room']
cost_2 = config['cost_2_room']
cost_3 = config['cost_3_room']

@app.route('/')
def main_page():  # put application's code here
    return render_template('index.html', cost_1 = cost_1, cost_2 = cost_2, cost_3 = cost_3)
@app.route('/<variable>', methods=['GET'])
def render_var(variable):
    #do your code here
    return render_template(f"{variable}", cost_1 = cost_1, cost_2 = cost_2, cost_3 = cost_3)
@app.route('/send_order_info',  methods=['POST'])
def send_order_info():
    js_temp = json.loads(request.data)
    # Create a secure SSL context
    context = ssl.create_default_context()
    global sender_email
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        receiver_email = "alegnin@mail.ru"
        message = f"""\
        Content-type: text/html
        Subject: SMTP HTML e-mail test

        <b>Новая заявка с сайта:</b>
        <h1>Телефон:{js_temp['tel']}</h1>
        <h1>Зовут:{js_temp['name']}</h1>
        <h1>Даты:{js_temp['date_in']} - {js_temp['date_out']}</h1>
        <h1>Что хочет:{js_temp['num']}</h1>
        """
        message = u''.join((message)).encode('utf-8').strip()
        server.sendmail(sender_email,receiver_email,message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
