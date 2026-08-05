# 📊 Vendor Performance Analysis Dashboard

## 📌 Project Overview

The Vendor Performance Analysis project is an end-to-end data analytics solution designed to evaluate vendor performance using real-world inventory, purchasing, and sales data. The project integrates PostgreSQL, Python, and Power BI to transform raw transactional data into meaningful business insights that support data-driven decision-making.

The dashboard provides insights into sales performance, purchasing trends, profitability, vendor contribution, inventory efficiency, and freight costs through interactive visualizations.

---

## 🎯 Objectives

- Analyze vendor sales and purchase performance.
- Identify top-performing vendors and brands.
- Evaluate vendor profitability using Gross Profit and Profit Margin.
- Monitor inventory efficiency using Stock Turnover.
- Analyze purchase contribution across vendors.
- Enable interactive drill-down analysis using Power BI Decomposition Tree.
- Build a scalable ETL pipeline for automated data preparation.

---

## 📂 Dataset

The project uses a real-world inventory dataset containing information about:

- Vendors
- Products
- Purchases
- Sales
- Freight Charges
- Purchase Prices
- Inventory Details

---

## 🛠 Tech Stack

### Programming

- Python

### Database

- PostgreSQL

### Data Analysis

- Pandas
- NumPy

### Data Visualization

- Power BI

### ETL & Database Connectivity

- SQLAlchemy
- psycopg2

### Version Control

- Git
- GitHub

---

## 📁 Project Structure

```
Vendor-Performance-Analysis/
│
├── data/
├── notebooks/
├── scripts/
│   ├── ingestion.py
│   ├── vendor_summary.py
│   └── ...
│
├── dashboard/
│   └── Vendor_Performance.pbix
│
├── logs/
│
├── requirements.txt
│
└── README.md
```

---

## ⚙️ Workflow

### 1. Data Collection

Raw inventory and sales datasets are collected.

↓

### 2. Data Cleaning

- Missing value handling
- Data type conversion
- Duplicate removal
- Data validation

↓

### 3. ETL Pipeline

Python automates:

- Data preprocessing
- Business metric calculation
- PostgreSQL loading

↓

### 4. Database

Processed data is stored in PostgreSQL.

↓

### 5. Dashboard Development

Power BI connects directly with PostgreSQL to create an interactive dashboard.

---

## 📈 Business Metrics Calculated

- Total Sales
- Total Purchase
- Gross Profit
- Profit Margin
- Stock Turnover
- Sales-to-Purchase Ratio
- Unsold Capital
- Freight Cost

---

## 📊 Dashboard Features

### KPI Cards

- Total Sales
- Total Purchase
- Gross Profit
- Profit Margin
- Unsold Capital

### Interactive Visualizations

- Purchase Contribution by Vendor (Donut Chart)
- Top Vendors by Sales
- Top Brands by Sales
- Low Performing Vendors
- Sales Performance Breakdown (Decomposition Tree)

---

## 🔍 Key Insights

- Identified vendors generating the highest revenue.
- Measured vendor profitability through Gross Profit and Profit Margin.
- Compared purchase and sales trends.
- Detected vendors with low inventory turnover.
- Analyzed brand-wise sales contribution.
- Enabled interactive drill-down from Vendor → Brand → Product Volume.

---

## 🚀 Key Features

- End-to-End ETL Pipeline
- Automated Data Cleaning
- PostgreSQL Integration
- Interactive Power BI Dashboard
- Dynamic DAX Measures
- Drill-Down Analytics
- Business KPI Monitoring

---

## 📷 Dashboard Preview

<img width="1276" height="720" alt="image" src="https://github.com/user-attachments/assets/1c822dae-0163-4126-8573-e4cb5e838861" />


---

## Future Improvements

- Forecast future sales using Machine Learning.
- Automated dashboard refresh.
- Vendor risk scoring.
- Sales forecasting.
- Inventory demand prediction.

---

## 👨‍💻 Author

**Karan Singh**

B.Tech Artificial Intelligence & Machine Learning

Chandigarh Group of Colleges, Jhanjeri

---

## ⭐ If you found this project useful, consider giving it a star!
