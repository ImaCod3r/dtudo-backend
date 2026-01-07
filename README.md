# Dtudo Backend

Backend robusto e escalável desenvolvido em Flask para a plataforma **Dtudo**, um sistema de e-commerce com suporte a afiliados, notificações push e gestão completa de pedidos.

---

## 🚀 Tecnologias

- **Linguagem:** Python 3.x
- **Framework Web:** Flask
- **ORM:** Peewee
- **Banco de Dados:** MySQL (Suporte a remoto)
- **Autenticação:** JWT (JSON Web Tokens)
- **Notificações:** PyWebPush (Web Push Notifications)
- **Gerenciamento de Imagens:** Local storage com roteamento estático
- **Middleware:** Log de requisições e tratamento de erros

---

## 📦 Funcionalidades Principais

- **Autenticação e Usuários:** Registro, login e gestão de perfis com diferentes permissões (Admin/User).
- **Gestão de Produtos:** CRUD completo, sistema de categorias, filtros para "Novidades" e "Mais Vendidos".
- **Sistema de Carrinho:** Persistência e gestão de itens no carrinho.
- **Pedidos (Orders):** Fluxo completo de pedidos, desde a criação até a atualização de status (Pendente, Confirmado, Enviado, etc.).
- **Afiliados:** Sistema de recompensas e links de afiliados vinculados a produtos específicos.
- **Endereços:** Gestão de múltiplos endereços de entrega por usuário.
- **Notificações Push:** Integração para envio de alertas em tempo real sobre status de pedidos.
- **Painel Administrativo:** Endpoints dedicados para gestão de estoque, configurações do sistema e logs.

---

## 🛠️ Instalação Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/dtudo-backend.git
   cd dtudo-backend
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   DB_NAME=dtudo
   DB_USER=root
   DB_PASSWORD=sua_senha
   DB_HOST=localhost
   DB_PORT=3306
   ALLOWED_ORIGINS=http://localhost:5173
   JWT_SECRET=sua_chave_secreta
   ```

5. **Execute as migrações (se aplicável):**
   ```bash
   python migrator.py
   ```

6. **Inicie o servidor de desenvolvimento:**
   ```bash
   python run.py
   ```
   A API estará disponível em `http://localhost:3000`.

---

## 📂 Estrutura do Projeto

```text
├── app/
│   ├── models/          # Definições das tabelas do banco de dados (Peewee)
│   ├── routes/          # Endpoints da API (Blueprints)
│   ├── services/        # Lógica de negócio e integrações
│   ├── middlewares/     # interceptores de requisição (Logs, Auth)
│   ├── config.py        # Configurações de rotas e DB
│   └── static/          # Armazenamento de imagens e arquivos estáticos
├── migrator.py          # Script de migração de banco de dados
├── run.py               # Ponto de entrada da aplicação
└── requirements.txt     # Dependências do projeto
```

---

## 🌐 Deploy

Para instruções detalhadas de como colocar este projeto em produção em uma VPS (Ubuntu 22.04) na Hostinger, consulte o arquivo:
👉 [Guia de Deploy (VPS Hostinger)](./README_DEPLOY.md)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
