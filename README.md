# 🚀 CashNova

CashNova is a full-stack MERN application for managing shared group expenses efficiently.  
It enables users to create groups, add expenses, track balances, and analyze spending in a clean, modern interface.

🔗 GitHub Repository: https://github.com/Yungstunner/CashNova  

---

# 🌐 Live Application & Demo

🚀 Live App:  
👉 https://cash-nova.vercel.app/

🎬 Demo Video:  
👉 https://drive.google.com/file/d/1ymlphmbwZU8cNNVjJKoYRyBYJ0FGSQIg/view?usp=drive_link 

---

# 🧠 What CashNova Solves

Managing shared expenses in trips, hostels, teams, or events becomes messy.  
CashNova simplifies this by:

- Creating expense groups
- Tracking who paid what
- Automatically displaying balances
- Filtering expenses by category or description
- Providing structured analytics

---

# 🛠️ Tech Stack

## Frontend
- React.js
- Ant Design
- Context API
- Axios

## Backend
- Node.js
- Express.js
- MongoDB (Atlas)
- Mongoose
- JWT Authentication

## Integrations
- Google OAuth
- Gemini API
- Environment-based configuration

---

# 📁 Project Structure

```
CashNova/
│
├── backend/
│   ├── models/
│   ├── routes/
│   ├── controllers/
│   ├── middleware/
│   ├── connection.js
│   └── index.js
│
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── helpers/
│   ├── context/
│   ├── externalAPI/
│   └── App.jsx
│
├── .gitignore
└── README.md
```

---

# ⚙️ Complete Local Setup Guide

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Yungstunner/CashNova.git
cd CashNova
```

---

# 🔹 Backend Setup

```bash
cd backend
npm install
```

Create a `.env` file inside the **backend folder**:

```
MONGO_URL=your_mongodb_connection_string
PORT=4000
JWT_SECRET=your_super_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
GEMINI_API_KEY=your_gemini_api_key
```

⚠️ Important:
- Do NOT use quotes
- Keep `.env` inside backend folder only

---

### Start Backend

```bash
npm run dev
```

or

```bash
nodemon index.js
```

Backend runs at:

```
http://localhost:4000
```

---

# 🔹 Frontend Setup

Open new terminal:

```bash
cd frontend
npm install
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

# 🔗 Frontend-Backend Connection

Ensure `frontend/src/externalAPI/api.js` contains:

```js
const api = axios.create({
  baseURL: "http://localhost:4000/api"
});
```

For production:

```js
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL
});
```

---

# 📡 API Overview

| Method | Endpoint | Description |
|--------|----------|------------|
| POST | /api/auth/login | User login |
| POST | /api/auth/register | Register user |
| GET | /api/groups | Get user groups |
| POST | /api/groups | Create group |
| GET | /api/expenses/:groupId | Fetch group expenses |
| POST | /api/expenses | Add expense |

---

# ✨ Core Features

## 🔐 Authentication
- JWT-based login
- Google OAuth
- Protected routes

## 👥 Group Management
- Create groups
- View members
- Manage shared expenses

## 💰 Expense Tracking
- Add expenses
- Display payer
- Real-time updates
- Date formatting

## 🔎 Smart Filtering
- Search by description
- Filter by category

## 📊 Analytics
- Expense breakdown
- Balance tracking

---

# 🚀 Production Deployment Guide

## Backend Deployment (Render / Railway / VPS)

1. Deploy backend folder
2. Add environment variables in hosting dashboard
3. Start command:

```
node index.js
```

---

## Frontend Deployment (Vercel / Netlify)

1. Deploy frontend folder
2. Add environment variable:

```
REACT_APP_API_URL=https://your-backend-url/api
```

3. Redeploy

---

# 🔐 Security Practices

- JWT authentication
- MongoDB Atlas secure connection
- Environment variable isolation
- Protected API routes
- No sensitive data exposed in frontend

---

# 📈 Future Enhancements

- WebSocket real-time sync
- Push notifications
- Expense export (PDF/CSV)
- Advanced analytics dashboard
- Mobile-first UI optimization

---

# 👨‍💻 Author

Siddhant Dwivedi  
Backend-Focused Developer  
GitHub: https://github.com/Yungstunner  

---

⭐ If you found this project helpful, consider giving it a star!
