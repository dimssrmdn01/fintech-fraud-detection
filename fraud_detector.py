import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import sqlite3
from datetime import datetime

# ==========================================
# 1. ENGINES DATABASE SQLITE (AUDIT LAYER)
# ==========================================
def init_audit_db():
    conn = sqlite3.connect('fraud_audit.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blacklisted_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp_deteksi TEXT,
            nominal_transaksi_rb REAL,
            frekuensi_harian INTEGER,
            status_review TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_fraud_to_sql(df_anomali):
    if df_anomali.empty:
        return 0
        
    conn = sqlite3.connect('fraud_audit.db')
    cursor = conn.cursor()
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    kontor_input = 0
    for _, row in df_anomali.iterrows():
        cursor.execute('''
            INSERT INTO blacklisted_transactions (timestamp_deteksi, nominal_transaksi_rb, frekuensi_harian, status_review)
            VALUES (?, ?, ?, ?)
        ''', (waktu_sekarang, float(row['Nominal_Transaksi (Rb)']), int(row['Frekuensi_Harian']), 'PENDING_INVESTIGATION'))
        kontor_input += 1
        
    conn.commit()
    conn.close()
    return kontor_input

def fetch_blacklist_audit_report():
    conn = sqlite3.connect('fraud_audit.db')
    df = pd.read_sql_query("SELECT * FROM blacklisted_transactions ORDER BY id DESC", conn)
    conn.close()
    return df

# Inisialisasi skema SQL
init_audit_db()

# ==========================================
# 2. SIMULASI DATA SINTETIS (FINTECH ENGINE)
# ==========================================
np.random.seed(42)
n_normal = 800
n_fraud = 20

# Data normal
normal_data = {
    'Nominal_Transaksi (Rb)': np.random.normal(150, 30, n_normal),
    'Frekuensi_Harian': np.random.randint(1, 5, n_normal),
    'Label_Asli': [0] * n_normal
}
df_normal = pd.DataFrame(normal_data)

# Data fraud (anomali: nominal raksasa & frekuensi sangat tinggi)
fraud_data = {
    'Nominal_Transaksi (Rb)': np.random.uniform(2000, 5000, n_fraud),
    'Frekuensi_Harian': np.random.randint(20, 50, n_fraud),
    'Label_Asli': [1] * n_fraud
}
df_fraud = pd.DataFrame(fraud_data)

df_total = pd.concat([df_normal, df_fraud], ignore_index=True)

# ==========================================
# 3. CORE MACHINE LEARNING PIPELINE
# ==========================================
X = df_total[['Nominal_Transaksi (Rb)', 'Frekuensi_Harian']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Menggunakan Isolation Forest untuk deteksi tanpa label
model = IsolationForest(contamination=0.025, random_state=42)
df_total['Prediksi_Anomaly'] = model.fit_predict(X_scaled)
df_total['Prediksi_Fraud'] = np.where(df_total['Prediksi_Anomaly'] == -1, 1, 0)

print("=== 🚨 FINTECH ANOMALY & FRAUD DETECTION ENGINE (PRO) ===")
print(f"Total Arus Transaksi Diproses: {len(df_total)}")

# Matriks Evaluasi Lokal
tabel_kontingensi = pd.crosstab(df_total['Label_Asli'], df_total['Prediksi_Fraud'], 
                                rownames=['Asli'], colnames=['Prediksi'])
print("\n--- 📊 MATRIX EVALUASI DETEKSI ANOMALI ---")
print(tabel_kontingensi)

# ==========================================
# 4. ISOLASI & PROSES PIPELINE DATABASE SQL
# ==========================================
df_terdeteksi_fraud = df_total[df_total['Prediksi_Fraud'] == 1]

# Kirim data fraud ke database SQL secara otomatis
jumlah_tercatat = log_fraud_to_sql(df_terdeteksi_fraud)
print(f"\n[SINKRONISASI SQL] Berhasil mengisolasi {jumlah_tercatat} transaksi mencurigakan ke database.")

print("\n" + "="*60)
print("🔍 LIVE QUERY: LAPORAN AUDIT FRAUD DARI TABEL SQL (5 DATA TERBARU)")
print("="*60)

# Tarik data langsung dari SQL database untuk pembuktian data persistence
df_laporan_sql = fetch_blacklist_audit_report()
if not df_laporan_sql.empty:
    print(df_laporan_sql.head(5).to_string(index=False))
else:
    print("Database audit masih kosong.")