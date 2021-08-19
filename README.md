# Video Fetch API
Tech Stack: DRF, Postgrest, Docker 

- Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- A basic search API to search the stored videos using their title and description.
- Dockerize the project.
- It should be scalable and optimised.
- Add support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.
- Make a dashboard to view the stored videos with filters and sorting options (optional)
- Optimise search api, so that it's able to search videos containing partial match for the search query in either video title or description.
    - Ex 1: A video with title *`How to make tea?`* should match for the search query `tea how`

## Postgres Setup:
```Create a Postgresql database in the system  
Add the credetings in .env file like .env.example or change the .env.example to .env 
Add credentials DB_USER, DB_PASS, DP_HOST, DB_NAME 
If you have no role assiged, make DB_USER as root 
You can follow the instructions here  https://www.postgresql.org/docs/9.0/sql-createdatabase.html 
```

## Environment setup:

```
git clone https://github.com/ankit2001/Video_Fetch_API.git 
cd Video_Fetch_API 
sudo apt install python3 python3-pip or brew install python3 python3-pip\
python3 -m venv ~/env 
source ~/env/bin/activate 
sudo -H pip install -r requirements.txt
(without -H in linux)
```

(For below process, use python command if environment is activated otherwise python3)
## Migrations for models
```
python manage.py migrate 
If it does not works, use remove the migrations in migrations folder and use below command 
python manage.py makemigrations 
```

## Run the server
```
python manage.py process_tasks & python manage.py runserver 
process_tasks command for starting the background tasks in django and then it will start the server 
Not Get access to 127.0.0.1:8000 on web browser (As DEBUG=TRUE in this case) or using postman
127.0.0.1:8000/admin for Django admin 
127.0.0.1:8000/api for using APIs
```

## Building and Running with docker
```
git clone https://github.com/ankit2001/Video_Fetch_API.git 
cd Video_Fetch_API 
sudo docker-compose build
sudo docker-compose up 
sudo docker-compose -d up (for deattached mode)  
(You can also modify the DB_USER, DP_PASS, POSTGRES_PASSWORD, POSTRES_USER in docker-compose.yml
```


# Documentation to use the APIs

## Swagger Documentation
```
Check out the link 127.0.0.1:8000/api/swagger/ for documentation, as the apis has swagger support
```
## Video_Fetch API

**Get request to following url:**
```
127.0.0.1:8000/api/find_videos/

This URL also works on inbuilt collected static files for RestFramework 
You can sort and search query in options
```
**You can also use 127.0.0.1:8000/admin for getting videos stored in admin portal also**

## Search API
**Get request to following url with parameters:**
```
127.0.0.1:8000/api/search/
Searching is optimised with queryset bitwise operations. 
Ex: 127.0.0.1:8000/api/search?query=India&type=title 
```

**You can change it to type=description also and if you provide simple** 

```
Ex: 127.0.0.1:8000/api/search?query=India It will give results on both params. 
For adding string with multiple words having spaces. Either encode the string into URL or 
Just use it using (+) operator. 
Ex: India Wins => India+Wins 
127.0.0.1:8000/api/search?query=India+Wins&type=title 
```
**You can add the API Keys from youtube to fetch_api/keys.txt or make a .env file and change the keys.txt in background_process.py to .env**


