FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Обновляем apt и устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    firefox-esr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Загрузка и установка geckodriver вручную
RUN GECKODRIVER_VERSION="v0.32.0" && \
    wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xvzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем ваш скрипт
CMD ["python", "async_corrected_blogabet_bot.py"]
