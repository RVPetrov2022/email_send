#!/usr/bin/env python3
import csv
import smtplib
import os
import time
import random
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# ВОТ ЭТОЙ СТРОКИ У ВАС СЕЙЧАС НЕТ В КОДЕ, ДОБАВЬТЕ ЕЁ:
from email.mime.application import MIMEApplication

# ==================== НАСТРОЙКИ РАССЫЛКИ ====================
CSV_FILE_NAME = "moscow_factories_full.csv"

# 1. Аккаунт отправки
YOUR_EMAIL = "aor8200@yandex.ru"
APP_PASSWORD = ""  # Вставьте новый токен без пробелов

# 2. Настройки лимитов и пауз (изменено под ваши условия)
EMAILS_PER_BLOCK = 50          # Отправляем 80 писем за один блок
DEEP_SLEEP_HOURS = 2           # Скрипт спит ровно 1 час между блоками


# Файлы резюме убраны во вложения для обхода блокировок. Ссылки добавлены в текст.
PDF_FILES = ["Linux_administrator.pdf"]  # Файлы резюме во вложении
# ============================================================

def load_csv_data():
    if not os.path.exists(CSV_FILE_NAME):
        print(f"Ошибка: Файл {CSV_FILE_NAME} не найден!")
        return None, []
    with open(CSV_FILE_NAME, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames) if reader.fieldnames else []
        rows = list(reader)
    if "Status" not in fieldnames:
        fieldnames.append("Status")
    return fieldnames, rows

def save_csv_data(fieldnames, rows):
    with open(CSV_FILE_NAME, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def generate_random_html(company, timestamp_str):
    """Генератор уникальной HTML-верстки для каждого письма (Антиспам-щит)"""
    
    # 1. Рандомизация приветствий
    greetings = [
        f"Здравствуйте, уважаемая команда {company}!",
        f"Добрый день, команда {company}!",
        f"Здравствуйте! Приветствую команду {company}.",
        f"Приветствую экспертов {company}! Добрый день."
    ]
    
    # 2. Рандомизация текстовых блоков (перетасовка предложений)
    block_intro = "Направляю вам свое сопроводительное письмо и резюме на позицию Системного администратора Linux / Инженера по автоматизации."
    block_exp = "Обладаю крепким бэкграундом в администрировании серверов и автоматизации задач. Разворачиваю серверные среды (Matrix, LiveKit) в Proxmox VE, успешно внедряю РЕД ОС в корпоративный домен, настраиваю сетевые службы Samba, FTP, CUPS, Apache, MySQL."
    block_skills = "Моя главная специализация — избавление от рутины. Пишу отказоустойчивые Python-скрипты, ETL-процессы, модули парсинга логов и watchdog-скрипты автоматического контроля и самовосстановления служб (heartbeat)."
    
    text_paragraphs = [block_exp, block_skills]
    random.shuffle(text_paragraphs)  # Меняем абзацы местами для уникализации структуры
    
    # 3. Рандомизация стека навыков (перемешивание плашек)
    skills_admin = ["Linux (Debian/Ubuntu/РЕД ОС)", "Proxmox VE / VMware", "Samba, FTP, Apache, MySQL", "Сетевые технологии", "Интеграция в домен"]
    skills_dev = ["Python 3 (Автоматизация)", "Bash Scripting", "Парсинг логов", "Watchdog (Self-healing)", "REST API & Webhooks", "Git"]
    random.shuffle(skills_admin)
    random.shuffle(skills_dev)
    
    admin_badges = "".join([f'<span style="display: inline-block; background-color: #eef2ff; color: #4f46e5; padding: 5px 12px; margin: 0 6px 8px 0; border-radius: 4px; font-size: 13px; font-weight: 500;">{s}</span>' for s in skills_admin])
    dev_badges = "".join([f'<span style="display: inline-block; background-color: #eef2ff; color: #4f46e5; padding: 5px 12px; margin: 0 6px 8px 0; border-radius: 4px; font-size: 13px; font-weight: 500;">{s}</span>' for s in skills_dev])

    # 4. Рандомизация элементов оформления (случайный цвет акцента полосы и кнопок)
    brand_colors = ["#005ffc", "#4f46e5", "#0f766e", "#1e3a8a"]
    accent_color = random.choice(brand_colors)

    # 5. Сборка монолитного HTML-кода
    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin: 0; padding: 0; background-color: #f4f6f9; font-family: Arial, sans-serif;">
    <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #f4f6f9; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #e1e5ed;">
                    <tr><td height="6" style="background-color: {accent_color};"></td></tr>
                    <tr>
                        <td style="padding: 40px 50px 30px 50px;">
                            <h2 style="margin: 0 0 20px 0; color: #1f293d; font-size: 22px; font-weight: 700; line-height: 1.3;">{random.choice(greetings)}</h2>
                            <p style="margin: 0 0 16px 0; color: #4b5565; font-size: 15px; line-height: 1.6;">{block_intro}</p>
                            <p style="margin: 0 0 16px 0; color: #4b5565; font-size: 15px; line-height: 1.6;">{text_paragraphs[0]}</p>
                            <p style="margin: 0 0 16px 0; color: #4b5565; font-size: 15px; line-height: 1.6;">{text_paragraphs[1]}</p>
                            
                            <p style="margin: 0 0 24px 0; color: #4b5565; font-size: 15px; line-height: 1.6;">
                                Подробные резюме доступны для скачивания на Яндекс Дисках: 
                                <br>• <a href="ССЫЛКА_НА_АДМИН_РЕЗЮМЕ" target="_blank" style="color: {accent_color}; font-weight: 600; text-decoration: none;">Скачать Резюме Администратора Linux</a>
                                <br>• <a href="ССЫЛКА_НА_РАДИО_РЕЗЮМЕ" target="_blank" style="color: {accent_color}; font-weight: 600; text-decoration: none;">Скачать Резюме Ведущего Инженера</a>
                             </p>

                            <p style="margin: 20px 0 10px 0; color: #1f293d; font-size: 14px; font-weight: 600; text-transform: uppercase;">Администрирование:</p>
                            <div style="margin: 0 0 15px 0;">{admin_badges}</div>
                            <p style="margin: 0 0 10px 0; color: #1f293d; font-size: 14px; font-weight: 600; text-transform: uppercase;">Автоматизация:</p>
                            <div style="margin: 0 0 30px 0;">{dev_badges}</div>

                            <table border="0" cellspacing="0" cellpadding="0">
                                <tr>
                                    <td align="center" bgcolor="{accent_color}" style="border-radius: 5px;">
                                        <a href="https://github.com" target="_blank" style="font-size: 15px; color: #ffffff; text-decoration: none; padding: 12px 30px; display: inline-block; font-weight: 600;">Открыть Профиль GitHub</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 20px 50px; background-color: #fafbfc; border-top: 1px solid #e1e5ed;">
                            <p style="margin: 0 0 4px 0; color: #1f293d; font-size: 14px; font-weight: 600;">С уважением, Роман</p>
                            <p style="margin: 0; color: #7f8c8d; font-size: 13px;">Email: proftpd@mail.ru | Тел: +7 (905) 341-79-19</p>
                        </td>
                    </tr>
                    <tr>
                        <td bgcolor="#ECEBCF" style="padding: 20px 50px; border-top: 1px solid #e1e5ed; font-size: 12px; color: #777777;">
                            <strong>С уважением, Петров Р.В.</strong><br>
                            Python: send_yandex_resume_v1.py | Отправлено: {timestamp_str}
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
    return html
def send_mail():
    while True:
        fieldnames, rows = load_csv_data()
        if not fieldnames:
            return

        # Автоматически определяем названия колонок (компания — 1-я, email — 2-я)
        company_key = fieldnames[0]
        email_key = fieldnames[1]

        recipients = []
        for index, row in enumerate(rows):
            email = row.get(email_key, "").strip()
            company = row.get(company_key, "").strip()
            status = row.get("Status", "").strip()

            if email and "@" in email and "не указан" not in email.lower() and not status:
                recipients.append((index, email, company))

        # Если пустых строк не осталось — сбрасываем статусы для запуска по новому кругу
        if not recipients:
            print("\n[!] Все письма отправлены. Очищаем статусы в CSV для запуска по новому кругу...")
            for row in rows:
                row["Status"] = ""
            save_csv_data(fieldnames, rows)
            continue

        print(f"\n Найдено неотправленных адресов: {len(recipients)}")
        print(f" Начинаем отправку текущего блока из {min(EMAILS_PER_BLOCK, len(recipients))} писем...")
        
        block_sent_count = 0

        for global_index, email, company in recipients:
            if block_sent_count >= EMAILS_PER_BLOCK:
                break

            now = datetime.now()
            timestamp_str = now.strftime("%d.%m.%Y %H:%M:%S")
            time_for_subject = now.strftime("%H:%M")

            print(f"\n[{block_sent_count + 1}/{EMAILS_PER_BLOCK}] Отправка на {email} ({company})...")

            # Подключение к SMTP-серверу Яндекса
            try:
                server = smtplib.SMTP_SSL("smtp.yandex.ru", 465, timeout=15)
                server.login(YOUR_EMAIL, APP_PASSWORD.replace(" ", ""))
            except Exception as e:
                print(f"Ошибка SMTP-авторизации: {e}. Ожидание 5 минут...")
                time.sleep(300)
                continue

            # Рандомизация тем писем (Антиспам)
            subjects = [
                f"Резюме: Системный администратор Linux / Инженер ({company}) [{time_for_subject}] [id:{random.randint(100,999)}]",
                f"Отклик на вакансию: Системный администратор Linux ({company}) [{time_for_subject}]",
                f"Системный администратор Linux (резюме Петрова Романа для {company})"
            ]

            msg = MIMEMultipart()
            msg["From"] = YOUR_EMAIL
            msg["To"] = email
            msg["Subject"] = random.choice(subjects)
            msg["Reply-To"] = YOUR_EMAIL

            # Генерация полностью уникального HTML-кода (метод Spintax)
            personalized_html = generate_random_html(company, timestamp_str)
            msg.attach(MIMEText(personalized_html, "html", "utf-8"))

            # ФИЗИЧЕСКОЕ ПРИКРЕПЛЕНИЕ ОДНОГО ФАЙЛА ЛИНУКС
            file_path = "Linux_administrator.pdf"
            if os.path.exists(file_path):
                try:
                    with open(file_path, "rb") as f_pdf:
                        attachment = MIMEApplication(f_pdf.read(), _subtype="pdf")
                        attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(file_path))
                        msg.attach(attachment)
                except Exception as file_err:
                    print(f"Ошибка прикрепления файла {file_path}: {file_err}")
            else:
                print(f"Предупреждение: Файл резюме не найден в папке скрипта: {file_path}")

            # Отправка и запись лога прямо в CSV таблицу
            try:
                server.sendmail(YOUR_EMAIL, [email], msg.as_string())
                print(f" Успешно доставлено с файлом резюме.")
                
                # Фиксируем статус в таблице
                rows[global_index]["Status"] = f"Отправлено {timestamp_str}"
                save_csv_data(fieldnames, rows)
                
                block_sent_count += 1
            except Exception as e:
                err_msg = str(e)
                print(f"Ошибка отправки: {err_msg}")
                if "ratelimit" in err_msg.lower() or "spam" in err_msg.lower():
                    print("Яндекс временно заблокировал сессию за подозрение на спам. Останавливаем блок.")
                    try: server.quit()
                    except: pass
                    break
            finally:
                try:
                    server.quit()
                except:
                    pass

            # Длинная безопасная пауза между письмами: от 4 до 20 минут
            pause_time = random.randint(30, 200)
            print(f"Ожидание {pause_time // 60} мин. {pause_time % 60} сек. перед следующим шагом...\n")
            time.sleep(pause_time)

        # Конец отправки текущего блока
        print(f"\n=== Блок из {block_sent_count} писем успешно отправлен! ===")
        print(f" Скрипт засыпает на {DEEP_SLEEP_HOURS} час(а) перед следующим блоком...")
        time.sleep(DEEP_SLEEP_HOURS * 3600)

if __name__ == "__main__":
    send_mail()