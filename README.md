# SwiftSign

SwiftSign is a modern, AI-powered smart attendance system designed for educational institutions. It leverages facial recognition, real-time session management, and a user-friendly web interface to streamline and secure the attendance process for both teachers and students.

---

## 🚀 Features

### 1. **Role-Based Login**
- **Teacher Login:** Secure authentication with email and password. Teachers can manage attendance sessions and view reports.
- **Student Login:** Simple email-based login, restricted to institutional domains (e.g., `@hns-re2sd.dz`).

### 2. **Student Registration**
- Students register with their name, class, and institutional email.
- After registration, students capture and upload a profile photo for future facial recognition.

### 3. **Attendance Session Management**
- **Teacher Dashboard:** Teachers can start and end attendance sessions, select modules and groups, and monitor session duration.
- **Session Control:** Only one active session per module/group at a time. Students can only mark attendance when a session is active.

### 4. **AI-Powered Attendance**
- **Facial Recognition:** Students mark attendance by capturing a live photo, which is compared to their registered profile using DeepFace (ArcFace model).
- **Manual Override:** Teachers can manually mark students as present or absent if needed.

### 5. **Real-Time Attendance Table**
- Teachers see a live-updating table of students, showing self-recorded and teacher-marked statuses.
- Manual marking and search/sort features for efficient management.

### 6. **Reporting & Export**
- Download attendance reports as PDF files directly from the dashboard.
- (Planned) Export attendance data as Excel files.

### 7. **Responsive & Modern UI**
- Built with Vue.js and Bootstrap for a clean, responsive experience.
- Dark mode toggle for accessibility and comfort.
- Animated feedback, error popups, and smooth transitions.

### 8. **Security & Session Management**
- Secure session handling for both teachers and students.
- Only authenticated users can access protected routes and features.

---

## 🖥️ How It Works

1. **Teacher starts a session** from the dashboard, selecting the module and group.
2. **Students log in** with their institutional email and are allowed to mark attendance only if a session is active.
3. **Student captures a live photo** using their webcam. The backend compares this photo to the registered profile using DeepFace.
4. **Attendance is marked** as "self-recorded" if the face matches, or teachers can manually override.
5. **Teachers monitor attendance** in real time and can export reports at the end of the session.

---

## 🧑‍💻 Technologies Used

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Session, Flask-Migrate, Flask-Bcrypt
- **Frontend:** Vue.js (CDN), Bootstrap 5, Bootstrap Icons, jsPDF
- **AI Integration:** DeepFace (ArcFace model), OpenCV
- **Database:** SQLite (default, easily swappable)
- **Other:** dotenv for configuration, responsive design, dark mode

---

## 📋 Setup & Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/swift-sign-org/SwiftSign.git
   cd SwiftSign
   ```

2. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the root directory with at least:
     ```
     SECRET_KEY=your_secret_key
     DATABASE_URL=sqlite:///BackEnd/Database/SwiftSignDB.db
     ```

4. **Run database migrations:**
   ```sh
   flask db upgrade
   ```

5. **Start the Flask app:**
   ```sh
   python app.py
   ```

6. **Access the app:**
   - Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🏗️ Project Structure

```
SwiftSign/
├── BackEnd/
│   ├── API.py                # Flask API endpoints (login, attendance, registration)
│   ├── routes.py             # Flask routes for HTML pages
│   └── Database/
│       └── ProjectDatabase.py # SQLAlchemy models for Teacher, Student, Class, Subject
├── FrontEnd/
│   ├── HTML/                 # All HTML templates (login, dashboard, registration, etc.)
│   ├── CSS/                  # Custom styles for each page
│   └── JavaScript/           # Vue.js logic for each page/component
├── AI-Integration/
│   └── face_recognition_asyn.py  # DeepFace-based facial recognition scripts
├── app.py                    # Flask app entry point
├── __init__.py               # Flask app factory and configuration
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 📅 Implementation Plan

See [`plan.md`](plan.md) for a detailed breakdown of features, UI components, and development phases.

---

## 📝 License

MIT License. See [`LICENSE`](LICENSE) for details.

---

## 🤝 Contributing

This project is private, only our members can contribute.

---

## 📧 Contact

For questions or support, contact the project maintainer at [ne.benrahla@hns-re2sd.dz](mailto:ne.benrahla@hns-re2sd.dz).

---