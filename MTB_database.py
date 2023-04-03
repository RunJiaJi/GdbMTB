from flask import Flask, render_template, url_for
app = Flask(__name__)

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
        return 'Your sequence has been uploaded'
    
if __name__ == '__main__':
    app.run(debug=True)