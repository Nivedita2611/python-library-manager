from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html',title="login/registe")

@app.route('/')
def signup():
    return render_template('signup.html',title="signup")

@app.route('/')
def search():
    return render_template('search',title="search")

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/library')
def library_list():
    return render_template('list.html')

@app.route('/search')
def search():
    return render_template('Search.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug= True)


