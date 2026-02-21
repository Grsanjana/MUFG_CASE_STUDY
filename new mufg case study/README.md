# DataTransform Pro - Banking & Finance Dataset Operations Platform

Enterprise-grade web application for banking and finance dataset operations with data cleaning, mathematical operations, and advanced financial analysis.

## Features

- **Step 1: Upload Dataset** - Drag & drop support for CSV, XLS, XLSX files
- **Step 2: Cleaning Operations** - Remove nulls, duplicates, rename columns, change data types, trim whitespaces
- **Step 3: Mathematical Operations** - Sum, Average, Min, Max, Count
- **Step 4: Advanced Financial Operations** - Gross Profit, Net Profit, Monthly P&L, Quarterly P&L

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Open `frontend/index.html` in a web browser, or

2. Use a local server (recommended):
   - Python: `python -m http.server 8000` (from frontend directory)
   - Node.js: `npx serve` (from frontend directory)

3. Open `http://localhost:8000` in your browser

## API Endpoints

### Upload
- `POST /upload` - Upload CSV/XLS/XLSX file

### Cleaning Operations
- `POST /clean/remove-null` - Remove null values
- `POST /clean/remove-duplicate` - Remove duplicate rows
- `POST /clean/rename-columns` - Rename columns
- `POST /clean/change-datatypes` - Change data types
- `POST /clean/trim-whitespaces` - Trim whitespaces

### Mathematical Operations
- `POST /math/sum` - Calculate sum
- `POST /math/average` - Calculate average
- `POST /math/min` - Find minimum
- `POST /math/max` - Find maximum
- `POST /math/count` - Count values

### Advanced Financial Operations
- `POST /advanced/pl/gross-profit` - Calculate gross profit
- `POST /advanced/pl/net-profit` - Calculate net profit
- `POST /advanced/pl/monthly` - Monthly P&L statement
- `POST /advanced/pl/quarterly` - Quarterly P&L statement

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python, Flask, Pandas
- **Data Processing**: Pandas for CSV/Excel operations

## Notes

- All data processing is done in-memory (no database required)
- The application supports CSV, XLS, and XLSX file formats
- CORS is enabled for cross-origin requests

