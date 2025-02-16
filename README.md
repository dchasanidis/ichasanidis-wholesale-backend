---

# 📸 FastAPI Image Upload Service  

A lightweight FastAPI-based service for uploading, storing, retrieving, and updating image metadata with PostgreSQL as the database. Designed for scalability, this project leverages Docker for easy deployment.  

## 🚀 Features  
- 📤 **Upload Images**: Store images in a local directory and save metadata in a PostgreSQL database.  
- 🔄 **Update Metadata**: Modify business-related metadata for stored images.  
- 📥 **Retrieve Images**: Download stored images by ID.  
- 📋 **List All Images**: Fetch all uploaded images with metadata.  
- 🛠 **Docker Support**: Fully containerized setup using Docker Compose.  

## 📂 Project Structure  
```
📦 fastapi-image-service  
├── 📜 main.py           # FastAPI application with endpoints  
├── 📜 database.py       # Database models & connection setup  
├── 📜 Dockerfile        # Docker configuration for containerization  
├── 📜 docker-compose.yml # Docker Compose for database & app  
├── 📜 requirements.txt  # Dependencies for the project  
└── 📁 bucket            # Directory for storing uploaded images  
```  

## 🏗️ Setup & Installation  

### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/your-username/fastapi-image-service.git  
cd fastapi-image-service  
```

### **2️⃣ Set Up Environment Variables**  
Create a `.env` file (or modify `docker-compose.yml`):  
```ini
DB_HOST=db  
DB_USER=postgres  
DB_PASSWORD=mysecretpassword  
DB_NAME=ichasanidis_images  
DB_PORT=5432  
```

### **3️⃣ Run with Docker Compose**  
```sh
docker-compose up --build  
```
This starts both the FastAPI app and PostgreSQL database.

### **4️⃣ API Endpoints**  

| Method | Endpoint                 | Description |
|--------|--------------------------|-------------|
| `POST`  | `/images`               | Upload an image |
| `PUT`   | `/images/{img_id}`       | Update metadata |
| `GET`   | `/images/{img_id}`       | Retrieve an image |
| `GET`   | `/images`                | List all images |
| `GET`   | `/images/{img_id}/metadata` | Get image metadata |

### **5️⃣ Run Without Docker (Local Setup)**  
Make sure you have Python 3.9+ and PostgreSQL installed.  
```sh
pip install -r requirements.txt  
uvicorn main:app --host 0.0.0.0 --port 8000  
```

## 🛠️ Tech Stack  
- **FastAPI** - High-performance Python web framework  
- **SQLAlchemy** - ORM for PostgreSQL  
- **Docker & Docker Compose** - Containerized deployment  
- **Pydantic** - Data validation  

## 📜 License  
This project is open-source and available under the MIT License.  

---

Let me know if you'd like any modifications! 🚀
