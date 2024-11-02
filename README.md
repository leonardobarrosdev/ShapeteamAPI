# ShapeTeamAPI - API for social network

The ShapeTeam project consists of developing a social network platform aimed at people interested in finding training partners for different physical exercises. The platform will allow users to create profiles, find workout partners with similar interests, schedule workout sessions, share experiences and motivate each other to achieve their fitness goals.

## 🖥️ **Technologies Usedes**

- **Python3.11**: Language.
- **Django Restframework**: To create a API.
- **PostgreSQL**: Database.

## 📁 **Diretorie Structure**

```
core/               # The core of the system
    /asgi.py
    /settings.py    # Settings
    /urls.py
    /wsgi
/shapeteam          # App
      # files of app shapeteam
.coveragerc        # Test Coverage
manage.py          # Manage from system
requirements.txt   # Requirements
```

## 🚀 **How runing local project**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/leonardobarrosdev/Annabela-website.git
   ```

2. **Navigate to the project folder:**
   ```bash
   cd ShapeteamAPI
   ```


3. **Virtual enviroment**:
In order for you to have a development environment that is as conducive as possible and not clutter your machine with many dependencies that you probably won't use in another project, it is important to establish a development environment for each project. One of the most used environments for developing in Django is Virtualenv and those who are already familiar with Docker can use it too.
[Virtualenv][https://virtualenv.pypa.io/en/latest/]
[Docker - Django][https://docs.docker.com/samples/django/]


4. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Gerenerate a `.env` local based in .env.example**


7. **Sicronize the database**:
   ```bash
   python manage.py migrate
   ```
   
8. **Create a User (System Admin)**:
   ```bash
   python manage.py createsuperuser
   ```

9. **Run the development server**:
```bash
python manage.py runserver
```


## 🌟 **Funtionalities**

- **Users to Create Profiles**: Apresentação visual e elegante de Anna Bela, com links para as principais seções.
- **Find workout partners with similar interests**
- **Schedule workout sessions**
- **share experiences**

## 🔗 **Deploy**

This API can be easily hosted on platforms like Render, Netlify or any other service. 
Obs: Use [gunicorn](https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/gunicorn/)

## 📝 **Licença**

This project it's licenced by [MIT License](LICENSE), allowing free use and modification, as long as copyright is maintained.

---

If you need more help, just let me know!
