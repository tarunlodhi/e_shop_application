# e_shop_application
Pre-Requirement
1.	Python
2.	PostgresSQL
How to run the Application
1.	Clone the Project From GitHub
git clone https://github.com/tarunlodhi/e_shop_application.git

2.	Inspect the Project Files

3.	Set Up a Virtual Environment
https://docs.python.org/3/library/venv.html

4.	Install the requirements
pip install -r requirements.txt

5.	Create a Database
Change settings.py inside the project

6.	Migrate Project to the Database
python manage.py makemigrations
python manage.py migrate
Note :- if table is not created in the database use this command  
python manage.py migrate –run-syncdb

7.	Run the Project
python manage.py runserver
