from .worker import celery
from .models import Users,Orders
from jinja2 import Template
from celery.schedules import crontab
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(email,subject,email_content):
    smtp_server_host = "localhost"
    smtp_port = 1025
    sender_email = "admin@gmail.com"
    sender_password = ""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(email_content,"html"))

    server = smtplib.SMTP(host =smtp_server_host,port = smtp_port)
    server.login(sender_email,sender_password)
    server.send_message(msg)
    server.quit()
    print("email sent")

    

def get_html_report(username,data):
    with open("/report.html","r") as file:
        jinja_template = Template(file.read())
        html_report = jinja_template.render(username=username,data=data)
        return html_report
@celery.on_after_configure.connect
def setup_periodic_tasks(sender,**kwargs):
    sender.add_periodic_task(10.0,monthly_report.s(),name="report at every 10 sec for test")

    sender.add_periodic_task(10.0,daily_remainder,name="daily remainder at 10 am")

    sender.add_periodic_task(crontab(hour = 8, minute = 0),daily_remainder,name = "daily remainder at 8 am")
@celery.task
def test(arg):
    print(arg)

@celery.task
def daily_remainder():
    customer = Users.query.filter_by(role="customer").all()
    for customer in customer:
        msg = f"<h1>hello {customer.name}! Please visit grocery store today</h1>"
        send_mail(email = customer.email,email_content=msg,subject="Daily Report")
    print("Remainder sent")

@celery.task
def monthly_report():
    customer = Users.query.filter_by(role="customer").all()
    for customer in customer:
        orders = Orders.query.filter_by(customer_id=customer.id).all()
        orders_detail = []
        for order in orders:
            temp_order = []
            temp_order.append(order.product_id)
            temp_order.append(order.quantity)
            temp_order.append(order.date_of_purchase)
            temp_order.append(order.products.name)
            temp_order.append(order.products.price)
            temp_order.append(order.products.unit)
            orders_detail.append(temp_order)
        html_report = get_html_report(username = customer.name,data = orders_detail)
        send_mail(email = customer.email,subject="Monthly Report",email_content=html_report)

    print("email sent")
    