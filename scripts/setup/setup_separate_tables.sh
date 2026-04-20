#!/bin/bash

echo "🔄 Настраиваем отдельные таблицы..."

# Исправляем member tracker код
cd "/root/beget_deployment 2"
sed -i "s/SPREADSHEET_NAME = 'MemberTracking'/SPREADSHEET_NAME = 'ShepoitBukmekera'/" bot.py
sed -i 's/worksheet("Participants")/worksheet("MemberTracking")/' bot.py

# Создаем лист MemberTracking
source /root/bot_env/bin/activate
python3 -c "
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials1.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('ShepoitBukmekera')

try:
    spreadsheet.worksheet('MemberTracking')
    print('Лист MemberTracking уже существует')
except:
    spreadsheet.add_worksheet(title='MemberTracking', rows=1000, cols=4)
    print('Лист MemberTracking создан')
"

echo "✅ Настройки применены"
