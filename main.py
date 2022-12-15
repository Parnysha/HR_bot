import config
import telebot
from telebot import types
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
bot = telebot.TeleBot(config.TOKEN)
spisok = {}
def send_email(subject_, message_, to_addrs, format='html'):
	mail = MIMEMultipart("alternative")
	if format=='html':
		mail = MIMEMultipart("alternative", None, [MIMEText(message_,'html')])
	if format=='text':
		mail = MIMEMultipart("alternative", None, [MIMEText(message_)])
	mail['subject'] = subject_
	mail['from'] = config.from_addr
	if to_addrs==list(to_addrs):
		mail['to'] = ', '.join(to_addrs)
	else:
		mail['to'] = (to_addrs)
	server = smtplib.SMTP_SSL(config.smtp_ssl_host, config.smtp_ssl_port)
	server.login(config.username, config.password)
	server.sendmail(config.from_addr, to_addrs, mail.as_string())
	server.quit()
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Погнали!')
    markup = types.InlineKeyboardMarkup()
    markup1 = types.InlineKeyboardButton(text='Мужской', callback_data='Мужской')
    markup2 = types.InlineKeyboardButton(text='Женский', callback_data='Женский')
    markup.add(markup1, markup2)
    bot.send_message(message.chat.id, 'Ваш пол: ', reply_markup=markup)
@bot.callback_query_handler(func = lambda call:True)
def step_4(call):
    global spisok
    if call.data == 'Мужской':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Ваш пол: мужской')
        spisok['Пол']='Мужской'
        pol = bot.send_message(call.message.chat.id, 'Ваше ФИО: ')
        bot.register_next_step_handler(pol, step6)
    elif call.data == 'Женский':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Ваш пол: женский')
        spisok['Пол']='Женский'
        pol = bot.send_message(call.message.chat.id, 'Ваше ФИО: ')
        bot.register_next_step_handler(pol, step6)
    if call.data == 'Изменить':
        change_step = bot.send_message(call.message.chat.id, "Введите цифру пункта который хотите исправить")
        bot.register_next_step_handler(change_step, step12)
    elif call.data == 'Оставить':
        send_email(spisok["ФИО"], f'Пол: {spisok["Пол"]} \n'
                          f'ФИО:{spisok["ФИО"]} \n'
                          f'Возраст: {spisok["Возраст"]} \n'
                          f'Желаемая профессия: {spisok["Профессия"]} \n'
                          f'Желаемая ЗП:{spisok["ЗП"]} \n'
                          f'Образование: {spisok["Образование"]} \n'
                          f'Опыт работы: {spisok["Опыт работы"]}', config.legal_list, format='text')
        bot.send_message(call.message.chat.id, f'Готово! Мы получили вашу информацию и передадим ее нашим специалистам. Спасибо, что воспользовались нашим Ботом.')
    if call.data == 'Мужской испр':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Ваш пол: мужской')
        spisok['Пол']='Мужской'
        bot.send_message(call.message.chat.id, f'Спасибо, мы получили информацию о вас! \n {spisok}')
        markup = types.InlineKeyboardMarkup()
        markup1 = types.InlineKeyboardButton(text='Изменить', callback_data='Изменить')
        markup2 = types.InlineKeyboardButton(text='Оставить', callback_data='Оставить')
        markup.add(markup1, markup2)
        bot.send_message(call.message.chat.id, 'Все верно или вы хотели бы что-то изменить?', reply_markup=markup)
    elif call.data == 'Женский испр':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Ваш пол: женский')
        spisok['Пол']='Женский'
        bot.send_message(call.message.chat.id, f'Спасибо, мы получили информацию о вас! \n {spisok}')
        markup = types.InlineKeyboardMarkup()
        markup1 = types.InlineKeyboardButton(text='Изменить', callback_data='Изменить')
        markup2 = types.InlineKeyboardButton(text='Оставить', callback_data='Оставить')
        markup.add(markup1, markup2)
        bot.send_message(call.message.chat.id, 'Все верно или вы хотели бы что-то изменить?', reply_markup=markup)
@bot.message_handler(content_types='text')
def step6(message):
    global spisok
    age_step = bot.send_message(message.chat.id, 'Возраст: ')
    bot.register_next_step_handler(age_step, step7)
    spisok['ФИО'] = message.text
def step7(message):
    global spisok
    spec_step = bot.send_message(message.chat.id, 'Желаемая профессия: ')
    bot.register_next_step_handler(spec_step, step8)
    spisok['Возраст'] = message.text
def step8(message):
    global spisok
    ZP_step = bot.send_message(message.chat.id, 'Желаемая ЗП: ')
    bot.register_next_step_handler(ZP_step, step9)
    spisok['Профессия'] = message.text
def step9(message):
    global spisok
    edu_step = bot.send_message(message.chat.id, 'Образование: ')
    bot.register_next_step_handler(edu_step, step10)
    spisok['ЗП'] = message.text
def step10(message):
    global spisok
    workage_step = bot.send_message(message.chat.id, 'Опыт работы: ')
    bot.register_next_step_handler(workage_step, step11)
    spisok['Образование'] = message.text
def step11(message):
    global spisok
    spisok['Опыт работы'] = message.text
    bot.send_message(message.chat.id, f'Спасибо, мы получили информацию о вас! \n {spisok}.')
    markup = types.InlineKeyboardMarkup()
    markup1 = types.InlineKeyboardButton(text='Изменить', callback_data='Изменить')
    markup2 = types.InlineKeyboardButton(text='Оставить', callback_data='Оставить')
    markup.add(markup1, markup2)
    bot.send_message(message.chat.id, 'Все верно или вы хотели бы что-то изменить?', reply_markup=markup)
def step12(message):
    global spisok
    if message.text == '1':
        markup = types.InlineKeyboardMarkup()
        markup1 = types.InlineKeyboardButton(text='Мужской', callback_data='Мужской испр')
        markup2 = types.InlineKeyboardButton(text='Женский', callback_data='Женский испр')
        markup.add(markup1, markup2)
        bot.send_message(message.chat.id, 'Ваш пол: ', reply_markup=markup)
    elif message.text == '2':
        pol = bot.send_message(message.chat.id, 'Ваше ФИО: ')
        bot.register_next_step_handler(pol, step_ispr_fio)
    elif message.text == '3':
        age_step = bot.send_message(message.chat.id, 'Возраст: ')
        bot.register_next_step_handler(age_step, step_ispr_vozrast)
    elif message.text == '4':
        spec_step = bot.send_message(message.chat.id, 'Желаемая профессия: ')
        bot.register_next_step_handler(spec_step, step_ispr_prof)
    elif message.text == '5':
        ZP_step = bot.send_message(message.chat.id, 'Желаемая ЗП: ')
        bot.register_next_step_handler(ZP_step, step_ispr_zp)
    elif message.text == '6':
        edu_step = bot.send_message(message.chat.id, 'Образование: ')
        bot.register_next_step_handler(edu_step, step_ispr_obraz)
    elif message.text == '7':
        workage_step = bot.send_message(message.chat.id, 'Опыт работы: ')
        bot.register_next_step_handler(workage_step, step_ispr_opyt)
def step_ispr_vozrast(message):
    global spisok
    spisok['Возраст'] = message.text
    bot.send_message(message.chat.id, f'Спасибо, мы получили информацию о вас! \n {spisok}')
    markup = types.InlineKeyboardMarkup()
    markup1 = types.InlineKeyboardButton(text='Изменить', callback_data='Изменить')
    markup2 = types.InlineKeyboardButton(text='Оставить', callback_data='Оставить')
    markup.add(markup1, markup2)
    bot.send_message(message.chat.id, 'Все верно или вы хотели бы что-то изменить?', reply_markup=markup)
def step_ispr_fio(message):
    global spisok
    spisok['ФИО'] = message.text
    bot.send_message(message.chat.id, f'Спасибо, мы получили информацию о вас! \n {spisok}')
    markup = types.InlineKeyboardMarkup()
    markup1 = types.InlineKeyboardButton(text='Изменить', callback_data='Изменить')
    markup2 = types.InlineKeyboardButton(text='Оставить', callback_data='Оставить')
    markup.add(markup1, markup2)
    bot.send_message(message.chat.id, 'Все верно или вы хотели бы что-то изменить?', reply_markup=markup)
def step_ispr_prof(message):
    global spisok
    spisok['Профессия'] = message.text
    bot.send_message(message.chat.id, f'Спасибо, мы получили информацию о вас! \n {spisok}')
    markup = types.InlineKeyboardMarkup()
    markup1 = types.InlineKeyboardButton(text='Изменить', callback_data='Изменить')
    markup2 = types.InlineKeyboardButton(text='Оставить', callback_data='Оставить')
    markup.add(markup1, markup2)
    bot.send_message(message.chat.id, 'Все верно или вы хотели бы что-то изменить?', reply_markup=markup)
def step_ispr_zp(message):
    global spisok
    spisok['ЗП'] = message.text
    bot.send_message(message.chat.id, f'Спасибо, мы получили информацию о вас! \n {spisok}')
    markup = types.InlineKeyboardMarkup()
    markup1 = types.InlineKeyboardButton(text='Изменить', callback_data='Изменить')
    markup2 = types.InlineKeyboardButton(text='Оставить', callback_data='Оставить')
    markup.add(markup1, markup2)
    bot.send_message(message.chat.id, 'Все верно или вы хотели бы что-то изменить?', reply_markup=markup)
def step_ispr_obraz(message):
    global spisok
    spisok['Образование'] = message.text
    bot.send_message(message.chat.id, f'Спасибо, мы получили информацию о вас! \n {spisok}')
    markup = types.InlineKeyboardMarkup()
    markup1 = types.InlineKeyboardButton(text='Изменить', callback_data='Изменить')
    markup2 = types.InlineKeyboardButton(text='Оставить', callback_data='Оставить')
    markup.add(markup1, markup2)
    bot.send_message(message.chat.id, 'Все верно или вы хотели бы что-то изменить?', reply_markup=markup)
def step_ispr_opyt(message):
    global spisok
    spisok['Опыт работы'] = message.text
    bot.send_message(message.chat.id, f'Спасибо, мы получили информацию о вас! \n {spisok}')
    markup = types.InlineKeyboardMarkup()
    markup1 = types.InlineKeyboardButton(text='Изменить', callback_data='Изменить')
    markup2 = types.InlineKeyboardButton(text='Оставить', callback_data='Оставить')
    markup.add(markup1, markup2)
    bot.send_message(message.chat.id, 'Все верно или вы хотели бы что-то изменить?', reply_markup=markup)

bot.polling(none_stop=True)