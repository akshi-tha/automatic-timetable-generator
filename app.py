from flask import Flask, render_template, request , redirect ,session ,logging,g, url_for,make_response,  flash,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from sqlalchemy import select,create_engine
from sqlalchemy.orm import Session
import random
import pandas as pd
from constraint import *
import constraint
import smtplib
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
import secrets   
from itsdangerous import URLSafeTimedSerializer  # For secure tokens
from apscheduler.schedulers.background import BackgroundScheduler



engine=create_engine('sqlite:///database.sqlite3',echo=True)
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
app.config['SECRETE_KEY']='secretkey'
 
bcrypt = Bcrypt(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # For SSL
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'autotimetablegen@gmail.com'
app.config['MAIL_PASSWORD'] = 'jtml evfh vuhm ymzy'
app.config['MAIL_USE_TLS'] = False

mail = Mail(app)

app.secret_key=os.urandom(24)
db =SQLAlchemy(app)
app.app_context().push()






class admin(db.Model,UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False, unique=True)
    email = db.Column(db.String(120),nullable=False, unique=True)
    password = db.Column(db.String(80),nullable=False)
    
    

class department(db.Model,UserMixin):
    d_id = db.Column(db.Integer, primary_key=True)
    dname = db.Column(db.String(20),nullable=False)
    admin_id=db.Column(db.Integer,db.ForeignKey(admin.admin_id))

    


class hod(db.Model,UserMixin):
    hod_id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    username = db.Column(db.String(200),nullable=False, unique=True)
    password = db.Column(db.String(200),nullable=False)
    mail=db.Column(db.String(80),nullable=False)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))
    admin_id=db.Column(db.Integer,db.ForeignKey(admin.admin_id))
    @staticmethod
    def generate_username_password():
        username = f"user_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        length = 12 
        random_string = secrets.token_hex(length // 2) 
        password_hash =f"{random_string}"
        print('===================================================', username, password_hash)
        return username, password_hash

    
class teacher(db.Model,UserMixin):
    teacher_id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(80))
    mail=db.Column(db.String(80))
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))
    admin_id=db.Column(db.Integer,db.ForeignKey(admin.admin_id))

    @staticmethod
    def generate_username_password():
        username = f"user_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        length = 12 
        random_string = secrets.token_hex(length // 2) 
        password_hash =f"{random_string}"
        print('===================================================', username, password_hash)
        return username, password_hash







def __repr__(self) -> str:
        return f"{self.sno}  -  {self.title}"



class subjects(db.Model):
    sid=db.Column(db.Integer,primary_key=True)
    sname= db.Column(db.String(20),nullable=False)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))



class classes(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    cname= db.Column(db.String(20),nullable=False)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))


class assign(db.Model):
    aid=db.Column(db.Integer,primary_key=True)
    teacher_id= db.Column(db.Integer,db.ForeignKey(teacher.teacher_id))
    cid=db.Column(db.Integer,db.ForeignKey(classes.cid))
    sid=db.Column(db.Integer,db.ForeignKey(subjects.sid))
    weekc=db.Column(db.Integer,nullable=False)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))


class lab_assign(db.Model):
    lid=db.Column(db.Integer,primary_key=True)
    teacher_id= db.Column(db.Integer,db.ForeignKey(teacher.teacher_id))
    cid=db.Column(db.Integer,db.ForeignKey(classes.cid))
    sid=db.Column(db.Integer,db.ForeignKey(subjects.sid))
    weekc=db.Column(db.Integer,nullable=False)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))

class external(db.Model):
    exid=db.Column(db.Integer,primary_key=True)
    teacher_id= db.Column(db.Integer,db.ForeignKey(teacher.teacher_id))
    cid=db.Column(db.Integer,db.ForeignKey(classes.cid))
    sid=db.Column(db.Integer,db.ForeignKey(subjects.sid))
    lort=db.Column(db.String(200),nullable=False)
    day=db.Column(db.String(200),nullable=False)
    period=db.Column(db.Integer)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))




class timetable(db.Model):
    ttid=db.Column(db.Integer,primary_key=True)
    teacher_id= db.Column(db.Integer,db.ForeignKey(teacher.teacher_id))
    cid=db.Column(db.Integer,db.ForeignKey(classes.cid))
    sid=db.Column(db.Integer,db.ForeignKey(subjects.sid))
    lort=db.Column(db.String(200),nullable=False)
    day=db.Column(db.String(200),nullable=False)
    period=db.Column(db.Integer)
    type=db.Column(db.String(200),nullable=False)
    exid=db.Column(db.Integer,db.ForeignKey(external.exid))
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))


class lab_timetable(db.Model):
    lab_ttid=db.Column(db.Integer,primary_key=True)
    teacher_id= db.Column(db.Integer,db.ForeignKey(teacher.teacher_id))
    cid=db.Column(db.Integer,db.ForeignKey(classes.cid))
    sid=db.Column(db.Integer,db.ForeignKey(subjects.sid))
    day=db.Column(db.String(200),nullable=False)
    period=db.Column(db.Integer)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))


class lab_avail(db.Model):
    lab_aid=db.Column(db.Integer,primary_key=True)
    day=db.Column(db.String(200),nullable=False)
    period=db.Column(db.Integer)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))

class lab_free(db.Model):
    lab_fid=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.Date)
    period=db.Column(db.Integer)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))

class lab_free_store(db.Model):
    lab_fsid=db.Column(db.Integer,primary_key=True)
    date=db.Column(db.Date)
    period=db.Column(db.Integer)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))




    
class Teacher_avail(db.Model):
    avid=db.Column(db.Integer,primary_key=True)
    teacher_id= db.Column(db.Integer,db.ForeignKey(teacher.teacher_id))
    day=db.Column(db.String(500))
    period=db.Column(db.Integer)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))

class Teacher_free(db.Model):
    tfid=db.Column(db.Integer,primary_key=True)
    teacher_id= db.Column(db.Integer,db.ForeignKey(teacher.teacher_id))
    date=db.Column(db.Date)
    period=db.Column(db.Integer)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))

class Teacher_free_store(db.Model):
    tfsid=db.Column(db.Integer,primary_key=True)
    teacher_id= db.Column(db.Integer,db.ForeignKey(teacher.teacher_id))
    date=db.Column(db.Date)
    period=db.Column(db.Integer)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))

class absent_teacher(db.Model):
    atid=db.Column(db.Integer,primary_key=True)
    teacher_id= db.Column(db.Integer,db.ForeignKey(teacher.teacher_id))
    date=db.Column(db.Date)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))



class substitution(db.Model):
    subid=db.Column(db.Integer,primary_key=True)
    teacher_id= db.Column(db.Integer,db.ForeignKey(teacher.teacher_id))
    original_teacher_id = db.Column(db.Integer, db.ForeignKey(teacher.teacher_id), nullable=False)
    cid=db.Column(db.Integer,db.ForeignKey(classes.cid))
    sid=db.Column(db.Integer,db.ForeignKey(subjects.sid))
    lort=db.Column(db.String(200),nullable=False)
    day=db.Column(db.String(200),nullable=False)
    period=db.Column(db.Integer)
    date=db.Column(db.Date)
    d_id=db.Column(db.Integer,db.ForeignKey(department.d_id))
    #__table_args__ = (db.UniqueConstraint(teacher_id, day, period ),)
    
    
    
    
    def __repr__(self) -> str:
        return f"{self.sno}  -  {self.title}"
    
    def __repr__(self) -> str:
        return f"{self.sno}  -  {self.title}"
    



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hod_home')
def hod_home():
     return render_template('hod_index.html')

@app.route('/teacher_home')
def teacher_home():
     return render_template('teacher_index.html')

@app.route('/admin_home')
def admin_home():
     return render_template('admin_index.html')
    

@app.route('/hod_guide')
def hod_guide():
    
    return render_template('hod_guide.html')

@app.route('/guide')
def guide() :
    
    return render_template('hod_guilde.html')

@app.route("/admin_register", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        uname = request.form['username']
        mail = request.form['email']
        passw = request.form['password']
        
        
        checku = admin.query.filter_by(username=uname).first()
        checkm = admin.query.filter_by( email = mail).first()
       


        if checku and checkm is not None:
            flash('username  and email already exists')
        elif checku  is not None:
            flash('username  already exists')
        elif checkm  is not None:
            flash(' email already exists')
        
        else:
            register = admin(username = uname, email = mail, password = passw)
            db.session.add(register)
            db.session.commit()

            return redirect(url_for("admin_login"))
    return render_template("admin_register.html")

@app.route("/admin_login",methods=["GET", "POST"])
def admin_login():
    if  g.user is not None:
        flash('ALREADY LOGGED IN','alert')
    else:
        if request.method == "POST":
                session.pop("user", None)
                uname = request.form['username']
                passw = request.form["password"]
                login = admin.query.filter_by(username=uname, password=passw).first()
                u= admin.query.filter_by(username=uname).first()
                
                p= admin.query.filter_by(password=passw).first()
               
                if u is None and p is  None:
                    flash("Please enter a valid user",'error')
                if u is None and p is not None:
                    flash("Please enter a valid user",'error')
                if u is not None and p is None:
                    flash("wrong password",'error')
                
                if login is not None:

                    session['user']=login.admin_id
                    print(session['user'])
                    return redirect(url_for("admin_profile"))
                
                else:
                
                    return redirect(url_for('admin_login'))
        #login = admin.query.filter_by(username=uname, password=passw).first()
        #if login is not None:
        #    return redirect(url_for("profile"))
    return render_template("admin_login.html")



@app.route('/admin_forgot-password', methods=['GET', 'POST'])
def admin_forgot_password():
    if request.method == 'POST':
        mail = request.form['email']
        user = admin.query.filter_by(email=mail).first()  # Assuming a User model

        if user:
            serializer = URLSafeTimedSerializer(app.secret_key)
            token = serializer.dumps(user.email, salt='admin_password-reset')
            reset_link = url_for('admin_reset_password', token=token, _external=True)

            # Send email with reset link (optional)
            if app.config['MAIL_USERNAME']:
                mail = Mail(app)
                msg = Message('Password Reset Request',
                              sender=app.config['MAIL_USERNAME'],
                              recipients=[user.email])
                msg.body = f'Click here to reset your password: {reset_link}'
                mail.send(msg)

            flash ('Password reset link sent!')
        else:
            flash ('Email not found')

    return render_template('forgot_password.html')


@app.route('/admin_reset-password/<token>', methods=['GET', 'POST'])
def admin_reset_password(token):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        email = serializer.loads(token, salt='admin_password-reset', max_age=3600)
        user = admin.query.filter_by(email=email).first()
    except:
        flash('Invalid or expired token') 

    if request.method == 'POST':
        new_password = request.form['new_password']
        user.password = new_password
        db.session.commit()
        flash( 'Password reset successfully!')
        return redirect("/admin_login")

    return render_template('reset_password.html')







@app.route('/admin_profile')
def admin_profile():
        if g.user:
            user1=session['user']
            alltta = admin.query.filter_by(admin_id=user1).all()
            df=pd.DataFrame([( r.username ,r.email)for r in alltta],columns=['username','gmail'])
            print(df)
            gmail=df['gmail'].tolist()
            mail=gmail[0]
            u=df['username'].tolist()
            us=u[0]
            
           
            
           
            return render_template('admin_profile.html',user=session['user'],mail=mail,us=us)
        else:
            return redirect(url_for('admin_login'))
        

@app.route('/add_department', methods=['GET','POST'])
def add_department():
    if  g.user is  None:
        flash("Login to access")
        return render_template("register.html")

    else:
        if request.method=='POST':
            if not request.form['name']:
                    alldepartment = classes.query.all()
                    return render_template('admin_add_department.html', alldepartment=alldepartment)
            else:
                name=request.form["name"]
                user=session['user']

                d=department.query.filter_by(dname=name, admin_id=user).first()
                
                
                if d is not None:
                    flash('Department  already entered.')
                else:


                
                    exist = bool(department.query.filter_by( admin_id=user,dname=name).first())
                    if exist is False:
                        c=department(dname=name,admin_id=user)
                        db.session.add(c)
                        db.session.commit()
                
                
        user=session['user']
        alldepartment= department.query.filter_by(admin_id=user).all()
        user1=session['user']
        alltta = admin.query.filter_by(admin_id=user1).all()
        df=pd.DataFrame([( r.username ,r.email)for r in alltta],columns=['username','gmail'])
        print(df)
        gmail=df['gmail'].tolist()
        mail=gmail[0]
        u=df['username'].tolist()
        us=u[0]
        
        return render_template('admin_add_department.html',us=us, alldepartment =alldepartment)


@app.route('/add_hod', methods=['GET','POST'])
def add_hod():
    if  g.user is  None:
        flash("Login to access")
        return render_template("register.html")

    else:
        if request.method=='POST':
            if not request.form['name']:
                    allhod = hod.query.all()
                    return render_template('admin_add_hod.html', allhod=allhod)
            else:

                
                name=request.form["name"]
                mail=request.form["mail"]
                depart=request.form["department"]
                username, password_hash = hod.generate_username_password()
                print('========================================',name,mail,depart)
                print()
                print(depart)
                d=department.query.filter_by(d_id=depart).all()
                
                check=hod.query.filter_by(d_id=depart).first()
                check2=hod.query.filter_by(mail=mail).first()
                if check is not None:
                    flash('Department HOD already entered.')
                else:
                    if check2 is not None:
                        flash('mail already entered.')
                    else:
                    
                        user=session['user']
                        exist = bool(hod.query.filter_by(admin_id=user,name=name,mail=mail).first())
                        if exist is False:
                            c=hod(name=name,admin_id=user,mail=mail, d_id=depart, username=username, password=password_hash)
                            db.session.add(c)
                            db.session.commit()
                    
                
        user=session['user']
        allhod= hod.query.filter_by(admin_id=user).all()
        alldepartment= department.query.filter_by(admin_id=user).all()
        d_names=[]
        for i  in alldepartment:
            if i.dname not in d_names:
                d_names+=[i.dname]
        user1=session['user']
        alltta = admin.query.filter_by(admin_id=user1).all()
        df=pd.DataFrame([( r.username ,r.email)for r in alltta],columns=['username','gmail'])
        print(df)
        gmail=df['gmail'].tolist()
        mail=gmail[0]
        u=df['username'].tolist()
        us=u[0]
        return render_template('admin_add_hod.html',us=us,d_names=d_names, allhod =allhod,alldepartment =alldepartment)
 
    return render_template('admin_add_hod.html',d_names=d_names, allhod =allhod,alldepartment =alldepartment)
        

@app.route('/send_email_hod', methods=["GET", "POST"])
def send_email_hod():
    user=session['user']
    a=admin.query.filter_by(admin_id=user).first()
    sender = '(AutoPlanify,autotimetablegen@gmail.com)'
    t=hod.query.filter_by(admin_id=user).all()
    
    for i in t:
            
            recipient = i.mail
            print(recipient)
    
            subject = 'AutoPlanify login credential'
            
            link = url_for('home',  _external=True)
            body = f"This email provides you with access to AutoPlanify as a Head of Department, a platform where you create  your  timetable, view your  timetable and upcoming substitutions.\n\nYour username:{i.username}\nYour password:{i.password}\n\nTo access AutoPlanify:Visit {link}\n\nEnter your username and password.\n\nClick Sign In and explore your timetable and substitutions.\n\n If you have any questions or encounter difficulties accessing the platform, please do not hesitate to contact {a.email}.\n\n\nSincerely,\nAutoPlanify"

            msg = Message(subject, sender=sender, recipients=[recipient])
            msg.body = body

            mail.send(msg)

    return redirect("/add_hod") 

@app.route('/hod_send_email_hod/<int:sno>',  methods=["GET", "POST"])
def hod_send_email_hod(sno):
    user=session['user']
    a=admin.query.filter_by(admin_id=user).first()
    sender = 'autotimetablegen@gmail.com'
    t=hod.query.filter_by(hod_id=sno).first()
    
   
            
    recipient = t.mail
            
    link = url_for('home',  _external=True)
    
    subject = 'AutoPlanify login credential'
    
    link = url_for('home',  _external=True)
    body = f"This email provides you with access to AutoPlanify as a Head of Department, a platform where you create  your  timetable, view your  timetable and upcoming substitutions.\n\nYour username:{t.username}\nYour password:{t.password}\n\nTo access AutoPlanify:Visit {link}\n\nEnter your username and password.\n\nClick Sign In and explore your timetable and substitutions.\n\n If you have any questions or encounter difficulties accessing the platform, please do not hesitate to contact {a.email}.\n\n\nSincerely,\nAutoPlanify"

    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = body

    mail.send(msg)

    return redirect("/add_hod") 
       


@app.route('/add_teacher', methods=['GET','POST'])
def add_teacher():
    if  g.user is  None:
        flash("Login to access")
        return render_template("admin_login.html")

    else:
        if request.method=='POST':
            if not request.form['name']:
                    allhod = teacher.query.all()
                    
                    return render_template('admin_add_teacher.html', allhod=allhod)
            else:

                
                name=request.form["name"]
                mail=request.form["mail"]
                depart=request.form["department"]
                username, password_hash = teacher.generate_username_password()
                
                d=department.query.filter_by(d_id=depart).all()
                check2=teacher.query.filter_by(mail=mail).first()
                if check2 is not None:
                        flash('mail already entered.')
                else:
                
                        
                    user=session['user']
                    exist = bool(teacher.query.filter_by(admin_id=user,name=name,mail=mail,d_id=depart).first())
                    if exist is False:
                            c=teacher(name=name,admin_id=user,mail=mail, d_id=depart, username=username, password=password_hash)
                            db.session.add(c)
                            db.session.commit()
                
                
        user=session['user']
        allteacher= teacher.query.filter_by(admin_id=user).all()
        allhod= hod.query.filter_by(admin_id=user).all()
        alldepartment= department.query.filter_by(admin_id=user).all()
        d_names=[]
        for i  in alldepartment:
            if i.dname not in d_names:
                d_names+=[i.dname]
        user1=session['user']
        alltta = admin.query.filter_by(admin_id=user1).all()
        df=pd.DataFrame([( r.username ,r.email)for r in alltta],columns=['username','gmail'])
        print(df)
        gmail=df['gmail'].tolist()
        mail=gmail[0]
        u=df['username'].tolist()
        us=u[0]
        return render_template('admin_add_teacher.html',us=us, allteacher=allteacher, d_names=d_names, allhod =allhod,alldepartment =alldepartment)
 
    return render_template('admin_add_teacher.html',d_names=d_names, allhod =allhod,alldepartment =alldepartment)
        
        
@app.route('/send_email', methods=["GET", "POST"])
def send_email():
    user=session['user']
    a=admin.query.filter_by(admin_id=user).first()
    sender = 'autotimetablegen@gmail.com'
    t=teacher.query.filter_by(admin_id=user).all()
    print(t)
    for i in t:
            
            recipient = i.mail
            print(recipient)
            
            subject = 'AutoPlanify login credential'
            
            link = url_for('home',  _external=True)
            body = f"This email provides you with access to AutoPlanify, a platform where you can view your current timetable and upcoming substitutions.\n\nYour username:{i.username}\nYour password:{i.password}\n\nTo accessAutoPlanify:Visit {link}\n\nEnter your username and password.\n\nClick Sign In and explore your timetable and substitutions.\n\n If you have any questions or encounter difficulties accessing the platform, please do not hesitate to contact {a.email}.\n\n\nSincerely,\nAutoPlanify"

            msg = Message(subject, sender=sender, recipients=[recipient])
            msg.body = body

            mail.send(msg)

    return redirect("/add_teacher") 

@app.route('/teacher_send_email/<int:sno>', methods=["GET", "POST"])
def teacher_send_email(sno):
    user=session['user']
    a=admin.query.filter_by(admin_id=user).first()
    sender = 'autotimetablegen@gmail.com'
    t=teacher.query.filter_by(teacher_id=sno).first()
    
            
    recipient = t.mail
    print(recipient)
    
    subject = 'AutoPlanify login credential'
    
    link = url_for('home',  _external=True)
    body = f"This email provides you with access to AutoPlanify, a platform where you can view your current timetable and upcoming substitutions.\n\nYour username:{t.username}\nYour password:{t.password}\n\nTo access AutoPlanify:Visit {link}\n\nEnter your username and password.\n\nClick Sign In and explore your timetable and substitutions.\n\n If you have any questions or encounter difficulties accessing the platform, please do not hesitate to contact {a.email}.\n\n\nSincerely,\nAutoPlanify"

    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = body

    mail.send(msg)

    return redirect("/add_teacher") 


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        mail = request.form['email']
        user = hod.query.filter_by(mail=mail).first()  # Assuming a User model

        if user:
            serializer = URLSafeTimedSerializer(app.secret_key)
            token = serializer.dumps(user.mail, salt='password-reset')
            reset_link = url_for('reset_password', token=token, _external=True)

            # Send email with reset link (optional)
            if app.config['MAIL_USERNAME']:
                mail = Mail(app)
                msg = Message(' AutoPlanify Password Reset Request',
                              sender=app.config['MAIL_USERNAME'],
                              recipients=[user.mail])
                msg.body = f'Click here to reset your password: {reset_link}'
                mail.send(msg)

            flash ('Password reset link sent!')
        else:
            flash ('Email not found')

    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
        user = hod.query.filter_by(mail=email).first()
    except:
        flash('Invalid or expired token') 

    if request.method == 'POST':
        new_password = request.form['new_password']
        user.password = new_password
        db.session.commit()
        flash( 'Password reset successfully!')
        return redirect("/hod_login")

    return render_template('reset_password.html')


    
@app.route("/hod_login", methods=["GET", "POST"])
def hod_login():
    if g.user is not None:
        flash('ALREADY LOGGED IN', 'alert')
    else:
        if request.method == "POST":
            session.pop("user", None)
            uname = request.form['username']
            passw = request.form["password"]
            remember_me = request.form.get('remember_me')  # Check if "Remember Me" is selected

            login = hod.query.filter_by(username=uname, password=passw).first()
            u = hod.query.filter_by(username=uname).first()
            p = hod.query.filter_by(password=passw).first()

            if u is None and p is None:
                flash("Please enter a valid user", 'error')
            if u is None and p is not None:
                flash("Please enter a valid user", 'error')
            if u is not None and p is None:
                flash("Wrong password", 'error')

            if login is not None:
                session['user'] = login.admin_id
                session['hod'] = login.hod_id

                # Check if "Remember Me" is selected and set a long-lived cookie if true
                if remember_me:
                    session['hod'] = login.hod_id
                    response = make_response(redirect(url_for("hod_profile")))
                    response.set_cookie('remember_hod', str(login.hod_id), max_age=30 * 24 * 60 * 60)  # 30 days
                    return response
                else:
                    return redirect(url_for("hod_profile"))
            else:
                return redirect(url_for('hod_login'))
    return render_template("hod_login.html")

@app.route('/hod_profile')
def hod_profile():
        if g.user:
            
                user=session['user']
                hod_user=session['hod']
                alltta = hod.query.filter_by(hod_id=hod_user).all()
                df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
                print(df)
                gmail=df['mail'].tolist()
                mail=gmail[0]
                u=df['name'].tolist()
                us=u[0]
                o=df['d_id'].tolist()
                id=o[0]
                

                d=department.query.filter_by(d_id=id).all()
                return render_template('hod_profile.html',user=session['user'],mail=mail,us=us,d=d,id=id)
            
            
        
@app.route('/add_class', methods=['GET','POST'])
def add_class():
    if  g.user is  None:
        flash("Login to access")
        return render_template("hod_index.html")

    else:

        if request.method=='POST':
            if not request.form['class']:
                    allclass = classes.query.all()
                    return render_template('hod_add_class.html', allclass=allclass)
            else:
                name=request.form["class"]
                user=session['user']
                hod_id=session['hod']
                h=hod.query.filter_by(hod_id=hod_id).first()
                print('[][][][][][][][][][][][0000000]', hod_id,h.d_id)
                exist = bool(classes.query.filter_by( d_id=h.d_id,cname=name).first())
                if exist is False:
                    c=classes(cname=name,d_id=h.d_id)
                    db.session.add(c)
                    db.session.commit()
                
                
        user=session['user']
        hod_id=session['hod']
        h=hod.query.filter_by(hod_id=hod_id).first()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        hod_user=session['hod']
        allttal = hod.query.filter_by(hod_id=hod_user).all()
        df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in allttal],columns=['name','mail','d_id'])
        print(df)
        gmail=df['mail'].tolist()
        mail=gmail[0]
        u=df['name'].tolist()
        us=u[0]
        
        return render_template('hod_add_class.html',us=us, allclass =allclass)
        
    return render_template('hod_add_class.html')

@app.route('/add_sub', methods=['GET','POST'])
def add_sub():
    if  g.user is  None:
        flash("Login to access")
        return render_template("hod_index.html")

    else:
        if request.method=='POST':
            if not request.form['name']:
                    allassign = assign.query.all()
                    return render_template('hod_add_subject.html', allsub=allsub)
            else:
                name=request.form["name"]
                
                user=session['user']
                hod_id=session['hod']
                h=hod.query.filter_by(hod_id=hod_id).first()
                exist = bool(subjects.query.filter_by( d_id=h.d_id,sname=name).first())
                if exist is False:
                    c=subjects(sname=name,d_id=h.d_id)
                    db.session.add(c)
                    db.session.commit()
        user=session['user']
        hod_id=session['hod']
        h=hod.query.filter_by(hod_id=hod_id).first()
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        hod_user=session['hod']
        alltta = hod.query.filter_by(hod_id=hod_user).all()
        df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
        print(df)
        gmail=df['mail'].tolist()
        mail=gmail[0]
        u=df['name'].tolist()
        us=u[0]
       
        return render_template('hod_add_subject.html',us=us,allsub=allsub)
    return render_template('hod_add_subject.html')

    
        
@app.route('/add_external', methods=['GET','POST'])
def add_external():
    if  g.user is  None:
        flash("Login to access")
        return render_template("hod_index.html")

    else:
       
        if request.method=='POST':
            hod_id=session['hod']
            h=hod.query.filter_by(hod_id=hod_id).first()
            user=session['user']
            hod_id=session['hod']
            name=request.form["teacher"]
            dept=request.form["department"]
            s= subjects.query.filter_by(d_id=h.d_id,sid=request.form["subject"]).first()

            c= classes.query.filter_by(d_id=h.d_id,cid=request.form['cname']).first()
                      
            day=request.form["day"]
            period=request.form["period"]
            
           
            checking=external.query.filter_by(  cid=c.cid, day=day, period=period, d_id=h.d_id).first()
            if(checking is  None):
                
                busy=timetable.query.filter_by(teacher_id=name, day=day, period=period, d_id=dept).first()
                teach=teacher.query.filter_by(teacher_id=name,d_id=dept).first()
                if(busy is  None):
                    busy_c=timetable.query.filter_by(cid=c.cid, day=day, period=period, d_id=h.d_id).first()
                    if(busy_c is  None):
                        allex=external(teacher_id=name,cid=c.cid, sid=s.sid , day=day, period=period,d_id=h.d_id,lort="Theory")
                        db.session.add(allex)
                        db.session.commit()
                        
                        this_ex=external.query.filter_by(teacher_id=name,cid=c.cid, sid=s.sid , day=day, period=period).first()
                        alltt=timetable(teacher_id=name, cid=c.cid, sid=s.sid, day=day, period=period,d_id=h.d_id,lort="Theory",type='ex',exid=this_ex.exid)
                        db.session.add(alltt)
                        db.session.commit()#

                        tt=timetable(teacher_id=name, cid=c.cid, sid=s.sid, day=day, period=period,d_id=dept,lort="Theory",type='ex',exid=this_ex.exid)
                        db.session.add(tt)
                        db.session.commit()
                    else:
                         flash(f'class {c.cname} is busy on that period', 'Error')
                    
                else:
                     flash(f'Teacher {teach.name} is busy on that period', 'Error')
            else:
                 flash('Already alloted')
        hod_id=session['hod']
        h=hod.query.filter_by(hod_id=hod_id).first()   
        
        
        user=session['user']
        allassign= assign.query.filter_by(d_id=h.d_id).all()
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        allTeachers= teacher.query.filter_by().all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        allex=external.query.filter_by(d_id=h.d_id).all()   
        d=department.query.filter_by(admin_id=user).all() 
        d_id=h.d_id
        hod_user=session['hod']
        alltta = hod.query.filter_by(hod_id=hod_user).all()
        df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
        print(df)
        gmail=df['mail'].tolist()
        mail=gmail[0]
        u=df['name'].tolist()
        us=u[0]
        return render_template('hod_external.html',us=us,d_id=hod_id, d=d,allassign= allassign, allsub=allsub ,allex=allex,  allclass = allclass , allTeachers=allTeachers)
    return render_template('other_teacher.html')

@app.route('/get_teachers/<int:department_id>', methods=['GET'])
def get_teachers(department_id):
    teachers = teacher.query.filter_by(d_id=department_id).all()
    teachers_data = [{'teacher_id': t.teacher_id, 'teacher_name': t.name} for t in teachers]
    print('-----------------',teachers_data)
    return jsonify(teachers_data)


@app.route('/lab_assign', methods=['GET','POST'])
def lab_assign_():
    if  g.user is  None:
        
        flash("Login to access")
        return render_template("hod_index.html")

    else:
       
        if request.method=='POST':
            hod_id=session['hod']   
            h=hod.query.filter_by(hod_id=hod_id).first()
            d=hod.query.filter_by(d_id=h.d_id).first()
        
            alert_message='qwqw'
            user=session['user']
            hod_id=session['hod']
            print('name23232323232323232=================',request.form['teacher'])
            t=teacher.query.filter_by(teacher_id=request.form['teacher'],d_id=h.d_id).first()
            s= subjects.query.filter_by(d_id=h.d_id,sid=request.form["subject"]).first()
            c= classes.query.filter_by(d_id=h.d_id,cid=request.form['cname']).first()
                      
            weekc=request.form["weekc"]
            
            check_lab=lab_assign.query.filter_by(teacher_id=t.teacher_id ,d_id=h.d_id).all()
            check_lab_p=lab_assign.query.filter_by(d_id=h.d_id).all()

            if(check_lab_p is not None):
                df_p=pd.DataFrame([(r.weekc)for r in check_lab_p],columns=['weekc'])
                print('00000000',df_p)
                d_p={'weekc':int(weekc)}
                df_p=df_p._append(d_p,ignore_index=True)
                sum=df_p['weekc'].sum()
                print('=========',sum)
                print('=========',df_p)
                if(sum < 26):
                

                    print('check--',check_lab)
                    if(check_lab is not None):
                        df=pd.DataFrame([(r.teacher_id,r.weekc)for r in check_lab],columns=['teacher','weekc'])
                        
                        d={'teacher':request.form['teacher'],'weekc':int(weekc)}
                        df=df._append(d,ignore_index=True)

                        print(df)

                        sum=df['weekc'].sum()
                        print(sum)
                        if(sum < 26):
                            check1= lab_assign.query.filter_by(cid=c.cid ,d_id=h.d_id).all()
                            df=pd.DataFrame([(r.cid,r.weekc)for r in check1],columns=['cname','weekc'])
                            
                            d={'cname':request.form['teacher'],'weekc':int(weekc)}
                            df=df._append(d,ignore_index=True)

                            print(df)

                            sum=df['weekc'].sum()
                            print(sum)
                            if(sum < 26):   


                                ass=lab_assign(teacher_id=t.teacher_id, cid=c.cid, sid=s.sid, weekc=weekc,d_id=h.d_id)
                                db.session.add(ass)
                                db.session.commit()
                            else:
                                flash('Class allocation exceeded (MAX:25)', 'Error')
                            

                            user=session['user']
                            allassign= assign.query.filter_by(d_id=h.d_id).all()
                            allsub= subjects.query.filter_by(d_id=h.d_id).all()
                            allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
                            allclass= classes.query.filter_by(d_id=h.d_id).all()
                            alltta = timetable.query.filter_by(d_id=h.d_id).all()
                            alllab= lab_assign.query.filter_by(d_id=h.d_id).all()
                            teachers_name=[]
                            for a in alltta:
                                if a.teacher_id not in teachers_name:
                                    teachers_name+=[a.teacher_id]
                            
                            
                        
                            return render_template('hod_lab_allotment.html',alllab=alllab,  teachers_name=teachers_name,allassign= allassign, allsub=allsub ,  allclass = allclass , allTeachers=allTeachers)
                                
                        else:
                            flash('Teacher allocation exceeded (MAX:25)', 'Error')
                            

                            user=session['user']
                            allassign= assign.query.filter_by(d_id=h.d_id).all()
                            allsub= subjects.query.filter_by(d_id=h.d_id).all()
                            allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
                            allclass= classes.query.filter_by(d_id=h.d_id).all()
                            alltta = timetable.query.filter_by(d_id=h.d_id).all()
                            alllab= lab_assign.query.filter_by(d_id=h.d_id).all()
                            teachers_name=[]
                            for a in alltta:
                                if a.name not in teachers_name:
                                    teachers_name+=[a.name]
                            
                            
                        
                            return render_template('hod_lab_allotment.html',alllab=alllab,  teachers_name=teachers_name,allassign= allassign, allsub=allsub ,  allclass = allclass , allTeachers=allTeachers)
                    else:
                        ass=lab_assign(teacher_id=t.teacher_id, cid=c.cid, sid=s.sid, weekc=weekc, d_id=h.d_id)
                        db.session.add(ass)
                        db.session.commit()
                else:
                            flash('lab  allocation exceeded (MAX:25)', 'Error')   

            else:
                        ass=lab_assign(teacher_id=t.teacher_id, cid=c.cid, sid=s.sid, weekc=weekc, d_id=h.d_id)
                        db.session.add(ass)
                        db.session.commit()


        hod_id=session['hod']   
        h=hod.query.filter_by(hod_id=hod_id).first()
        user=session['user']
        alllab= lab_assign.query.filter_by(d_id=h.d_id).all()
        allassign= assign.query.filter_by(d_id=h.d_id).all()
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        alltta = timetable.query.filter_by(d_id=h.d_id).all()
        teachers_name=[]
        for a in alltta:
            if a.teacher_id not in teachers_name:
                teachers_name+=[a.teacher_id]
        print('00000000000000000000000000--------------------====',alllab)
        hod_user=session['hod']
        alltta = hod.query.filter_by(hod_id=hod_user).all()
        df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
        print(df)
        gmail=df['mail'].tolist()
        mail=gmail[0]
        u=df['name'].tolist()
        us=u[0]
        return render_template('hod_lab_allotment.html',us=us,alllab=alllab, teachers_name=teachers_name,allassign= allassign, allsub=allsub ,  allclass = allclass , allTeachers=allTeachers)
    return render_template('add_assign.html')


@app.route('/lab_generate', methods=['GET','POST'])
def lab_generate():
    if  g.user is  None:
        flash("login to access")
        return render_template("hod_index.html")

    else:
        solutions=None
        while solutions==None:

            user=session['user']
            hod_id=session['hod']   
            h=hod.query.filter_by(hod_id=hod_id).first()
            ltt = lab_timetable.query.filter_by(d_id=h.d_id).first()
            print(ltt)
            if(ltt is None):  
                
                teachers_name=[]
                class_name=[]
                user=session['user']
                alllab = lab_assign.query.filter_by(d_id=h.d_id).all()
                problem = Problem( MinConflictsSolver()) 
                
                c=lab_assign.query.filter_by(d_id=h.d_id).all()
                df=pd.DataFrame([(r.teacher_id,r.cid,r.sid,r.weekc)for r in c],columns=['teacher','cname','sub','weekc'])
                df["teacher_class"]=df["teacher"].astype(str)+ "_"+ df["cname"].astype(str)
            
                ce=df["cname"].tolist()
                c=[]
            
                
                for j in ce:
                    if j not in c:
                        c.append(j)
                print("-------------------------------------------")
                

                
                    # Define variables (e.g., courses, teachers, classes, and slots)
                days = [1,2,3,4,5]
                    
                classes = c
                time_slots = [1,2,3,4,5]
                
                df1=df

                ex_d={}
                time_table=timetable.query.filter_by(d_id=h.d_id).all()
                ttdf=pd.DataFrame([(r.teacher_id,r.cid,r.sid,r.day,r.period)for r in time_table],columns=['teacher','cname','sub','day','period'])
                ttdf["external"]=ttdf["day"].astype(str)+ "_"+ ttdf["cname"].astype(str)+ "_"+ ttdf["period"].astype(str)
                print()
                print(ttdf)
                external=ttdf['external'].tolist()
                external_slot=[]
                for i in range(0,len(external)):
                    _d=external[i].split("_")[0]
                    if(_d=="mon"):
                                _d="1"
                    elif(_d=="tues"):
                            _d="2"
                    elif(_d=="wed"):
                                _d="3" 
                    elif(_d=="thurs"):
                                _d="4"  
                    else:
                                _d="5"

                    _c=external[i].split("_")[1]
                    _p=external[i].split("_")[2]
                    external_slot+=[f"{_d}_{_p}"]
                    ex_d[f"{_d}_{_p}"]=f"{_c}"
                print(ex_d)
                
                
                print('*******************************************************////////////////////////')
                days=[1,2,3,4,5]
                periods=[1,2,3,4,5]
                per=[]
                perl=[]
                for day in days:
                    for period in periods:
                        if period < 3:  # Exclude the last period (5) for pairs
                            per+=[f"{day}_{period}", f"{day}_{period + 1}"]
                            perl+=[per]
                        elif(period==4):  # Handle the last period (5) separately
                            per+=[f"{day}_{period}", f"{day}_{period + 1}"]
                            perl+=[per]
                        
                        
                        per=[]
                teacher_lab=df1['teacher_class'].tolist()
                var_d={}
                dp=[]
                total = df1['weekc'].sum()
                lab_class=df1['cname'].tolist()
                if total%2==0:
                    total_type='even'
                else:
                    total_type='odd' 
                
                
                flag=False
                while flag==False:
                    
                        random_p= random.choice(perl)
                        if (len(dp)==total-1 and total_type=='odd'):
                            f= random.choice(random_p)
                            
                            
                            if f  not in dp:
                                if (f  in ex_d):
                                    value=ex_d[f]
                                    t_l_f=[i for i in teacher_lab if value not in i]
                                    
                                    if(not t_l_f ):
                                        continue
                                    else:      
                                        dp+=[f]
                                        

                                                
                                        problem.addVariable(f,t_l_f )
                                        

                                                
                                        
                                        var_d[f]=t_l_f
                                        flag=True
                                                
                                else:
                                            dp+=[f]
                                            
                                            teacher_lab=df1['teacher_class'].tolist()
                                            problem.addVariable(f,teacher_lab )
                                            

                                            var_d[f]=teacher_lab
                                            flag=True
                        


                            
                        else:
                            f=random_p[0]
                            s=random_p[1]
                            if f  not in dp and s not in dp:
                                if (f in ex_d):
                                    value1=ex_d[f]
                                    t_l_f=[i for i in teacher_lab if value1 not in i]
                                    if(not t_l_f ):
                                        continue
                                if (s in ex_d):
                                    value2=ex_d[s]
                                    t_l_s=[i for i in teacher_lab if value2 not in i]
                                    if( not t_l_s):
                                        continue
                                    else:      
                                        dp+=[f]
                                        dp+=[s]
                                        print('0000000000000000000000000000')
                                        print(f,s)
                                        print(t_l_f,t_l_s)
                                        print(value1,value2)
                                        print(ex_d[f],ex_d[s])
                                        problem.addVariable(f,t_l_f )
                                        problem.addVariable(s,t_l_s )

                                                
                                        
                                        var_d[f]=t_l_f
                                        var_d[s]=t_l_s
                                        if(len(dp)==total):
                                            flag=True
                                                
                                else:
                                            dp+=[f]
                                            dp+=[s]
                                            teacher_lab=df1['teacher_class'].tolist()
                                            problem.addVariable(f,teacher_lab )
                                            problem.addVariable(s,teacher_lab)

                                            var_d[f]=teacher_lab
                                            var_d[s]=teacher_lab
                                            if(len(dp)==total):
                                                flag=True
                                        
                        
                l=len(teacher_lab)
                for i in range(0,l):
                    
                    row=df1[df1['teacher_class']==teacher_lab[i]]
                    ww=row['weekc'].tolist()
                    w=ww[0]
                    problem.addConstraint(constraint.SomeInSetConstraint([teacher_lab[i]], n=w,exact=True))                                         
                
                for i in range(0,int(len(dp)/2),2):     
                    problem.addConstraint(AllEqualConstraint(), dp[i:i+2])

                

                
    # Create a dictionary to store groups based on starting values
                grouped = {}

                # Iterate through the list
                for item in dp:
                    starting_value = item.split('_')[0]
                    if starting_value not in grouped:
                        grouped[starting_value] = [item]
                    else:
                        grouped[starting_value].append(item)

                # Convert the dictionary values to a list
                result = list(grouped.values())
                class_n=df['cname'].unique()
                distinct_c=class_n.tolist()  

                print('----------------------------------------------')
                for i in range(0,len(result)):
                    distinct_c = [str(item) for item in distinct_c]
                    for i in range(0,len(distinct_c)):
                                    domain= [j for j in teacher_lab if distinct_c[i] in j]
                                    
                                    problem.addConstraint(constraint.SomeInSetConstraint(domain,n=2,exact=False),result[i])
                                    print('d   ',domain)
                                    print('result',result[i])

                    
                    
                
            

                                

                
                
                
                            
                            
                print('ec',ex_d)     
                print('dp',dp)
                solutions = problem.getSolution()
                
            lab_slot=[]
            if (solutions):
                print("Timetable solutions:")
                
                for s in solutions:
                    
                    
                    k=s
                    d=k.split("_")[0]
                    p=k.split("_")[1]
                    if(d=="1"):
                        day="mon"
                    elif(d=="2"):
                        day="tues"
                    elif(d=="3"):
                        day="wed" 
                    elif(d=="4"):
                        day="thurs"  
                    else:
                        day="fri"
                    
                    k=solutions[s]
                    teach=k.split("_")[0]
                    c=k.split("_")[1]
                    
                    lab_a=lab_assign.query.filter_by(d_id=h.d_id).all()
                    df=pd.DataFrame([(r.teacher_id,r.cid,r.sid,r.weekc)for r in lab_a],columns=['teacher','cname','sub','weekc'])
                    cn=df[df["cname"]==int(c)]
                    
                    lab_slot+=[f"{d}_{c}_{p}"]
                    ctrow=cn[cn["teacher"]==int(teach)]
                    sb=ctrow['sub'].tolist()
                    sub1=sb[0]
                    
                        
                    check=lab_timetable.query.filter_by( cid=c, day=day, period=int(p),  d_id=h.d_id).first()
                    if(check is None):
                            
                            lab_tt=lab_timetable(teacher_id=teach, cid=c, sid=sub1, day=day, period=int(p), d_id=h.d_id)
                            db.session.add(lab_tt)
                            db.session.commit()
                            
                            tt=timetable(teacher_id=teach, cid=c, sid=sub1, day=day, period=int(p), lort="lab",type='out', d_id=h.d_id)
                            db.session.add(tt)
                            db.session.commit()
                        
                    
            
                                                                
            
                schedules = lab_timetable.query.filter_by(d_id=h.d_id).all()
                day=['mon','tues','wed','thurs','fri']
                for d in day:
                    for p in range(1, 6):  # Loop through days (1-5)
                          # Start with all periods available
                        s = timetable.query.filter_by(day=d, period=p, d_id=h.d_id).first()
                        
                        if s  is  None:
                            lab = lab_avail( period=p, day=d, d_id=h.d_id)
                            db.session.add(lab)
                            db.session.commit()




                    
            else:
                    print("No solutions found.")
            
        else: 
             flash('Already Generated')      


       
        return redirect(url_for('lab_show'))
    return redirect(url_for('login'))




@app.route('/lab_show')
def lab_show():
    if  g.user is  None:
        flash("Loginin to access")
        return render_template("hod_login.html")

    else:
        user=session['user']
        hod_id=session['hod']   
        h=hod.query.filter_by(hod_id=hod_id).first()
        alltt = lab_timetable.query.filter_by(d_id=h.d_id).all()
        days=["mon","tues","wed","thurs","fri"]
        teachers_name=[]
        for a in alltt:
            if a.teacher_id not in teachers_name:
                teachers_name+=[a.teacher_id]

        
        alltta = lab_timetable.query.filter_by(d_id=h.d_id).all()
        class_name=[]
        for a in alltta:
            if a.cid not in class_name:
                class_name+=[a.cid]
 
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        hod_user=session['hod']
        alltta = hod.query.filter_by(hod_id=hod_user).all()
        df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
        print(df)
        gmail=df['mail'].tolist()
        mail=gmail[0]
        u=df['name'].tolist()
        us=u[0]
       

    
        return render_template('hod_lab_timetable.html',us=us,class_name=class_name,teachers_name=teachers_name,days=days, alltt=alltt, allsub=allsub, allTeachers=allTeachers ,allclass=allclass )
    return render_template('lab_show.html')


    
    return redirect("/lab_show")



@app.route('/add_assign', methods=['GET','POST'])
def add_assign():
    if  g.user is  None:
        
        flash("login to access")
        return render_template("hod_index.html")

    else:
       
        if request.method=='POST':
            
            user=session['user']
            hod_id=session['hod']   
            h=hod.query.filter_by(hod_id=hod_id).first()
            allsub= subjects.query.filter_by(d_id=h.d_id).all()
            t=teacher.query.filter_by(d_id=h.d_id,teacher_id=request.form["teacher"]).first()
            
            c=classes.query.filter_by(d_id=h.d_id,cid=request.form['cname']).first()
            
            s=subjects.query.filter_by(d_id=h.d_id,sid=request.form["subject"]).first()
            weekc=request.form["weekc"]
            print('12121212------------',request.form["subject"])
            check= assign.query.filter_by(teacher_id=t.teacher_id ,d_id=h.d_id).all()
            print(check)
            df=pd.DataFrame([(r.teacher_id,r.weekc)for r in check],columns=['teacher','weekc'])
            
            check_lab= lab_assign.query.filter_by(teacher_id=t.teacher_id ,d_id=h.d_id).all()
            
            lab_df=pd.DataFrame([(r.teacher_id,r.weekc)for r in check_lab],columns=['teacher','weekc'])
            df=pd.concat([df, lab_df], ignore_index=True)
            print()
            print('assifgn_df')
            print(df)
            d={'teacher':t.teacher_id,'weekc':int(weekc)}
            df=df._append(d,ignore_index=True)

            print(df)

            sum=df['weekc'].sum()
            print(sum)
            t_name= teacher.query.filter_by(teacher_id=t.teacher_id ,d_id=h.d_id).first()
            if(sum < 26):
                check1= assign.query.filter_by(cid=c.cid ,d_id=h.d_id).all()
                df1=pd.DataFrame([(r.cid,r.weekc,r.teacher_id)for r in check1],columns=['cname','weekc','teacher'])
                
                check_class_lab= lab_assign.query.filter_by(cid=c.cid ,d_id=h.d_id).all()
                df_class_lab=pd.DataFrame([(r.cid,r.weekc,r.teacher_id)for r in check_class_lab],columns=['cname','weekc','teacher'])
                
                check_ex_lab= external.query.filter_by(cid=c.cid ,d_id=h.d_id).all()
                df_ex_lab=pd.DataFrame([(r.cid,1,'ex')for r in check_ex_lab],columns=['cname','weekc','teacher'])

                df1=pd.concat([df1, df_class_lab], ignore_index=True)
                df1=pd.concat([df1, df_ex_lab], ignore_index=True)

                print()
                print('assifgn_class_df')
                sum=df1['weekc'].sum()
                print('calss week',sum)
                print(df1)


                d={'cname':c.cid,'weekc':int(weekc)}
                df1=df1._append(d,ignore_index=True)


                
                print(df1)

                sum=df1['weekc'].sum()
                print('calss week',sum)
                df1=[]
                c_name= classes.query.filter_by(cid=c.cid ,d_id=h.d_id).first()
                if(sum < 26):   


                    ass=assign(teacher_id=t.teacher_id, cid=c.cid, sid=s.sid, weekc=weekc, d_id=h.d_id)
                    db.session.add(ass)
                    db.session.commit()
                else:
                     flash(f'Class {c_name.cname} allocation exceeded (MAX:25)', 'Error')
                

                user=session['user']
                alllab=lab_assign.query.filter_by(d_id=h.d_id).all()
                allex=external.query.filter_by(d_id=h.d_id).all()
        
                allassign= assign.query.filter_by(d_id=h.d_id).all()
                allsub= subjects.query.filter_by(d_id=h.d_id).all()
                allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
                allclass= classes.query.filter_by(d_id=h.d_id).all()
                alltta = timetable.query.filter_by(d_id=h.d_id).all()
                teachers_name=[]
                for a in alltta:
                    if a.teacher_id not in teachers_name:
                        teachers_name+=[a.teacher_id]
                hod_user=session['hod']
                alltta = hod.query.filter_by(hod_id=hod_user).all()
                df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
                print(df)
                gmail=df['mail'].tolist()
                mail=gmail[0]
                u=df['name'].tolist()
                us=u[0]
                
            
                return render_template('hod_assign.html',us=us,alllab=alllab,allex=allex,  teachers_name=teachers_name,allassign= allassign, allsub=allsub ,  allclass = allclass , allTeachers=allTeachers)
                     
            else:
                flash(f'Teacher {t_name.name} allocation exceeded (MAX:25)', 'Error')
                
                hod_id=session['hod']   
                h=hod.query.filter_by(hod_id=hod_id).first()
                user=session['user']
                alllab=lab_assign.query.filter_by(d_id=h.d_id).all()
                allex=external.query.filter_by(d_id=h.d_id).all()
        
                allassign= assign.query.filter_by(d_id=h.d_id).all()
                allsub= subjects.query.filter_by(d_id=h.d_id).all()
                allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
                allclass= classes.query.filter_by(d_id=h.d_id).all()
                alltta = timetable.query.filter_by(d_id=h.d_id).all()
                teachers_name=[]
                for a in alltta:
                    if a.teacher_id not in teachers_name:
                        teachers_name+=[a.teacher_id]
                hod_user=session['hod']
                alltta = hod.query.filter_by(hod_id=hod_user).all()
                df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
                print(df)
                gmail=df['mail'].tolist()
                mail=gmail[0]
                u=df['name'].tolist()
                us=u[0]
                
            
                return render_template('hod_assign.html',us=us,alllab=alllab,allex=allex,  teachers_name=teachers_name,allassign= allassign, allsub=allsub ,  allclass = allclass , allTeachers=allTeachers)

        hod_id=session['hod']   
        h=hod.query.filter_by(hod_id=hod_id).first()    
        user=session['user']
        ad=admin.query.filter_by(admin_id=user).first() 
        alllab=lab_assign.query.filter_by(d_id=h.d_id).all()
        allex=external.query.filter_by(d_id=h.d_id).all()
        
        allassign= assign.query.filter_by(d_id=h.d_id).all()
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
        whole_Teachers= teacher.query.filter_by().all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        alltta = timetable.query.filter_by(d_id=h.d_id).all()
        teachers_name=[]
        for a in alltta:
            if a.teacher_id not in teachers_name:
                teachers_name+=[a.teacher_id]
        hod_user=session['hod']
        alltta = hod.query.filter_by(hod_id=hod_user).all()
        df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
        print(df)
        gmail=df['mail'].tolist()
        mail=gmail[0]
        u=df['name'].tolist()
        us=u[0]
        return render_template('hod_assign.html',whole_Teachers=whole_Teachers,us=us,alllab=alllab,allex=allex, teachers_name=teachers_name,allassign= allassign, allsub=allsub ,  allclass = allclass , allTeachers=allTeachers)
    return render_template('hod_assign.html')


@app.route('/generate', methods=['GET','POST'])
def generate():
    if  g.user is  None:
        flash("login to access")
        return render_template("hod_index.html")

    else:
        
        hod_id=session['hod']   
        h=hod.query.filter_by(hod_id=hod_id).first() 
        teachers_name=[]
        class_name=[]
        user=session['user']
        allassign = assign.query.filter_by(d_id=h.d_id).all()
        problem = Problem( MinConflictsSolver()) 
        #c=pd.read_csv(r"C:\Users\ASUS\Pictures\extime\assign5.csv")
        c=assign.query.filter_by(d_id=h.d_id).all()
        df=pd.DataFrame([(r.teacher_id,r.cid,r.sid,r.weekc)for r in c],columns=['teacher','cname','sub','weekc'])
        #df=df[df["user"]==user]
    
        ce=df["cname"].tolist()
        c=[]
       
        
        for j in ce:
            if j not in c:
                c.append(j)
        print("-------------------------------------------")
        

        
            # Define variables (e.g., courses, teachers, classes, and slots)
        days = [1,2,3,4,5]
            
        classes = c
        time_slots = [1,2,3,4,5]
           

        time_table=timetable.query.filter_by(d_id=h.d_id).all()
        ttdf=pd.DataFrame([(r.teacher_id,r.cid,r.sid,r.day,r.period)for r in time_table],columns=['teacher','cname','sub','day','period'])
        ttdf["external"]=ttdf["day"].astype(str)+ "_"+ ttdf["cname"].astype(str)+ "_"+ ttdf["period"].astype(str)
        print()
        print(ttdf)
        external=ttdf['external'].tolist()
        external_slot=[]
        for i in range(0,len(external)):
            _d=external[i].split("_")[0]
            if(_d=="mon"):
                        _d="1"
            elif(_d=="tues"):
                       _d="2"
            elif(_d=="wed"):
                        _d="3" 
            elif(_d=="thurs"):
                        _d="4"  
            else:
                        _d="5"

            _c=external[i].split("_")[1]
            _p=external[i].split("_")[2]
            external_slot+=[f"{_d}_{_c}_{_p}"]
        print(external_slot)




        lab_time_table=lab_timetable.query.filter_by(d_id=h.d_id).all()
        lttdf=pd.DataFrame([(r.teacher_id,r.cid,r.sid,r.day,r.period)for r in lab_time_table],columns=['teacher','cname','sub','day','period'])
        lttdf["lab_external"]=lttdf["day"].astype(str)+ "_"+ lttdf["cname"].astype(str)+ "_"+ lttdf["period"].astype(str)
        print()
        print(lttdf)
        lab_external=lttdf['lab_external'].tolist()
        l={}
        
        grouped_df = lttdf.groupby('teacher')['lab_external'].agg(list).reset_index()

        # Convert the grouped DataFrame to a dictionary
        l = dict(zip(grouped_df['teacher'], grouped_df['lab_external']))
        l_t={}
        day_mapping = {'mon': 1, 'tues': 2, 'wed': 3, 'thurs': 4, 'fri': 5}

        for key, values in l.items():
            l_t[key] = [f"{day_mapping[value.split('_')[0]]}_{int(value.split('_')[1])}_{int(value.split('_')[2])}" for value in values]
        print('~~~~~~~~~~~~~~~~~~~~~~~###########~~~~~~~~~~',l_t)
        for i in range(0,len(lab_external)):
            _d=lab_external[i].split("_")[0]
            if(_d=="mon"):
                        _d="1"
            elif(_d=="tues"):
                       _d="2"
            elif(_d=="wed"):
                        _d="3" 
            elif(_d=="thurs"):
                        _d="4"  
            else:
                        _d="5"

            _c=lab_external[i].split("_")[1]
            _p=lab_external[i].split("_")[2]
            external_slot+=[f"{_d}_{_c}_{_p}"]
        print(external_slot)

             




            # Assign variables and their domains
        domains={}
        for day in days:
                for class_ in classes:
                    cc=df[df["cname"]==class_]
                    
                    for slot in time_slots:
                        add_v=f"{day}_{class_}_{slot}"
                        t=cc['teacher'].tolist()
                        result_keys = [key for key, values in l_t.items() if any(int(val.split('_')[0]) == day and int(val.split('_')[2]) == slot for val in values)]
                        filtered_t = [x for x in t if x not in result_keys]
                        if(add_v in external_slot ):
                             continue
                        else:
                            problem.addVariable(f"{day}_{class_}_{slot}", filtered_t)
                            print(add_v)
                            domains[f"{day}_{class_}_{slot}"]=filtered_t
            # Ensure that each class has four slots, each slot is filled with a subject,
            # and each subject has a teacher assigned
            
        for day in days:
                    subject_vars =[]
                    
                    for class_ in classes:
                                sub_v=f"{day}_{class_}_1"
                                if(sub_v in external_slot):
                                     continue
                                else:
                                    subject_vars += [f"{day}_{class_}_1" ]
                                    
                                    problem.addConstraint(AllDifferentConstraint(), subject_vars)
        print('1')
        print(subject_vars)
        for day in days:
                    subject_vars =[]
                    
                    for class_ in classes:
                                
                                sub_v=f"{day}_{class_}_2"
                                if(sub_v in external_slot):
                                     continue
                                else:
                        #
                                    subject_vars += [f"{day}_{class_}_2" ]
                                    
                                    problem.addConstraint(AllDifferentConstraint(), subject_vars)

        print('1')
        print(subject_vars)
        for day in days:
                    subject_vars =[]
                    
                    for class_ in classes:
                        #
                                sub_v=f"{day}_{class_}_3"
                                if(sub_v in external_slot):
                                     continue
                                else:
                                    subject_vars += [f"{day}_{class_}_3" ]
                                    
                                    problem.addConstraint(AllDifferentConstraint(), subject_vars)
        print('1')
        print(subject_vars)

        for day in days:
                    subject_vars =[]
                    
                    for class_ in classes:
                        #
                                sub_v=f"{day}_{class_}_4"
                                if(sub_v in external_slot):
                                     continue
                                else:
                                    subject_vars += [f"{day}_{class_}_4" ]
                                    
                                    problem.addConstraint(AllDifferentConstraint(), subject_vars)
        print('1')
        print(subject_vars)

        for day in days:
                    subject_vars =[]
                    
                    for class_ in classes:
                                sub_v=f"{day}_{class_}_5"
                                if(sub_v in external_slot):
                                     continue
                                else:
                        
                                    subject_vars += [f"{day}_{class_}_5" ]
                                    
                                    problem.addConstraint(AllDifferentConstraint(), subject_vars)
        periods=[1,2,3,4,5]



        for class_ in classes:
                    subject_vars =[]
                    cc=df[df["cname"]==class_]
                    t=cc['teacher'].tolist()
                    for p in periods:
                                sub_v=f"1_{class_}_{p}"
                                if(sub_v in external_slot):
                                     continue
                                else:
                                    subject_vars += [f"1_{class_}_{p}" ]
                    for i in range(0,len(t)):               
                        #problem.addConstraint(constraint.SomeInSetConstraint([t], n=2,exact=False),(subject_vars))
                        print()
                        print(t[i],subject_vars)
        
        for class_ in classes:
                    
                    cc=df[df["cname"]==class_]
                    t=cc['teacher'].tolist()
                    l=len(t)
                    
                    for i in range(0,l):
                        var=[]
                        tc=cc["teacher"]
                        trow=cc[cc["teacher"]==t[i]]
                        ww=trow["weekc"].tolist() 
                        w=ww[0] 
                        
                        for day in days: 
                            
                            for slot in time_slots:
                                sub_v=f"{day}_{class_}_{slot}"
                                if(sub_v in external_slot):
                                     continue
                                else:
                                
                                    var+=[f"{day}_{class_}_{slot}"]
                                    if((day==5) & (slot==5)):
                                        
                                        problem.addConstraint(constraint.SomeInSetConstraint([t[i]], n=w,exact=True),(var))                                         
                                        
                                                          
        

        
            # Add any additional constraints (e.g., specific course-teacher, teacher availability)

            # Solve the CSP
        solutions = problem.getSolution()
            
        

    
        
        user=session['user']
        if solutions:
            print("Timetable solutions:")
            
            for s in solutions:
                k=s
                d=k.split("_")[0]
                class_=k.split("_")[1]
                p=k.split("_")[2]
                if(d=="1"):
                     day="mon"
                elif(d=="2"):
                     day="tues"
                elif(d=="3"):
                     day="wed" 
                elif(d=="4"):
                     day="thurs"  
                else:
                     day="fri"
                tl=solutions[s]
                cn=df[df["cname"]==int(class_)]
                ctrow=cn[cn["teacher"]==solutions[s]]
                sb=ctrow["sub"].tolist()
                
                #lt=ctrow["lort"].tolist()
                #lort=lt[0]
                sb1=sb[0]
                sol=solutions[s]
                
                
                check=timetable.query.filter_by( cid=class_, day=day, period=int(p),  d_id=h.d_id).first()
                if(check is None):
                    
                    tt=timetable(teacher_id=tl, cid=class_, sid=sb1, day=day, period=int(p), lort='Theory',type='in', d_id=h.d_id)
                    db.session.add(tt)
                    db.session.commit()
            

            
                   

            teachers = teacher.query.filter_by(d_id=h.d_id).all()
            
            flash('TimeTable Generated','success')
                                                                
            for t in teachers:
                schedules = timetable.query.filter_by(teacher_id=teacher.teacher_id, d_id=h.d_id).all()
                day=['mon','tues','wed','thurs','fri']
                for d in day:
                    for p in range(1, 6):  # Loop through days (1-5)
                          # Start with all periods available
                        s = timetable.query.filter_by(teacher_id=t.teacher_id,day=d,period=p, d_id=h.d_id).first()
                        
                        if s  is  None:
                            teacher_avail = Teacher_avail(teacher_id=t.teacher_id, period=p, day=d,d_id=h.d_id)
                            db.session.add(teacher_avail)
                            db.session.commit()
                            

        else:
            print("No solutions found.")
            flash("TimeTable Not Generated,TRY AGAIN",'error')
            

        return redirect(url_for('hod_show'))
    return redirect(url_for('login'))


@app.route('/hod_show')
def hod_show():
    if  g.user is  None:
        flash("login to access")
        return render_template("hod_index.html")

    else:
        hod_id=session['hod']   
        h=hod.query.filter_by(hod_id=hod_id).first()
        user=session['user']
        alltt = timetable.query.filter_by(d_id=h.d_id).all()
        days=["mon","tues","wed","thurs","fri"]
        teachers_name=[]
        for a in alltt:
            if a.teacher_id not in teachers_name:
                teachers_name+=[a.teacher_id]

        allex=external.query.filter_by(d_id=h.d_id).all() 
        for e in allex:
            if e.teacher_id not in teachers_name:
                teachers_name+=[e.teacher_id]
        alltta = timetable.query.filter_by(d_id=h.d_id).all()
        class_name=[]
        for a in alltta:
            if a.cid not in class_name:
                class_name+=[a.cid]
        
        
        
        allsub= subjects.query.filter_by().all()
        allTeachers= teacher.query.filter_by().all()
        allclass= classes.query.filter_by().all()
        #alltime = Time_slot.query.filter_by(d_id=h.d_id).all()
        hod_user=session['hod']
        alltta = hod.query.filter_by(hod_id=hod_user).all()
        df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
        print(df)
        gmail=df['mail'].tolist()
        mail=gmail[0]
        u=df['name'].tolist()
        us=u[0]

    
        return render_template('hod_show.html',us=us,class_name=class_name,teachers_name=teachers_name,days=days, alltt=alltt, allsub=allsub, allTeachers=allTeachers ,allclass=allclass )
    return render_template('show.html')


@app.route('/hod_teacher_timetable/<t>')
def hod_teacher_timetable(t):
    if  g.user is  None:
        
        return render_template("register.html")

    else:
        hod_id=session['hod']   
        h=hod.query.filter_by(hod_id=hod_id).first()
        user=session['user']
        alltt = timetable.query.filter_by(d_id=h.d_id,teacher_id=t).all()
        days=["mon","tues","wed","thurs","fri"]
        t=t  
        user=session['user']
        alltta = timetable.query.filter_by(d_id=h.d_id).all()
        teachers_name=[]
        for a in alltta:
            if a.teacher_id not in teachers_name:
                teachers_name+=[a.teacher_id] 
        allex=external.query.filter_by(d_id=h.d_id).all() 
        for e in allex:
            if e.teacher_id not in teachers_name:
                teachers_name+=[e.teacher_id]
        class_name=[]
        for a in alltt:
            if a.cid not in class_name:
                class_name+=[a.cid]
        subjects_name=[]
        for a in alltt:
            if a.sid not in subjects_name:
                subjects_name+=[a.sid]
        
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        allTeachers= teacher.query.filter_by().all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        at= teacher.query.filter_by(teacher_id=t,d_id=h.d_id).first()
        
        if(external.query.filter_by(teacher_id=t).first()):
            ex=teacher.query.filter_by(teacher_id=t).first()
            tname=ex.name
        else:
            tname=at.name
        hod_user=session['hod']
        alltta = hod.query.filter_by(hod_id=hod_user).all()
        df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
        print(df)
        gmail=df['mail'].tolist()
        mail=gmail[0]
        u=df['name'].tolist()
        us=u[0]
        return render_template('hod_teacher_timetable.html',us=us,tname=tname,subjects_name=subjects_name,class_name=class_name,t=t,teachers_name=teachers_name, alltt=alltt,days=days,allsub=allsub, allTeachers=allTeachers ,allclass=allclass)
    #return render_template('teacher_timetable.html')
   


@app.route('/hod_class_timetable/<c>')
def hod_class_timetable(c):
    if  g.user is  None:
        flash("Sign in to access")
        return render_template("register.html")

    else:
        hod_id=session['hod']   
        h=hod.query.filter_by(hod_id=hod_id).first()
        user=session['user']
        alltt = timetable.query.filter_by(d_id=h.d_id,cid=c).all()
        days=["mon","tues","wed","thurs","fri"]
        c=c  
        user=session['user']
        alltta = timetable.query.filter_by(d_id=h.d_id).all()
        class_name=[]
        teachers_name=[]
        subjects_name=[]
        for a in alltta:
            if a.cid not in class_name:
                class_name+=[a.cid]
        for a in alltta:
            if a.teacher_id not in teachers_name:
                teachers_name+=[a.teacher_id] 
        allex=external.query.filter_by(d_id=h.d_id).all() 
        for e in allex:
            if e.teacher_id not in teachers_name:
                teachers_name+=[e.teacher_id]
        for a in alltt:
            if a.sid not in subjects_name:
                subjects_name+=[a.sid]
        ac= classes.query.filter_by(d_id=h.d_id,cid=c).first()
        name=ac.cname
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        allTeachers= teacher.query.filter_by().all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        hod_user=session['hod']
        alltta = hod.query.filter_by(hod_id=hod_user).all()
        df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
        print(df)
        gmail=df['mail'].tolist()
        mail=gmail[0]
        u=df['name'].tolist()
        us=u[0]

    
        return render_template('hod_class_timetable.html',us=us,subjects_name=subjects_name,c=c,class_name=class_name, alltt=alltt,days=days,allsub=allsub, allTeachers=allTeachers ,allclass=allclass,name=name)
    return render_template('hod_class_timetable.html')


@app.route('/hod_add_substitution', methods=['GET','POST'])
def hod_add_substitution():
    if  g.user is  None:
        flash("Login to access")
        return render_template("hod_index.html")
    else:

        if request.method=='POST':
                user=session['user']
                hod_id=session['hod']
                h=hod.query.filter_by(hod_id=hod_id).first()
                id=request.form['teacher']
                date=request.form["date"]
                if isinstance(date, str):
                    # Convert the string to a datetime.date object
                    date = datetime.strptime(date, '%Y-%m-%d').date()
                day=datetime.strftime(date, '%A')
                if day == 'Monday':
                    day= 'mon'
                elif day == 'Tuesday':
                    day ='tues'
                elif day == 'Wednesday':
                    day = 'wed'
                elif day == 'Thursday':
                    day = 'thurs'
                elif day == 'Friday':
                    day = 'fri'
                selected=teacher.query.filter_by(teacher_id=id,d_id=h.d_id).first()
                select_teacher=selected.name
                table=timetable.query.filter_by(teacher_id=id,day=day,d_id=h.d_id).all()
                that_day=absent_teacher.query.filter_by(teacher_id=id,date=date,d_id=h.d_id).first()
                if (that_day is None):
                    absent_class=[]
                    for a in table:
                        if a.cid not in absent_class:
                            absent_class+=[a.cid]
                    
                    flag=1
                    b=substitution.query.filter_by(teacher_id=id,date=date,d_id=h.d_id).all()
                    if (len(absent_class)==0 & len(b)!=0):
                            flash(f'No class for  {select_teacher} on {date},{day} !','Error')
                    elif(len(b)!=0):
                            br="<br>"
                            flash(f'Substitution class for {select_teacher}  on {date},{day} ! TRY DELETING THE SUBSTITUTION FOR THAT DAY AND TRY AGAIN','Error')
                    elif (len(absent_class)==0):
                        flash(f'No class for {select_teacher} on {date},{day} !','Error')
                        flag=0
                    if flag!=0:
                        insert=absent_teacher(teacher_id=id , date=date, d_id=h.d_id)
                        db.session.add(insert)
                        db.session.commit()
                        t_checking=Teacher_free.query.filter_by(date=date,d_id=h.d_id).all()
                        if len(t_checking) ==0:
                            copy=Teacher_avail.query.filter_by(day=day,d_id=h.d_id).all()
                            for i in copy:
                                num=i.teacher_id
                                if (int(num)!=int(id)):
                                        print(num,id)
                                        insert=Teacher_free(teacher_id=i.teacher_id , period=i.period , date=date, d_id=h.d_id)
                                        db.session.add(insert)
                                        db.session.commit()
                                if(int(num)==int(id)):
                                        this_insert=Teacher_free_store(teacher_id=i.teacher_id , period=i.period , date=date, d_id=h.d_id)
                                        db.session.add(this_insert)
                                        db.session.commit()
                        else:
                            dlt=Teacher_free.query.filter_by(teacher_id=id, date=date,d_id=h.d_id).first()  
                            while dlt is not None:
                                       
                                        insert=Teacher_free_store(teacher_id=dlt.teacher_id,date=date,period=dlt.period,d_id=h.d_id)
                                        db.session.add(insert)
                                        db.session.commit()
                                        print("insert:",insert)
                                        print("dlt",dlt)
                                        db.session.delete(dlt)
                                        db.session.commit()
                                        dlt=Teacher_free.query.filter_by(teacher_id=id, date=date,d_id=h.d_id).first()  
                                        
                        l_checking=lab_timetable.query.filter_by(d_id=h.d_id).first()
                        if(l_checking is not None):
                            l_checking2=lab_free.query.filter_by(date=date,d_id=h.d_id).all()
                            if len(l_checking2) ==0:
                                l_avail=lab_avail.query.filter_by(day=day,d_id=h.d_id).all()
                            
                                for i in l_avail:
                                    
                                    insert=lab_free(period=i.period , date=date, d_id=h.d_id)
                                    db.session.add(insert)
                                    db.session.commit()
                                    
                                    
                                    
                else:
                     flash(f'Already noted the absent for {select_teacher}  on {date},{day} !','Error')

        user=session['user']
        hod_id=session['hod']
        h=hod.query.filter_by(hod_id=hod_id).first()
        substitute= substitution.query.filter_by(d_id=h.d_id).all()
            
        allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        alltta = timetable.query.filter_by(d_id=h.d_id).all()
        teachers_name=[]
        for a in alltta:
                if a.teacher_id not in teachers_name:
                    teachers_name+=[a.teacher_id]
        absent_teachers=absent_teacher.query.filter_by(d_id=h.d_id).all()
        hod_user=session['hod']
        alltta = hod.query.filter_by(hod_id=hod_user).all()
        df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
        print(df)
        gmail=df['mail'].tolist()
        mail=gmail[0]
        u=df['name'].tolist()
        us=u[0]
        ss=substitution.query.filter_by(d_id=h.d_id).all()
        substi=[]
        for a in ss:
                if a.date not in substi:
                    substi+=[a.date]
        
        return render_template('hod_substitution.html',substi=substi,us=us,absent_teacher=absent_teachers ,substitute=substitute,teachers_name=teachers_name,allTeachers=allTeachers, allclass =allclass)
        
    return render_template('hod_substitut.html')



@app.route('/hod_substitution_generate')
def hod_substitution_generate():
    if  g.user is  None:
        flash("Login to access")
        return render_template("hod_index.html")

    else:

          
            user=session['user']
            hod_id=session['hod']
            h=hod.query.filter_by(hod_id=hod_id).first()
            
            absent_staff=[]
            row=absent_teacher.query.filter_by(d_id=h.d_id).all()
            for a in row:
                
                if a.teacher_id not in absent_staff:
                            absent_staff+=[a.teacher_id]
                
            print('absent_staff',absent_staff)
            for r in row: 
                id=r.teacher_id
                date=r.date
                if isinstance(date, str):
                    # Convert the string to a datetime.date object
                    date = datetime.strptime(date, '%Y-%m-%d').date()
                day=datetime.strftime(date, '%A')
                if day == 'Monday':
                    day= 'mon'
                elif day == 'Tuesday':
                    day ='tues'
                elif day == 'Wednesday':
                    day = 'wed'
                elif day == 'Thursday':
                    day = 'thurs'
                elif day == 'Friday':
                    day = 'fri'
                checking_flag=True
                print('qqqqqqqq',day)
                user=session['user']
                hod_id=session['hod']
                h=hod.query.filter_by(hod_id=hod_id).first()
            
                table=timetable.query.filter_by(teacher_id=id,day=day,d_id=h.d_id).all()
                print(table)
                absent_class=[]
                
                for a in table:
                    if a.cid not in absent_class:
                
                       absent_class+=[a.cid]
                    
                flag=True 

                selected=teacher.query.filter_by(teacher_id=id,d_id=h.d_id).first()
                select_teacher=selected.name
                q=True
                if q==True:
                    b=substitution.query.filter_by(teacher_id=id,date=date,d_id=h.d_id).all()
                    if (len(absent_class)==0 & len(b)!=0):
                        flash(f'No class for  {select_teacher} on {date},{day} !','Error')
                    elif(len(b)!=0):
                        br="<br>"
                        flash(f'Substitution class for {select_teacher}  on {date},{day} ! TRY DELETING THE SUBSTITUTION FOR THAT DAY AND TRY AGAIN','Error')
                        

                        flag=False
                    elif (len(absent_class)==0):
                        flash(f'No class for {select_teacher} on {date},{day} !','Error')
                    if flag!=False:     
                        substitute_t=[]
                        
                        print('absent_class',absent_class) 
                        print('substitute_t',substitute_t) 
                        absent_p=[]
                        
                        for a in table:
                            if a.period not in absent_p:
                                absent_p+=[a.period]

                        
                       
                        for i in absent_p:
                                substitute_t=[]
                                that_p=timetable.query.filter_by(teacher_id=id,period=i, day=day,d_id=h.d_id).first()
                                that_c=that_p.cid
                                teacher_table=timetable.query.filter_by(cid=that_c,d_id=h.d_id).all()
                                for a in teacher_table:
                                    if a.teacher_id not in substitute_t:
                                        substitute_t+=[a.teacher_id]


                                CHECKING=substitution.query.filter_by(original_teacher_id=id,period=i, date=date,d_id=h.d_id).all()
                                if len(CHECKING)!=0:
                                    flash(f'Already substituted for {date},{day} !','Error')
                                    checking_flag=False
                                    break
                                if checking_flag==True:    
                                    l_checking=lab_free.query.filter_by(period=i,date=date,d_id=h.d_id).all()

                                    All_avail=Teacher_free.query.filter_by(date=date,period=i,d_id=h.d_id).all()
                                    print('All_avail',All_avail)
                                    all_substitute_t=[]
                                    for a in All_avail:
                                        if a.teacher_id not in all_substitute_t:
                                            all_substitute_t+=[a.teacher_id]
                                        
                                    real_substitute=[ item for item in substitute_t if item in all_substitute_t ]
                                    check_count=[]
                                    for r in real_substitute:
                                        check=Teacher_free.query.filter_by(teacher_id=r,date=date,d_id=h.d_id).all()
                                        check_count+=[len(check)]
                                    sub_teacher=None
                                    if check_count:
                                        max_count=max(check_count) 
                                        for j in range(0,len(check_count)):
                                            if max_count==check_count[j]:
                                                sub_teacher=real_substitute[j]
                                                break
                                    l_checkings=lab_free.query.filter_by(period=i,date=date,d_id=h.d_id).all()
                                    if sub_teacher:
                                        absent_period=timetable.query.filter_by(teacher_id=id,period=i,day=day,d_id=h.d_id).first()
                                        coming_teacher=timetable.query.filter_by(teacher_id=sub_teacher,cid=absent_period.cid,d_id=h.d_id).first()
                                        substituting=substitution(teacher_id=sub_teacher, original_teacher_id=id,cid=absent_period.cid , sid=coming_teacher.sid, lort='Thoery' , day=day, period=i,date=date, d_id=h.d_id)
                                        db.session.add(substituting)
                                        db.session.commit()
                                        avail_update=Teacher_free.query.filter_by(teacher_id=sub_teacher,date=date,period=i,d_id=h.d_id).first()
                                        if avail_update:
                                            insert=Teacher_free_store(teacher_id=sub_teacher,date=date,period=i,d_id=h.d_id)
                                            db.session.add(insert)
                                            db.session.commit()
                                            db.session.delete(avail_update)
                                            db.session.commit()
                                        print('classs======================')
                                    elif (len(l_checkings)!=0 ):
                                                print('l_checking',l_checkings)
                                                absent_period=timetable.query.filter_by(teacher_id=id,period=i,day=day,d_id=h.d_id).first()
                                                coming_teacher=timetable.query.filter_by(teacher_id=sub_teacher,cid=absent_period.cid,d_id=h.d_id).first()
                                                substituting=substitution(teacher_id=00, original_teacher_id=id,cid=absent_period.cid , sid='lab', lort='lab' , day=day,date=date, period=i,d_id=h.d_id)
                                                db.session.add(substituting)
                                                db.session.commit()
                                                print('lab======================')
                                                avail_update1=lab_free.query.filter_by(date=date,period=i,d_id=h.d_id).first()
                                                if avail_update1:
                                                    insert=lab_free_store(date=date,period=i,d_id=h.d_id)
                                                    db.session.add(insert)
                                                    db.session.commit()
                                                    db.session.delete(avail_update1)
                                                    db.session.commit() 
                                                l_checkings=None
                                    else: 
                                        
                                        absent_period=timetable.query.filter_by(teacher_id=id,period=i,day=day,d_id=h.d_id).first() 
                                        coming_teacher=timetable.query.filter_by(teacher_id=sub_teacher,cid=absent_period.cid,d_id=h.d_id).first()
                                        substituting=substitution(teacher_id=-1, original_teacher_id=id,cid=absent_period.cid , sid='Library', lort='Library' , day=day, period=i,date=date,d_id=h.d_id)
                                        db.session.add(substituting)
                                        db.session.commit()       

            kl=lab_free.query.filter_by(date=date,d_id=h.d_id).all()
            print(';;;;;lab  kl',kl)
            user=session['user']
            hod_id=session['hod']
            h=hod.query.filter_by(hod_id=hod_id).first()
            substitute= substitution.query.filter_by(d_id=h.d_id).all()
            date_info=[]
            for a in substitute:
                if a.date not in date_info:
                    date_info+=[a.date]

            allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
            allclass= classes.query.filter_by(d_id=h.d_id).all()
            alltta = timetable.query.filter_by(d_id=h.d_id).all()
            teachers_name=[]
            for a in alltta:
                if a.teacher_id not in teachers_name:
                    teachers_name+=[a.teacher_id]
            print('ppppppp', date_info)
            absent_teachers=absent_teacher.query.filter_by(d_id=h.d_id).all()
            hod_user=session['hod']
            alltta = hod.query.filter_by(hod_id=hod_user).all()
            df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
            print(df)
            gmail=df['mail'].tolist()
            mail=gmail[0]
            u=df['name'].tolist()
            us=u[0]
            ss=substitution.query.filter_by(d_id=h.d_id).all()
            substi=[]
            for a in ss:
                if a.date not in substi:
                    substi+=[a.date]
            print('sub====',substi)
            return render_template('hod_substitution.html',substi=substi,us=us,date_info=date_info, absent_teacher=absent_teachers, substitute=substitute,teachers_name=teachers_name,allTeachers=allTeachers, allclass =allclass)
            
    return render_template('hod_substitut.html')


@app.route('/hod_substitution_message/<string:sno>')
def hod_substitution_message(sno):
    if  g.user is  None:
        flash("Login to access")
        return render_template("hod_index.html")

    else:

          
            user=session['user']
            hod_id=session['hod']
            h=hod.query.filter_by(hod_id=hod_id).first()
            sub=substitution.query.filter_by(date=sno,d_id=h.d_id).all()
            sno=sno
            substi=[]
            names=[]
            for a in sub:
                if a.teacher_id not in substi:
                    substi+=[a.teacher_id]
            substi = [element for element in substi if element not in [-1, 0]]

            sender = '(AutoPlanify,autotimetablegen@gmail.com)'
            for s in substi:
                i=teacher.query.filter_by(teacher_id=s,d_id=h.d_id).first()
                _outer_list=[]
                subs=substitution.query.filter_by(teacher_id=s,date=sno,d_id=h.d_id).all()
                for ss in subs:
                    inside_list=[]
                    cc=classes.query.filter_by(cid=ss.cid,d_id=h.d_id).first()
                    cc_name=cc.cname
                    inside_list=[cc_name,ss.period]
                    _outer_list+=[inside_list]


                recipient = i.mail
                print(recipient)
                subject = f"Autoplanify- Teacher Timetable Substitution Details for {sno} "
                        
                link = url_for('home',  _external=True)

                body = f"This email  inform you about the timetable substitution details for your classes on {sno} as generated by Autoplanify.\n\n class - period\n"

                for item in _outer_list:
                    first, second = item
                    body += f"{first} - {second}\n"

                msg = Message(subject, sender=sender, recipients=[recipient])
                msg.body = body

                mail.send(msg)



            return redirect("/hod_add_substitution")






@app.route("/teacher_login",methods=["GET", "POST"])
def teacher_login():
    if  g.user is not None:
        flash('ALREADY LOGGED IN','alert')
    else:
        if request.method == "POST":
                session.pop("user", None)
                uname = request.form['username']
                passw = request.form["password"]
                login_teacher = teacher.query.filter_by(username=uname, password=passw).first()
                login= teacher.query.filter_by(username=uname, password=passw).first()
                u= teacher.query.filter_by(username=uname).first()
                print('u----------',u)
                p= teacher.query.filter_by(password=passw).first()
                print('p----------',p)
                if u is None and p is  None:
                    print('both wrong')
                    flash("Please enter a valid user",'error')
                if u is None and p is not None:
                    print('invalid user')
                    flash("Please enter a valid user",'error')
                if u is not None and p is None:
                    print('wrong password')
                    flash("wrong password",'error')
                
                if login_teacher is not None:
                    print('login is not none ')
                    print()
                    session['user']=login.admin_id
                    session['teacher']=login.teacher_id
                    
                    print('4444444444444444444444444444',session['user'],session['teacher'])
                    
                     

                    
                    
                    
                    
                    return redirect(url_for("teacher_profile"))
                else:
                
                    return redirect(url_for('teacher_login'))
        #login = user.query.filter_by(username=uname, password=passw).first()
        #if login is not None:
        #    return redirect(url_for("profile"))
    return render_template("teacher_login.html")



@app.route('/teacher_forgot-password', methods=['GET', 'POST'])
def teacher_forgot_password():
    if request.method == 'POST':
        mail = request.form['email']
        user = teacher.query.filter_by(mail=mail).first()  # Assuming a User model

        if user:
            serializer = URLSafeTimedSerializer(app.secret_key)
            token = serializer.dumps(user.mail, salt='teacher_password-reset')
            reset_link = url_for('teacher_reset_password', token=token, _external=True)

            # Send email with reset link (optional)
            if app.config['MAIL_USERNAME']:
                mail = Mail(app)
                msg = Message('Password Reset Request',
                              sender=app.config['MAIL_USERNAME'],
                              recipients=[user.mail])
                msg.body = f'Click here to reset your password: {reset_link}'
                mail.send(msg)

            flash ('Password reset link sent!')
        else:
            flash ('Email not found')

    return render_template('forgot_password.html')


@app.route('/teacher_reset-password/<token>', methods=['GET', 'POST'])
def teacher_reset_password(token):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        email = serializer.loads(token, salt='teacher_password-reset', max_age=3600)
        user = teacher.query.filter_by(mail=email).first()
    except:
        flash('Invalid or expired token') 

    if request.method == 'POST':
        new_password = request.form['new_password']
        user.password = new_password
        db.session.commit()
        flash( 'Password reset successfully!')
        return redirect("/teacher_login")

    return render_template('reset_password.html')





@app.route('/teacher_profile')
def teacher_profile():
        
        if g.user:
            teacher_id=session['teacher']   
            h=teacher.query.filter_by(teacher_id=teacher_id).first()
            print('uer----',g.user)
            print('teacher----',session['teacher'])
            if(session['teacher'] is not None):
                user1=session['teacher']
                
                allttal = teacher.query.filter_by(teacher_id=h.teacher_id).first()
                d=department.query.filter_by(d_id=allttal.d_id).first()
                mail_=allttal.mail
                name=allttal.name
                id=d.dname
                return render_template('teacher_profile.html',id=id,name=name,user=session['teacher'],mail=mail_,hod=session['user'])
            
        else:
            return redirect(url_for('teacher_login'))

@app.route('/teacher_show')
def teacher_show():
    if  g.user is  None:
        flash("login to access")
        return render_template("teacher_login.html")

    else:
        teacher_id=session['teacher']   
        h=teacher.query.filter_by(teacher_id=teacher_id).first()
        user=session['user']
        alltt = timetable.query.filter_by(d_id=h.d_id).all()
        days=["mon","tues","wed","thurs","fri"]
        teachers_name=[]
        for a in alltt:
            if a.teacher_id not in teachers_name:
                teachers_name+=[a.teacher_id]
        allex=external.query.filter_by(d_id=h.d_id).all() 
        for e in allex:
            if e.teacher_id not in teachers_name:
                teachers_name+=[e.teacher_id]

        allex=external.query.filter_by(d_id=h.d_id).all() 
        for e in allex:
            if e.teacher_id not in teachers_name:
                teachers_name+=[e.teacher_name]
        alltta = timetable.query.filter_by(d_id=h.d_id).all()
        class_name=[]
        for a in alltta:
            if a.cid not in class_name:
                class_name+=[a.cid]
        
        
        
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        allTeachers= teacher.query.filter_by().all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        #alltime = Time_slot.query.filter_by(d_id=h.d_id).all()
        teacher_id=session['teacher']
        allttal = teacher.query.filter_by(teacher_id=h.teacher_id).first()
        d=department.query.filter_by(d_id=allttal.d_id).first()
        mail_=allttal.mail
        name=allttal.name
        id=d.dname
    
        return render_template('teacher_show.html',name=name,class_name=class_name,teachers_name=teachers_name,days=days, alltt=alltt, allsub=allsub, allTeachers=allTeachers ,allclass=allclass )
    return render_template('show.html')


@app.route('/teacher_teacher_timetable/<t>')
def teacher_teacher_timetable(t):
    if  g.user is  None:
        
        return render_template("register.html")

    else:
        teacher_id=session['teacher']   
        h=teacher.query.filter_by(teacher_id=teacher_id).first()
        user=session['user']
        alltt = timetable.query.filter_by(d_id=h.d_id,teacher_id=t).all()
        days=["mon","tues","wed","thurs","fri"]
        t=t  
        user=session['user']
        alltta = timetable.query.filter_by(d_id=h.d_id).all()
        teachers_name=[]
        for a in alltta:
            if a.teacher_id not in teachers_name:
                teachers_name+=[a.teacher_id] 
        allex=external.query.filter_by(d_id=h.d_id).all() 
        for e in allex:
            if e.teacher_id not in teachers_name:
                teachers_name+=[e.teacher_id]
        class_name=[]
        for a in alltt:
            if a.cid not in class_name:
                class_name+=[a.cid]
        subjects_name=[]
        for a in alltt:
            if a.sid not in subjects_name:
                subjects_name+=[a.sid]
        
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        allTeachers= teacher.query.filter_by().all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        at= teacher.query.filter_by(teacher_id=t,d_id=h.d_id).first()
        if(external.query.filter_by(teacher_id=t).first()):
            ex=teacher.query.filter_by(teacher_id=t).first()
            tname=ex.name
        else:
            tname=at.name
        allttal = teacher.query.filter_by(teacher_id=h.teacher_id).first()
        d=department.query.filter_by(d_id=allttal.d_id).first()
        mail_=allttal.mail
        name=allttal.name
        id=d.dname
        return render_template('teacher_teacher_timetable.html',name=name,tname=tname,subjects_name=subjects_name,class_name=class_name,t=t,teachers_name=teachers_name, alltt=alltt,days=days,allsub=allsub, allTeachers=allTeachers ,allclass=allclass)
    #return render_template('teacher_timetable.html')
   

@app.route('/teacher_class_timetable/<c>')
def teacher_class_timetable(c):
    if  g.user is  None:
        flash("Sign in to access")
        return render_template("register.html")

    else:
        teacher_id=session['teacher']   
        h=teacher.query.filter_by(teacher_id=teacher_id).first()
        user=session['user']
        alltt = timetable.query.filter_by(d_id=h.d_id,cid=c).all()
        days=["mon","tues","wed","thurs","fri"]
        c=c  
        user=session['user']
        alltta = timetable.query.filter_by(d_id=h.d_id).all()
        class_name=[]
        teachers_name=[]
        subjects_name=[]
        for a in alltta:
            if a.cid not in class_name:
                class_name+=[a.cid]
        for a in alltta:
            if a.teacher_id not in teachers_name:
                teachers_name+=[a.teacher_id] 
        allex=external.query.filter_by(d_id=h.d_id).all() 
        for e in allex:
            if e.teacher_id not in teachers_name:
                teachers_name+=[e.teacher_id]
        for a in alltt:
            if a.sid not in subjects_name:
                subjects_name+=[a.sid]
        ac= classes.query.filter_by(d_id=h.d_id,cid=c).first()
        name=ac.cname
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        allTeachers= teacher.query.filter_by().all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        allttal = teacher.query.filter_by(teacher_id=h.teacher_id).first()
        d=department.query.filter_by(d_id=allttal.d_id).first()
        mail_=allttal.mail
        name=allttal.name
        id=d.dname
    
        return render_template('teacher_class_timetable.html',name=name,subjects_name=subjects_name,c=c,class_name=class_name, alltt=alltt,days=days,allsub=allsub, allTeachers=allTeachers ,allclass=allclass)
    return render_template('teacher_class_timetable.html')


@app.route('/teacher_lab_show')
def teacher_lab_show():
    if  g.user is  None:
        flash("Loginin to access")
        return render_template("teacher_login.html")

    else:
        user=session['user']
        teacher_id=session['teacher']   
        h=teacher.query.filter_by(teacher_id=teacher_id).first()
        alltt = lab_timetable.query.filter_by(d_id=h.d_id).all()
        days=["mon","tues","wed","thurs","fri"]
        teachers_name=[]
        for a in alltt:
            if a.teacher_id not in teachers_name:
                teachers_name+=[a.teacher_id]

        
        alltta = lab_timetable.query.filter_by(d_id=h.d_id).all()
        class_name=[]
        for a in alltta:
            if a.cid not in class_name:
                class_name+=[a.cid]
 
        allsub= subjects.query.filter_by(d_id=h.d_id).all()
        allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        allttal = teacher.query.filter_by(teacher_id=h.teacher_id).first()
        d=department.query.filter_by(d_id=allttal.d_id).first()
        mail_=allttal.mail
        name=allttal.name
        id=d.dname
       

    
        return render_template('teacher_lab_timetable.html',name=name,class_name=class_name,teachers_name=teachers_name,days=days, alltt=alltt, allsub=allsub, allTeachers=allTeachers ,allclass=allclass )
    return render_template('teachger_lab_show.html')



@app.route('/teacher_add_substitution', methods=['GET','POST'])
def teacher_add_substitution():
    if  g.user is  None:
        flash("Login to access")
        return render_template("hod_index.html")
    else:

        if request.method=='POST':
                user=session['user']
                hod_id=session['teacher']
                h=hod.query.filter_by(hod_id=hod_id).first()
                teacher_id=session['teacher']
                h=teacher.query.filter_by(teacher_id=teacher_id).first()
                id=request.form['teacher']
                date=request.form["date"]
                if isinstance(date, str):
                    # Convert the string to a datetime.date object
                    date = datetime.strptime(date, '%Y-%m-%d').date()
                day=datetime.strftime(date, '%A')
                if day == 'Monday':
                    day= 'mon'
                elif day == 'Tuesday':
                    day ='tues'
                elif day == 'Wednesday':
                    day = 'wed'
                elif day == 'Thursday':
                    day = 'thurs'
                elif day == 'Friday':
                    day = 'fri'
                selected=teacher.query.filter_by(teacher_id=id,d_id=h.d_id).first()
                select_teacher=selected.name
                table=timetable.query.filter_by(teacher_id=id,day=day,d_id=h.d_id).all()
                that_day=absent_teacher.query.filter_by(teacher_id=id,date=date,d_id=h.d_id).first()
                if (that_day is None):
                    absent_class=[]
                    for a in table:
                        if a.cid not in absent_class:
                            absent_class+=[a.cid]
                    
                    flag=1
                    b=substitution.query.filter_by(teacher_id=id,date=date,d_id=h.d_id).all()
                    if (len(absent_class)==0 & len(b)!=0):
                            flash(f'No class for  {select_teacher} on {date},{day} !','Error')
                    elif(len(b)!=0):
                            br="<br>"
                            flash(f'Substitution class for {select_teacher}  on {date},{day} ! TRY DELETING THE SUBSTITUTION FOR THAT DAY AND TRY AGAIN','Error')
                    elif (len(absent_class)==0):
                        flash(f'No class for {select_teacher} on {date},{day} !','Error')
                        flag=0
                    if flag!=0:
                        insert=absent_teacher(teacher_id=id , date=date, d_id=h.d_id)
                        db.session.add(insert)
                        db.session.commit()
                        t_checking=Teacher_free.query.filter_by(date=date,d_id=h.d_id).all()
                        if len(t_checking) ==0:
                            copy=Teacher_avail.query.filter_by(day=day,d_id=h.d_id).all()
                            for i in copy:
                                num=i.teacher_id
                                if (int(num)!=int(id)):
                                        print(num,id)
                                        insert=Teacher_free(teacher_id=i.teacher_id , period=i.period , date=date, d_id=h.d_id)
                                        db.session.add(insert)
                                        db.session.commit()
                                if(int(num)==int(id)):
                                        this_insert=Teacher_free_store(teacher_id=i.teacher_id , period=i.period , date=date, d_id=h.d_id)
                                        db.session.add(this_insert)
                                        db.session.commit()
                        else:
                            dlt=Teacher_free.query.filter_by(teacher_id=id, date=date,d_id=h.d_id).first()  
                            while dlt is not None:
                                       
                                        insert=Teacher_free_store(teacher_id=dlt.teacher_id,date=date,period=dlt.period,d_id=h.d_id)
                                        db.session.add(insert)
                                        db.session.commit()
                                        print("insert:",insert)
                                        print("dlt",dlt)
                                        db.session.delete(dlt)
                                        db.session.commit()
                                        dlt=Teacher_free.query.filter_by(teacher_id=id, date=date,d_id=h.d_id).first()  
                                        
                        l_checking=lab_timetable.query.filter_by(d_id=h.d_id).first()
                        if(l_checking is not None):
                            l_checking2=lab_free.query.filter_by(date=date,d_id=h.d_id).all()
                            if len(l_checking2) ==0:
                                l_avail=lab_avail.query.filter_by(day=day,d_id=h.d_id).all()
                            
                                for i in l_avail:
                                    
                                    insert=lab_free(period=i.period , date=date, d_id=h.d_id)
                                    db.session.add(insert)
                                    db.session.commit()
                else:
                     flash(f'Already noted the absent for {select_teacher}  on {date},{day} !','Error')

        user=session['user']
        hod_id=session['teacher']
        h=hod.query.filter_by(hod_id=hod_id).first()
        teacher_id=session['teacher']
        h=teacher.query.filter_by(teacher_id=teacher_id).first()
        substitute= substitution.query.filter_by(d_id=h.d_id).all()
            
        allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
        allclass= classes.query.filter_by(d_id=h.d_id).all()
        alltta = timetable.query.filter_by(d_id=h.d_id).all()
        teachers_name=[]
        for a in alltta:
                if a.teacher_id not in teachers_name:
                    teachers_name+=[a.teacher_id]
        absent_teachers=absent_teacher.query.filter_by(d_id=h.d_id).all()
        teacher_id=session['teacher']
        h=teacher.query.filter_by(teacher_id=teacher_id).first()
        allttal = teacher.query.filter_by(teacher_id=h.teacher_id).first()
        d=department.query.filter_by(d_id=allttal.d_id).first()
        mail_=allttal.mail
        name=allttal.name
        id=d.dname
        ss=substitution.query.filter_by(d_id=h.d_id).all()
        substi=[]
        for a in ss:
                if a.date not in substi:
                    substi+=[a.date]
        return render_template('teacher_substitution.html',substi=substi,name=name,absent_teacher=absent_teachers ,substitute=substitute,teachers_name=teachers_name,allTeachers=allTeachers, allclass =allclass)
        
    return render_template('hod_substitut.html')



@app.route('/teacher_substitution_generate')
def teacher_substitution_generate():
    if  g.user is  None:
        flash("Login to access")
        return render_template("hod_index.html")

    else:

          
            user=session['user']
            hod_id=session['teacher']
            h=hod.query.filter_by(hod_id=hod_id).first()
            teacher_id=session['teacher']
            h=teacher.query.filter_by(teacher_id=teacher_id).first()
            absent_staff=[]
            row=absent_teacher.query.filter_by(d_id=h.d_id).all()
            for a in row:
                
                if a.teacher_id not in absent_staff:
                            absent_staff+=[a.teacher_id]
                
            print('absent_staff',absent_staff)
            for r in row: 
                id=r.teacher_id
                date=r.date
                if isinstance(date, str):
                    # Convert the string to a datetime.date object
                    date = datetime.strptime(date, '%Y-%m-%d').date()
                day=datetime.strftime(date, '%A')
                if day == 'Monday':
                    day= 'mon'
                elif day == 'Tuesday':
                    day ='tues'
                elif day == 'Wednesday':
                    day = 'wed'
                elif day == 'Thursday':
                    day = 'thurs'
                elif day == 'Friday':
                    day = 'fri'
                checking_flag=True
                print('qqqqqqqq',day)
                user=session['user']
                teacher_id=session['teacher']
                h=teacher.query.filter_by(teacher_id=teacher_id).first()
            
                table=timetable.query.filter_by(teacher_id=id,day=day,d_id=h.d_id).all()
                print(table)
                absent_class=[]
                
                for a in table:
                    if a.cid not in absent_class:
                
                       absent_class+=[a.cid]
                    
                flag=True 

                selected=teacher.query.filter_by(teacher_id=id,d_id=h.d_id).first()
                select_teacher=selected.name
                q=True
                if q==True:
                    b=substitution.query.filter_by(teacher_id=id,date=date,d_id=h.d_id).all()
                    if (len(absent_class)==0 & len(b)!=0):
                        flash(f'No class for  {select_teacher} on {date},{day} !','Error')
                    elif(len(b)!=0):
                        br="<br>"
                        flash(f'Substitution class for {select_teacher}  on {date},{day} ! TRY DELETING THE SUBSTITUTION FOR THAT DAY AND TRY AGAIN','Error')
                        

                        flag=False
                    elif (len(absent_class)==0):
                        flash(f'No class for {select_teacher} on {date},{day} !','Error')
                    if flag!=False:     
                        
                        print('absent_class',absent_class) 
                        print('substitute_t',substitute_t) 
                        absent_p=[]
                        
                        for a in table:
                            if a.period not in absent_p:
                                absent_p+=[a.period]

                        
                       
                        for i in absent_p:
                                substitute_t=[]
                                that_p=timetable.query.filter_by(teacher_id=id,period=i, day=day,d_id=h.d_id).first()
                                that_c=that_p.cid
                                teacher_table=timetable.query.filter_by(cid=that_c,d_id=h.d_id).all()
                                for a in teacher_table:
                                    if a.teacher_id not in substitute_t:
                                        substitute_t+=[a.teacher_id]
                        
                                CHECKING=substitution.query.filter_by(original_teacher_id=id,period=i, date=date,d_id=h.d_id).all()
                                if len(CHECKING)!=0:
                                    flash(f'Already substituted for {date},{day} !','Error')
                                    checking_flag=False
                                    break
                                if checking_flag==True:    
                                    l_checking=lab_free.query.filter_by(period=i,date=date,d_id=h.d_id).all()

                                    All_avail=Teacher_free.query.filter_by(date=date,period=i,d_id=h.d_id).all()
                                    print('All_avail',All_avail)
                                    all_substitute_t=[]
                                    for a in All_avail:
                                        if a.teacher_id not in all_substitute_t:
                                            all_substitute_t+=[a.teacher_id]
                                        
                                    real_substitute=[ item for item in substitute_t if item in all_substitute_t ]
                                    check_count=[]
                                    for r in real_substitute:
                                        check=Teacher_free.query.filter_by(teacher_id=r,date=date,d_id=h.d_id).all()
                                        check_count+=[len(check)]
                                    sub_teacher=None
                                    if check_count:
                                        max_count=max(check_count) 
                                        for j in range(0,len(check_count)):
                                            if max_count==check_count[j]:
                                                sub_teacher=real_substitute[j]
                                                break
                                    l_checkings=lab_free.query.filter_by(period=i,date=date,d_id=h.d_id).all()
                                    if sub_teacher:
                                        absent_period=timetable.query.filter_by(teacher_id=id,period=i,day=day,d_id=h.d_id).first()
                                        coming_teacher=timetable.query.filter_by(teacher_id=sub_teacher,cid=absent_period.cid,d_id=h.d_id).first()
                                        substituting=substitution(teacher_id=sub_teacher, original_teacher_id=id,cid=absent_period.cid , sid=coming_teacher.sid, lort='Thoery' , day=day, period=i,date=date, d_id=h.d_id)
                                        db.session.add(substituting)
                                        db.session.commit()
                                        avail_update=Teacher_free.query.filter_by(teacher_id=sub_teacher,date=date,period=i,d_id=h.d_id).first()
                                        if avail_update:
                                            insert=Teacher_free_store(teacher_id=sub_teacher,date=date,period=i,d_id=h.d_id)
                                            db.session.add(insert)
                                            db.session.commit()
                                            db.session.delete(avail_update)
                                            db.session.commit()
                                        print('classs======================')
                                    elif (len(l_checkings)!=0 ):
                                                print('l_checking',l_checkings)
                                                absent_period=timetable.query.filter_by(teacher_id=id,period=i,day=day,d_id=h.d_id).first()
                                                coming_teacher=timetable.query.filter_by(teacher_id=sub_teacher,cid=absent_period.cid,d_id=h.d_id).first()
                                                substituting=substitution(teacher_id=00, original_teacher_id=id,cid=absent_period.cid , sid='lab', lort='lab' , day=day,date=date, period=i,d_id=h.d_id)
                                                db.session.add(substituting)
                                                db.session.commit()
                                                print('lab======================')
                                                avail_update1=lab_free.query.filter_by(date=date,period=i,d_id=h.d_id).first()
                                                if avail_update1:
                                                    insert=lab_free_store(date=date,period=i,d_id=h.d_id)
                                                    db.session.add(insert)
                                                    db.session.commit()
                                                    db.session.delete(avail_update1)
                                                    db.session.commit() 
                                                l_checkings=None
                                    else: 
                                        
                                        absent_period=timetable.query.filter_by(teacher_id=id,period=i,day=day,d_id=h.d_id).first() 
                                        coming_teacher=timetable.query.filter_by(teacher_id=sub_teacher,cid=absent_period.cid,d_id=h.d_id).first()
                                        substituting=substitution(teacher_id=-1, original_teacher_id=id,cid=absent_period.cid , sid='Library', lort='Library' , day=day, period=i,date=date,d_id=h.d_id)
                                        db.session.add(substituting)
                                        db.session.commit()       


            user=session['user']
            hod_id=session['teacher']
            h=hod.query.filter_by(hod_id=hod_id).first()
            teacher_id=session['teacher']
            h=teacher.query.filter_by(teacher_id=teacher_id).first()
            substitute= substitution.query.filter_by(d_id=h.d_id).all()
            date_info=[]
            for a in substitute:
                if a.date not in date_info:
                    date_info+=[a.date]

            allTeachers= teacher.query.filter_by(d_id=h.d_id).all()
            allclass= classes.query.filter_by(d_id=h.d_id).all()
            alltta = timetable.query.filter_by(d_id=h.d_id).all()
            teachers_name=[]
            for a in alltta:
                if a.teacher_id not in teachers_name:
                    teachers_name+=[a.teacher_id]
            print('ppppppp', date_info)
            absent_teachers=absent_teacher.query.filter_by(d_id=h.d_id).all()
            hod_user=session['teacher']
            alltta = teacher.query.filter_by(teacher_id=hod_user).all()
            df=pd.DataFrame([( r.name ,r.mail,r.d_id)for r in alltta],columns=['name','mail','d_id'])
            print(df)
            gmail=df['mail'].tolist()
            mail=gmail[0]
            u=df['name'].tolist()
            us=u[0]
            teacher_id=session['teacher']
            h=teacher.query.filter_by(teacher_id=teacher_id).first()
            allttal = teacher.query.filter_by(teacher_id=h.teacher_id).first()
            d=department.query.filter_by(d_id=allttal.d_id).first()
            mail_=allttal.mail
            name=allttal.name
            id=d.dname
            ss=substitution.query.filter_by(d_id=h.d_id).all()
            substi=[]
            for a in ss:
                if a.date not in substi:
                    substi+=[a.date]
            return render_template('teacher_substitution.html',substi=substi,name=name,date_info=date_info, absent_teacher=absent_teachers, substitute=substitute,teachers_name=teachers_name,allTeachers=allTeachers, allclass =allclass)



@app.route('/teacher_substitution_message/<string:sno>')
def teacher_substitution_message(sno):
    if  g.user is  None:
        flash("Login to access")
        return render_template("teacher_index.html")

    else:

          
            user=session['user']
            id=session['teacher']
            h=teacher.query.filter_by(teacher_id=id).first()
            sub=substitution.query.filter_by(date=sno,d_id=h.d_id).all()
            sno=sno
            substi=[]
            names=[]
            for a in sub:
                if a.teacher_id not in substi:
                    substi+=[a.teacher_id]
            substi = [element for element in substi if element not in [-1, 0]]

            sender = '(AutoPlanify,autotimetablegen@gmail.com)'
            for s in substi:
                i=teacher.query.filter_by(teacher_id=s,d_id=h.d_id).first()
                _outer_list=[]
                subs=substitution.query.filter_by(teacher_id=s,date=sno,d_id=h.d_id).all()
                for ss in subs:
                    inside_list=[]
                    cc=classes.query.filter_by(cid=ss.cid,d_id=h.d_id).first()
                    cc_name=cc.cname
                    inside_list=[cc_name,ss.period]
                    _outer_list+=[inside_list]


                recipient = i.mail
                print(recipient)
                subject = f"Autoplanify- Teacher Timetable Substitution Details for {sno} "
                        
                link = url_for('home',  _external=True)

                body = f"This email  inform you about the timetable substitution details for your classes on {sno} as generated by Autoplanify.\n\nclass - period\n"

                for item in _outer_list:
                    first, second = item
                    body += f"{first} - {second}\n"

                msg = Message(subject, sender=sender, recipients=[recipient])
                msg.body = body

                mail.send(msg)



            return redirect("/teacher_add_substitution")





@app.route('/delete_department/<int:sno>')
def delete_department(sno):
    d = department.query.filter_by(d_id=sno).first()
    db.session.delete(d)
    db.session.commit()
    h = hod.query.filter_by(d_id=sno).first()
    if h is not None:
        db.session.delete(h)
        db.session.commit()
    t =teacher.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =teacher.query.filter_by(d_id=sno).first()
    t=classes.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =classes.query.filter_by(d_id=sno).first()
    t=subjects.query.filter_by(d_id=sno).first()  
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =subjects.query.filter_by(d_id=sno).first() 
    t =external.query.filter_by(d_id=sno).first() 
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =external.query.filter_by(d_id=sno).first()
    t =lab_avail.query.filter_by(d_id=sno).first() 
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =lab_avail.query.filter_by(d_id=sno).first()
    t =lab_free.query.filter_by(d_id=sno).first() 
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =lab_free.query.filter_by(d_id=sno).first()
    t =lab_free_store.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =lab_free_store.query.filter_by(d_id=sno).first()
    t =assign.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =assign.query.filter_by(d_id=sno).first() 
    t =lab_assign.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =lab_assign.query.filter_by(d_id=sno).first() 
    t =lab_timetable.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =lab_timetable.query.filter_by(d_id=sno).first() 
    t =Teacher_avail.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =Teacher_avail.query.filter_by(d_id=sno).first()
    t =Teacher_free.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =Teacher_free.query.filter_by(d_id=sno).first()
    t =Teacher_free_store.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =Teacher_free_store.query.filter_by(d_id=sno).first()
    t =absent_teacher.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =absent_teacher.query.filter_by(d_id=sno).first()
    t =substitution.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =substitution.query.filter_by(d_id=sno).first()
    t =timetable.query.filter_by(d_id=sno).first()
    while(t is not None):
        db.session.delete(t)
        db.session.commit()
        t =timetable.query.filter_by(d_id=sno).first()
    return redirect("/add_department")



@app.route('/delete_hod/<int:sno>')
def delete_hod(sno):
    h = hod.query.filter_by(hod_id=sno).first()
    db.session.delete(h)
    db.session.commit()
    return redirect("/add_hod")

@app.route('/delete_teacher/<int:sno>')
def delete_teacher(sno):
    h = teacher.query.filter_by(teacher_id=sno).first()
    db.session.delete(h)
    db.session.commit()
    return redirect("/add_teacher")

@app.route('/delete_class/<int:sno>')
def delete_class(sno):
    h = classes.query.filter_by(cid=sno).first()
    db.session.delete(h)
    db.session.commit()
    return redirect("/add_class")

@app.route('/delete_sub/<int:sno>')
def delete_sub(sno):
    h = subjects.query.filter_by(sid=sno).first()
    db.session.delete(h)
    db.session.commit()
    return redirect("/add_sub")

@app.route('/delete_external/<int:sno>')
def delete_external(sno):
    h = external.query.filter_by(exid=sno).first()
    db.session.delete(h)
    db.session.commit()
    t = timetable.query.filter_by(exid=h.exid,type='ex').first()
    while(t is not None):
        
        db.session.delete(t)
        db.session.commit()
        t = timetable.query.filter_by(exid=h.exid,type='ex').first()
    return redirect("/add_external")

@app.route('/delete_lab/<int:sno>')
def delete_lab(sno):
    h = lab_assign.query.filter_by(lid=sno).first()
    db.session.delete(h)
    db.session.commit()
    return redirect("/lab_assign")

@app.route('/delete_lab_assign')
def delete_lab_assign():
    hod_id=session['hod']
    h=hod.query.filter_by(hod_id=hod_id).first()
    u = lab_assign.query.filter_by(d_id=h.d_id).first()
    while(u is not None):
        
        db.session.delete(u)
        db.session.commit()
        u = lab_assign.query.filter_by(d_id=h.d_id).first()
    return redirect("/lab_assign")


@app.route('/delete_lab_tt')
def delete_lab_tt():
    
    user=session['user']
    hod_id=session['hod']
    h=hod.query.filter_by(hod_id=hod_id).first()
    
    u = lab_timetable.query.filter_by(d_id=h.d_id).first()
    while(u is not None):
        
        db.session.delete(u)
        db.session.commit()
        u = lab_timetable.query.filter_by(d_id=h.d_id).first()
        
    t = timetable.query.filter_by(d_id=h.d_id,type='out').first()
    while(t is not None):
        
        db.session.delete(t)
        db.session.commit()
        t = timetable.query.filter_by(d_id=h.d_id,type='out').first()
    
    u = lab_avail.query.filter_by(d_id=h.d_id).first()
    while(u is not None):
        
        db.session.delete(u)
        db.session.commit()
        u =lab_avail.query.filter_by(d_id=h.d_id).first()
    uf = lab_free.query.filter_by(d_id=h.d_id).first()
    while(uf is not None):
        
        db.session.delete(uf)
        db.session.commit()
        uf =lab_free.query.filter_by(d_id=h.d_id).first()
    ufs = lab_free_store.query.filter_by(d_id=h.d_id).first()
    while(ufs is not None):
        
        db.session.delete(ufs)
        db.session.commit()
        ufs =lab_free.query.filter_by(d_id=h.d_id).first()

    return redirect("/lab_show")


@app.route('/delete_substitute/<int:sno>')
def delete_substitute(sno):
    h = substitution.query.filter_by(subid=sno).first()
    db.session.delete(h)
    db.session.commit()
    if (h.teacher_id==00):
        l=lab_free(date=h.date, period=h.period ,d_id=h.d_id)
        db.session.add(l)
        db.session.commit()

        la=lab_free_store.query.filter_by(date=h.date, period=h.period ,d_id=h.d_id).first()
        if(la is not None):
            db.session.delete(la)
            db.session.commit()
    elif(h.teacher_id==-1):
        l=0
    else:
        t=Teacher_free(teacher_id=h.teacher_id,date=h.date,period=h.period ,d_id=h.d_id)
        db.session.add(t)
        db.session.commit()
        tf=Teacher_free_store.query.filter_by(teacher_id=h.teacher_id,date=h.date,period=h.period ,d_id=h.d_id).first()
        db.session.delete(tf)
        db.session.commit()
    return redirect("/hod_add_substitution")

@app.route('/delete_absent_t/<int:sno>')
def delete_absent_t(sno):
    user=session['user']
    hod_id=session['hod']
    h=hod.query.filter_by(hod_id=hod_id).first()
    h = absent_teacher.query.filter_by(atid=sno).first()
    db.session.delete(h)
    db.session.commit()   
    a=Teacher_free_store.query.filter_by(teacher_id=h.teacher_id,d_id=h.d_id).all()
    for i in a:
            insert=Teacher_free(teacher_id=i.teacher_id,date=i.date,period=i.period ,d_id=h.d_id)
            db.session.add(insert)
            db.session.commit()
            db.session.delete(i)
            db.session.commit()
         
        
         
    return redirect("/hod_add_substitution")


@app.route('/delete_date_substitute/<string:sno>')
def delete_date_substitute(sno):
    print('sno',sno)
    user=session['user']
    hod_id=session['hod']
    h=hod.query.filter_by(hod_id=hod_id).first()
    u = substitution.query.filter_by(date=sno , d_id=h.d_id).first()
    while(u is not None):
        
        db.session.delete(u)
        db.session.commit()
        u = substitution.query.filter_by(date=sno , d_id=h.d_id).first()
    absent=absent_teacher.query.filter_by(date=sno,d_id=h.d_id).all()
    absent_list=[]
    for i in absent:
         if i.teacher_id not in absent_list:
              absent_list+=[i.teacher_id]
              
    a=Teacher_free_store.query.filter_by(date=sno,d_id=h.d_id).all()
    for i in a:
        if i.teacher_id in absent_list:
             continue
        else:
             
        
            insert=Teacher_free(teacher_id=i.teacher_id,date=i.date,period=i.period ,d_id=h.d_id)
            db.session.add(insert)
            db.session.commit()
            db.session.delete(i)
            db.session.commit()
           
    lls=lab_free_store.query.filter_by(date=sno,d_id=h.d_id).all()
    for i in lls:
            insert=lab_free(date=i.date,period=i.period ,d_id=h.d_id)
            db.session.add(insert)
            db.session.commit()
            db.session.delete(i)
            db.session.commit()
         
    return redirect("/hod_add_substitution")



@app.route('/teacher_delete_absent_t/<int:sno>')
def teacher_delete_absent_t(sno):
    user=session['user']
    id=session['teacher']
    h=teacher.query.filter_by(hod_id=id).first()
    h = absent_teacher.query.filter_by(atid=sno).first()
    db.session.delete(h)
    db.session.commit()   
    a=Teacher_free_store.query.filter_by(teacher_id=h.teacher_id,d_id=h.d_id).all()
    for i in a:
            insert=Teacher_free(teacher_id=i.teacher_id,date=i.date,period=i.period ,d_id=h.d_id)
            db.session.add(insert)
            db.session.commit()
            db.session.delete(i)
            db.session.commit()
         
        
         
    return redirect("/teacher_add_substitution")





@app.route('/teacher_delete_substitute/<int:sno>')
def teacher_delete_substitute(sno):
    h = substitution.query.filter_by(subid=sno).first()
    db.session.delete(h)
    db.session.commit()
    if (h.teacher_id==00):
        l=lab_free(date=h.date, period=h.period ,d_id=h.d_id)
        db.session.add(l)
        db.session.commit()

        la=lab_free_store.query.filter_by(date=h.date, period=h.period ,d_id=h.d_id).first()
        if(la is not None):
            db.session.delete(la)
            db.session.commit()
    elif(h.teacher_id==-1):
        l=0
    else:
        t=Teacher_free(teacher_id=h.teacher_id,date=h.date,period=h.period ,d_id=h.d_id)
        db.session.add(t)
        db.session.commit()
        tf=Teacher_free_store.query.filter_by(teacher_id=h.teacher_id,date=h.date,period=h.period ,d_id=h.d_id).first()
        db.session.delete(tf)
        db.session.commit()
    return redirect("/teacher_add_substitution")


@app.route('/teacher_delete_date_substitute/<string:sno>')
def teacher_delete_date_substitute(sno):
    user=session['user']
    id=session['teacher']
    h=teacher.query.filter_by(teacher_id=id).first()
    u = substitution.query.filter_by(date=sno , d_id=h.d_id).first()
    while(u is not None):
        
        db.session.delete(u)
        db.session.commit()
        u = substitution.query.filter_by(date=sno , d_id=h.d_id).first()
    absent=absent_teacher.query.filter_by(date=sno,d_id=h.d_id).all()
    absent_list=[]
    for i in absent:
         if i.teacher_id not in absent_list:
              absent_list+=[i.teacher_id]
              
    a=Teacher_free_store.query.filter_by(date=sno,d_id=h.d_id).all()
    for i in a:
        if i.teacher_id in absent_list:
             continue
        else:
             
        
            insert=Teacher_free(teacher_id=i.teacher_id,date=i.date,period=i.period ,d_id=h.d_id)
            db.session.add(insert)
            db.session.commit()
            db.session.delete(i)
            db.session.commit()
           
    lls=lab_free_store.query.filter_by(date=sno,d_id=h.d_id).all()
    for i in lls:
            insert=lab_free(date=i.date,period=i.period ,d_id=h.d_id)
            db.session.add(insert)
            db.session.commit()
            db.session.delete(i)
            db.session.commit()
    return redirect("/teacher_add_substitution")


@app.route('/delete_assign/<int:sno>')
def delete_assign(sno):
    
    h = assign.query.filter_by(aid=sno).first()
    db.session.delete(h)
    db.session.commit()
    return redirect("/add_assign")

@app.route('/delete_all_assign')
def delete_all_assign():
    hod_id=session['hod']
    h=hod.query.filter_by(hod_id=hod_id).first()
    u = assign.query.filter_by(d_id=h.d_id).first()
    while(u is not None):
        
        db.session.delete(u)
        db.session.commit()
        u = assign.query.filter_by(d_id=h.d_id).first()
    return redirect("/add_assign")

@app.route('/delete_tt')
def delete_tt():
    hod_id=session['hod']
    h=hod.query.filter_by(hod_id=hod_id).first()
    user=session['user']
    
    u = timetable.query.filter_by(d_id=h.d_id,type='in').first()
    while(u is not None):
        
        db.session.delete(u)
        db.session.commit()
        u = timetable.query.filter_by(d_id=h.d_id,type='in').first()
    
    u = Teacher_avail.query.filter_by(d_id=h.d_id).first()
    while(u is not None):
        
        db.session.delete(u)
        db.session.commit()
        u =Teacher_avail.query.filter_by(d_id=h.d_id).first()
    uf = Teacher_free.query.filter_by(d_id=h.d_id).first()
    while(uf is not None):
        
        db.session.delete(uf)
        db.session.commit()
        uf =Teacher_free.query.filter_by(d_id=h.d_id).first()
    ufs = Teacher_free_store.query.filter_by(d_id=h.d_id).first()
    while(ufs is not None):
        
        db.session.delete(ufs)
        db.session.commit()
        ufs =Teacher_free.query.filter_by(d_id=h.d_id).first()
    s = substitution.query.filter_by(d_id=h.d_id).first()
    while(s is not None):
        
        db.session.delete(s)
        db.session.commit()
        s =substitution.query.filter_by(d_id=h.d_id).first()
    a = absent_teacher.query.filter_by(d_id=h.d_id).first()
    while(a is not None):
        
        db.session.delete(a)
        db.session.commit()
        a =absent_teacher.query.filter_by(d_id=h.d_id).first()
    return redirect("/hod_show")





@app.before_request
def before_request():
    g.user=None
    g.teacher=None
    g.hod=None
    
    if 'user' in session:
        g.user=session['user']
    if 'teacher' in session:
        t=session['teacher']
    if 'hod' in session:
        h=session['hod']


@app.route('/dropsession')
def dropsession():
        session.pop('user',None)
       
        return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True, port=2200)
    
