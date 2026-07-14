##  Fintech Fraud Detection Simulation

A proof-of-concept machine learning architecture built to identify anomalous transaction patterns. This project utilizes a synthetic financial stream simulation to demonstrate feature engineering, model evaluation, and deployment concepts in a controlled environment.


##  Key Features

* **Unsupervised Anomaly Detection:** Leverages the `Isolation Forest` algorithm to automatically flag multi-dimensional outliers (abnormal transaction amounts paired with hyper-frequent daily velocities) without requiring historical fraud labels.
* **Feature Scaling Pipeline:** Implements `StandardScaler` to normalize feature distributions, ensuring distance metrics and isolation splits remain mathematically unbiased.
* **SQL Compliance Audit Trail:** Automatically isolates flagged anomalies and commits them in real-time into a dedicated SQLite database (`fraud_audit.db`) under a pending investigation state.
* **Forensic Live-Query Interface:** Implements structured data querying to pull the latest security logs directly from the SQL database for real-time security auditing.

---

##  Repository Structure

* `fraud_detector.py` - Core execution script containing the synthetic financial stream simulation, the machine learning pipeline, and SQL synchronization hooks.

---

##  Tech Stack & Dependencies

* **Language:** Python
* **Machine Learning & Preprocessing:** Scikit-Learn
* **Data Engineering & Manipulation:** NumPy, Pandas
* **Database Architecture:** SQLite3 (Native Python Module)

---

##  Installation & Execution Guide

1. **Clone the Repository:**
```bash
   git clone [https://github.com/dimssrmdn01/fintech-fraud-detection.git](https://github.com/dimssrmdn01/fintech-fraud-detection.git)
   cd fintech-fraud-detection
   ```

2. **Install Core Machine Learning Libraries:**
```bash
   pip install scikit-learn pandas numpy
   ```

3. **Execute the Analytical Pipeline:**
```bash
   python fraud_detector.py
   ```

---

##  Evaluation & Log Schema

| Database Column | Data Type | Analytical Importance |
| :--- | :--- | :--- |
| **timestamp_deteksi** | TEXT | Automated audit trail mapping for security incident response timelines. |
| **nominal_transaksi_rb** | REAL | Numerical scale tracking the financial severity of the anomaly. |
| **frekuensi_harian** | INTEGER | Transaction velocity metric indicating potential brute-force carding or system exploitation. |
| **status_review** | TEXT | State machine tracker initialization (`PENDING_INVESTIGATION`) for compliance teams. |
