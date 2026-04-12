import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class QuantumHardwareConnector:
    """
    Handles connection to IBM Quantum Services or local Aer simulators.
    Now supports lazy-loading to prevent 'ImportError' in CPU-only environments.
    """
    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.getenv("IBM_QUANTUM_TOKEN")
        self.service = None
        self.backend = None
        
        # 1. Attempt Real Quantum Hardware (Lazy Import)
        if self.api_token:
            try:
                from qiskit_ibm_runtime import QiskitRuntimeService
                try:
                    self.service = QiskitRuntimeService(channel="ibm_quantum", token=self.api_token)
                    self.backend = self.service.least_busy(simulator=False, operational=True)
                    print(f"✅ Gerçek Kuantum Donanımına Bağlanıldı: {self.backend.name}")
                except Exception as e1:
                    try:
                        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.api_token)
                        self.backend = self.service.least_busy(simulator=False, operational=True)
                        print(f"✅ Gerçek Kuantum Donanımına Bağlanıldı (Platform): {self.backend.name}")
                    except Exception as e2:
                        print(f"❌ IBM Quantum bağlantı hatası: {e1} | {e2}")
                        self._init_simulator()
            except ImportError:
                print("⚠️  'qiskit-ibm-runtime' yüklü değil, donanım modulleri devre dışı.")
                self._init_simulator()
        else:
            self._init_simulator()

    def _init_simulator(self):
        """Initializes the local AerSimulator fallback."""
        try:
            from qiskit_aer import AerSimulator
            self.backend = AerSimulator()
            print("🚀 Yerel Kuantum Simülatörü (Aer) Başlatıldı.")
        except ImportError:
            print("⚠️  'qiskit-aer' yüklü değil. Kuantum simülasyonu yapılamaz.")
            self.backend = None

    def run_measurement(self, probabilities: np.ndarray, shots: int = 1024):
        """
        Executes a measurement cycle on the selected backend.
        """
        if self.backend is None:
            raise RuntimeError("Kuantum backend başlatılamadı (Aer veya IBM QPU bulunamadı).")

        try:
            from qiskit import QuantumCircuit, transpile
            from qiskit_ibm_runtime import SamplerV2 as Sampler
        except ImportError:
            raise ImportError("Bu işlem için 'qiskit' ve 'qiskit-ibm-runtime' kütüphaneleri gereklidir.")

        num_qubits = int(np.log2(len(probabilities)))
        qc = QuantumCircuit(num_qubits)
        
        # We must pass probability amplitudes (square roots of probabilities) because
        # qiskit's qc.initialize requires sum(|amp|^2) = 1
        amplitudes = np.sqrt(probabilities)
        qc.initialize(amplitudes, range(num_qubits))
        qc.measure_all()
        
        # Real IBM Hardware requires compilation/transpilation of abstract gates (like initialize)
        from qiskit import transpile
        try:
            qc = transpile(qc, backend=self.backend)
        except Exception as transpile_err:
            print(f"[!] Target hardware transpilation issue: {transpile_err}")
            
        # Using the standard V2 sampler pattern
        sampler = Sampler(mode=self.backend)
        job = sampler.run([(qc,)])
        result = job.result()[0]
        
        # Convert bitstring counts to an ordered list of outcomes
        counts_dict = result.data.meas.get_counts()
        outcomes = [counts_dict.get(format(i, f'0{num_qubits}b'), 0) for i in range(len(probabilities))]
        return outcomes

    def is_real_hardware(self):
        return self.service is not None
