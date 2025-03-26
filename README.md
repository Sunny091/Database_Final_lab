# Traffic Accident Insight Web App

A Flask-powered web application for querying and visualizing traffic accident data in Taichung. This project provides insightful analytics based on location, time, weather, driving behavior, and more. Users can interactively select queries, input license or ID data, and receive detailed accident insights in real time.

---

## 🚀 Features

-   **Interactive Query Engine**
    -   Top districts by accident frequency
    -   Leading causing factors
    -   Time-of-day vs accident occurrence
    -   Correlation between protective gear and injury site
    -   Alcohol level vs injury severity
    -   Weather & location correlation
    -   Road condition vs accidents
    -   Time vs causing factor
    -   DUI accident hotspots by district
-   **Individual Record Lookup**

    -   Query using License Number + ID
    -   Full record mapped into human-readable format

-   **Localized Data Mapping**

    -   Converts coded values into Chinese labels (e.g., district names, accident types, road types, etc.)

-   **Dynamic CSV Rendering**

    -   Converts query result into table-ready CSV and displays via HTML templates

-   **Frontend Templates**
    -   Styled using images in `static/` (e.g., `poster.jpg`, `bg.jpg`)
    -   Display results in various formats based on query type

---

## 🌐 System Architecture

```plaintext
Browser (Form Input)
       |
       V
   Flask (app.py)
       |
       V
    MySQL Database  <--- data from: accident, location, time, road, state...
       |
       V
Templates: test.html / answer(x2).html / answer(search).html...
```

---

## 📁 Project Structure

```bash
project_root/
├── app.py
├── templates/
│   ├── test.html
│   ├── answer(x2).html
│   └── ...
├── static/
│   ├── bg.jpg
│   └── poster.jpg
```

---

## 💡 Technologies

-   **Backend:** Flask + Python
-   **Frontend:** HTML (Jinja2), CSS
-   **Database:** MySQL
-   **Deployment:** waitress

---

## 📖 Setup & Run

### 1. Install dependencies

```bash
pip install flask mysql-connector-python waitress
```

### 2. Configure MySQL

Make sure to have a local MySQL database named `lab` with required tables and data:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your-password",
    database="lab",
)
```

### 3. Launch app

```bash
python app.py
```

Visit: [http://localhost:8080](http://localhost:8080)

---

## 📅 Use Cases

-   For city transportation departments
-   Road safety analysis
-   Public education platforms
-   Academic research & student projects

---

## 🙏 Credits

Developed by [Chih-Hsuan, Shen & Yun-Chieh, Chang & Min-Yu, Liang]

---

## ✨ Future Improvements

-   Export results as downloadable `.csv`
-   Add chart visualizations (bar, line, heatmaps)
-   Mobile responsiveness
-   Login/auth for secure queries

---

## ✉️ Contact

For questions or collaboration: [s890919@gmail.com]
