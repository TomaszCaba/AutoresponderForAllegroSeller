#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install requests python-crontab datetime urllib3

echo "Zarejestruj aplikację w allegro."
echo "Nazwa aplikacji: autoresponder"
echo "Opis: -"
echo "Rodzaj aplikacji: Aplikacja ma dostęp do przeglądarki."
echo "Ścieżka przkekierowania: https://localhost:8000"
echo "Uprawnienia aplikacji: Zarządzanie wiadomościami"
echo "Link: https://apps.developer.allegro.pl.allegrosandbox.pl/"
echo "Podaj CLIENT_ID: "
read CLIENT_ID
echo "Podaj CLIENT_SECRET: "
read CLIENT_SECRET
python -m set_app_info "$CLIENT_ID" "$CLIENT_SECRET"
python -m set_crontab
python -m get_token
echo "Your allegro autoresponder had been installed successfully."

deactivate