# How to Run DataTransform Pro

## Quick Start Guide

### Step 1: Start the Backend Server

Open a **PowerShell** or **Command Prompt** terminal and run:

```powershell
cd "C:\Users\HP\OneDrive\Desktop\new mufg case study\backend"
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

**Keep this terminal window open!** The backend must be running for the app to work.

---

### Step 2: Open the Frontend

You have **3 options**:

#### Option A: Open Directly (Easiest)
1. Navigate to: `C:\Users\HP\OneDrive\Desktop\new mufg case study\frontend\`
2. Double-click `index.html`
3. It will open in your default browser

#### Option B: Use Python HTTP Server (Recommended)
Open a **NEW** terminal window and run:

```powershell
cd "C:\Users\HP\OneDrive\Desktop\new mufg case study\frontend"
python -m http.server 8000
```

Then open your browser and go to: **http://localhost:8000**

#### Option C: Use Live Server (VS Code Extension)
If you're using VS Code:
1. Right-click on `index.html`
2. Select "Open with Live Server"

---

## Complete Command Sequence

### Terminal 1 (Backend):
```powershell
cd "C:\Users\HP\OneDrive\Desktop\new mufg case study\backend"
python app.py
```

### Terminal 2 (Frontend - Optional, only if using Option B):
```powershell
cd "C:\Users\HP\OneDrive\Desktop\new mufg case study\frontend"
python -m http.server 8000
```

---

## Verify It's Working

1. ✅ Backend running: Check terminal shows "Running on http://127.0.0.1:5000"
2. ✅ Frontend open: You should see "DataTransform Pro ✨" header
3. ✅ Test upload: Try uploading a CSV file

---

## Troubleshooting

**Backend won't start?**
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Check if port 5000 is already in use

**Frontend can't connect to backend?**
- Make sure backend is running on port 5000
- Check browser console for errors (F12)

**File upload not working?**
- Make sure backend is running
- Check file format (CSV, XLS, or XLSX)

---

## That's It!

Once both are running, you can:
1. Upload a dataset (CSV/XLS/XLSX)
2. Clean your data
3. Perform mathematical operations
4. Run financial analysis

Enjoy! 🚀

