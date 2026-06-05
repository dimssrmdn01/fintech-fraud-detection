import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n_normal = 800
n_fraud = 20

normal_danasiwa = {
    'Nominal_Transaksi (Rb)': np.random.normal(150, 30, n_normal),
    'Frekuensi_Harian': np.random.randint(1, 5, n_normal)
}
df_normal = pd.DataFrame(normal_danasiwa)
df_normal['Label_Asli'] = 0

fraud_danasiwa = {
    'Nominal_Transaksi (Rb)': np.random.uniform(2000, 5000, n_fraud),
    'Frekuensi_Harian': np.random.randint(20, 50, n_fraud)
}
df_fraud = pd.DataFrame(fraud_danasiwa)
df_fraud['Label_Asli'] = 1

df_total = pd.concat([df_normal, df_fraud], ignore_index=True)

X = df_total[['Nominal_Transaksi (Rb)', 'Frekuensi_Harian']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(contamination=0.025, random_state=42)
df_total['Prediksi_Anomaly'] = model.fit_predict(X_scaled)

df_total['Prediksi_Fraud'] = np.where(df_total['Prediksi_Anomaly'] == -1, 1, 0)

print("=== FINTECH ANOMALY & FRAUD DETECTION ENGINE ===")
print(f"Total Data Transaksi Diproses: {len(df_total)}\n")

tabel_kontingensi = pd.crosstab(df_total['Label_Asli'], df_total['Prediksi_Fraud'], 
                                rownames=['Asli'], colnames=['Prediksi'])

print("--- MATRIX EVALUASI DETEKSI ANOMALI ---")
print(tabel_kontingensi)

total_terdeteksi = df_total['Prediksi_Fraud'].sum()
print(f"\nSistem berhasil mengisolasi {total_terdeteksi} transaksi mencurigakan.")