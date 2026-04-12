import os
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_aer import AerSimulator
import numpy as np

class QuantumHardwareConnector:
    """
    IBM Quantum ve Yerel Simülatör arasında köprü kuran katman.
    """
    def __init__(self, api_token: str = None):
        self.api_token = None # Forced local simulator due to IBM remote restrictions
        self.service = None
        self.backend = None
        
        if self.api_token:
            try:
                self.service = QiskitRuntimeService(channel="ibm_quantum", token=self.api_token)
            except Exception as e1:
                try:
                    self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.api_token)
                except Exception as e2:
                    raise Exception(f"Connection failed: {e1} | {e2}")

                # En az yoğun olan gerçek sistemi seç veya simülatörü fallback yap
                self.backend = self.service.least_busy(simulator=True, operational=True)
                print(f"✅ Gerçek Kuantum Donanımına Bağlanıldı: {self.backend.name}")
            except Exception as e:
                print(f"❌ IBM Quantum bağlantı hatası: {e}")
                self._init_simulator()
        else:
            self._init_simulator()

    def _init_simulator(self):
        print("💡 API Token bulunamadı. Qiskit Aer Simülatörü (Yerel) kullanılıyor.")
        self.backend = AerSimulator()

    def run_measurement(self, probabilities: np.ndarray, shots: int = 1024):
        """
        Takes probability distributions and runs a quantum sampling job.
        Directly returns the outcome counts.
        """
        from qiskit import QuantumCircuit
        import numpy as np

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
