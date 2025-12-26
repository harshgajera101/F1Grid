# 🏎️ F1Grid

> A dedicated social platform for Formula 1 fans to share opinions, create polls, and engage with the F1 community.

![Django](https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-MVP-orange?style=for-the-badge)

---

## 📖 About The Project

**F1Grid** is a Twitter-like social platform built exclusively for Formula 1 enthusiasts. It provides a space where F1 fans can share race updates, hot takes, memes, polls, and engage with fellow fans through an interactive reaction system.

This project was created as a **learning exercise to master Django fundamentals** and explore full-stack web development. It's currently in the **MVP (Minimum Viable Product)** stage with core features implemented and working.

### 🎯 Purpose

- **For F1 Fans:** A dedicated platform to discuss races, drivers, teams, and F1 culture
- **For Learning:** Hands-on practice with Django's core concepts and modern web development
- **For Community:** Building a niche social network tailored to a specific interest group

> ⚠️ **Note:** This is an early-stage MVP built for learning purposes.  It's not a production-ready application and is actively being developed.

---

## ✨ Features

### 🔥 Core Functionality
- **User Authentication** - Register, login, logout with session management
- **Post Creation** - Create posts with 5 different types: 
  - 🏁 Race Updates
  - 📰 Breaking News
  - 💭 Opinions
  - 😂 Memes
  - 📊 Polls

### 🗳️ Interactive Polls
- Create polls with 2-4 options
- Real-time vote counting
- Visual progress bars with animations

### 🎭 Reaction System
- 5 F1-themed emoji reactions:  🔥 🏆 🏁 🚀 💥
- Click to react, click again to remove (toggle)
- Live reaction counts

### 🏎️ F1-Specific Features
- **Team Tagging** - Tag posts with F1 teams (McLaren, Ferrari, Red Bull, etc.)
- **Driver Tagging** - Tag posts with F1 drivers
- **Smart Filtering** - Filter posts by type, team, or driver
- **Dynamic Driver Selection** - Driver dropdown auto-filters based on selected team

### 👤 User Profiles
- Personalized profile pages with retro F1 styling
- Comprehensive stats dashboard: 
  - Total posts, polls created, reactions received
  - Favorite team and driver (auto-calculated)
  - Post activity breakdown by type
  - Recent activity tracking
- Member since date


### 🔧 Additional Features
- Full CRUD operations (Create, Read, Update, Delete)
- Media uploads for posts
- Real-time post filtering
- Login-required actions with redirect

---

## 🛠️ Tech Stack

### Backend
- **Django 4.2** - Python web framework
- **SQLite** - Database (development)
- **Python 3.9+** - Programming language

### Frontend
- **HTML5 & CSS3** - Structure and styling
- **Bootstrap 5** - UI components
- **JavaScript** - Dynamic interactions
- **Google Fonts** - Custom typography

### Key Libraries
- **Django Auth** - User authentication
- **Django Forms** - Form handling
- **Pillow** - Image processing
- **WhiteNoise** - Static file serving (production)

---

## 📂 Project Structure

```
F1Grid/
├── f1shit/                      # Main project directory
│   ├── f1shit/                  # Django project settings
│   │   ├── settings.py          # Project configuration
│   │   ├── urls.py              # Root URL routing
│   │   └── wsgi.py              # WSGI configuration
│   │
│   ├── tweet/                   # Main app (posts/tweets)
│   │   ├── models.py            # Database models (Tweet, Reaction, Poll, etc.)
│   │   ├── views.py             # View functions (business logic)
│   │   ├── forms.py             # Django forms (TweetForm, PollForm)
│   │   ├── urls.py              # App URL patterns
│   │   ├── admin.py             # Admin panel configuration
│   │   ├── migrations/          # Database migrations
│   │   └── templates/           # HTML templates
│   │       └── tweet/
│   │           ├── tweet_list.html
│   │           ├── tweet_form.html
│   │           ├── profile.html
│   │           └── components/
│   │               └── post_card.html
│   │
│   ├── templates/               # Global templates
│   │   ├── layout. html         # Base template with navbar/footer
│   │   └── registration/        # Auth templates
│   │
│   ├── static/                  # Static files
│   │   ├── css/
│   │   │   └── style.css        # Main stylesheet
│   │   └── images/
│   │       └── favicon.png      # Site logo
│   │
│   ├── media/                   # User-uploaded files
│   │   └── photos/              # Post images
│   │
│   └── manage.py                # Django management script
│
├── requirements.txt             # Python dependencies
├── . gitignore                  # Git ignore rules
└── README.md                    # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/harshgajera101/F1Grid.git
   cd F1Grid
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements. txt
   ```

4. **Navigate to project directory**
   ```bash
   cd f1shit
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage. py migrate
   ```

6. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load F1 data (optional)**
   
   Run Django shell and add teams/drivers: 
   ```bash
   python manage.py shell
   ```
   
   Then paste: 
   ```python
   from tweet.models import Team, Driver

   # Create Teams
   red_bull = Team.objects.create(name="Red Bull Racing", color="#0600EF")
   ferrari = Team.objects.create(name="Ferrari", color="#DC0000")
   mercedes = Team.objects.create(name="Mercedes", color="#00D2BE")
   mclaren = Team.objects.create(name="McLaren", color="#FF8700")
   aston_martin = Team.objects.create(name="Aston Martin", color="#006F62")
   alpine = Team.objects.create(name="Alpine", color="#0090FF")
   williams = Team.objects.create(name="Williams", color="#005AFF")
   alfa_romeo = Team.objects.create(name="Kick Sauber", color="#900000")
   haas = Team.objects.create(name="Haas F1 Team", color="#FFFFFF")
   rb = Team.objects.create(name="RB", color="#2B4562")

   # Create Drivers
   Driver.objects.create(name="Max Verstappen", team=red_bull)
   Driver.objects.create(name="Sergio Perez", team=red_bull)
   Driver.objects.create(name="Charles Leclerc", team=ferrari)
   Driver.objects.create(name="Carlos Sainz", team=ferrari)
   Driver.objects.create(name="Lewis Hamilton", team=mercedes)
   Driver.objects.create(name="George Russell", team=mercedes)
   Driver.objects.create(name="Lando Norris", team=mclaren)
   Driver.objects.create(name="Oscar Piastri", team=mclaren)
   Driver.objects.create(name="Fernando Alonso", team=aston_martin)
   Driver.objects.create(name="Lance Stroll", team=aston_martin)
   Driver.objects.create(name="Pierre Gasly", team=alpine)
   Driver.objects.create(name="Esteban Ocon", team=alpine)
   Driver.objects.create(name="Alex Albon", team=williams)
   Driver.objects.create(name="Logan Sargeant", team=williams)
   Driver.objects.create(name="Valtteri Bottas", team=alfa_romeo)
   Driver.objects.create(name="Zhou Guanyu", team=alfa_romeo)
   Driver.objects.create(name="Kevin Magnussen", team=haas)
   Driver.objects.create(name="Nico Hulkenberg", team=haas)
   Driver.objects.create(name="Yuki Tsunoda", team=rb)
   Driver.objects.create(name="Daniel Ricciardo", team=rb)
   
   print("✅ All F1 Teams and Drivers created successfully!")
   exit()
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   
   Open your browser and go to:  `http://127.0.0.1:8000/tweet/`

---

## 📸 Screenshots

### Home Feed
<img width="1470" height="796" alt="Screenshot 2025-12-25 at 9 54 48 PM" src="https://github.com/user-attachments/assets/f257319a-e5ee-490d-8e8a-c98b6f0bd82d" />
The main feed displays all posts with filtering options by type, team, and driver.

### Create Post
<img width="800" height="761" alt="Screenshot 2025-12-26 at 8 20 50 PM" src="https://github.com/user-attachments/assets/83da8e49-e95e-4776-87b5-961ab3b10ae2" />

Users can create different types of posts including polls with dynamic options.

### Profile Dashboard
<img width="1470" height="797" alt="Screenshot 2025-12-25 at 9 56 37 PM" src="https://github.com/user-attachments/assets/1c77e7aa-3c2b-46a6-85b5-b10caf54fc8d" />
Comprehensive user stats with retro F1 styling and activity breakdowns.


---

## 🎯 Roadmap

### ✅ Completed (MVP)
- [x] User authentication system
- [x] Post creation and Poll creation with Reaction system
- [x] Team and driver tagging
- [x] Dynamic filtering
- [x] User profiles with stats
- [x] Responsive design

### 🔜 Planned Features
- [ ] Search functionality
- [ ] Hashtag support
- [ ] User following system
- [ ] Notifications
- [ ] Race calendar integration
- [ ] Live race discussion threads
- [ ] User avatars/profile pictures
- [ ] Comment system (currently disabled)
- [ ] Leaderboards for top contributors

---

## 🤝 Contributing

This is a personal learning project, but suggestions and feedback are welcome! 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available for educational purposes.

---

## 👨‍💻 Author

**Harsh Gajera**

- GitHub: [@harshgajera101](https://github.com/harshgajera101)
- LinkedIn: [gajera-harsh](https://www.linkedin.com/in/gajera-harsh)
- Project Link: [F1Grid](https://github.com/harshgajera101/F1Grid)

---

## 📌 Notes

- This is an **MVP (Minimum Viable Product)** - not production-ready
- Built for **learning Django** and web development fundamentals
- **No real F1 affiliation** - fan-made project
- Uses SQLite for development (PostgreSQL recommended for production)
- Media files are stored locally (cloud storage recommended for production)

---

<div align="center">

### 🏁 Made with ❤️ for F1 Fans

**F1Grid** - Where the Grid Never Sleeps

![F1](https://img.shields.io/badge/F1-Fans-red?style=flat-square&logo=formula1)
![Django](https://img.shields.io/badge/Built_with-Django-green?style=flat-square&logo=django)
![Open Source](https://img.shields.io/badge/Open-Source-blue?style=flat-square)

</div>
