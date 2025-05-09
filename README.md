# 📝 MyDiary - Personal Diary Web App

**MyDiary** is a secure, web-based personal diary built with Django. It allows users to write, organize, and revisit their thoughts, emotions, and daily experiences through a rich-text editor. Users can register, log in, and manage their entries privately using features similar to Google Docs or Microsoft Word, with mood tracking and emoji-based filters.

---

## 📌 Features

- 🔐 Secure User Authentication (Sign Up, Login, Logout)
- 🖋️ Rich Text Editor (Bold, Italic, Underline, Lists, Fonts, Images, etc.)
- 😊 Mood selection with emojis
- 📅 Auto-filled editable titles with the current date
- 🔍 Search by date, mood, or keywords
- 🗂️ Sidebar navigation of entries with mood icons
- 📱 Responsive design using Bootstrap 5
- ✅ CSRF protection and input validation

---

## 💻 Tech Stack

- **Frontend**: HTML, CSS, Bootstrap 5, CKEditor
- **Backend**: Django (Python)
- **Database**: SQLite
- **Other Tools**: Django messages framework, CSRF Middleware, Django forms

---

## 🧑‍💻 About the Developer

Hi! I'm **Ishardeep Singh**, a computer science undergraduate at Chitkara University, specializing in AI. I'm passionate about building meaningful digital experiences, and I love blending creativity with code.

- 🧠 Interests: Web Development, AI, Problem-Solving, UI Design, Anime, Sports
- 📫 Email: singhishardeep06@gmail.com
- 🔗 LinkedIn: [https://www.linkedin.com/in/ishardeep-singh](https://www.linkedin.com/in/ishardeep-singh)


---

## 🛠️ Setup Instructions (For Beginners - Windows & Mac)

### ✅ Step 1: Install Python

- Go to [https://www.python.org/downloads](https://www.python.org/downloads)
- Download and install Python (version 3.8+)
- During installation, **check the box** that says: `Add Python to PATH`

### ✅ Step 2: Install Git (Optional but useful)
- [https://git-scm.com/downloads](https://git-scm.com/downloads)

### ✅ Step 3: Clone the Project or Download ZIP

```bash
git clone https://github.com/ishar06/MyDiary.git
cd MyDiary
```

Or download the ZIP and extract it.

### ✅ Step 4: Set Up Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### ✅ Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist yet, install manually:

```bash
pip install asgiref Django django-jazzmin sqlparse
```

### ✅ Step 6: Set Up the Database

```bash
python manage.py migrate
```

### ✅ Step 7: Run the Django Server

```bash
python manage.py runserver
```

Go to `http://127.0.0.1:8000` in your browser.

### ✅ Step 8: Create Superuser (Optional for Admin Panel)

```bash
python manage.py createsuperuser
```

---

## 😅 Challenges Faced

- Configuring and customizing CKEditor in Django forms
- Designing an intuitive sidebar with emoji filters
- Managing authenticated views and entry ownership securely
- Making the rich text editor mobile responsive

---

## ✨ Experience Gained

- Learned how to structure a Django app with templates, static files, and models
- Understood how to use third-party editors inside Django forms
- Improved frontend skills using Bootstrap
- Gained hands-on experience with session management, CSRF protection, and validation

---

## 📃 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this software for personal or commercial purposes, as long as the original license and copyright notice are included.

> For full license details, refer to the [LICENSE](LICENSE) file in the repository.

---

*Happy journaling! 🚀*
