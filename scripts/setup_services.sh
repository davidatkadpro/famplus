#!/usr/bin/env bash
# Simple helper to install and start MySQL, Redis and optional MailHog
set -euo pipefail

sudo apt-get update
sudo apt-get install -y mysql-server redis-server

if ! command -v mailhog >/dev/null 2>&1; then
    echo "Installing MailHog..."
    sudo wget -qO /usr/local/bin/mailhog https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64
    sudo chmod +x /usr/local/bin/mailhog
fi

sudo service mysql start
sudo service redis-server start

sudo mysql -e "CREATE DATABASE IF NOT EXISTS famplusdb; CREATE USER IF NOT EXISTS 'famplususer'@'localhost' IDENTIFIED BY 'pnQtfMn6ZSLST7okghkg'; GRANT ALL PRIVILEGES ON famplusdb.* TO 'famplususer'@'localhost'; FLUSH PRIVILEGES;"

echo "MySQL and Redis are running. Use 'mailhog' command to start MailHog if needed."
