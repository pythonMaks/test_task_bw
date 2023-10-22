1 Для запуска СУБД PostgreSQL с помощью docker-compose:
- склонируйте репозиторий git clone https://github.com/pythonMaks/test_task_bw
- в файле docker-compose.yml замените данные для подключения к бд на желаемые:

 POSTGRES_USER: user

 POSTGRES_PASSWORD: password
 
 POSTGRES_DB: db_name

 - запустите СУБД с помощью команды 
 docker-compose up -d postgres


2 Для запуска веб-сервиса из второго задания:
- в файле main.py замените данные(user, password и db_name) в строке 
DATABASE_URL = "postgresql+asyncpg://user:password@postgres:5432/db_name"
на ваши данные для подключения к СУБД(см. п.1)
- запустите сервис с помощью команды
docker-compose up -d app

