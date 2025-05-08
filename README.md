# Hybrid Multimodal AI Framework for Real-Time Employee Activity Recognition and Workplace Motion Analytics (HMAI-ERA)

## 📌 Overview

HMAI-ERA is an AI-powered framework designed for real-time employee activity recognition and workplace motion analytics. It integrates multiple modalities, including face recognition, screen monitoring, mouse and keyboard activity tracking, to assess employee engagement and detect unusual patterns. The system also provides an admin dashboard for monitoring, reports, and analytics.

## 🚀 Features

- **Face Recognition**: Identifies employees using MTCNN and `face_recognition` library.
- **Activity Monitoring**: Tracks screen usage, keyboard, and mouse movements to determine work status.
- **Database Storage**: Logs employee activity into MongoDB for later analysis.
- **Admin Dashboard**: Provides authentication, employee tracking, data visualization, and reports.
- **Anomaly Detection**: Flags inactivity or repetitive motion as potential issues.
- **Unknown Face Detection**: Stores images of unrecognized individuals for security.
- **Reports Generation**: Weekly/monthly work-hour summaries available in CSV format.

## 📂 Project Structure

```
📁 Hybrid-Multimodal-AI-Framework
│── 📂 data/                     # Known employee face images
│── 📂 unknown_faces/            # Detected unknown faces
│── 📂 templates/                # HTML files for Flask dashboard
│── 📂 static/                   # CSS & JS files for frontend
│── 📜 main.py                   # Real-time monitoring script
│── 📜 app.py                    # Flask web application
│── 📜 config.py                 # Configuration file
│── 📜 requirements.txt          # Python dependencies
│── 📜 README.md                 # Project documentation
```

## 🛠️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/HMAI-ERA.git
cd HMAI-ERA
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up MongoDB

Ensure MongoDB is running and update the `MONGO_URI` in `config.py` accordingly.

### 4️⃣ Run Face Recognition & Activity Tracker

```bash
python main.py
```

### 5️⃣ Start Admin Dashboard

```bash
python app.py
```

Then open **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)** in your browser.

## 🔑 Default Admin Credentials

- **Username:** `admin`
- **Password:** `admin123` (Change this after setup!)

## 📊 Admin Dashboard Features

- **Login Authentication**
- **Employee Activity Logs**
- **Search & Filtering**
- **Data Visualization (Charts & Graphs)**
- **Unknown Face Management**
- **Report Download (CSV Format)**

## 📝 Future Improvements

- Enhancing real-time alerts for inactivity.
- Integrating gesture recognition.
- Cloud storage for reports and analytics.

## 📜 License

This project is open-source and available under the **MIT License**.

## 📧 Contact

For any queries, feel free to reach out at **arunchandran2k4\@gmail.com** or create an issue in the repository!

