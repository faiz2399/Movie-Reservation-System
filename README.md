# Movie-Reservation-System
Built a movie reservation system with Flask Python API and MySQL database. Contains different MySQL script and Flask Application.

In order to run this project follow the following steps

# 1) Create a virtual Environment
a) Open your command prompt(cmd)\
b) conda create -n <name of your virtual environment> \
c) Once created active the environment using conda activate <virtual environement> 
  
# 2) Install the dependencies
 a) Once your environment is activated, change your directory to requirements.txt and run the following command on cmd 'pip install -r requirements.txt'(without quotes) \
 b) Now all the dependencies have been installed in your environment 
  
# 3) Connecting to MySQL Database 
 a)Open rhe app.py file \
 b) Goto the MySQL connecter part of the code, and enter your MySQL workbench credentials. \ (Make sure you put in the correct databse name)\
 c) Now you are all set.Run python app.py file. \
 d) After running the file, go to your web browser and type in the local host(usually: http://127.0.0.1:5000/ ) and you should see the welcome page. \
 e) In order to see the user's dashboard Register first and then enter the user's credentials on the Login Page
 f) In order to see the admin page type in username:admin, password: admin (You can also change admin credentials in the users table in the database) \ 
 g) The functions of different SQL scripts and working of different UI buttons is present in the project report present in this repository.
  
 
