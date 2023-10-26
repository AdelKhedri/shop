virtualenv env 
source env/bin/activate
cd shop
pip install -r requirments.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

enter a phone number like 9123456789 10 number
enter a email
enter a username
enter اجازه ورود: True
enter password :
enter password egain: 
if password is easy enter Y to create user

python manage.py runserver

by defaul when a user created by the createsuperuser command , its dose not has a profile(but if it is created by thr sinup page profile created automaticaly).
so login to admin page:
after local address : oq39r71t!7i6i67w@2fbh4&iyi76*23r(8o7834t-)ry521_trh79a+gre67-wef%3D12ew[w233]2ew3{23eq%3B234WFEW2>234<23Q,/
127.0.0.1:8000/oq39r71t!7i6i67w@2fbh4&iyi76*23r(8o7834t-)ry521_trh79a+gre67-wef%3D12ew[w233]2ew3{23eq%3B234WFEW2>234<23Q,/

and go to پروفایل and create a profile for yourself.
so use this 2 links for map site:
127.0.0.1:8000/all
127.0.0.1:8000/profile/
