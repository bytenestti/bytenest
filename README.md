# ByteNest - Plataforma de Tecnologia

Uma plataforma completa para a empresa ByteNest, desenvolvida com Django, incluindo landing page moderna e sistema de autenticação por email.

## 🚀 Tecnologias Utilizadas

- **Backend**: Django 5.2.5
- **Banco de Dados**: SQLite (desenvolvimento)
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Autenticação**: Sistema personalizado com login por email
- **Servidor**: Django Development Server

## 📋 Pré-requisitos

- Python 3.11+
- pip (gerenciador de pacotes Python)
- Git

## 🛠️ Instalação e Execução

### 1. Clone o repositório
```bash
git clone <repository-url>
cd bytenest
```

### 2. Crie e ative o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados
```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

### 5. Coletar arquivos estáticos
```bash
python manage.py collectstatic --noinput
```

### 6. Execute o servidor
```bash
python manage.py runserver
```

### 7. Acesse a aplicação
- **Landing Page**: http://127.0.0.1:8000
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Dashboard**: http://127.0.0.1:8000/accounts/dashboard/
- **Admin Django**: http://127.0.0.1:8000/admin

## 🔑 Sistema de Autenticação

### Credenciais Padrão
- **Email**: admin@bytenest.com
- **Senha**: admin123

### Funcionalidades
- ✅ **Login por email** (não username)
- ✅ **Dashboard personalizado**
- ✅ **Logout seguro**
- ✅ **Proteção de rotas**
- ✅ **Interface moderna e responsiva**

## 📁 Estrutura do Projeto

```
bytenest/
├── apps/
│   ├── landing_page/          # App da landing page
│   │   ├── templates/
│   │   │   └── landing_page/
│   │   │       └── landing_page.html
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── models.py
│   └── accounts/              # App de autenticação
│       ├── templates/
│       │   └── accounts/
│       │       ├── login.html
│       │       └── dashboard.html
│       ├── models.py          # Modelo User personalizado
│       ├── views.py           # Views de login/logout/dashboard
│       ├── urls.py
│       └── admin.py
├── core/                      # Configurações do projeto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   └── base.html              # Template base
├── staticfiles/               # Arquivos estáticos coletados
├── media/                     # Arquivos de mídia
├── requirements.txt
├── manage.py
└── README.md
```

## 🎨 Funcionalidades da Landing Page

- **Design Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- **Animações**: Efeitos visuais modernos com CSS e JavaScript
- **Formulário de Contato**: Funcional com validação AJAX
- **Seções**:
  - Hero Section com CTAs
  - Estatísticas da empresa
  - Serviços oferecidos
  - Terceirização de TI (diferencial)
  - Sobre a empresa
  - Depoimentos de clientes
  - Formulário de contato
  - Footer completo

## 🔧 Serviços Oferecidos

1. **Desenvolvimento Web**
2. **Apps Mobile**
3. **Automação**
4. **Cloud Solutions**
5. **Analytics & BI**
6. **Cybersecurity**
7. **Terceirização de TI** (com suporte presencial)

## 🎯 URLs Disponíveis

### Públicas
- `/` - Landing page principal
- `/contato/` - Endpoint do formulário de contato

### Autenticação
- `/accounts/login/` - Página de login
- `/accounts/logout/` - Logout
- `/accounts/dashboard/` - Dashboard do usuário

### Admin
- `/admin/` - Interface administrativa do Django

## 🛠️ Comandos Úteis

### Gerenciamento do Django
```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar testes
python manage.py test

# Shell interativo
python manage.py shell
```

### Gerenciamento do Ambiente Virtual
```bash
# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Desativar ambiente virtual
deactivate
```

## 🔒 Configurações de Segurança

O projeto está configurado com:
- ✅ **HTTPS desabilitado** em desenvolvimento
- ✅ **CSRF protection** ativado
- ✅ **XSS protection** ativado
- ✅ **Content Security Policy** configurado
- ✅ **Autenticação personalizada** por email

## 🚀 Deploy em Produção

Para deploy em produção, considere:

1. **Configurar variáveis de ambiente**:
   ```python
   DEBUG = False
   SECRET_KEY = 'sua-chave-secreta-segura'
   ALLOWED_HOSTS = ['seu-dominio.com']
   ```

2. **Usar banco de dados PostgreSQL**:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'bytenest_prod',
           'USER': 'usuario',
           'PASSWORD': 'senha',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Configurar servidor web** (Nginx + Gunicorn)
4. **Configurar SSL/HTTPS**
5. **Configurar CDN** para arquivos estáticos

## 📞 Contato

- **Email**: contato@bytenest.com.br
- **Telefone**: +55 (11) 99999-9999
- **Localização**: São Paulo, SP - Brasil

## 📄 Licença

Este projeto é propriedade da ByteNest. Todos os direitos reservados.

---

**Desenvolvido com ❤️ pela equipe ByteNest**