python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
docker-compose up -d
jupyter notebook "main.ipynb"
@REM jupyter-lab "main.ipynb"
docker-compose down
deactivate
