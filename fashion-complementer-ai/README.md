# fashion-complementer-ai
An AI-powered fashion recommendation system that analyzes outfit images to suggest matching accessories using Computer Vision, CNNs, and a Node.js/React full-stack architecture.
great:)

---

## הוראות הרצה

### 1. MongoDB

פתח את MongoDB Compass או הרץ בטרמינל:
```
mongod
```
> מתחבר אוטומטית ל־`mongodb://localhost:27017` עם DB בשם `fashion_db`

---

### 2. Server (PyCharm)

פתח את תיקיית `server` ב־PyCharm.

**התקנת תלויות (פעם אחת):**
```
pip install -r requirements.txt
```

**הרצה:**

ב־PyCharm פתח את Terminal ורוץ מתוך תיקיית `server`:
```
cd server
```
```
uvicorn app.main:app --reload
```
> השרת יעלה על `http://localhost:8000`

---

### 3. Client (VS Code)

פתח את תיקיית `client` ב־VS Code.

**התקנת תלויות (פעם אחת):**
```
cd client
```

```
npm install
```

**הרצה:**
```
npm run dev
```
> האפליקציה תיפתח על `http://localhost:5173`
