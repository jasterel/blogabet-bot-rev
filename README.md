Перед компиляцией контейнера измените данные в боте на нужные вам:

- Telegram Token
- Telegram Channel ID
- Email и пароль от blogabet.com

------------------------------------------------------------------------
1.** Установите Docker:**
- **Обновите пакеты:**
  sudo apt-get update
  
- **Установите необходимые зависимости:**
  sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
  
- **Добавьте GPG-ключ Docker:**
  curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
  
- **Добавьте репозиторий Docker:**
  echo "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
  
- **Установите Docker:**
  sudo apt-get update \n
  sudo apt-get install -y docker-ce
  
- **Проверьте, что Docker установлен:**
  sudo systemctl status docker
  
2. **Развертывание проекта**
- **Компиляция**
  docker build -t blogabet-bot .

- **Запуск**
  docker run -d --name blogabet-bot-container blogabet-bot
