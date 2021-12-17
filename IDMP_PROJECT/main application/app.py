

#############################################################################
### Importing the required libraries and packages requiredfor the project ###
#############################################################################

from myproject import app,db
from flask import render_template, redirect, request, url_for, flash,abort, send_file
from flask_login import login_user,login_required,logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm, Book, AdminForm, DelStatus, UpStatus, TakeDate, TakeMovie, UserInfo, UserCancel
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, text
import io
import base64
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd

#############################################################################
### Importing the required SQL libraries to connect with python and Flask ###
#############################################################################

from mysql.connector import connect, Error
from getpass import getpass


#############################################################################
### Connecting with the local MYSQL Database ###
### Enter your Database name and password between the codes ###
#############################################################################

conn = connect(host = 'localhost',user = 'root',password = '',database = '') #


#############################################################################
### Routing to the homepage and showing the home.html template ###
#############################################################################

@app.route('/')
def home():
    return render_template('home.html')

########################################################################################

### Below function and decorator  routes to the visualization tab on the admin page ###
### @login_required - ensures that the user or admin is logged in before seeing the views ###

#########################################################################################

@app.route('/visualize',methods=['GET', 'POST'])
@login_required
def visualize():
    return render_template('visualize.html')


#######################################################################################
### Below function allows users to view the cancellation page and cancel the tickets ###
#########################################################################################

@login_required
@app.route('/user_cancel',methods=['GET', 'POST'] )
def user_cancel():

    #######################################################################################
    ### form is an object of UserCancel class from form.py file###
    #########################################################################################

    form =UserCancel()

        #######################################################################################
        ### Calling the cancellation stored procedure using python by extracting data from forms ###
        #########################################################################################

    if form.validate_on_submit():
        with conn.cursor() as cursor:
            cursor.callproc('cancellation',(form.book_id.data,form.schedule_id.data))
            conn.commit()

        return render_template('cancel.html', form=form)



    return render_template('user_cancel.html', form=form)

#######################################################################################
### Below function allows admin to view the actual plots, which are plotted using seaborn ###
#########################################################################################


@app.route('/visualize_plot')
@login_required

def visualize_plot():

    fig, ax  = plt.subplots(figsize=(10,6))
    ax = sns.set_style(style = "darkgrid")
    x1 = [i for i in range(100)]
    y1 = [j for j in range(100)]
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM movie")
        myresult=cursor.fetchall()
        year = []
        for elem in myresult:
            year.append(int(elem[4]))

        df = pd.DataFrame({'year':year})



    plt.subplot(1,2,1)
    plt.title('Histogram of top movies by year')
    sns.histplot(data=df, x='year',bins = 20)

    #######################################################################################
    ### Extracting information for the plot from the databsse ###
    #########################################################################################

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM movie")
        myresult_pie=cursor.fetchall()

        labels = ['Drama','Comedy', 'Action','Fantasy','Horror', 'Romance' ,'Western','Thriller']
        list_new = []
        for elem in myresult_pie:
            list_new.append(elem[5])

            df_pie = pd.DataFrame({'genre': list_new})


    #######################################################################################
    ### Plotting the charts using seaborn ###
    #########################################################################################

    df_pie = df_pie.value_counts().rename_axis('unique_values').reset_index(name='counts')
    labels = df_pie['unique_values'].tolist()
    data = df_pie['counts'].tolist()
    colors = sns.color_palette('bright')[0:8]
    plt.subplot(1,2,2)
    plt.title('Genres of top 250 movies')
    plt.pie(data , labels=labels, colors =colors, autopct='%1.1f%%')


    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='img/png')



#######################################################################################
### Below function allows user to book the tickets ###
#########################################################################################

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = Book()
    if form.validate_on_submit():
        #######################################################################################
        ### Calling the transaction 'add_booking_transaction'  ###
        #########################################################################################
        with conn.cursor() as cursor:
            cursor.callproc('add_booking_transaction',(form.schedule.data,form.username.data))
            conn.commit()
        return render_template('confirmation.html', form=form)
    return render_template('book.html', form=form)


#######################################################################################
### Below gives view for the admin page to add a movie to the schedule ###
#########################################################################################

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    form = AdminForm()
    if form.validate_on_submit():
        with conn.cursor() as cursor:
            cursor.callproc('create_show',(form.movie_id.data,form.date.data, form.time.data))
            conn.commit()

            return render_template('confirm_admin.html',form=form)

    return render_template('admin.html',form=form)

#######################################################################################
### Below gives view to admin to administer the active movie counts ###
#########################################################################################

@app.route('/show_count', methods=['GET', 'POST'])
@login_required
def show_count():

    with conn.cursor() as cursor:
        cursor.execute("Select active_mov()")
        result=cursor.fetchall()

    return render_template('show_count.html',result=result)

#######################################################################################
### Below gives view to admin to administer the revenue of movie per day ###
#########################################################################################

@app.route('/show_revenue', methods=['GET', 'POST'])
@login_required
def show_revenue():
    form = TakeDate()
    if form.validate_on_submit():
        data = form.date.data

        with conn.cursor() as cursor:
            cursor.execute("Select revenue_at_particular_day(%s)",(data,))
            result=cursor.fetchall()

            return render_template('show_revenue.html',result=result)

    return render_template('take_date.html',form=form)


#######################################################################################
### Below gives view to admin to administer the revenue of movie according to movie name ###
#########################################################################################

@app.route('/show_revenue_movie', methods=['GET', 'POST'])
@login_required
def show_revenue_movie():
    form = TakeMovie()
    if form.validate_on_submit():
        data = form.movie_name.data

        with conn.cursor() as cursor:
            cursor.execute("Select revenue_of_movie(%s)",(data,))
            result=cursor.fetchall()

            return render_template('show_revenue_movie.html',result=result, data=data)

    return render_template('take_movie.html',form=form)


#######################################################################################
### Below gives view to admin to clear the statuses of the movie ###
#########################################################################################

@app.route('/delete_status', methods=['GET', 'POST'])
@login_required
def delete_status():
    form = DelStatus()
    if form.validate_on_submit():
        with conn.cursor() as cursor:
            cursor.callproc('delete_status',())
            conn.commit()

            return render_template('confirm_admin.html',form=form)

    return render_template('delete_status.html',form=form)

#######################################################################################
### Below gives view to admin to update the status of the movies to A  ###
#########################################################################################
@app.route('/update_status', methods=['GET', 'POST'])
@login_required
def update_status():
    form = UpStatus()
    if form.validate_on_submit():
        with conn.cursor() as cursor:
            cursor.callproc('update_status',(form.movie_id.data,))
            conn.commit()

            return render_template('confirm_admin.html',form=form)

    return render_template('update_status.html',form=form)







@app.route('/user_info',  methods=['GET', 'POST'])
@login_required

def user_info():

    form = UserInfo()

    if form.validate_on_submit():

        user_name  = form.user_name.data

        lst = []
        with conn.cursor() as cursor:
            cursor.callproc('BOOKING', (user_name, ))
            results = cursor.stored_results()

            for result in results:
                for course in result.fetchall():
                    lst.append(course)
            return render_template('user_info_display.html', lst=lst)

    return render_template('user_info.html',form =form)

@app.route('/schedule')
@login_required
def schedule():

    with conn.cursor() as cursor:
        cursor.execute('Select * from display_schedule')
        result = cursor.fetchall()
    return render_template('schedule.html', result=result)

@app.route('/display_actors')
@login_required
def display_actors():

    with conn.cursor() as cursor:
        cursor.execute('Select * from display_actors')
        result = cursor.fetchall()
    return render_template('display_actor.html', result=result)


@app.route('/display_user')
@login_required
def display_user():

    with conn.cursor() as cursor:
        cursor.execute('Select * from display_user')
        result = cursor.fetchall()
    return render_template('display_admin_user.html', result=result)


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        if user.admin_check == 'Y' and user.password == form.password.data:
            login_user(user)

            return redirect(url_for('admin'))


        # Check that the user was supplied and the password is right


        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # if next == None or next[0] == '/schedule':
            #     next = url_for('schedule')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():




        # Here Call the Stored Proceedure and make form.email.data, form.username.data as arguments
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)


        with conn.cursor() as cursor:


            cursor.callproc('login_proc',(user.email,user.username,user.password))
            conn.commit()

        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
