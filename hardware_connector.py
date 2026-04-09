import os
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_aer import AerSimulator

class QuantumHardwareConnector:
    """
    IBM Quantum ve Yerel Simülatör arasında köprü kuran katman.
    """
    def __init__(self, api_token: str = None):
        self.api_token = api_token or os.getenv("IBM_QUANTUM_TOKEN")
        self.service = None
        self.backend = None
        
        if self.api_token:
            try:
                self.service = QiskitRuntimeService(channel="ibm_quantum", token=self.api_token)
                # En az yoğun olan gerçek sistemi seç veya simülatörü fallback yap
                self.backend = self.service.least_busy(simulator=False, operational=True)
                print(f"✅ Gerçek Kuantum Donanımına Bağlanıldı: {self.backend.name}")
            except Exception as e:
                print(f"❌ IBM Quantum bağlantı hatası: {e}")
                self._init_simulator()
        else:
            self._init_simulator()

    def _init_simulator(self):
        print("💡 API Token bulunamadı. Qiskit Aer Simülatörü (Yerel) kullanılıyor.")
        self.backend = AerSimulator()

    def get_sampler(self):
        """Devreleri çalıştırmak için bir Sampler (Örnekleyici) döndürür."""
        return Sampler(backend=self.backend)

    def is_real_hardware(self):
        return self.service is not None
