docker build -t data_to_full_app .
docker run -d --name data_to_full_app -p 5432:5432 -p 6379:6379 -p 8080:8080 data_to_full_app
Start-Process "http://localhost:8888"
@REM para linux usar 'xdg-open http://localhost:8888'
@REM para parar o container 'docker stop meu-container'
@REM para remover o container 'docker rm meu-container'
