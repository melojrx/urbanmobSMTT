FROM python:3.8.10

WORKDIR /home/ubuntu/maceio-server/urbanmobSMTT

# Copie os arquivos de requirements.txt
COPY requirements.txt .

# Instale as dependências dentro da venv
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyreportjasper
RUN apt-get update && apt-get install -y default-jre

# Define o valor da variável de ambiente JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/default-java

# Adicione o diretório bin da JVM ao PATH
ENV PATH $PATH:$JAVA_HOME/bin

# Copie o restante do código
COPY . .
