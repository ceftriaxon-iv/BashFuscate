# ScriptFuscate
Simple script obfuscation toolkit, written in Python <br>
Простой обфускатор разных скриптов, написанный на Python <br>

# Obfuscation
Powershell: <br>
Converts the script into a base-64 cipher and a one-line decryptor of this very Base64 cipher <br>
Переделывает скрипт в шифр base-64 и однострочник-расшифровщик этого самого шифра base64

Batch: <br>
Replaces each character with a reference in the shuffled string <br>
Заменяет каждый символ на ссылку в перемешанной строке 

Bash: <br>
Replaces each character with a reference in the shuffled string <br>
Заменяет каждый символ на ссылку в перемешанной строке

# Requirements & Installation
To use this, you need Python 3 <br>
Чтобы это использовать, вам нужен будет Python 3 <br>
<br>
git clone https://github.com/ceftriaxon-iv/ScriptFuscate/  <br>
cd ScriptFuscate  <br>
python main.py -f (Script name with extension here, ex. thingamajong.ps1) -o (Output filename, optional)

# Warning
This was made by retard, and may break complex scripts with active function usage. Also in batch files there is limit on script size, and large scripts may become non-executable <br>
<br>
Это было сделано дауном, и может сломать исполнение сложных скриптов с активным использованием функций. Также в bat-файлах есть максимум на размер скрипта и большие скрипты могут стать нерабочими <br>

# TODO
- Усилить безопасность кода (всмысле запускаемость)
- Добавить удалятор комментариев еще и в batch/bash
- Добавить batch-файлам проверку на размер
