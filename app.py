from flask import Flask, render_template, session, request, redirect, flash, url_for
from sqlalchemy import create_engine
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from database import User
from queue import Queue
import random
from threading import Thread
import time
from handler import *
from librarymanager import *
import re

app = Flask(__name__)
app.secret_key = "the basics of life with python"

# for validating an Email 
def validate_email(email):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):  
        return True 
    return False

def get_db():
    engine = create_engine('sqlite:///database.sqlite')
    Session = scoped_session(sessionmaker(bind=engine))
    return Session()
    

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username:
            if password and len(password)>=6:
                try:
                    sess = get_db()
                    user = sess.query(User).filter_by(name=username,password=password).first()
                    if user:
                        session['isauth'] = True
                        session['email'] = user.email
                        session['id'] = user.id
                        session['name'] = user.name
                        del sess
                        flash('login successfull','success')
                        return redirect('/home')
                    else:
                        flash('email or password is wrong','danger')
                except Exception as e:
                    flash(e,'danger')
    return render_template('login.html',title='login')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if name and len(name) >= 3:
            if email and validate_email(email):
                if password and len(password)>=6:
                    if cpassword and cpassword == password:
                        try:
                            sess = get_db()
                            newuser = User(name=name,email=email,password=password)
                            sess.add(newuser)
                            sess.commit()
                            del sess
                            flash('registration successful','success')
                            return redirect('/')
                        except:
                            flash('email account already exists','danger')
                    else:
                        flash('confirm password does not match','danger')
                else:
                    flash('password must be of 6 or more characters','danger')
            else:
                flash('invalid email','danger')
        else:
            flash('invalid name, must be 3 or more characters','danger')
    return render_template('signup.html',title='register')

@app.route('/home',methods=['GET','POST'])
def home():
    if session.get('isauth'):
        username = session.get('name')
        return render_template('home.html',title=f'Home|{username}')
    flash('please login to continue','warning')
    return redirect('/')

@app.route('/logout')
def logout():
    if session.get('isauth'):
        session.clear()
        flash('you have been logged out','warning')
    return redirect('/')

@app.route('/library')
def library_list():
    logfile = load_libs()
    lib_info = []
    with open(logfile,'r') as f:
        data = f.read()
        if data:
            names = data.split('---')[-1].strip()
            names = names.splitlines()
            for name in names:
                if '==' in name:
                    name, version = name.split('==')
                    lib_info.append({
                        'name':name.strip(),
                        'version':version.strip(),
                        'source':'pip'
                    })
                elif '@' in name:
                    name, version = name.split('@')
                    lib_info.append({
                        'name':name.strip(),
                        'version':version.strip(),
                        'source':'conda'
                    })
        else:
            names = []
    return render_template('list.html',title='Library',names=lib_info)

@app.route('/update/<path:library>',methods=['GET','POST'])
def lib_update_lib(library):
    return_code = uplib(library)
    if return_code == 0:
        flash(f'{library} updated successfully','success')
    else:
        flash(f'failed to update {library}','danger')
    return redirect('/library')

@app.route('/uninstall/<path:library>',methods=['GET','POST'])
def uninstall_lib(library):
    
    q.put(unlib(library))

    flash(f'{library} uninstalled successfully','success')
    return redirect('/library')

@app.route('/install/<path:library>',methods=['GET','POST'])
def install_lib(library):
    if request.method == 'POST':
        # return_code = install_lib(library)
        q.put(inlib(library))
        # if return_code == 0:
        flash(f'{library} installed successfully','success')
        # else:
        #     flash(f'failed to uninstall {library}','danger')
    return redirect('/library')


@app.route('/view/<path:library>')
def view(library):
    info = get_library_info(library)
    return render_template('view.html',title=library,info=info, library=library)

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        if not query:
            flash('please enter a Library name','warning')
        else:
            pass
    return render_template('search.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


def worker():
    while True:
        item = q.get()
        print(item)
        if item is None:
            break
        print('Processing %s' % item)  # do the work e.g. update database
        time.sleep(1)
        q.task_done()



if __name__ == '__main__':
    q = Queue()
    t = Thread(target=worker)
    t.start()
    app.run(host='0.0.0.0', port=8000, debug= True)
    q.join()
    q.put(None)
    t.join()

