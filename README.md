#  Credit Approval System - Django Backend API

A backend API project built with Django and Django REST Framework to manage a credit approval system. It handles customer data, loan applications, and automated loan approval decisions based on custom business logic.

---

## 🔧 Features

* Create and manage customer records
* Submit and evaluate loan applications
* Loan approval based on credit rules
* RESTful API built with Django REST Framework
* PostgreSQL database integration
* Environment variable support for credentials

---

## 🛠 Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** PostgreSQL
* **Tools:** Postman (for testing), Git, GitHub
* **Language:** Python 3.x

---

##  Project Structure

```
credit_approval_system/
├── api/                    # App containing models, views, serializers
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
├── credit_approval_system/ # Django project settings
│   ├── settings.py
│   ├── urls.py
├── manage.py
├── requirements.txt
└── .env
```

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/credit-approval-system.git
cd credit-approval-system
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up `.env` File

Create a `.env` file in the root directory and add your database credentials:

```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run Development Server

```bash
python manage.py runserver
```

---

##  API Endpoints Overview

| Method | Endpoint           | Description             |
| ------ | ------------------ | ----------------------- |
| POST   | `/api/register/`  | Create a new customer   |
| POST   | `/api//check-eligibility`      | check-eligiblity     |
| POST    | `/api//create-loan` | create new loan |
| GET    | `/api/view-loan/<id>` | get loan details by loan id |
| GET    | `/api/view-loans/<id>` | get loans by customer id |


Sample JSON payload for loan request:

```json
{
  "customer_id": 5,
  "loan_amount": 50000,
  "interest_rate": 10.5,
  "tenure": 12
}
```

---

##  Demo

 YouTube Demo: [Watch the video](https://youtu.be/rOyFIYvAHPM)

---

## 💻 Author

**Vikas Bansode**
📧 [vikasbansode804@gmail.com](mailto:vikasbansode804@gmail.com)
🌐 [Portfolio Website](https://codebyvikas.xyz)


