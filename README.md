# FaceStyle AI – AI-Based Face Shape Detection & Hairstyle Recommendation System

**Academic Level:** TY B.Sc. Information Technology (Final-Year College Project)  
**Technology Stack:** Python 3.12, Django 5.1, MediaPipe Face Landmarker, OpenCV, NumPy, Bootstrap 5, Font Awesome, SQLite/MySQL

---

## 1. Project Overview

**FaceStyle AI** is a commercial-grade, artificial intelligence web application designed to eliminate guesswork from personal styling. The system allows users to upload a portrait photograph or capture a live webcam portrait, extracts 468 3D facial landmark coordinates using **Google MediaPipe**, performs mathematical anthropometry to determine face proportions, and estimates the user's geometric face shape among six archetypes:

1. **Oval Face**
2. **Round Face**
3. **Square Face**
4. **Heart Face**
5. **Diamond Face**
6. **Oblong (Long) Face**

Based on the detected face shape and geometric observations, FaceStyle AI recommends personalized hairstyles across multiple categories (Short, Medium, Long, Straight, Wavy, Curly, Modern, Traditional, Male, Female, and Unisex) along with objective cosmetology styling advice and maintenance tips.

---

## 2. Key Features

- **Dual Image Input Modes:**
  - Direct image file upload (drag-and-drop, JPG, JPEG, PNG, up to 10 MB).
  - Live webcam capture with user permission, live video preview, and snapshot freeze.
- **468-Point Facial Landmark AI:**
  - Real-time landmark localization using Google MediaPipe Face Landmarker.
  - Automatic validation ensuring a face is present.
  - Multi-face validation preventing misleading predictions by asking the user to provide an image with a single face.
- **True Geometric Proportion Engine:**
  - Euclidean distance calculations for Face Length ($L$), Forehead Width ($W_f$), Cheekbone Width ($W_c$), and Jawline Width ($W_j$).
  - Anthropometric ratio heuristics ($R_{LW} = L / W_c$, $R_{FJ} = W_f / W_j$, $R_{CJ} = W_c / W_j$, $R_{FC} = W_f / W_c$).
  - Calibrated estimation confidence indicator.
  - High-tech neon landmark overlay visualization generator.
- **Personalized Hairstyle Recommendation Engine:**
  - Filterable by hair length (Short, Medium, Long), texture (Straight, Wavy, Curly), category (Modern, Traditional, Casual, Formal), and collection (Men, Women, Unisex).
  - One-click AJAX bookmarking to "My Favourites".
  - Objective, positive styling advice focused on balance without judgmental beauty ratings.
- **User Authentication & Dashboard:**
  - Registration, login (supporting username or email), and profile preference management.
  - Interactive dashboard showing recent analyses, facial proportion stats, and quick recommendations.
- **Privacy & Security Architecture:**
  - Optional photo retention: users can choose to discard uploaded photos after inference or save them in private history.
  - Complete history deletion and media file cleanup.
  - CSRF protection, secure password hashing, and authorization checks.
- **Full Django Admin Panel:**
  - Manage hairstyles, upload images, manage categories, and inspect user analysis records.

---

## 3. Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript ES6, Bootstrap 5, Font Awesome 6 |
| **Backend** | Python 3.12, Django 5.1 (Model-View-Template Architecture) |
| **AI & Computer Vision** | MediaPipe Face Landmarker (468 3D vertices), OpenCV (cv2), PIL (Pillow) |
| **Mathematical Logic** | NumPy & Euclidean geometry formulas |
| **Database** | SQLite3 (development) / MySQL compatible ORM |
| **Styling & Design** | Dark purple (`#1D063A`), lavender (`#E0AAFF`), soft pink (`#FF7597`) aesthetic |

---

## 4. Project Directory Structure

```text
FaceStyleAI/
│
├── manage.py                          # Django management runner
├── requirements.txt                   # Project dependencies
├── db.sqlite3                         # Database (pre-seeded with 28+ styles)
├── README.md                          # Comprehensive documentation & viva guide
│
├── facesite/                          # Project configuration package
│   ├── __init__.py
│   ├── settings.py                   # Settings (static, media, templates, database)
│   ├── urls.py                       # Root URL routing
│   └── wsgi.py                       # WSGI server gateway
│
├── main/                              # Core Django Application
│   ├── __init__.py
│   ├── apps.py                       # App configuration
│   ├── models.py                     # UserProfile, Hairstyle, FaceAnalysis, FavouriteHairstyle
│   ├── views.py                      # Controller logic for all 10+ pages
│   ├── urls.py                       # Application endpoints
│   ├── forms.py                      # Forms with strict validation & webcam handling
│   ├── admin.py                      # Customized Django Admin dashboard
│   ├── tests.py                      # 11 automated unit tests
│   ├── migrations/                   # Database schema migrations
│   └── management/
│       └── commands/
│           └── seed_hairstyles.py    # Database seeder generating 28+ hairstyles & images
│
├── ai_engine/                         # AI & Computer Vision Engine
│   ├── __init__.py
│   ├── face_detection.py             # MediaPipe detection & annotated image generation
│   ├── measurements.py               # Euclidean distance & geometric classification
│   ├── recommendation.py             # Hairstyle matching & cosmetology principles
│   └── models/
│       └── face_landmarker.task      # MediaPipe model asset (pre-packaged)
│
├── templates/                         # HTML5 Django Templates
│   ├── base.html                     # Navbar, flash messages, footer
│   ├── home.html                     # Hero landing page & features
│   ├── register.html                 # User signup with validation
│   ├── login.html                    # User signin
│   ├── dashboard.html                # User dashboard & metrics
│   ├── upload.html                   # Dual mode (File Upload / Webcam Capture)
│   ├── result.html                   # Face shape report & hairstyle recommendations
│   ├── hairstyles.html               # Searchable & filterable hairstyle catalog
│   ├── hairstyle_detail.html         # Individual hairstyle detail & tips
│   ├── favourites.html               # Saved hairstyles collection
│   ├── history.html                  # Chronological analysis history
│   ├── confirm_delete.html           # Deletion confirmation
│   ├── profile.html                  # User profile & hair preferences
│   ├── about.html                    # Mathematical theory & college viva guide
│   └── includes/
│       └── hairstyle_card.html       # Reusable hairstyle card component
│
├── static/                            # Static Assets
│   ├── css/
│   │   └── style.css                 # Custom design system & animations
│   └── js/
│       └── main.js                   # Webcam streamer, AJAX favorites, UI scanner
│
└── media/                             # Dynamic Media Storage
    ├── hairstyles/                   # Seeded hairstyle visual graphics
    ├── uploads/                      # User portraits (when user opts to retain)
    └── annotated/                    # Neon AI landmark visualization outputs
```

---

## 5. Quick Installation & Setup

### Step 1: Open Terminal in Project Root
Navigate to the directory:
```bash
cd C:\Users\abhis\.gemini\antigravity\scratch\FaceStyleAI
```

*(Recommended: Set `C:\Users\abhis\.gemini\antigravity\scratch\FaceStyleAI` as your active workspace in your IDE).*

### Step 2: Install Dependencies (if not already installed)
```bash
pip install -r requirements.txt
```
*(Packages: `Django>=5.1.0`, `mediapipe>=0.10.0`, `opencv-python>=4.8.0`, `numpy>=1.24.0`, `pillow>=10.0.0`)*

### Step 3: Apply Migrations & Seed Hairstyle Database
The database already comes pre-migrated and pre-seeded, but you can re-run at any time:
```bash
python manage.py migrate
python manage.py seed_hairstyles
```

### Step 4: Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 6. Default Admin Credentials

A superuser account is already configured for easy evaluation and viva demonstration:

- **Admin Login URL:** `http://127.0.0.1:8000/admin/`
- **Username:** `admin`
- **Password:** `admin123`

### In Django Admin, you can:
- View all registered users and their profiles.
- Add, edit, or delete hairstyles (uploading custom photos, changing compatible face shapes).
- Inspect `Face Analysis Records` (viewing geometric measurements and landmark visualizations).
- Track user favourites and bookmarks.

---

## 7. How Face Shape Detection Works (For Viva Examiners)

### 1. Key 468-Mesh Landmarks
- **Trichion / Upper Forehead Midline:** Vertex `10`
- **Gnathion / Lowest Chin Point:** Vertex `152`
- **Cheekbones (Zygomatic Arches):** Vertices `234` (Right) and `454` (Left)
- **Forehead Temples:** Vertices `103` (Right) and `332` (Left)
- **Jawline Angles (Gonions):** Vertices `58` (Right) and `288` (Left)

### 2. Anthropometric Formulas
$$\text{Face Length } (L) = \text{dist}(\text{Vertex } 10, \text{Vertex } 152)$$
$$\text{Cheekbone Width } (W_c) = \text{dist}(\text{Vertex } 234, \text{Vertex } 454)$$
$$\text{Forehead Width } (W_f) = \text{dist}(\text{Vertex } 103, \text{Vertex } 332)$$
$$\text{Jaw Width } (W_j) = \text{dist}(\text{Vertex } 58, \text{Vertex } 288)$$

### 3. Classification Decision Matrix
- **Oval:** $1.30 \le L / W_c \le 1.48$, $W_f \ge W_j$, with soft curved jawline.
- **Round:** $L / W_c < 1.30$, cheekbones are widest ($W_c > W_f, W_c > W_j$), circular contour.
- **Square:** $L / W_c < 1.30$, $W_f \approx W_c \approx W_j$ (ratios within 10-15%), sharp angular jaw corners.
- **Heart:** $W_f / W_j > 1.25$, wide forehead tapering to a narrow chin.
- **Diamond:** $W_c > W_f$ and $W_c > W_j$ with narrow forehead ($W_f / W_c < 0.90$) and tapered jaw.
- **Oblong:** $L / W_c > 1.48$, elongated vertical silhouette with parallel sides.

---

## 8. Complete Project Viva Demonstration Workflow

Follow this sequence during your project evaluation to impress external examiners:

1. **Demonstrate Landing Page (`/`):**
   - Showcase the modern, dark purple & lavender aesthetic with glassmorphism.
   - Point out the 3-step pipeline, 6 face shape category cards, and trending hairstyles.
2. **Demonstrate User Registration & Login (`/register/` and `/login/`):**
   - Create a new student user account.
   - Show validation error handling (e.g. mismatched passwords).
   - Sign in and land on the **User Dashboard** (`/dashboard/`).
3. **Demonstrate AI Face Analysis (`/analyze/`):**
   - Show the dual options: **Upload Image** vs. **Webcam Capture**.
   - Capture a live snapshot using the webcam or choose a portrait photo.
   - Point out the privacy toggle: *"Save photo thumbnail in my private history (optional)"*.
   - Click **"Analyze My Face"** to demonstrate the animated scanning progress bar.
4. **Demonstrate Face Shape Result Page (`/result/<id>/`):**
   - Explain the detected face shape and calibrated confidence meter.
   - Click the **"View AI Landmarks"** button to toggle the high-tech glowing mesh overlay.
   - Review the **Anthropometric Proportions Table** and **AI Geometric Observations**.
   - Browse the recommended hairstyles filtered by Short, Medium, and Long.
   - Click the heart icon to save a style to **Favourites** via AJAX.
5. **Demonstrate Hairstyle Catalog (`/hairstyles/`):**
   - Filter hairstyles by length, texture, category, and face shape.
   - Open a hairstyle detail page (`/hairstyles/<id>/`) to view styling and maintenance tips.
6. **Demonstrate Saved Favourites & History (`/favourites/` and `/history/`):**
   - Show the bookmarked hairstyles in the favourites collection.
   - Open the history page to view chronological past tests.
   - Demonstrate the privacy deletion feature by removing a record.
7. **Demonstrate Django Admin Dashboard (`/admin/`):**
   - Log in as `admin` / `admin123`.
   - Show Hairstyle CRUD operations, Face Analysis records, and User Profiles.
8. **Run Unit Tests:**
   - Run `python manage.py test main` in the terminal to show all 11 automated test cases passing.

---

## 9. Switching to MySQL Database (Optional)

The project is built using standard Django ORM with full MySQL compatibility. To switch to MySQL for college lab presentation:

1. Install `mysqlclient` or `PyMySQL`:
   ```bash
   pip install pymysql
   ```
2. Open `facesite/settings.py` and replace `DATABASES['default']` with:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'facestyle_ai_db',
           'USER': 'root',
           'PASSWORD': 'your_mysql_password',
           'HOST': '127.0.0.1',
           'PORT': '3306',
           'OPTIONS': {
               'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
               'charset': 'utf8mb4',
           }
       }
   }
   ```
3. Run `python manage.py migrate` and `python manage.py seed_hairstyles`.

---

## 10. Authors & Acknowledgments

- **Student:** TY B.Sc. Information Technology
- **Project Title:** FaceStyle AI – AI-Based Face Shape Detection & Hairstyle Recommendation System
- **Frameworks & AI Libraries:** Google MediaPipe, OpenCV, Django Project Community, Bootstrap
