
from flask import Flask,render_template, url_for,redirect,flash
from flask_mysqldb import MySQL
from flask.globals import request, session
from werkzeug.utils import validate_arguments
from login_req import driver_login_required,driver_vehicle_login_required,admin_login_required
import MySQLdb.cursors
import random,string
import datetime as dt

app =Flask(__name__)
app.secret_key= "preeth"

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="J@nagan1998"
app.config["MYSQL_DB"]="parking"

mysql=MySQL(app)

driver_id = None
vehicle_id = None

@app.route("/")
@app.route("/dashboard")
def dashboard():
    
    print(session)
    
    return render_template('dashboard.html')

@app.route('/driverlogin',methods= ['GET','POST'])
def driverlogin():
    if request.method == 'POST' and 'name' in request.form and 'ticket' in request.form:
        d_name = request.form['name']
        d_password = request.form['ticket']
        print(d_name,d_password)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
        cursor.execute (''' select ticket ,first_name,d.user_id ,vehicle_id from parking p
                                inner join transports t on t.parked_id = p.parked_id 
                                inner join driver d on d.user_id = t.user_id and p.ticket = %s and first_name =%s ''' 
                                ,(d_password,d_name))
        account = cursor.fetchone()
            
        if account:
            session["driverid"]=  account['user_id']
            session["driver_login"] = True
            # print(session["driverid"])
            session["vehicleid"] = account['vehicle_id']
            session['vehicle_login'] =True

            msg= "Sucessfully logged in {}".format(d_name)
            print(msg)
            return redirect(url_for('parking'))
    elif request.method == 'GET' :
        if 'driver_login' in session and session["driver_login"]:
            if 'vehicle_login' in session and session["driver_login"]:
                redirect(url_for("parking"))
            redirect(url_for('Vehicledetails'))
        
        
    return render_template('driverlogin.html')

@app.route("/User-Driver",methods=['GET','POST'])
def Userdetails():
    print(session)
    if request.method== 'POST' :
        fname= request.form["f_fname"]
        lname = request.form["f_lname"] 
        phoneno = request.form["f_phno"]
        phoneno='{:.0f}'.format(float(phoneno))
        location = request.form["f_location"]
        passengers = int(request.form["f_passengers"])


        print(fname,lname,phoneno,location,passengers,sep=" ")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # insert user details
        # sql = "insert into driver (first_name,last_name,phone_no,location,no_of_people) values (%s,%s,%s,%s,%s)"
        # val= [fname,lname,phoneno,location,passengers]
        cursor.execute("insert into driver (first_name,last_name,phone_no,location,no_of_people) values (%s,%s,%s,%s,%s)",(fname,lname,phoneno,location,passengers))
        # get user id

        sql = "SELECT user_id from driver where first_name = %(f_name)s and last_name =%(l_name)s"
        cursor.execute(sql,{'f_name':fname,'l_name':lname})
        driver_id = cursor.fetchone()
        
        mysql.connection.commit()
        if driver_id:        
            session["driverid"]= driver_id['user_id']
            session["driver_login"] = True
            return redirect(url_for("Vehicledetails"))
        else:
            print("db commit error")

    elif request.method == 'GET' and 'driver_login' in session and  session["driver_login"]:
        return redirect(url_for('Vehicledetails'))
            

         

    return render_template('driverdetails.html')

@app.route("/User-vehicle" ,methods=['GET','POST'])
@driver_login_required
def Vehicledetails():
    
    if request.method== 'POST' and request.form['f_model'] != "" and session["driver_login"]:
        fcompany= request.form["f_company"]
        fid = request.form["f_plate_no"] 
        fmodel = request.form["f_model"]
        
        print(fcompany,fid,fmodel,sep=" ")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # get vehicle model
        sql = " SELECT type_id from vehicle_type WHERE vehicle_model = %(v_model)s"
        cursor.execute(sql,{ 'v_model':fmodel })
        fmodel_id = cursor.fetchone()
        # insert vehicle details
        
       

        # sql ="INSERT into vehicle (company,plate_no,type_id) values (%s,%s,%s)"
        # val =[fcompany,fid,int(fmodel_id['type_id'])]
        cursor.execute("INSERT into vehicle (company,plate_no,type_id) values (%s,%s,%s)",(fcompany,fid,int(fmodel_id['type_id'])))

        # get vehicle id
        sql =" SELECT vehicle_id from vehicle where plate_no = %(f_plate)s and company = %(f_company)s"
        cursor.execute(sql,{ 'f_plate':fid,'f_company':fcompany })
        vehicle_id= cursor.fetchone()
        
        print(vehicle_id)
    
        mysql.connection.commit()

        if vehicle_id:
            print("vehicle registered")
            # add sessions
            session['vehicleid'] = vehicle_id['vehicle_id']
            session['vehicle_login'] =True
            did =session['driverid']
            print(did,vehicle_id['vehicle_id'])

            # assign user and vehicles together in db 
            # sql ="INSERT into transports (user_id,vehicle_id) values(%s,%s)"
            # val =[session['driverid'],vehicle_id]
            cursor.execute("INSERT into transports (user_id,vehicle_id) values(%s,%s)",(did,vehicle_id['vehicle_id']))
            mysql.connection.commit()
            print("inserted transports")

            return redirect(url_for('parking'))
        else:
            print("db error")
    # elif request.method == 'GET' and  'vehicle_login' in session and session['vehicle_login']:
    #     return redirect(url_for('parking'))
    



    return render_template('vehicledetails.html')



def park_my_car(did,vid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # check for existing
    sql =''' select ticket from parking p ,transports t
            where t.parked_id = p.parked_id and t.user_id = %(driverid)s
            and t.vehicle_id = %(vehicleid)s '''
    cursor.execute(sql,{'driverid':did,'vehicleid':vid})
    tkt=cursor.fetchone()
    print(tkt)
  
    
    
    if tkt != None:
        print("existing")
        print(tkt['ticket'])
        return tkt['ticket']
    # only for new user
    # inserted the vehicle and slot to the  allocates table
    print(did,vid)


    sql =''' Insert into allocates 
            select s.slot_id , v.vehicle_id from slot s ,vehicle_type t,vehicle v 
            where s.status ='Unoccupied' and t.type_id = v.type_id and 
            s.slot_type = t.vehicle_model and v.vehicle_id = %(vehicleid)s limit 1'''
    cursor.execute(sql,{'vehicleid':vid})
    print("updated allocates")
    # update the status of slot
    sql='''update slot s  inner join allocates a on a.slot_id = s.slot_id
            set status ="Occupied"   where   a.vehicle_id = %(vehicleid)s'''
    cursor.execute(sql,{'vehicleid':vid})
    print("updating time in and slot")
    mysql.connection.commit()
    # get transport id
    sql="select parked_id from transports where user_id = %(userid)s and vehicle_id = %(vehicleid)s"
    cursor.execute(sql, {'userid':did,'vehicleid':vid})
    allocate=cursor.fetchone()
    print(allocate)
    # insert to parking table with time in and parked id
    time_in= dt.datetime.now().strftime("%H:%M:%S")
    ticket =''.join(random.choice(string.ascii_uppercase ) for _ in range(2))+"".join(random.choice( string.digits) for _ in range(3))
    
    sql =''' select ticket from  parking where ticket = %(tkt)s'''
    cursor.execute(sql,{'tkt':ticket})
    records = cursor.fetchall()
    print(records)
    while len(records):
        ticket =''.join(random.choice(string.ascii_uppercase ) for _ in range(2))+"".join(random.choice( string.digits) for _ in range(3))
        sql =''' select ticket from  parking where ticket = %(tkt)s'''
        cursor.execute(sql,{'tkt':ticket})
        records = cursor.fetchall()

    # sql= ''' Insert into parking (ticket,time_in,parked_id) values (%s,%s,%s) '''
    # val =[ticket,time_in,allocate['parked_id']]
    print("inserted to parking")
    cursor.execute(''' Insert into parking (ticket,time_in,parked_id) values (%s,%s,%s) ''',(ticket,time_in,allocate['parked_id']))
    mysql.connection.commit()
    return ticket

def checkout_my_car(ticket):

  
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

      # check for existing 
    
    sql =''' select payment_id from payment
            where ticket = %(tkt)s '''
    cursor.execute(sql,{'tkt':ticket})
    pid=cursor.fetchone()
    print(pid)
  
    
    
    if pid != None:
        print("existing payment")
        return 

    sql = ''' select time_in,time_out from parking where ticket= %(tkt)s '''
    cursor.execute(sql,{'tkt':ticket})
    times = cursor.fetchone()
    frmt = '%H:%M:%S'
    dur = dt.datetime.strptime(times['time_out'],frmt) - dt.datetime.strptime(times['time_in'],frmt)

    minutes = round(dur.total_seconds() / 60,2)
    charge = round(minutes*0.5,2)
    status ="unpaid"
    # sql = ''' Insert into payment (charges,status,duration,ticket) values (:1,:2,:3,:4) '''
    # val =[charge,status,minutes,ticket]
 
    cursor.execute("Insert into payment (charges,status,duration,ticket) values (%s,%s,%s,%s)",(charge,status,minutes,ticket))
    # update slot status
    sql='''update slot s  inner join allocates a on a.slot_id = s.slot_id
    set status ="Unoccupied"   where  a.vehicle_id = %(vehicleid)s'''
    vid= session['vehicleid']
    cursor.execute(sql,{'vehicleid':vid})
    # delete from allocates
    sql=''' DELETE FROM allocates WHERE vehicle_id = %(vehicleid)s '''
    cursor.execute(sql,{'vehicleid':vid})
    mysql.connection.commit()
    


@app.route("/parking",methods=['POST','GET'])
@driver_vehicle_login_required
def parking():
    
    driver_id=session["driverid"]
    vehicle_id =session['vehicleid']
   
    tkt = park_my_car(driver_id,vehicle_id)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql='''select ticket, time_in, first_name, plate_no, vehicle_model, company from parking  p 
            inner join transports t on p.parked_id = t.parked_id and p.ticket = %(tkt)s
            inner join driver d on d.user_id = t.user_id  
            inner join vehicle v on v.vehicle_id = t.vehicle_id 
            inner join vehicle_type vt on  vt.type_id=v.type_id'''
    cursor.execute(sql,{'tkt':tkt})
    pdata=cursor.fetchone()
    
    sql='''  select slot_type, floor, direction1,direction2,direction3,status from parking p  
            inner join transports t on p.parked_id = t.parked_id and p.ticket=%(tkt)s
            inner join allocates a on a.vehicle_id= t.vehicle_id
            inner join slot s on s.slot_id = a.slot_id
            inner join path pt on pt.path_id = s.path_id'''      
    cursor.execute(sql,{'tkt':tkt})
    sdata=cursor.fetchone()
    sdata['floor']= int(sdata['floor'])
    
    
    session['paydata']= pdata
   
    session['slotdata']=sdata
    
    if request.method == 'GET'  :
        session["ticket"]=tkt
        sql =''' Select time_out,authority_id from parking where ticket =%(tkt)s '''
        cursor.execute(sql,{'tkt':tkt})
        chk = cursor.fetchone()
        print(chk)
       
        
        if chk['time_out'] != None and chk['authority_id'] != None:
            pdata['time_out'] = chk['time_out']
            session['paydata']= pdata
            print("check3")
            return redirect(url_for('checkout'))
        else:
            sdata['floor']= int(sdata['floor'])
            if chk['time_out'] == None:
                checkout_status ="Check Out"
                print("check1")
                # print(pdata,sdata)
                return render_template('parking.html',pdata=pdata,sdata=sdata, checkout_status = checkout_status)
            elif chk['time_out'] != None and chk['authority_id'] == None:
                print("check2")
                pdata['time_out'] = chk['time_out']
                session['paydata']= pdata
                checkout_status="Checking Out"
                return render_template('parking.html',pdata=pdata,sdata=sdata, checkout_status = checkout_status)
        
           
    elif request.method == 'POST':
        if request.form['status'] == "Check Out":
            print("checking out")
            time_out= dt.datetime.now().strftime("%H:%M:%S")
            print(time_out,tkt)

            sql=''' update parking set time_out = %(timeout)s where ticket = %(tkt)s'''
            cursor.execute(sql,{'timeout':time_out,'tkt':tkt} )

            mysql.connection.commit()
            print("commited")
            print(session)
            return redirect(url_for('parking'))
        else:
            return redirect(url_for('parking'))
    return render_template('parking.html')

@app.route("/checkout", methods =['POST','GET'])
@driver_vehicle_login_required
def checkout():
    ticket =session['ticket']
    checkout_my_car(ticket)
    pdata = session['paydata']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql= ''' select duration,charges from payment where ticket= %(tkt)s '''
    cursor.execute(sql,{'tkt':ticket})
    ydata= cursor.fetchone()
    print(pdata)

    if request.method == 'GET':
        sql =''' Select status,authority_id from payment where ticket =%(tkt)s '''
        cursor.execute(sql,{'tkt':ticket})
        chk = cursor.fetchone()
        if chk['status'] == 'unpaid':
            pay_status = "Pay"
            return render_template('checkout.html',pdata=pdata,ydata=ydata,pay_status = pay_status)
        elif chk['status'] == 'paid' and chk['authority_id'] == None:
            pay_status="paying"
            return render_template('checkout.html',pdata=pdata,ydata=ydata,pay_status = pay_status)
        # thank you page
        else:
            pay_status='paid'

            return render_template('checkout.html',pdata=pdata,ydata=ydata,pay_status = pay_status)
    elif request.method == 'POST':
        if request.form['status'] == "Pay":
            sql=''' update payment set status = 'paid' where ticket = %(tkt)s '''
            cursor.execute(sql,{'tkt':ticket} )
            mysql.connection.commit()
            return redirect(url_for('parking'))
    return render_template('checkout.html')

@app.route("/driverlogout",methods =["POST", "GET"])
@driver_vehicle_login_required
def driverlogout():
    session.pop("driverid",None)
    session.pop("driver_login",None) 
    session.pop("vehicleid",None)
    session.pop("vehicle_login",None)
    session.pop('paydata',None)
    session.pop("ticket",None)
    session.pop('slotdata',None)
    return redirect(url_for('dashboard'))



@app.route("/admin-login", methods =['POST','GET'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        admin_name = request.form['username']
        admin_password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute (" SELECT * FROM admin WHERE admin_name= %s and password = %s " ,(admin_name,admin_password))
        account = cursor.fetchone()
        if account:
            session["admin"]= account["admin_name"]
            session["admin_login"] = True
            session["admin_id"] = account["authority_id"]
            msg= "Sucessfully logged in {}".format(admin_name)
            print(msg)
            return redirect('/requests')


    return render_template('adminlogin.html')

@app.route("/adminlogout",methods =["POST", "GET"])
@admin_login_required
def adminlogout():
    
    session.pop("admin",None)
    session.pop("admin_login",None)
    session.pop("admin_id",None)
    
    return redirect(url_for("login"))

@app.route("/requests",methods =['POST','GET'])
@admin_login_required
def park_details():
    admin = session['admin_id']
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = '''SELECT row_number() over()  as id, u.first_name,v.plate_no,v.company,p.ticket,p.time_in,p.time_out
                    FROM driver u, vehicle v, parking p,transports t 
                    WHERE  t.parked_id =p.parked_id and u.user_id = t.user_id and v.vehicle_id = t.vehicle_id 
                        and p.time_out is not null and p.authority_id is null '''
                
        cursor.execute(sql)
        parkdata= cursor.fetchall()
        sql2 ='''SELECT   row_number() over() as id , u.first_name,v.plate_no,v.company, d.ticket ,d.duration,d.charges,d.status
                    FROM  payment d , parking p , transports t , driver u, vehicle v
                    WHERE  p.ticket =d.ticket and t.parked_id =p.parked_id and u.user_id = t.user_id
                        and v.vehicle_id= t.vehicle_id and  d.authority_id is null  '''
        cursor.execute(sql2)
        paydata = cursor.fetchall()
    except:
            print("DB connection Error")
    if request.method== 'GET':
        return render_template('admindetails.html',paydata=paydata,parkdata=parkdata)

    elif request.method== 'POST':
        if 'pay' in request.form:
            req_tkt = request.form['pay']
            sql = ''' update payment set authority_id = %(id)s where ticket = %(tkt)s '''
            cursor.execute(sql,{'id': admin,'tkt':req_tkt})
            mysql.connection.commit()

        elif 'park' in request.form:
            req_tkt = request.form['park']
            sql = ''' update parking set authority_id = %(id)s where ticket = %(tkt)s '''
            cursor.execute(sql,{'id': admin,'tkt':req_tkt})
            mysql.connection.commit()
        return redirect(url_for('park_details'))
    return render_template('admindetails.html',paydata=paydata,parkdata=parkdata)


if __name__ == '__main__':
    app.run(debug=True)