#!/bin/bash

echo "📊 Создаем новую таблицу для Member Tracker..."

cd "/root/beget_deployment 2"

# Создаем новую таблицу
source /root/bot_env/bin/activate
python3 -c "
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials1.json', scope)
client = gspread.authorize(creds)

# Создаем новую таблицу
spreadsheet = client.create('MemberTrackerTable')
print(f'Создана таблица: {spreadsheet.url}')

# Переименовываем лист и добавляем заголовки
worksheet = spreadsheet.get_worksheet(0)
worksheet.update_title('Members')
worksheet.update('A1:C1', [['User ID', 'Link Name', 'Join Date']])
print('Лист настроен с заголовками')
"

# Изменяем код member tracker
sed -i "s/SPREADSHEET_NAME = 'ShepoitBukmekera'/SPREADSHEET_NAME = 'MemberTrackerTable'/" bot.py
sed -i 's/worksheet("MemberTracking")/worksheet("Members")/' bot.py

echo "✅ Настройки применены"
echo "Invite Tracker → таблица 'ShepoitBukmekera'"
echo "Member Tracker → таблица 'MemberTrackerTable'"
