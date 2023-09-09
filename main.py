import telebot
import requests
import os
import subprocess

token = 'secret'
root_path = '/home/scemer/navidrome/music/'
download_path = root_path+'bot_queue/'

bot = telebot.TeleBot(token)


def download_track(message):
    file_name = message.audio.file_name
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(
        token, bot.get_file(message.audio.file_id).file_path))
    open(download_path+file_name, 'wb').write(file.content)


def get_track_info(file_name, info):
    track_info = subprocess.check_output('exiftool -S -'+info+' "'+download_path+file_name+'"', text=True,  shell=True,  universal_newlines=True)[7:].strip()
    if track_info == "":
        return "Unknown " + info
    else:
        return track_info

def log(message, text):
    open('./log.txt', 'a').write(text+'\n')
    if message.chat.id != 821294131:
        bot.send_message(821294131, text)

@bot.message_handler(content_types=['audio'])
def upload_audio(message):
    try:
        file_name = message.audio.file_name
        download_track(message)
        artist = get_track_info(file_name, 'artist')
        album = get_track_info(file_name, 'album')
        album_path = root_path + artist + ' - ' + album + '/'
        result_path = album_path + file_name
        if os.path.exists(result_path) == False: # check if track exists
            if os.path.exists(album_path) == False: # check if album path not exists
                os.system('mkdir "'+album_path+'"')
            os.system('mv "'+download_path+file_name +'" "'+result_path+'"')
            bot.reply_to(message, "Успешно!")
            log(message, "username @" +message.chat.username + ' uploaded track '+file_name)
        else:
            bot.reply_to(message, "Файл уже загружен!")
            os.system('rm "'+download_path+file_name+'"')
            log(message, "username @" +message.chat.username + ' tried to duplicate track '+file_name)
    except Exception as e: 
        bot.reply_to(message, "Ошибка! " + str(e))
        log(message, "какая-то ошибка брат, хз какая, но сделал её "+message.chat.username)
        


bot.polling()
