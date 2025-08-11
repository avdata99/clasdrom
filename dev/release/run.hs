# failing because it look like heroku run this in a different environment
pip install -r requirements.prod.txt
cd cdrom
python manage.py migrate
