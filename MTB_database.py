from flask import Flask, render_template, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'user_files/'


############################# functions ↓ ###########################
def save_user_file(email, file):
    new_path = os.path.join(UPLOAD_FOLDER, f'{datetime.utcnow().timestamp()}_{email}')
    file.save(new_path)
    return new_path

def send_mail():
    import smtplib
    from email.mime.text import MIMEText

    FROM='sender@qq.com'                                #发送方邮箱
    PASSWD='bbphmxqqphpmidcj'                           #填入发送方邮箱的授权码
    TO='receiver@gmail.com'                             #收件人邮箱
    SUBJECT='TITLE'                                     #主题     
    msg = MIMEText('CONTENT')

    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(FROM, PASSWD)
        s.sendmail(FROM, TO, msg.as_string())
        print("发送成功")
    except:
        print("发送失败")
    finally:
        s.quit()

def handle_user_file(email, path):
    pass

#############################  routers  ↓ ###########################
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/browser")
def browser():
    return render_template('browser.html', title='Browser')

@app.route("/tree")
def tree():
    return render_template('tree.html', title='Tree')

@app.route("/statistics")
def statistics():
    return render_template('statistics.html', title='Statistics')

@app.route("/download")
def download():
    return render_template('download.html', title='Download')

@app.route("/tools", methods = ['GET', 'POST'])
def tools():
    if request.method == 'GET':
        return render_template('tools.html', title='Tools')
    if request.method == 'POST':
        print(request.form)
        email = request.form['useremail']
        file = request.files['userfile']
        new_path = save_user_file(email, file)
        handle_user_file(email, new_path)
        return f'Your sequence has been uploaded successfully! An email will be sent to {email}, check later please.'


if __name__ == '__main__':
    app.run(debug=True)