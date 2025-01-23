from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask_login import login_required, current_user, logout_user
from .datamodels import User,Admin,Audio ,Uploadannouncement, Baptismbooking, Confirmationbooking, Massbooking, Uploadreading, get_pdf_for_date, get_pdf_for_dateannouncement
from . import db
from datetime import datetime
from flask_login import login_required, current_user, login_user
from werkzeug.utils import secure_filename
import os
import io
from io import  BytesIO


views = Blueprint('views', __name__)

#ADMIN VIEWS
@views.route('/adminlogout')
@login_required
def adminlogout():
    return redirect(url_for('views.adminhome'))



@views.route('/adminhome')
def adminhome():
    return render_template('admin/admin_admin_home.html')

    
@views.route('/registeradmin', methods=['GET','POST'])
@login_required
def registeradmin():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        designation = request.form.get('designation')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password1 = request.form.get('password')

        new_admin = Admin(
            first_name=firstname,
            last_name=lastname,
            designation=designation,
            email=email,
            password=password1,
            phone=phone
        )

        db.session.add(new_admin)
        db.session.commit()

        return redirect(url_for('views.adminhome'))

    return render_template('admin/admin_register_admin.html')


@views.route('/registeruser', methods=['GET','POST'])
@login_required
def registeruser():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        group = request.form.get('group')
        scc = request.form.get('scc')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password1 = request.form.get('password')

        new_user = User(
            first_name=firstname,
            last_name=lastname,
            group=group,
            small_christian_community=scc,
            password=password1,
            phone=phone
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('views.userhome'))
    return render_template('admin/admin_register_user.html')

@views.route('/baptismbookings', methods=['GET','POST'])
@login_required
def baptismbookings():
    if request.method=='GET':
        baptismbooking=Baptismbooking.query.all()
    return render_template('admin/baptism_bookings.html', baptismbooking=baptismbooking)

@views.route('/confirmationbooking', methods=['GET','POST'])
@login_required
def confirmationmbookingbookings():
    if request.method == 'GET':
        confirmationbooking=Confirmationbooking.query.all()
    return render_template('admin/confirmation_bookings.html', confirmationbooking=confirmationbooking)

@views.route('/massbookings', methods=['GET', 'POST'])
@login_required
def massbookings():
    if request.method == 'GET':
        massbooking=Massbooking.query.all()
    return render_template('admin/mass_bookings.html', massbooking=massbooking)


@views.route('/manageusers', methods=['GET','POST'])
@login_required
def manageusers():
    if request.method == 'GET':
        user=User.query.all()
    return render_template('admin/manage_users.html', user=user)

@views.route('/checktithe')
@login_required
def checktithe():
    return render_template('admin/tithe_management.html')

@views.route('/adminlogin', methods=['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        admin = Admin.query.filter_by(email=email).first()
        if admin:
            if password == admin.password:
                login_user(admin, remember=True)
                return redirect(url_for('views.adminhome'))
            else:
                return f'Incorrect password'
        else:
            return f'Incorrect email'
        
    return render_template('admin/admin_admin_login.html')


@views.route('/adminsignup', methods=['GET','POST'])
def adminsignup():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        designation = request.form.get('designation')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password1 = request.form.get('password')

        new_admin = Admin(
            first_name=firstname,
            last_name=lastname,
            designation=designation,
            email=email,
            password=password1,
            phone=phone
        )

        db.session.add(new_admin)
        db.session.commit()
        login_user(new_admin, remember=True)

        return redirect(url_for('views.adminhome'))

    return render_template('admin/admin_admin_signup.html')

@views.route('/postreading', methods=['GET','POST'])
@login_required
def postreading():
    if request.method == 'POST':
        date_str= request.form.get('date')

        file=request.files['file']
        pdf_data=file.read()
        date=datetime.strptime(date_str, '%Y-%m-%d')

        new_reading=Uploadreading(date=date, pdf_data=pdf_data, filename=file.filename)
        db.session.add(new_reading)
        db.session.commit()

        return f'Reading sent successfully'
    return render_template('admin/upload_readings.html')


@views.route('/postannouncement', methods=['GET','POST'])
@login_required
def post_announcement():
    if request.method == 'POST':
        date_str = request.form.get('date')

        file = request.files['file']
            # Save the binary data of the file to the database
        pdf_data = file.read()
        date = datetime.strptime(date_str, '%Y-%m-%d')

            # Save information to the database
        announcement = Uploadannouncement(date=date, pdf_data=pdf_data, filename=file.filename)
        db.session.add(announcement)
        db.session.commit()

            #flash('File uploaded successfully.', 'success')
            #return redirect(url_for('views.home'))  # Redirect to some route after a successful upload
        #else:
            #flash('Invalid file format.', 'error')
            #return render_template('/admin/upload_announcement.html')
        return f'Uploaded:{file.filename}'

    return render_template('/admin/upload_announcement.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['ALLOWED_EXTENSIONS']


#USER VIEWS
@views.route('/')
def userhome():
    return render_template('user/user_home.html')

@views.route('/userlogout')
@login_required
def userlogout():
    return redirect(url_for('views.userhome'))


@views.route('/aboutus')
def aboutus():
    return render_template('user/user_about_us.html')


@views.route('/worship')
@login_required
def worship():
    return render_template('user/worship.html')

@views.route('/ministries')
@login_required
def ministries():
    return render_template('user/ministries.html')

@views.route('/events')
@login_required
def events():
    return render_template('user/events.html')

@views.route('/donateoffertory')
@login_required
def donateoffertory():
    return render_template('user/donate_offering.html')

@views.route('/donatetithe')
@login_required
def donatetithe():
    return render_template('user/donate_tithe.html')


@views.route('/userbaptismbooking', methods=['GET','POST'])
@login_required
def userbaptismbooking():
    if request.method =='POST':
        candidate_firstname=request.form.get('candidate_firstname')
        candidate_lastname=request.form.get('candidate_lastname')
        candidate_age=request.form.get('candidate_age')
        date_str=request.form.get('date')
        guardian_firstname=request.form.get('guardian_firstname')
        guardian_lastname=request.form.get('guardian_lastname')
        guardian_phone=request.form.get('guardian_phone')

        father_firstname=request.form.get('father_firstname')
        father_lastname=request.form.get('father_lastname')
        father_phone=request.form.get('father_phone')

        mother_firstname=request.form.get('mother_firstname')
        mother_lastname=request.form.get('mother_lastname')
        mother_phone=request.form.get('mother_phone')
        
        date = datetime.strptime(date_str, '%Y-%m-%d')
        new_baptismbooking=Baptismbooking(candidate_f_name=candidate_firstname, candidate_l_name=candidate_lastname, candidate_age=candidate_age, date=date, guardian_f_name=guardian_firstname, guardian_l_name=guardian_lastname, guardian_phone=guardian_phone, father_f_name=father_firstname, father_l_name=father_lastname, father_phone=father_phone, mother_f_name=mother_firstname, mother_l_name=mother_lastname, mother_phone=mother_phone)
        db.session.add(new_baptismbooking)
        db.session.commit()
        return f'Booking sent!'

    return render_template('user/baptism_booking.html')


@views.route('/usermassbooking', methods=['GET','POST'])
@login_required
def usermassbooking():
    if request.method == 'POST':
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        scc=request.form.get('scc')
        phone=request.form.get('phone')
        date_str=request.form.get('date')

        date= datetime.strptime(date_str, '%Y-%m-%d')

        new_massbooking=Massbooking(f_name=firstname, l_name=lastname, scc=scc, phone=phone, date=date)
        db.session.add(new_massbooking)
        db.session.commit()
        return f'Mas Booking sent'
    
    return render_template('user/mass_booking.html')



@views.route('/userconfirmationbooking', methods=['GET','POST'])
@login_required
def userconfirmationbooking():
    if request.method =='POST':
        candidate_firstname=request.form.get('candidate_firstname')
        candidate_lastname=request.form.get('candidate_lastname')
        candidate_age=request.form.get('candidate_age')
        date_str=request.form.get('date')
        guardian_firstname=request.form.get('guardian_firstname')
        guardian_lastname=request.form.get('guardian_lastname')
        guardian_phone=request.form.get('guardian_phone')

        father_firstname=request.form.get('father_firstname')
        father_lastname=request.form.get('father_lastname')
        father_phone=request.form.get('father_phone')

        mother_firstname=request.form.get('mother_firstname')
        mother_lastname=request.form.get('mother_lastname')
        mother_phone=request.form.get('mother_phone')
        
        date = datetime.strptime(date_str, '%Y-%m-%d')
        new_confirmationbooking=Confirmationbooking(candidate_f_name=candidate_firstname, candidate_l_name=candidate_lastname, candidate_age=candidate_age, date=date, guardian_f_name=guardian_firstname, guardian_l_name=guardian_lastname, guardian_phone=guardian_phone, father_f_name=father_firstname, father_l_name=father_lastname, father_phone=father_phone, mother_f_name=mother_firstname, mother_l_name=mother_lastname, mother_phone=mother_phone)
        db.session.add(new_confirmationbooking)
        db.session.commit()
        return f'Booking sent!'
    return render_template('user/confirmation_bookings.html')


@views.route('/userlogin', methods=['GET','POST'])
def userlogin():
    if request.method == 'POST':
            phone = request.form.get('phone')
            password = request.form.get('password')

            user = User.query.filter_by(phone=phone).first()
            if user:
                if password == user.password:
                    login_user(user, remember=True)
                    return redirect(url_for('views.userhome'))
                else:
                    return f'Incorrect password'
            else:
                return f'Incorrect phone'
    return render_template('user/user_login.html')

@views.route('/usersignup', methods=['GET','POST'])
def usersignup():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        group = request.form.get('group')
        scc = request.form.get('scc')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password1 = request.form.get('password')

        new_user = User(
            first_name=firstname,
            last_name=lastname,
            group=group,
            small_christian_community=scc,
            password=password1,
            phone=phone
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)

        return redirect(url_for('views.userhome'))
    return render_template('user/user_signup.html')


@views.route('/getreadings', methods=['GET','POST'])
@login_required
def getreadings():
    if request.method == 'POST':
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d')

        pdf_data = get_pdf_for_date(date)
        if pdf_data and pdf_data.pdf_data:
            # Use BytesIO to create a file-like object from the bytes data
            pdf_bytes_io = BytesIO(pdf_data.pdf_data)

            response = send_file(
                pdf_bytes_io,
                as_attachment=True,
                download_name=f'readings_{date}.pdf',
                mimetype='application/pdf'
            )
            return response

    return render_template('user/readings.html')

def get_pdf_for_date(date):
    return Uploadreading.query.filter_by(date=date).first()

@views.route('/weeklyannouncements', methods=['GET','POST'])
@login_required
def weekly_announcements():
    if request.method == 'POST':
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d')

        pdf_data = get_pdf_for_dateannouncement(date)
        if pdf_data and pdf_data.pdf_data:
            # Use BytesIO to create a file-like object from the bytes data
            pdf_bytes_io = BytesIO(pdf_data.pdf_data)

            response = send_file(
                pdf_bytes_io,
                as_attachment=True,
                download_name=f'announcement_{date}.pdf',
                mimetype='application/pdf'
            )
            return response

    return render_template('user/announcements.html')



@views.route('/get_audio/<int:audio_id>')
def get_audio(audio_id):
    audio_list = Audio.query.all()
    audio = Audio.query.get_or_404(audio_id)
    return send_file(io.BytesIO(audio.audio_data), mimetype='audio/mpeg', audio_list=audio_list)


@views.route('/uploadaudio',methods=['GET','POST'])
def uploadaudio():
    if request.method == 'POST':
        audio_file = request.files['audio_file']
        audio_name = request.form['audio_name']

        new_audio = Audio(name=audio_name, audio_data=audio_file.read())
        db.session.add(new_audio)
        db.session.commit()
        return f'Audio uploaded successfully:{audio_file.filename}'

    return render_template('admin/upload_audio.html')

def accepted_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['Accepted_Extensions']




