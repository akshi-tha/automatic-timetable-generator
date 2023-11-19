from flask import Flask, render_template, request , redirect ,session ,logging,g, url_for,flash
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


engine=create_engine('sqlite:///database.sqlite3',echo=True)
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATION']= False
app.config['SECRETE_KEY']='secretkey'

app.secret_key=os.urandom(24)
db =SQLAlchemy(app)
app.app_context().push()







class user(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False, unique=True)
    email = db.Column(db.String(120),nullable=False, unique=True)
    password = db.Column(db.String(80),nullable=False)

def __repr__(self) -> str:
        return f"{self.sno}  -  {self.title}"

class Teacher(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(200))
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created =db.Column(db.DateTime,default=datetime.utcnow)
    
class assign(db.Model):
    aid=db.Column(db.Integer,primary_key=True)
    teacher= db.Column(db.String(200),nullable=False)
    cname=db.Column(db.String(200),nullable=False)
    sub=db.Column(db.String(200),nullable=False)
    weekc=db.Column(db.Integer,nullable=False)
    lort=db.Column(db.String)
    user = db.Column(db.String(200))

class timetable(db.Model):
    ttid=db.Column(db.Integer,primary_key=True)
    teacher= db.Column(db.String(200),nullable=False)
    cname=db.Column(db.String(200),nullable=False)
    sub=db.Column(db.String(200),nullable=False)
    lort=db.Column(db.String(200),nullable=False)
    day=db.Column(db.String(200),nullable=False)
    period=db.Column(db.Integer)
    user = db.Column(db.String(200))
    
class subjects(db.Model):
    sid=db.Column(db.Integer,primary_key=True)
    sname= db.Column(db.String(200))
    user = db.Column(db.String(200))

class Teachers(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    dept=   db.Column(db.String(200))
    user = db.Column(db.String(200))

class classes(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    cname= db.Column(db.String(200))
    user = db.Column(db.String(200))

class Time_slot(db.Model):
    slot_id=db.Column(db.Integer,primary_key=True)
    start= db.Column(db.String(200))
    end=db.Column(db.String(200))
    day=db.Column(db.String(500))
    user = db.Column(db.String(200))
    
class Teacher_avail(db.Model):
    avid=db.Column(db.Integer,primary_key=True)
    tid=db.Column(db.Integer)
    slot_id=db.Column(db.Integer)
    day = db.Column(db.String(200))
    user = db.Column(db.String(200))
    
    
    
    def __repr__(self) -> str:
        return f"{self.sno}  -  {self.title}"
    
class Room(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(200))
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created =db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno}  -  {self.title}"
    

    
    
        


@app.route("/login",methods=["GET", "POST"])
def login():
    if  g.user is not None:
        flash('ALREADY LOGGED IN','alert')
    else:
        if request.method == "POST":
                session.pop("user", None)
                uname = request.form['uname']
                passw = request.form["passw"]
                login = user.query.filter_by(username=uname, password=passw).first()
                u= user.query.filter_by(username=uname).first()
                p= user.query.filter_by(password=passw).first()
                if u is None and p is  None:
                    flash("Please enter a valid user",'error')
                if u is None and p is not None:
                    flash("Please enter a valid user",'error')
                if u is not None and p is None:
                    flash("wrong password",'error')
                
                if login is not None:

                    session['user']=request.form['uname']
                    
                    return redirect(url_for("profile"))
                else:
                
                    return redirect(url_for('login'))
        #login = user.query.filter_by(username=uname, password=passw).first()
        #if login is not None:
        #    return redirect(url_for("profile"))
    return render_template("login.html")


@app.route("/logout",methods=["GET", "POST"])
def logout(): 
    return render_template("register.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        checku = user.query.filter_by(username=uname).first()
        checkm = user.query.filter_by( email = mail).first()

        if checku and checkm is not None:
            flash('username  and email already exists')
        elif checku  is not None:
            flash('username  already exists')
        elif checkm  is not None:
            flash(' email already exists')
        else:
            register = user(username = uname, email = mail, password = passw)
            db.session.add(register)
            db.session.commit()

            return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/teacher', methods=['GET','POST'])
def index():
    if  g.user is  None:
        
        return render_template("register.html")

    else:
        if request.method=='POST':
            if not request.form['title'] or not request.form['desc']:
                    allTeacher = Teacher.query.all()
                    return render_template('index.html', allTeacher=allTeacher)
            else:
                title=request.form["title"]
                desc=request.form["desc"]
                user=session['user']
            
                teacher = Teacher(title=title , desc=desc,user=user)
                db.session.add(teacher)
                db.session.commit()
        user=session['user']
        allTeacher = Teacher.query.filter_by(user=user).all()
       
                   
    
        return render_template('index.html', allTeacher=allTeacher)
    return render_template('index.html')

@app.route('/classes', methods=['GET','POST'])
def index1():
    if  g.user is  None:
        #flash("Sign in to access")
        return render_template("register.html")

    else:
        if request.method=='POST':
            if not request.form['title'] or not request.form['desc']:
                allRoom = Room.query.all()
                return render_template('b.html', allRoom=allRoom)
            else:
                title=request.form["title"]
                desc=request.form["desc"]
                user=session['user']
                room = Room(title=title , desc=desc,user=user)
                db.session.add(room)
                db.session.commit()
        user=session['user']
        allRoom = Room.query.filter_by(user=user).all()
        return render_template('b.html', allRoom=allRoom)
    return render_template('b.html')
    

@app.route('/')
def home():
    
    return render_template('index11.html')


@app.route('/add', methods=['GET','POST'])
def add():
    if  g.user is  None:
        flash("Sign in to access")
        return render_template("register.html")

    else:
        if request.method=='POST':
            if not request.form['name']:
                    allTeachers = Teachers.query.all()
                    return render_template('add.html', allTeachers=allTeachers)
            else:
                name=request.form["name"]
                
                user=session['user']
                exist = bool(Teachers.query.filter_by( user=user,name=name).first())
                if exist is False:
                    teachers = Teachers(name=name,user=user)
                    db.session.add(teachers)
                    db.session.commit()
        user=session['user']
        allTeachers= Teachers.query.filter_by(user=user).all()


    
        return render_template('add.html', allTeachers=allTeachers)
    return render_template('add.html')

@app.route('/add_class', methods=['GET','POST'])
def add_class():
    if  g.user is  None:
        flash("Sign in to access")
        return render_template("register.html")

    else:
        if request.method=='POST':
            if not request.form['class']:
                    allclass = classes.query.all()
                    return render_template('class.html', allclass=allclass)
            else:
                name=request.form["class"]
                user=session['user']
                exist = bool(classes.query.filter_by( user=user,cname=name).first())
                if exist is False:
                    c=classes(cname=name,user=user)
                    db.session.add(c)
                    db.session.commit()
                
                
        user=session['user']
        allclass= classes.query.filter_by(user=user).all()
        
        return render_template('class.html', allclass =allclass)
        
    return render_template('class.html')

@app.route('/add_sub', methods=['GET','POST'])
def add_sub():
    if  g.user is  None:
        flash("Sign in to access")
        return render_template("register.html")

    else:
        if request.method=='POST':
            if not request.form['name']:
                    allassign = assign.query.all()
                    return render_template('add_sub.html', allsub=allsub)
            else:
                name=request.form["name"]
                user=session['user']
                exist = bool(subjects.query.filter_by( user=user,sname=name).first())
                if exist is False:
                    c=subjects(sname=name,user=user)
                    db.session.add(c)
                    db.session.commit()
        user=session['user']
        allsub= subjects.query.filter_by(user=user).all()
       
       
        return render_template('add_sub.html',allsub=allsub)
    return render_template('add_sub.html')

@app.route('/add_assign', methods=['GET','POST'])
def add_assign():
    if  g.user is  None:
        flash("Sign in to access")
        return render_template("register.html")

    else:
       
        if request.method=='POST':
            user=session['user']
            name=request.form["teacher"]
            t=Teachers.query.filter_by(user=user,name=name).first()
            cname=request.form['cname']
            c=classes.query.filter_by(user=user,cname=cname).first()
            sname=request.form["subject"]
            s=subjects.query.filter_by(user=user,sname=sname).first()
            weekc=request.form["weekc"]
            lort=request.form["lort"]
           
            ass=assign(teacher=t.name, cname=c.cname, sub=s.sname, weekc=weekc, lort=lort, user=user)
            db.session.add(ass)
            db.session.commit()

                
        user=session['user']
        allassign= assign.query.filter_by(user=user).all()
        allsub= subjects.query.filter_by(user=user).all()
        allTeachers= Teachers.query.filter_by(user=user).all()
        allclass= classes.query.filter_by(user=user).all()
        alltta = timetable.query.filter_by(user=user).all()
        teachers_name=[]
        for a in alltta:
            if a.teacher not in teachers_name:
                teachers_name+=[a.teacher]
       
        return render_template('add_assign.html',teachers_name=teachers_name,allassign= allassign, allsub=allsub ,  allclass = allclass , allTeachers=allTeachers)
    return render_template('add_assign.html')


@app.route('/other_teacher', methods=['GET','POST'])
def other_teacher():
    if  g.user is  None:
        flash("Sign in to access")
        return render_template("register.html")

    else:
       
        if request.method=='POST':
            user=session['user']
            name=request.form["name"]
           
            cname=request.form['cname']
            
            sname=request.form["subject"]
           
            day=request.form["day"]
            period=request.form["period"]
           
            alltt=timetable(teacher=name, cname=cname, sub=sname, day=day, period=period, user=user,lort="theory")
            db.session.add(alltt)
            db.session.commit()
                
        user=session['user']
        allassign= assign.query.filter_by(user=user).all()
        allsub= subjects.query.filter_by(user=user).all()
        allTeachers= Teachers.query.filter_by(user=user).all()
        allclass= classes.query.filter_by(user=user).all()

       
        return render_template('other_teacher.html',allassign= allassign, allsub=allsub ,  allclass = allclass , allTeachers=allTeachers)
    return render_template('other_teacher.html')


@app.route('/show')
def show():
    if  g.user is  None:
        flash("Sign in to access")
        return render_template("register.html")

    else:
        user=session['user']
        alltt = timetable.query.filter_by(user=user).all()
        teachers_name=[]
        for a in alltt:
            if a.teacher not in teachers_name:
                teachers_name+=[a.teacher]
        alltta = timetable.query.filter_by(user=user).all()
        class_name=[]
        for a in alltta:
            if a.cname not in class_name:
                class_name+=[a.cname]
        
        
        
        allsub= subjects.query.filter_by(user=user).all()
        allTeachers= Teachers.query.filter_by(user=user).all()
        allclass= classes.query.filter_by(user=user).all()
        alltime = Time_slot.query.filter_by(user=user).all()
       

    
        return render_template('show.html',class_name=class_name,teachers_name=teachers_name, alltt=alltt, allsub=allsub, allTeachers=allTeachers ,allclass=allclass, alltime = alltime )
    return render_template('show.html')
   
   
@app.route('/teacher_timetable/<t>')
def teacher_timetable(t):
    if  g.user is  None:
        
        return render_template("register.html")

    else:
        user=session['user']
        alltt = timetable.query.filter_by(user=user,teacher=t).all()
        days=["mon","tues","wed","thurs","fri"]
        t=t  
        user=session['user']
        alltta = timetable.query.filter_by(user=user).all()
        teachers_name=[]
        for a in alltta:
            if a.teacher not in teachers_name:
                teachers_name+=[a.teacher] 
        class_name=[]
        for a in alltt:
            if a.cname not in class_name:
                class_name+=[a.cname]
        subjects_name=[]
        for a in alltt:
            if a.sub not in subjects_name:
                subjects_name+=[a.sub]
        
        
        

    
        return render_template('teacher_timetable.html',subjects_name=subjects_name,class_name=class_name,t=t,teachers_name=teachers_name, alltt=alltt,days=days)
    #return render_template('teacher_timetable.html')
   
   
@app.route('/class_timetable/<c>')
def class_timetable(c):
    if  g.user is  None:
        flash("Sign in to access")
        return render_template("register.html")

    else:
        user=session['user']
        alltt = timetable.query.filter_by(user=user,cname=c).all()
        days=["mon","tues","wed","thurs","fri"]
        c=c  
        user=session['user']
        alltta = timetable.query.filter_by(user=user).all()
        class_name=[]
        teachers_name=[]
        subjects_name=[]
        for a in alltta:
            if a.cname not in class_name:
                class_name+=[a.cname]
        for a in alltta:
            if a.teacher not in teachers_name:
                teachers_name+=[a.teacher] 
        for a in alltt:
            if a.sub not in subjects_name:
                subjects_name+=[a.sub]
        

    
        return render_template('class_timetable.html',subjects_name=subjects_name,c=c,class_name=class_name, alltt=alltt,days=days)
    return render_template('class_timetable.html')
   


@app.route('/generate', methods=['GET','POST'])
def generate():
    if  g.user is  None:
        flash("Sign in to access")
        return render_template("register.html")

    else:
        
        teachers_name=[]
        class_name=[]
        user=session['user']
        allassign = assign.query.filter_by(user=user).all()
        problem = Problem( MinConflictsSolver()) 
        #c=pd.read_csv(r"C:\Users\ASUS\Pictures\extime\assign5.csv")
        c=assign.query.filter_by(user=user).all()
        df=pd.DataFrame([(r.teacher,r.cname,r.sub,r.weekc,r.lort)for r in c],columns=['teacher','cname','sub','weekc','lort'])
        #df=df[df["user"]==user]
    
        ce=df["cname"].tolist()
        c=[]
        df["teacher_type"]=df["teacher"].astype(str)+ "_"+ df["lort"].astype(str)
        df["s"]=df["sub"].astype(str)+"_"+df["lort"].astype(str)
        for j in ce:
            if j not in c:
                c.append(j)
        print("-------------------------------------------")
        

        
            # Define variables (e.g., courses, teachers, classes, and slots)
        days = [1,2,3,4,5]
            
        classes = c
        time_slots = [1,2,3,4,5]
        print(df)   
            # Assign variables and their domains
        for day in days:
                for class_ in classes:
                    cc=df[df["cname"]==class_]
                    t=cc['teacher'].tolist()
                    for slot in time_slots:
                        
                        
                        problem.addVariable(f"{day}_{class_}_{slot}", t)
                    
            # Ensure that each class has four slots, each slot is filled with a subject,
            # and each subject has a teacher assigned
            
        for day in days:
                    subject_vars =[]
                    
                    for class_ in classes:
                        #
                                subject_vars += [f"{day}_{class_}_1" ]
                                
                                problem.addConstraint(AllDifferentConstraint(), subject_vars)
        for day in days:
                    subject_vars =[]
                    
                    for class_ in classes:
                        #
                                subject_vars += [f"{day}_{class_}_2" ]
                                
                                problem.addConstraint(AllDifferentConstraint(), subject_vars)
        for day in days:
                    subject_vars =[]
                    
                    for class_ in classes:
                        #
                                subject_vars += [f"{day}_{class_}_3" ]
                                
                                problem.addConstraint(AllDifferentConstraint(), subject_vars)
        for day in days:
                    subject_vars =[]
                    
                    for class_ in classes:
                        #
                                subject_vars += [f"{day}_{class_}_4" ]
                                
                                problem.addConstraint(AllDifferentConstraint(), subject_vars)
        for day in days:
                    subject_vars =[]
                    
                    for class_ in classes:
                        
                                subject_vars += [f"{day}_{class_}_5" ]
                                
                                problem.addConstraint(AllDifferentConstraint(), subject_vars)
                               

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
                                
                                    var+=[f"{day}_{class_}_{slot}"]
                                    if((day==5) & (slot==5)):
                                        
                                        problem.addConstraint(constraint.SomeInSetConstraint([t[i]], n=w),(var))                                         
                                        print(t[i])
                                        print()
         #lab                                                  
        

        
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
                cn=df[df["cname"]==class_]
                ctrow=cn[cn["teacher"]==solutions[s]]
                sb=ctrow["s"].tolist()
                
                #lt=ctrow["lort"].tolist()
                #lort=lt[0]
                sb1=sb[0]
                sol=solutions[s]
                sub1=sb1.split("_")[0]
                lort=sb1.split("_")[1]
                print("sub1",sub1)
                check=timetable.query.filter_by( cname=class_, day=day, period=int(p),  user=user).first()
                if(check is None):
                    
                    tt=timetable(teacher=tl, cname=class_, sub=sub1, day=day, period=int(p), lort=lort, user=user)
                    db.session.add(tt)
                    db.session.commit()
                for i in solutions:
                     print(i,"----",solutions[i])   
            
        else:
            print("No solutions found.")

            
        #print(i)    

          #  tt=timetable(cname=random.choice(class_name),teacher=teachers_name[i],sub='er',period=i,day="mon")
           # db.session.add(tt)
            #db.session.commit()
        #alltt=timetable.query.filter_by(user=user).all()
        #allsub= subjects.query.filter_by(user=user).all()
        #allTeachers= Teachers.query.filter_by(user=user).all()
        #allclass= classes.query.filter_by(user=user).all()
        #alltime = Time_slot.query.filter_by(user=user).all()
       
        return redirect(url_for('show'))
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
        if g.user:
           return render_template('profile.html',user=session['user'])
        else:
            return redirect(url_for('login'))

    #return render_template('profile.html')

@app.before_request
def before_request():
    g.user=None
    
    if 'user' in session:
        g.user=session['user']

@app.route('/dropsession')
def dropsession():
        session.pop('user',None)
       
        return render_template('index11.html')
    


    
@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        if not request.form['title'] or not request.form['desc']:
            teacher = Teacher.query.filter_by(sno=sno).first()
            return render_template('update.html', teacher=teacher)
        
        else:
            title=request.form["title"]
            desc=request.form["desc"]
            teacher = Teacher.query.filter_by(sno=sno).first()
            teacher.title=title
            teacher.desc=desc
            db.session.add(teacher)
            db.session.commit()
            return redirect('/teacher')
    teacher = Teacher.query.filter_by(sno=sno).first()
    return render_template('update.html', teacher=teacher)




@app.route('/u/<int:sno>', methods=['GET','POST'])
def u(sno):
    if request.method=='POST':
        if not request.form['title'] or not request.form['desc']:
            room = Room.query.filter_by(sno=sno).first()
            return render_template('u.html', room=room)
        
        else:
       
            title=request.form["title"]
            desc=request.form["desc"]
            room = Room.query.filter_by(sno=sno).first()
            room.title=title
            room.desc=desc
            db.session.add(room)
            db.session.commit()
            return redirect('/classes')
    
    room = Room.query.filter_by(sno=sno).first()
    return render_template('u.html', room=room)

@app.route('/delete/<int:cid>')
def delete_class(cid):
    c = classes.query.filter_by(cid=cid).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/add_class")

@app.route('/delete2/<int:tid>')
def delete_teachers(tid):
    c = Teachers.query.filter_by(tid=tid).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/add")

@app.route('/delete3/<int:slot_id>')
def delete_time(slot_id):
    c = Time_slot.query.filter_by(slot_id=slot_id).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/add_time")

@app.route('/delete4/<int:aid>')
def delete_assign(aid):
    c = assign.query.filter_by(aid=aid).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/add_assign")

@app.route('/delete5/<int:sid>')
def delete_sub(sid):
    c = subjects.query.filter_by(sid=sid).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/add_sub")


@app.route('/delete0/<int:sno>')
def delete_teacher(sno):
    teacher = Teacher.query.filter_by(sno=sno).first()
    db.session.delete(teacher)
    db.session.commit()
    return redirect("/teacher")

@app.route('/delete1/<int:sno>')
def delete_class1(sno):
    room = Room.query.filter_by(sno=sno).first()
    db.session.delete(room )
    db.session.commit()
    return redirect("/classes")

@app.route('/show1')
def show1() :
    
    return redirect("/show")








if __name__=="__main__":
    app.run(debug=True, port=2210)
    