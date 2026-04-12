import os
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

def generate_actual_execution_circuit():
    """
    Bu fonksiyon, sistemin "gerçekten" neyi çalıştırdığını gösterir.
    Kafadan bir devre değil, hardware_connector.py içerisindeki 
    aynı simülatör transpile pipeline'ını kullanarak gerçek
    fiziksel / simüle edilmiş operasyon şemasını çıkarır.
    """
    print("[*] Replicating Real Execution Circuit Topology...")
    
    # 1. Temsili bir probabilites (veri) seti kullan (Kodu testlerdeki gibi)
    probabilities = np.random.rand(16)
    probabilities /= np.sum(probabilities) # Normalize to 1
    amplitudes = np.sqrt(probabilities) # qiskit initialize format
    
    num_qubits = int(np.log2(len(probabilities)))
    
    # 2. Asıl devre (Abstract Circuit)
    qc = QuantumCircuit(num_qubits)
    # Etiket ile initialize ettiğimizi gösteriyoruz metodolojideki gibi
    qc.initialize(amplitudes, range(num_qubits))
    qc.measure_all()
    
    # 3. Aer Simulator Backend (Kullandığımız asıl yapı)
    backend = AerSimulator()
    
    # 4. Asıl Transpilation (Gerçek kapılara dönüşüm)
    # abstract initialize(v) = U3, CX vb kombinasyonlarına dönüşür
    print("[*] Transpiling to native basis gates (AerSimulator)...")
    transpiled_qc = transpile(qc, backend=backend, optimization_level=1)
    
    # 5. Görselleştir ve Kaydet
    output_dir = os.path.join(os.path.dirname(__file__), "results")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_img = os.path.join(output_dir, "self_ref_circuit.png")
    
    try:
        # Pylatexenc yüklü olmayabilir, bu yüzden qiskit'in kendi drawer'ı üzerinden 
        # mpl veya text tabanlı yüksek çözünürlüklü çıktı alınıyor.
        fig = transpiled_qc.draw(output='mpl', fold=50, style="clifford")
        fig.savefig(output_img, dpi=300, bbox_inches='tight')
        print(f"[*] SUCCESS: Transpiled Circuit graphic saved to {output_img}")
    except Exception as e:
        print(f"[!] Warning: MPL Drawer failed ({e}). Falling back to terminal/text drawing.")
        # Çizim kütüphanesi yoksa terminal çıktısını dosyaya yaz
        with open(os.path.join(output_dir, "self_ref_circuit_text.txt"), "w") as f:
            f.write(transpiled_qc.draw(output='text'))
            
if __name__ == "__main__":
    generate_actual_execution_circuit()
