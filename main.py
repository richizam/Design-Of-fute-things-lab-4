import sys

import requests, pyttsx3, pyaudio, vosk
from reportlab.pdfgen import canvas
import json, os

tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')

for voice in voices:
    print(voice.name)
    if voice.name == 'Microsoft David Desktop - English (United States)':
        tts.setProperty('voice', voice.id)
model = vosk.Model('C:/Users/ricar/Desktop/vosk-model-small-ru-0.4')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format = pyaudio.paInt16,
                 channels = 1,
                 rate = 16000,
                 input = True,
                 frames_per_buffer = 8000)
stream.start_stream()

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow = False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']

def speak(say):
    tts.say(say)
    tts.runAndWait()

print('start')
pwd = ''
for text in listen():

    if text == 'создать':
        data_user = requests.get('https://randomuser.me/api/')
        data_user = data_user.json()
        data_user = data_user['results'][0]
        pdf = 'УСПЕШНО СОЗДАН НОВЫЙ ПОЛЬЗОВАТЕЛЬ'
        print(pdf)
        print()
        speak(pdf)
    elif text == 'имя':
        name = data_user['name'].values()
        name = ' '.join(map(str, name))
        print('Имя пользователя:', name)
        speak(name)
    elif text == 'страна':
        country = data_user['location']['country']
        print('Страна:', country)
        speak(country)
    elif text == 'анкета':
        print('************************************')
        print('***********************************\n')
        name = ' '.join(data_user['name'].values())
        ank = f'Имя пользователя: {name}'
        print(ank)
        speak(ank)
        gender = data_user['gender']
        ank = f'Пол: {gender}'
        print(ank)
        speak(ank)
        loc = data_user['location']
        country, city = loc['country'], loc['city']
        ank = f'Расположение: {country}, {city}'
        print(ank)
        speak(ank)
        email = data_user['email']
        ank = f'Электронная почта: {email}'
        print(ank)
        speak(ank)
        username = data_user['login']['username']
        ank = f'Никнейм: {username}'
        print(ank)
        speak(ank)
        password = data_user['login']['password']
        ank = f'Пароль: {password}'
        print(ank)
        speak(ank)
        print('************************************')
        print('***********************************\n')
    elif text == 'сохранить' or text == 'сохранит':
        path = data_user['picture']['large']
        pdf_path = 'answer.pdf'  # Path to save the PDF file
        link_text = 'Link to photo: {}'.format(path)
        c = canvas.Canvas(pdf_path)
        c.drawString(100, 100, link_text)
        c.save()

        print('Ответ сохранен в файле: {}'.format(pdf_path))

    elif text == 'закрыть'or text == 'закрыт':
        print('Программа завершена.')
        sys.exit()
    else:
        print(text)
