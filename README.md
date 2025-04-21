# ShapeTeamAPI - API for social network

The ShapeTeam project consists of developing a social network platform aimed at people interested in finding training partners for different physical exercises. The platform will allow users to create profiles, find workout partners with similar interests, schedule workout sessions, share experiences and motivate each other to achieve their fitness goals.

## 🖥️ **Technologies Usedes**

- **Python3.11**: Language.
- **Django Rest Framework**: To create the API.
- **PostgreSQL**: Database.
- **Redis**: Database NoSQL.
- **Knox**: Authentify.


## 🚀 **How runing local project**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/leonardobarrosdev/ShapeteamAPI
   ```

2. **Navigate to the project folder:**
   ```bash
   cd ShapeteamAPI
   ```

3. **Virtual environment**:
For managing Python dependencies and creating isolated environments, we use `uv`, a fast Python package installer and resolver written in Rust. It provides better performance and reliability compared to traditional tools.
[uv documentation][https://github.com/astral-sh/uv]

4. **Install requirements:**
   ```bash
   uv install
   source .venv/bin/activate
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

9. You can **populate the database**:
   ```bash
   python manage.py loaddata shapeteam/fixtures/*.json
   ```]
   Obs: Not realize this comand (9) for production.

10. **Run the development server**:
   ```bash
   python manage.py runserver
   ```


## 🌟 **Funtionalities**

- **User authentication**
- **Find workout partners with similar interests**
- **Schedule workout sessions**
- **Invite partner for workout sessions**
- **share experiences**
- **Chat one to one**

## 🔗 **Deploy**

This API can be easily hosted on platforms like Render, Netlify or any other service. 
Obs: Use [gunicorn](https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/gunicorn/)

## 📝 **Licença**

This project it's licenced by [MIT License](LICENSE), allowing free use and modification, as long as copyright is maintained.

---

If you need more help, just let me know!
