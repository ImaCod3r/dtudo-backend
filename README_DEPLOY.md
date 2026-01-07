# Guia de Deploy VPS Hostinger (Ubuntu 22.04)

Este guia descreve o processo completo para configurar o backend Flask em uma VPS Ubuntu utilizando Nginx, Gunicorn e um banco de dados **MySQL Remoto** da Hostinger.

---

## 1. Acesso e Atualização Inicial
Acesse sua VPS via SSH:
```bash
ssh root@seu_ip_vps
```

Atualize o sistema:
```bash
sudo apt update && sudo apt upgrade -y
```

---

## 2. Instalação de Dependências
Instale o Python, ambiente virtual, servidor web e bibliotecas para conexão com MySQL:
```bash
sudo apt install python3-pip python3-venv nginx git libmysqlclient-dev pkg-config -y
```
*Nota: Não instalaremos o `mysql-server` localmente, pois utilizaremos o banco remoto da Hostinger.*

---

## 3. Configuração do Banco de Dados (Remoto Hostinger)
Como você usará o banco de dados da própria Hostinger (fora da VPS):

1. **Criar Banco**: No painel da Hostinger, crie o banco de dados e o usuário MySQL.
2. **Permissão de Acesso**: No painel MySQL da Hostinger, localize a seção de "MySQL Remoto" e:
   - Adicione o **IP da sua VPS** à lista de IPs permitidos (Whitelist). Isso é essencial para que a VPS consiga se conectar ao banco.
3. **Dados de Conexão**: Anote o **Host** (geralmente algo como `sql123.hostinger.com.br`), Nome do Banco, Usuário e Senha.

---

## 4. Configuração do Projeto
Vá para o diretório web e clone seu repositório:
```bash
cd /var/www
# Substitua pela URL do seu repositório
git clone https://github.com/seu-usuario/dtudo-backend.git
cd dtudo-backend
```

Configure o ambiente virtual e instale as dependências:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn pymysql
```

---

## 5. Variáveis de Ambiente
Crie o arquivo `.env`:
```bash
nano .env
```

Configurações para Banco Remoto:
```env
DB_NAME=u123456789_dtudo     # Nome exato dado pela Hostinger
DB_USER=u123456789_user      # Usuário exato dado pela Hostinger
DB_PASSWORD=SUA_SENHA_SEGURA
DB_HOST=sql123.hostinger.com # Endereço do host fornecido no painel
DB_PORT=3306
ALLOWED_ORIGINS=https://seu-dominio-frontend.com,http://localhost:5173
```

---

## 6. Configuração do Systemd (Gunicorn)
Crie o arquivo de serviço para que o backend rode em segundo plano:
```bash
sudo nano /etc/systemd/system/dtudo.service
```

Cole o conteúdo abaixo:
```ini
[Unit]
Description=Gunicorn instance to serve dtudo-backend
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/dtudo-backend
Environment="PATH=/var/www/dtudo-backend/venv/bin"
ExecStart=/var/www/dtudo-backend/venv/bin/gunicorn --workers 3 --bind unix:dtudo.sock -m 007 run:app

[Install]
WantedBy=multi-user.target
```

Ative o serviço:
```bash
sudo systemctl start dtudo
sudo systemctl enable dtudo
```

---

## 7. Configuração do Nginx (Proxy Reverso)
Crie um novo arquivo de configuração no Nginx:
```bash
sudo nano /etc/nginx/sites-available/dtudo
```

Conteúdo:
```nginx
server {
    listen 80;
    server_name api.seudominio.com; # Substitua pelo seu domínio

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/dtudo-backend/dtudo.sock;
    }

    location /static {
        alias /var/www/dtudo-backend/app/static;
    }
}
```

Habilite o site e reinicie o Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/dtudo /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

## 8. Segurança e SSL (HTTPS)
Instale o Certbot para gerar certificados automáticos:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.seudominio.com
```

---

## 9. Logs e Depuração
Caso ocorra algum erro (especialmente de conexão com o banco), verifique:

- **Teste de Conexão Manual**:
  Tente conectar ao banco remoto via terminal para testar o acesso:
  `mysql -h seu_host_remoto -u seu_usuario -p`

- **Logs da Aplicação (Gunicorn):**
  ```bash
  sudo journalctl -u dtudo
  ```

- **Logs do Nginx:**
  ```bash
  sudo tail -f /var/log/nginx/error.log
  ```
