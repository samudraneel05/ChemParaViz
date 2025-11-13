# ChemParaViz API Documentation

Complete reference for all API endpoints. For quick setup, see [README.md](README.md).

**Base URL:** `http://localhost:8000/api`

---

## 🔐 Authentication

All endpoints require authentication **except** registration and login.

**How it works:**
1. Register or login to get a token
2. Include token in all subsequent requests
3. Token never expires (for this project)

**Header format:**
```
Authorization: Token <your_token_here>
```

---

## 📋 Endpoints Overview

| Endpoint | Method | Auth Required | Purpose |
|----------|--------|---------------|---------|
| `/auth/register/` | POST | ❌ | Create new account |
| `/auth/login/` | POST | ❌ | Get auth token |
| `/upload/` | POST | ✅ | Upload CSV dataset |
| `/datasets-list/` | GET | ✅ | List all your datasets |
| `/dataset/{id}/` | GET | ✅ | Get dataset details + analytics |
| `/dataset/{id}/report/` | GET | ✅ | Download PDF report |
| `/dataset/{id}/delete/` | DELETE | ✅ | Delete dataset |
| `/history/` | GET | ✅ | Get 5 most recent datasets |

---

## 🚀 Getting Started

### 1. Create an Account

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password",
    "email": "you@example.com"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "you@example.com"
  },
  "token": "your-sample-token"
}
```

💾 **Save that token!** You'll need it for all other requests.

### 2. Login (If Already Registered)

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "you@example.com"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Common errors:**
- `400 Bad Request` - Missing username or password
- `401 Unauthorized` - Wrong username/password

---

## 📤 Upload Dataset

```bash
curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Token your_token_here" \
  -F "file=@sample_equipment_data.csv"
```

**What happens:**
1. CSV is validated (correct columns, data types)
2. Data is parsed and stored in database
3. Statistics are calculated automatically
4. Dataset ID is returned

```json
{
  "id": 1,
  "filename": "equipment_data.csv",
  "uploaded_at": "2025-11-13T10:30:00Z",
  "total_count": 15,
  "avg_flowrate": 118.5,
  "avg_pressure": 5.8,
  "avg_temperature": 115.3,
  "equipment_type_distribution": {
    "Pump": 4,
    "Valve": 3,
    "Compressor": 2,
    "HeatExchanger": 2,
    "Reactor": 2,
    "Condenser": 2
  }
}
```

**Common errors:**
- `400 Bad Request` - CSV format is wrong (missing columns, invalid data)
- `401 Unauthorized` - Missing or invalid token

**CSV Requirements:**
- Must have these exact column names: `Equipment Name,Type,Flowrate,Pressure,Temperature`
- Flowrate, Pressure, Temperature must be numeric
- No empty rows

---

## 📊 Get All Your Datasets

```bash
curl -X GET http://localhost:8000/api/datasets-list/ \
  -H "Authorization: Token your_token_here"
```

**Response:**
```json
[
  {
    "id": 1,
    "filename": "equipment_data.csv",
    "uploaded_at": "2025-11-13T10:30:00Z",
    "total_count": 15,
    "avg_flowrate": 118.5,
    "avg_pressure": 5.8,
    "avg_temperature": 115.3
  },
  {
    "id": 2,
    "filename": "another_dataset.csv",
    "uploaded_at": "2025-11-14T14:20:00Z",
    "total_count": 20,
    "avg_flowrate": 125.0,
    "avg_pressure": 6.2,
    "avg_temperature": 120.0
  }
]
```

Returns an **empty array** `[]` if you haven't uploaded anything yet.

---

## 🔍 Get Dataset Details

```bash
curl -X GET http://localhost:8000/api/dataset/1/ \
  -H "Authorization: Token your_token_here"
```

**What you get:**
- Summary statistics (count, averages)
- Equipment type breakdown
- **Full list of all equipment** with their measurements

**Response:**
```json
{
  "total_count": 15,
  "averages": {
    "flowrate": 118.5,
    "pressure": 5.8,
    "temperature": 115.3
  },
  "equipment_type_distribution": {
    "Pump": 4,
    "Valve": 3,
    "Compressor": 2
  },
  "equipment_details": [
    {
      "equipment_name": "Pump-1",
      "equipment_type": "Pump",
      "flowrate": 120.0,
      "pressure": 5.2,
      "temperature": 110.0
    },
    {
      "equipment_name": "Compressor-1",
      "equipment_type": "Compressor",
      "flowrate": 95.0,
      "pressure": 8.4,
      "temperature": 95.0
    },
    // ... all equipment items
  ]
}
```

**This is the data that powers the dashboard charts!**

**Errors:**
- `404 Not Found` - Dataset ID doesn't exist or doesn't belong to you
- `401 Unauthorized` - Invalid/missing token

---

## 📥 Download PDF Report

```bash
curl -X GET http://localhost:8000/api/dataset/1/report/ \
  -H "Authorization: Token your_token_here" \
  -o report.pdf
```

**What's in the report:**
- Dataset filename and upload date
- Summary statistics (count, averages)
- Equipment type distribution table
- Complete equipment details table

**Response:**
- Binary PDF file downloads immediately
- Filename: `{your_csv_name}_report.pdf`

**Errors:**
- `404 Not Found` - Dataset doesn't exist
- `500 Internal Server Error` - PDF generation failed (contact admin)

---

## 🗑️ Delete Dataset

```bash
curl -X DELETE http://localhost:8000/api/dataset/1/delete/ \
  -H "Authorization: Token your_token_here"
```

**Response:**
```json
{
  "message": "Dataset deleted successfully"
}
```

⚠️ **Warning:** This is permanent! The CSV file and all associated data are deleted.

**Errors:**
- `404 Not Found` - Dataset doesn't exist or isn't yours
- `401 Unauthorized` - Invalid/missing token

---

## 🕐 Get Recent History

```bash
curl -X GET http://localhost:8000/api/history/ \
  -H "Authorization: Token your_token_here"
```

**Response:** Last 5 datasets you uploaded (most recent first)
```json
[
  {
    "id": 5,
    "filename": "latest_data.csv",
    "uploaded_at": "2025-11-13T15:00:00Z",
    "total_count": 20,
    "avg_flowrate": 125.0,
    "avg_pressure": 6.5,
    "avg_temperature": 118.0
  },
  {
    "id": 4,
    "filename": "data_nov12.csv",
    "uploaded_at": "2025-11-12T14:30:00Z",
    "total_count": 15,
    "avg_flowrate": 120.0,
    "avg_pressure": 6.0,
    "avg_temperature": 115.0
  }
]
```

Returns **empty array** `[]` if you haven't uploaded anything.

---

## 📊 Understanding the Data

### What Gets Calculated

When you upload a CSV, the backend automatically:

1. **Counts** total equipment items
2. **Calculates averages** for flowrate, pressure, temperature
3. **Groups by type** - counts how many of each equipment type
4. **Validates** all data (correct types, no missing values)

### Equipment Type Distribution

Example:
```json
{
  "Pump": 4,
  "Valve": 3,
  "Compressor": 2,
  "HeatExchanger": 2,
  "Reactor": 2,
  "Condenser": 2
}
```

This means your dataset has 4 pumps, 3 valves, etc. These counts are used for the pie chart on the dashboard.

### Averages

```json
{
  "flowrate": 118.5,
  "pressure": 5.8,
  "temperature": 115.3
}
```

These are the **mean values** across all equipment. Used for the bar chart visualization.

---

## 🔧 Advanced Usage

### Testing with curl

**Complete workflow:**

```bash
# 1. Register
TOKEN=$(curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass"}' \
  | jq -r '.token')

# 2. Upload dataset
DATASET_ID=$(curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Token $TOKEN" \
  -F "file=@sample_equipment_data.csv" \
  | jq -r '.id')

# 3. Get details
curl -X GET http://localhost:8000/api/dataset/$DATASET_ID/ \
  -H "Authorization: Token $TOKEN"

# 4. Download report
curl -X GET http://localhost:8000/api/dataset/$DATASET_ID/report/ \
  -H "Authorization: Token $TOKEN" \
  -o report.pdf

# 5. Delete
curl -X DELETE http://localhost:8000/api/dataset/$DATASET_ID/delete/ \
  -H "Authorization: Token $TOKEN"
```

### Using with Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Login
response = requests.post(f"{BASE_URL}/auth/login/", json={
    "username": "your_username",
    "password": "your_password"
})
token = response.json()["token"]

# Upload CSV
headers = {"Authorization": f"Token {token}"}
files = {"file": open("sample_equipment_data.csv", "rb")}
response = requests.post(f"{BASE_URL}/upload/", headers=headers, files=files)
dataset = response.json()

print(f"Uploaded dataset {dataset['id']}: {dataset['filename']}")
print(f"Total count: {dataset['total_count']}")
print(f"Avg flowrate: {dataset['avg_flowrate']}")

# Get details
response = requests.get(f"{BASE_URL}/dataset/{dataset['id']}/", headers=headers)
details = response.json()
print(f"Equipment types: {details['equipment_type_distribution']}")

# Download report
response = requests.get(f"{BASE_URL}/dataset/{dataset['id']}/report/", headers=headers)
with open("report.pdf", "wb") as f:
    f.write(response.content)
```

---

## 🔒 Security Notes

- **Tokens never expire** in this version
- Each user can only see/modify their own datasets
- File uploads are limited to CSV format
- All data is stored in SQLite database locally

For production use, we can later implement:
- Token expiration and refresh
- Rate limiting
- File size limits
- Database migration to PostgreSQL
- HTTPS/SSL

---

## ❓ Common Issues

**"Invalid token" errors**
- Make sure you're including the word "Token" before your token
- Format: `Authorization: Token abc123...`
- Not: `Authorization: abc123...`

**"Dataset not found"**
- Check the dataset ID is correct
- Make sure it belongs to your user (can't access other users' datasets)

**CSV upload fails**
- Column names must match exactly (case-sensitive)
- Required: `Equipment Name,Type,Flowrate,Pressure,Temperature`
- No extra columns, no missing columns

**401 Unauthorized**
- You forgot the Authorization header
- Token is wrong/invalid
- Token format is wrong (missing "Token" prefix)

---

## 📚 Related Documentation

- **[README.md](README.md)** - Complete project overview and setup guide
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Architecture and design details

---

**Built for clarity and ease of use** 🚀

### Dataset
```python
{
  "id": int,
  "user": User,
  "filename": string,
  "file": FileField,
  "uploaded_at": datetime,
  "total_count": int,
  "avg_flowrate": float,
  "avg_pressure": float,
  "avg_temperature": float,
  "equipment_type_distribution": dict
}
```

### Equipment
```python
{
  "id": int,
  "dataset": Dataset,
  "equipment_name": string,
  "equipment_type": string,
  "flowrate": float,
  "pressure": float,
  "temperature": float
}
```

---

## CSV File Requirements

Your CSV file must have exactly these columns:

| Column Name | Type | Description |
|------------|------|-------------|
| Equipment Name | string | Unique identifier for equipment |
| Type | string | Equipment type (e.g., Pump, Valve) |
| Flowrate | float | Flow rate value |
| Pressure | float | Pressure value |
| Temperature | float | Temperature value |

**Example:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
```

---

## Error Codes

| Status Code | Meaning |
|------------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Request successful, no content to return |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Authentication required |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

---

## Rate Limiting

Currently, there is no rate limiting in the development version. For production deployment, implement appropriate rate limiting.

---

## Testing with cURL

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

### Upload CSV
```bash
curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "file=@sample_equipment_data.csv"
```

### Get Datasets
```bash
curl -X GET http://localhost:8000/api/datasets-list/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Download Report
```bash
curl -X GET http://localhost:8000/api/dataset/1/report/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -o report.pdf
```

---

## Postman Collection

Import this JSON into Postman for easy testing:

```json
{
  "info": {
    "name": "ChemParaViz API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Register",
          "request": {
            "method": "POST",
            "url": "{{baseUrl}}/auth/register/",
            "body": {
              "mode": "raw",
              "raw": "{\"username\":\"testuser\",\"password\":\"testpass123\"}"
            }
          }
        },
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "url": "{{baseUrl}}/auth/login/",
            "body": {
              "mode": "raw",
              "raw": "{\"username\":\"testuser\",\"password\":\"testpass123\"}"
            }
          }
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "baseUrl",
      "value": "http://localhost:8000/api"
    }
  ]
}
```
