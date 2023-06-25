FROM python:3.8.10

WORKDIR /home/ubuntu/maceio-server/urbanmobSMTT

# Crie a venv
RUN python -m venv venv

# Ative a venv e configure o ambiente
ENV PATH="/home/ubuntu/maceio-server/urbanmobSMTT/venv/bin:$PATH"

# Copie os arquivos de requirements.txt
COPY requirements.txt .

# Instale as dependências dentro da venv
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código
COPY . .