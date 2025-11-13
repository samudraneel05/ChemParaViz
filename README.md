# ChemParaViz - Chemical Equipment Parameter Visualizer

A modern hybrid web and desktop application for visualizing chemical equipment data. Upload CSV files and get instant analytics with beautiful charts, detailed statistics, and downloadable PDF reports.

Built as a technical screening project for FOSSEE 2025 demonstrating full-stack development with React, Django, and PyQt5.

## Features

### Core Functionality
- **CSV Data Upload & Processing** - Drag and drop CSV files with equipment parameters
- **Real-time Data Analytics** - Instant calculation of averages, counts, and distributions
- **Interactive Visualizations** - Beautiful charts showing equipment distribution and parameter trends
- **Statistical Distribution** - Quartile analysis with gradient bar visualizations
- **Dynamic Filtering** - Filter data by equipment type and visualize specific parameters
- **PDF Report Generation** - One-click export of complete analysis reports
- **Dataset History** - Automatically saves your last 5 datasets for quick access

### Technical Highlights
- **Dual Platform Support** - Identical functionality on web (React) and desktop (PyQt5)
- **RESTful API** - Clean Django REST Framework backend
- **Secure Authentication** - Token-based user authentication
- **Professional UI** - Minimalist design with Inter font and consistent color palette
- **Responsive Layout** - Adapts seamlessly to different screen sizes

## Design System

The application features a clean, professional aesthetic:
- **Colors**: Monochrome palette with blue-teal-green accent spectrum
- **Typography**: Inter for UI, JetBrains Mono for data
- **Layout**: Minimal borders (1px), subtle radius (2px), clean spacing
- **Charts**: Color-coded visualizations (#0284c7 → #14b8a6 → #84cc16)

## Project Structure

```
ChemParaViz/
├── backend/                    # Django Backend
│   ├── chemparaviz/           # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── api/                   # API application
│   │   ├── models.py         # Database models
│   │   ├── views.py          # API endpoints
│   │   ├── serializers.py    # Data serializers
│   │   ├── utils.py          # Utility functions
│   │   └── pdf_generator.py  # PDF report generation
│   ├── manage.py
│   └── requirements.txt
│
├── frontend-web/              # React Web Application
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Login.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Auth.css
│   │   │   └── Dashboard.css
│   │   ├── contexts/         # Context providers
│   │   │   └── AuthContext.js
│   │   ├── services/         # API services
│   │   │   └── api.js
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   │   └── index.html
│   └── package.json
│
├── frontend-desktop/          # PyQt5 Desktop Application
│   ├── main.py               # Main application file
│   └── requirements.txt
│
├── sample_equipment_data.csv  # Sample dataset
├── instructions.txt           # Project requirements
└── README.md                  # This file
```

## 📋 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend (Web) | React.js + Chart.js | Interactive web interface with charts |
| Frontend (Desktop) | PyQt5 + Matplotlib | Native desktop application |
| Backend | Django + Django REST Framework | RESTful API server |
| Data Processing | Pandas | CSV parsing and analytics |
| Database | SQLite | Dataset storage |
| Reports | ReportLab | PDF report generation |

## Quick Start

### Prerequisites
- Python 3.8+ (tested with Python 3.13)
- Node.js 14+ and npm
- macOS, Linux, or Windows

### 1. Backend Setup (Django API)

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # macOS/Linux
# or: venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create your user account
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

✅ Backend running at `http://localhost:8000`

### 2. Web App Setup (React)

```bash
# Open a new terminal, navigate to web frontend
cd frontend-web

# Install dependencies
npm install

# Start development server
npm start
```

✅ Web app opens automatically at `http://localhost:3000`

### 3. Desktop App Setup (PyQt5)

```bash
# Open a new terminal, navigate to desktop frontend
cd frontend-desktop

# Use the same virtual environment from backend
source ../backend/venv/bin/activate

# Install desktop dependencies
pip install PyQt5 matplotlib requests

# Launch the app
python main.py
```

✅ Desktop app window opens

## 📝 Using the Application

### First Time Setup
1. **Register an account** - Use the web or desktop app to create your account
2. **Upload sample data** - Use the provided `sample_equipment_data.csv` file
3. **Explore the dashboard** - View charts, statistics, and data tables

### CSV File Format

Your CSV must have these exact column names:

| Column Name | Data Type | Example |
|------------|-----------|---------|
| Equipment Name | String | Pump-1, Valve-2 |
| Type | String | Pump, Compressor, Valve |
| Flowrate | Float | 120.0, 95.5 |
| Pressure | Float | 5.2, 8.4 |
| Temperature | Float | 110.0, 95.0 |

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120.0,5.2,110.0
Compressor-1,Compressor,95.0,8.4,95.0
Valve-1,Valve,60.0,4.1,105.0
```

See `sample_equipment_data.csv` for a complete working example.

## 🔌 API Reference

For complete API documentation including all endpoints, request/response examples, authentication details, and usage examples, see **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**.

**Quick overview:**
- `POST /api/auth/register/` - Create account
- `POST /api/auth/login/` - Get auth token
- `POST /api/upload/` - Upload CSV dataset
- `GET /api/datasets-list/` - List all your datasets
- `GET /api/dataset/{id}/` - Get dataset details + analytics
- `GET /api/dataset/{id}/report/` - Download PDF report
- `DELETE /api/dataset/{id}/delete/` - Delete dataset
- `GET /api/history/` - Get recent uploads

## 🎯 Usage Guide

### Web Application

1. **Register/Login**: Create an account or login with existing credentials
2. **Upload Data**: Click "Choose CSV File" and select your dataset
3. **View Analytics**: See real-time statistics and charts
4. **Download Reports**: Generate PDF reports for any dataset
5. **Manage History**: View and delete previous uploads

### Desktop Application

1. **Login**: Enter your credentials (same as web app)
2. **Upload Dataset**: Click "Choose CSV File" to upload
3. **View Visualizations**: Charts appear automatically using Matplotlib
4. **Download Reports**: Save PDF reports to your computer
5. **Delete Datasets**: Remove unwanted datasets

## Common Workflows

### Uploading Your First Dataset

**Web App:**
1. Login at `http://localhost:3000`
2. Click "Choose CSV File" button in the upload section
3. Select your CSV (must match the format above)
4. Click "Upload" and wait for processing
5. Dashboard updates automatically with your data

**Desktop App:**
1. Launch the app and login
2. Click "Choose CSV File" button
3. Select your CSV file
4. Click "Upload" button
5. Charts render immediately after processing

### Analyzing Equipment Data

Once uploaded, you'll see:
- **Total count** of equipment items in your dataset
- **Average values** for flowrate, pressure, and temperature
- **Distribution charts** showing quartile ranges for each parameter
- **Equipment type breakdown** showing how many of each type you have
- **Dynamic visualizer** - filter by equipment type, parameter, and chart style

### Generating Reports

1. View any dataset in the dashboard
2. Click the "Download Report" button
3. PDF downloads automatically with:
   - Summary statistics
   - Equipment type distribution
   - Complete data table

### Managing Your Data

- **Delete datasets** you no longer need using the delete button
- **View history** of recent uploads in the history section
- **Switch between datasets** to compare different sets of equipment

## Troubleshooting

### "Invalid credentials" when logging in
- **Make sure you've registered first** using the same username/password
- Check that backend is running (`http://localhost:8000`)
- Try registering via web app first, then use same credentials in desktop app

### CSV upload fails
- **Column names must match exactly**: `Equipment Name,Type,Flowrate,Pressure,Temperature`
- Check for extra spaces or special characters
- Numbers should be numeric (not text)
- Use the provided `sample_equipment_data.csv` as a template

### Charts not displaying
- **Web**: Hard refresh the page (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)
- **Desktop**: Close and reopen the application
- Check browser console (F12) for JavaScript errors

### Backend won't start
- **Port 8000 already in use**: Another app is using that port
  ```bash
  # Find what's using port 8000
  lsof -i :8000
  # Kill it or use a different port
  python manage.py runserver 8001
  ```
- **Database locked**: Close any other Django processes
- **Module import errors**: Activate your virtual environment first

### Desktop app crashes on startup
- **PyQt5 installation issue**: Reinstall with `pip install --upgrade PyQt5`
- **Matplotlib backend error**: Update matplotlib `pip install --upgrade matplotlib`
- **Cannot connect to API**: Start the Django backend first

### PDF download fails
- Check that ReportLab is installed: `pip install reportlab`
- Ensure dataset has data (can't generate report for empty dataset)
- Check browser's download folder permissions

### Desktop Application
```bash
cd frontend-desktop
# Install PyInstaller
pip install pyinstaller

# Build standalone executable
pyinstaller --onefile --windowed --name ChemParaViz main.py

# Find executable in 'dist/' folder
```

### Backend Deployment
```bash
# Use gunicorn for production
pip install gunicorn
gunicorn chemparaviz.wsgi:application --bind 0.0.0.0:8000

# Or use Docker, nginx + uWSGI, etc.
```

## Additional Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference with examples
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Architecture and design overview

## About This Project

Built as a technical screening task to demonstrate:
- Full-stack development (Django + React + PyQt5)
- RESTful API design and implementation
- Data processing with Pandas
- Professional UI/UX design
- Cross-platform development
- Clean, maintainable code

## Support

If something isn't working:
1. Check this README's troubleshooting section
2. Look at the console/terminal output for error messages
3. Verify all prerequisites are installed
4. Make sure the backend is running before starting frontends



---

**Built with attention to design, functionality, and user experience** 
