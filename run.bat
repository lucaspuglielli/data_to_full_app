python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
docker-compose up -d
@REM jupyter notebook "main.ipynb"
jupyter-lab "main.ipynb"
docker-compose down
deactivate
