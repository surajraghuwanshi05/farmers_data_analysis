# 🌱 Data Quality Check Project

## 📌 Project Overview

Ensuring data quality is crucial for maintaining accurate and reliable datasets. This project performs **validation checks** on **farmer-related data**, identifying inconsistencies and separating invalid records.  

The primary goal is to **detect missing, incorrect, or inconsistent data**, store failed records separately, and maintain a **clean dataset for further analysis**.  

Since removing invalid rows would significantly reduce the dataset, we have opted **not to exclude them** outright. Instead, these records are stored in a dedicated `failed_data.csv` file. Additional details regarding these issues can be found in the **logs** for further inspection. 
🌐 Live Streamlit App: [Farmers Data Analysis App](https://surajraghuwanshi05-farmers-data-analysis-main-pedjcf.streamlit.app/)

---

## 📊 Assumptions & Validation Rules

The project follows specific **assumptions and business rules** to validate data quality:  

- **Unique ID Validation:**  
  - The `uid` field must contain **unique** values.  

- **Mandatory Fields:**  
  - The following fields must **not be empty**:  
    - `uid` (Unique Identifier)  
    - `farmer_name`  
    - `program_year`  

- **Date & Format Validation:**  
  - `program_year` must follow the **YYYY** format.  

- **Geographical Constraints:**  
  - Plantations should only be held in specific regions:  
    - **Districts**: `['A', 'B']`  
    - **Blocks**: `['p', 'q', 'r', 's']`  

- **Tree Plantation Count Validation:**  
  - The total number of trees planted should be within the range **350-450**.  

- **Species-Wise Tree Count Verification:**  
  - The **sum of species-wise tree counts** should match the `tree_planted` column.  

- **Contract & Payment Validation:**  
  - If a **contract is uploaded**, then **payment must be collected**.  

---

## 🔍 Key Findings  

### 🌱 **Plantation Data Issues**  
- **70% of the dataset** contains records where the plantation figures fall **outside the expected range** (350-450 trees).  
- These records have been **flagged** in the error logs for further analysis.  

### 🌳 **Species-Wise Distribution Mismatch**  
- Over **50% of the records** show **a mismatch between the total number of trees planted** and the **sum of species-wise tree distribution**.  
- Removing these records would significantly reduce the dataset, so they are **logged separately** for further review.  

### 💰 Payment Submission Gaps
- **63.6%** of participants did not submit the payment.



---

## 🛠️ Methodology  

The data quality check follows a structured **six-step validation process**:  

1️⃣ **Load the Dataset**  
   - Load `farmer_data.csv` using **Pandas** for processing.  

2️⃣ **Perform Data Quality Checks**  
   - **Check for unique IDs**  
   - **Verify completeness of mandatory fields**  
   - **Ensure correct data formats and types**  
   - **Validate business rules (tree count, geographical limits, contracts, etc.)**  

3️⃣ **Log Data Quality Issues**  
   - Any records that **fail validation** are logged into `data_quality_report.log`.  

4️⃣ **Store Invalid Records Separately**  
   - Failed records are moved to `failed_data.csv` for further review.  

5️⃣ **Generate Clean Dataset**  
   - Valid records are saved in `clean_data.csv` for downstream processing.  

6️⃣ **Generate Summary Reports**  
   - Error logs and a summary report are created to track issues.  

---

## 🚀 How to Run the Project  

### 📌 **Prerequisites**  
1. Ensure **Python 3.x** is installed.  
2. Install the required dependencies:  

   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running the Application
To execute the Data Quality Check script and launch the Streamlit Dashboard, run:

bash
   ```bash
   streamlit run main.py
   ```





