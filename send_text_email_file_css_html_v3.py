#!/usr/bin/env python3
import csv
import smtplib
import os
import time
import random
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# ==================== НАСТРОЙКИ РАССЫЛКИ ====================
CSV_FILE_NAME = "moscow_factories_full.csv"
YOUR_EMAIL = "proftpd@mail.ru"        # Вставьте вашу почту Яндекса
APP_PASSWORD = ""  # Вставьте 16-значный пароль приложения

PDF_FILES = ["Radio_Engineering.pdf", "Linux_administrator.pdf"]  # Файлы резюме во вложении
LOG_FILE = "sent_emails.txt"   # Лог успешных отправок

# Шаблон HTML-письма (метка времени вставится автоматически в конец)
BODY_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Сопроводительное письмо</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f6f9; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;-webkit-font-smoothing: antialiased;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f4f6f9; padding: 20px 0;">
        <tr>
            <td align="center">
                <!-- Основной контейнер письма -->
                <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #e1e5ed;">
                    
                    <!-- Верхняя цветная полоса-акцент -->
                    <tr>
                        <td height="6" style="background-color: #005ffc;"></td>
                    </tr>
                    
                    <!-- Главный контент -->
                    <tr>
                        <td style="padding: 40px 50px 30px 50px;">
                            <h2 style="margin: 0 0 20px 0; color: #1f293d; font-size: 22px; font-weight: 700; line-height: 1.3;">
                                Здравствуйте!
                            </h2>
                            
                            <p style="margin: 0 0 16px 0; color: #4b5565; font-size: 15px; line-height: 1.6;">
                                Меня заинтересовала вакансия в вашей компании. Обладая базовым радиотехническим образованием и уверенными навыками программирования на Python, я нацелен на решение сложных технических задач и автоматизацию процессов на стыке софта и «железа».
                            </p>
                            
                            <p style="margin: 0 0 24px 0; color: #4b5565; font-size: 15px; line-height: 1.6;">
                                В процессе работы и личных проектов я активно применяю стек технологий, который позволяет мне эффективно разбираться в архитектуре систем и писать отказоустойчивый код.
                            </p>
                            
                            <!-- Блок ключевых навыков / тегов -->
                            <p style="margin: 0 0 10px 0; color: #1f293d; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                                Ключевые компетенции:
                            </p>
                            <div style="margin: 0 0 30px 0; padding-bottom: 20px;">
                                <span style="display: inline-block; background-color: #eef2ff; color: #4f46e5; padding: 5px 12px; margin: 0 6px 8px 0; border-radius: 4px; font-size: 13px; font-weight: 500;">Python 3</span>
                                <span style="display: inline-block; background-color: #eef2ff; color: #4f46e5; padding: 5px 12px; margin: 0 6px 8px 0; border-radius: 4px; font-size: 13px; font-weight: 500;">Linux (Bash)</span>
                                <span style="display: inline-block; background-color: #eef2ff; color: #4f46e5; padding: 5px 12px; margin: 0 6px 8px 0; border-radius: 4px; font-size: 13px; font-weight: 500;">Network Protocols</span>
                                <span style="display: inline-block; background-color: #eef2ff; color: #4f46e5; padding: 5px 12px; margin: 0 6px 8px 0; border-radius: 4px; font-size: 13px; font-weight: 500;">Automation</span>
                                <span style="display: inline-block; background-color: #eef2ff; color: #4f46e5; padding: 5px 12px; margin: 0 6px 8px 0; border-radius: 4px; font-size: 13px; font-weight: 500;">Git</span>
                            </div>
                            
                            <p style="margin: 0 0 30px 0; color: #4b5565; font-size: 15px; line-height: 1.6;">
                                Подробное резюме со списком выполненных проектов и разбором кейсов я прикрепил к этому письму в формате PDF. Буду рад получить обратную связь и обсудить, какие задачи я смогу решать в вашей команде.
                            </p>
                            
                            <!-- Кнопка-ссылка на Портфолио/GitHub -->
                            <table border="0" cellspacing="0" cellpadding="0" style="margin: 0 0 10px 0;">
                                <tr>
                                    <td align="center" bgcolor="#005ffc" style="border-radius: 5px;">
                                        <a href="https://github.com" target="_blank" style="font-size: 15px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; border-radius: 5px; padding: 12px 30px; border: 1px solid #005ffc; display: inline-block; font-weight: 600;">
                                            Открыть Профиль GitHub
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Подвал письма -->
                    <tr>
                        <td style="padding: 20px 50px; background-color: #fafbfc; border-top: 1px solid #e1e5ed; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td>
                                        <p style="margin: 0 0 4px 0; color: #1f293d; font-size: 14px; font-weight: 600;">
                                            С уважением, Роман
                                        </p>
                                        <p style="margin: 0; color: #7f8c8d; font-size: 13px;">
                                            Email: roma_pik_2025_roman@mail.ru | Инженер-разработчик
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                </table>
                <!-- Конец контейнера -->
            </td>
        </tr>
        <tr><td>
        <!--  Подпись -->
    <div style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; line-height: 1.5;">
        <h2 style="margin: 0 0 20px 0; color: #1f293d; font-size: 22px; font-weight: 700; line-height: 1.3;">
            Здравствуйте!
        </h2>
        <p>Направляю вам свое сопроводительное письмо и резюме на позицию Инженера-разработчика / Системного инженера.</p>
        <p>Буду рад получить обратную связь и обсудить возможные варианты сотрудничества.</p>
        <br>
        <p style="margin-bottom: 5px;">С уважением,<br>Петров Р.В.</p>
        <p style="color: #777777; font-size: 12px; margin-top: 20px;">
            ###################<br>
            Отправлено: {current_datetime}
        </p>
    </div>        
        </td</tr>
        
    </table>
</body>
</html>


"""
# ============================================================

def send_mail():
    recipients = []
    
    # 1. Загружаем список тех, кому уже отправляли ранее (защита от дубликатов)
    already_sent = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as log:
            already_sent = {line.strip() for line in log if line.strip()}

    # 2. Читаем контакты из CSV-файла
    if not os.path.exists(CSV_FILE_NAME):
        print(f"Ошибка: Файл с контактами {CSV_FILE_NAME} не найден!")
        return

    with open(CSV_FILE_NAME, "r", encoding="utf-8") as f:
        # Устанавливаем delimiter="," так как LibreOffice обнаружил запятую
        reader = csv.reader(f, delimiter=",")
        next(reader, None)  # Пропускаем строку-заголовок ("Название компании", "Email...")

        for row in reader:
            # Проверяем, что в строке есть хотя бы 2 столбца (Имя и Email)
            if len(row) > 1:
                company_name = row[0].strip()  # Столбец 1: Название компании (Деморобот, Хайтэк...)
                email = row[1].strip()         # Столбец 2: Email для резюме
                
                # Валидация адреса
                if email and "@" in email and "не указан" not in email.lower():
                    if email in already_sent:
                        continue
                    recipients.append((email, company_name))

    if not recipients:
        print("Список получателей пуст или не содержит новых адресов.")
        return

    print(f"Успешно загружено новых адресов для рассылки: {len(recipients)}")
    
    session_sent_count = 0

    # 3. Цикл отправки писем
    for email, company in recipients:
        # Безопасный лимит Яндекса на один непрерывный запуск (до 80 писем)
        if session_sent_count >= 80:
            print("\n Сессионный лимит безопасности (80 писем) достигнут. Скрипт делает паузу.")
            print("Запустите скрипт повторно позже (например, завтра), он продолжит с нового места.")
            break

        # Получаем текущую дату и время в красивом формате
        now = datetime.now()
        timestamp_str = now.strftime("%d.%m.%Y %H:%M:%S")
        time_for_subject = now.strftime("%H:%M") # Короткое время для темы писем

        print(f"\n[{session_sent_count + 1}/80] Подготовка письма для '{company}': {email}")
        
        # Подключение к SMTP серверу Яндекса
        try:
            server = smtplib.SMTP_SSL("smtp.yandex.ru", 465, timeout=15)
            server.login(YOUR_EMAIL, APP_PASSWORD.replace(" ", ""))
        except Exception as e:
            print(f"Не удалось авторизоваться на сервере Яндекса: {e}")
            print("Ожидание 5 минут перед повторной попыткой подключения...")
            time.sleep(300)
            continue

        # Рандомизация ТЕМЫ ПИСЬМА (Название компании + Время отправки + Случайный ID)
        rand_id = random.randint(100, 999)
        dynamic_subject = f"Резюме: Инженер-разработчик / Системный инженер ({company}) [{time_for_subject}] [id:{rand_id}]"
        
        # Персонализация ТЕЛА ПИСЬМА (Добавляем имя компании и уникальную Дату/Время)
        personalized_html = BODY_HTML.replace(
            '<h2 style="margin: 0 0 20px 0; color: #1f293d; font-size: 22px; font-weight: 700; line-height: 1.3;">\n            Здравствуйте!\n        </h2>',
            f'<h2 style="margin: 0 0 20px 0; color: #1f293d; font-size: 22px; font-weight: 700; line-height: 1.3;">\n            Здравствуйте, команда {company}!\n        </h2>'
        )
        # Подставляем дату и время вниз письма
        personalized_html = personalized_html.format(current_datetime=timestamp_str)

        # Сборка MIME структуры
        msg = MIMEMultipart()
        msg["From"] = YOUR_EMAIL
        msg["To"] = email
        msg["Subject"] = dynamic_subject
        msg["Reply-To"] = REPLY_TO_EMAIL  # <--- ОБЯЗАТЕЛЬНО ДОПИШИТЕ ЭТУ СТРОКУ СЮДА
        
        # Вкладываем HTML текст
        msg.attach(MIMEText(personalized_html, "html", "utf-8"))

        # Прикрепление файлов резюме
        for file_path in PDF_FILES:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "rb") as f_pdf:
                        attachment = MIMEApplication(f_pdf.read(), _subtype="pdf")
                        attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(file_path))
                        msg.attach(attachment)
                except Exception as file_err:
                    print(f"Ошибка прикрепления файла {file_path}: {file_err}")
            else:
                print(f"Предупреждение: Файл резюме не найден: {file_path}")

        # Физическая отправка писем
        try:
            server.sendmail(YOUR_EMAIL, [email], msg.as_string())
            print(f"Успешно отправлено на {email}")
            
            # Записываем адрес в лог успешных отправлений
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"{email}\n")
            
            session_sent_count += 1
                
        except Exception as e:
            err_msg = str(e)
            print(f"Ошибка отправки на {email}: {err_msg}")
            if "ratelimit" in err_msg.lower() or "limit exceeded" in err_msg.lower():
                print("Сработал жесткий лимит Яндекса. Завершаем текущую сессию.")
                try: server.quit() 
                except: pass
                break
        finally:
            # Отключаемся от сервера после каждого письма
            try:
                server.quit()
            except:
                pass

        # РАНДОМНАЯ ПАУЗА: от 3 до 5 минут (от 180 до 300 секунд)
        pause_time = random.randint(180, 300)
        print(f"Ожидание {pause_time // 60} мин. {pause_time % 60} сек. перед следующим шагом...")
        time.sleep(pause_time)

    print("\nРабота скрипта в этой сессии успешно завершена!")

if __name__ == "__main__":
    send_mail()
