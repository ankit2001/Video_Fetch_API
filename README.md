# Video Fetch API
Tech Stack: DRF, Postgrest, Docker 

## Postgres Setup:
<p>Create a Postgresql database in the system  <br>
Add the credetings in .env file like .env.example or change the .env.example to .env <br>
Add credentials DB_USER, DB_PASS, DP_HOST, DB_NAME <br>
If you have no role assiged, make DB_USER as root <br>
You can follow the instructions here  https://www.postgresql.org/docs/9.0/sql-createdatabase.html </p>

## Environment setup:
<p>git clone https://github.com/ankit2001/Video_Fetch_API.git <br>
cd Video_Fetch_API <br>
sudo apt install python3 python3-pip or brew install python3 python3-pip<br> 
python3 -m venv ~/env <br>
source ~/env/bin/activate <br>
sudo -H pip install -r requirements.txt
(without -H in linux)</p>

(For below process, use python command if environment is activated otherwise python3)
## Migrations for models
<p>python manage.py migrate <br>
If it does not works, use remove the migrations in migrations folder and use below command <br>
python manage.py makemigrations </p>

## Run the server
<p>python manage.py process_tasks & python manage.py runserver <br>
process_tasks command for starting the background tasks in django and then it will start the server <br>
Not Get access to 127.0.0.1:8000 on web browser (As DEBUG=TRUE in this case) or using postman<br>
127.0.0.1:8000/admin for Django admin <br>
127.0.0.1:8000/api for using APIs</p>

## Building and Running with docker
<p>git clone https://github.com/ankit2001/Video_Fetch_API.git <br>
cd Video_Fetch_API <br>
sudo docker-compose build<br>
sudo docker-compose up <br>
sudo docker-compose -d up (for deattached mode)  <br>
(You can also modify the DB_USER, DP_PASS, POSTGRES_PASSWORD, POSTRES_USER in docker-compose.yml</p>


# Documentation to use the APIs
## Video_Fetch API
<p>Get request to following url: <br>
<b>127.0.0.1:8000/api/find_videos/</b> <br>
This URL also works on inbuilt collected static files for RestFramework <br>
You can sort and search query in options
You can also use 127.0.0.1:8000/admin for getting videos stored in admin portal also</p>

## Search API
<p>Get request to following url with parameters: <br>
<b>127.0.0.1:8000/api/search/</b> <br>
Searching is optimised with queryset bitwise operations. <br>
Ex: 127.0.0.1:8000/api/search?query=India&type=title <br>
You can change it to type=description also and if you provide simple <br>
Ex: 127.0.0.1:8000/api/search?query=India It will give results on both params. <br>
For adding string with multiple words having spaces. Either encode the string into URL or <br>
Just use it using (+) operator. <br>
Ex: India Wins => India+Wins <br>
127.0.0.1:8000/api/search?query=India+Wins&type=title <br>

You can add the API Keys from youtube to fetch_api/keys.txt or make a .env file and change the keys.txt in background_process.py to .env


