venv/scripts/activate
venv/bin/activate
Wenn permission denied: chmod +x venv/bin/activate

Wenn Umgebungsvariablen nicht gefunden werden, das ausführen:
set -a && source .env && set +a

pip install flask flask_migrate flask_login werkzeug celery kombu openai yfinance

python -m celery -A celery_config.celery_init.celery_app worker --purge
celery -A app.celery worker --loglevel=INFO -P gevent

which python
which celery
python -m celery -A celery_config.celery_init.celery_app worker --pool=solo --loglevel=info 
    wenn ENV_VARIABLES error: set -a && source .env && set +a

python -m venv venv
pip install -r requirements.txt

flask db init
flask db migrate -m 'Message'
flask db upgrade

pip freeze > requirements.txt

python
from app import app
from models import db
app.app_context().push()
db.create_all()
exit()

git init 
git add .
git commit -m 'Aenderungen'
git remote rename origin old-origin
git remote add origin (link)
git push -u origin main
- Procfile korrekt parsen
- Datenbankzugriff auf postgres umstellen
- Postgres und Redis Credentials überprüfen
- Key-System auf Heroku-Modus umstellen
- Datenbankveränderungen über GO propagieren

in cd sein bei Mac für heroku cli

wenn explorer oder anderes icon weg ist
Drücke Ctrl+Shift+P
Tippe: Views: Reset View Locations

Einzelne Scripts testen:
  set -a && source .env && set +a && python -m word_addin.call_api -> hier script als modul nennen
  python -m word_addin.word_addin_auth


pybael:
PYTHONPATH=. pybabel extract -F babel.cfg -k _l -o messages.pot .
PYTHONPATH=. pybabel update -i messages.pot -d translations
PYTHONPATH=. pybabel compile -d translations

Checkout GitHub Branch on previous Commit:
git checkout -b new-branch-name commit-id

heroku redis:maxmemory redis-polished-20433 --policy allkeys-lru --app olympai