# CA Automation Tool

A Python-based automation system designed to streamline invoice reconciliation workflows for Chartered Accountants (CAs) by comparing client-submitted bills with portal data and identifying discrepancies.

---

## 🚀 Problem

In real-world CA workflows, invoice reconciliation is time-consuming and error-prone.

Common issues:
- Clients submit **fewer invoices** than recorded on the portal
- Clients submit **extra invoices** not present on the portal
- Continuous **manual follow-ups via email** are required

This leads to:
- Delays in compliance
- Increased manual workload
- Inefficient communication

---

## 💡 Solution

This tool automates the reconciliation process by:

- Comparing **client invoice data** with **portal/GST data**
- Identifying:
  - Missing invoices
  - Extra/unmatched invoices
- Generating **automated alert messages** for follow-ups

---

## ⚙️ Features

- Data comparison using Python & Pandas  
- Cleans and normalizes financial data  
- Detects mismatches between datasets  
- Generates:
  - Client reminder messages  
  - Internal action notes  
- Handles numeric inconsistencies (₹, commas, text formats)

---

## 🛠️ Tech Stack

- Python  
- Pandas  
- Regex (data cleaning)  
- Excel/CSV Processing  

---

## 🔄 How It Works

1. Load client invoice data  
2. Load portal/GST data  
3. Normalize and clean data  
4. Compare both datasets  
5. Identify:
   - Missing from client  
   - Missing from portal  
6. Generate output alerts

---

## 📂 Example Output

### Client Missing Bills:

Hi [Client Name], please submit invoice [Invoice Number] for ₹[Amount].

### Portal Missing Entries:

---

## ▶️ How to Run

```bash
pip install pandas
python main.py


📈 Use Case

* Chartered Accountants
* Accounting firms
* GST compliance workflows
* Invoice reconciliation processes

⸻

🔮 Future Improvements

* Automatic email sending (SMTP integration)
* Dashboard for tracking mismatches
* Integration with GST portal APIs
* Web-based interface

👨‍💻 Author

Shrikant Pawade

* GitHub: https://github.com/Shree927432
* LinkedIn: https://www.linkedin.com/in/shrikant-pawade-b36514293
