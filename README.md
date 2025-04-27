
# DevOps Icons Library

Welcome to the **DevOps Icons Library**!  
This project contains **1000+ categorized tech logos and UI icons** available in **PNG** and **SVG** formats.  
It demonstrates modern DevOps practices using **GitHub**, **Jenkins**, and **Docker**.

## ✨ Features

- 1000+ high-quality icons
- Search and filter by **format** (PNG/SVG) and **category** (Technology, Social Media, Brands)
- Mobile-friendly and responsive design
- Built with **HTML**, **CSS**, **Vanilla JS (ES Modules)**
- Automated CI/CD pipeline using **Jenkins** and **Docker Hub**

---

## 📂 Project Structure

```
suryaakkala-icon-lib/
├── Dockerfile
├── Jenkinsfile
├── nginx.conf
├── README.md
└── src/
    ├── index.html
    ├── css/
    │   └── style.css
    ├── icons/
    │   ├── png/
    │   └── svg/
    ├── js/
    │   ├── app.mjs
    │   └── icons.mjs
    └── scripts/
        ├── fetch_icons.py
        └── listgenerator.py
```

---

## 🚀 How to Run Locally with Docker

Make sure you have **Docker** installed.  
If not, [download Docker here](https://www.docker.com/products/docker-desktop/).

### 1. Clone the repository

```bash
git clone https://github.com/suryaakkala/icon-lib.git
cd icon-lib
```

### 2. Build the Docker image

```bash
docker build -t icon-library .
```

### 3. Run the container

```bash
docker run -d -p 3000:80 --name icon-library-container icon-library
```

Your site will now be available at: [http://localhost:3000](http://localhost:3000)

---

## ⚙️ Jenkins CI/CD Pipeline Overview

The **Jenkinsfile** performs:

1. **Checkout** code from GitHub
2. **Build** Docker image
3. **Test** the container health (via `curl` check on port 3000)
4. **Deploy**: Push Docker image to Docker Hub if build succeeds

**Docker Hub credentials** are stored in Jenkins as a secret named `docker-hub-credentials`.

---

## 📊 Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Modules)
- **Backend Server**: Nginx (Alpine version)
- **Containerization**: Docker
- **CI/CD**: Jenkins
- **Version Control**: GitHub
