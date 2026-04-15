import os
import zipfile
import subprocess

files_to_include = [
    "src/quantum_rag_layer/encoding.py",
    "src/quantum_rag_layer/math_engine.py",
    "src/quantum_rag_layer/memory.py",
    "src/quantum_rag_layer/agent_model.py",
    "src/quantum_rag_layer/rag_engine.py",
    "src/quantum_rag_layer/middleware.py",
    "tests/test_drift.py",
    "tests/test_scientific_benchmark.py",
    "tests/run_academic_benchmark.py",
    "tests/generate_circuit_diagram.py",
    "tests/results/drift_results.json",
    "tests/results/objective_results.json",
    "tests/results/formal_benchmark_statistics.md",
    "tests/results/qcs_graph.png",
    "tests/results/final_evolution_plot.png",
    "tests/results/self_ref_circuit.png",
    "requirements.txt",
    "setup.py",
    "pytest.ini"
]

zip_name = "Academic_Paper_Source_v4.8_No_Synergy.zip"
commit_hash = "5361abf"

def build_zip():
    print(f"Creating {zip_name} using version from commit {commit_hash}...")
    with zipfile.ZipFile(zip_name, 'w') as zf:
        for f in files_to_include:
            # We fetch .py / text files from the pure academic commit.
            # We fetch .png / .json (results) from the local disk if git doesn't have them
            
            # 1. Try to get it from git (v4.8 commit)
            git_path = f.replace('\\', '/')
            try:
                # If the file was in git, git show will print it
                res = subprocess.run(["git", "show", f"{commit_hash}:{git_path}"], capture_output=True)
                if res.returncode == 0:
                    zf.writestr(f"Self-Reference-Quantum-Rag-main/{f}", res.stdout)
                    print(f"[+] Git version added: {f}")
                    continue
            except Exception:
                pass
            
            # 2. If it is NOT in git (like generated graphs), pull it from local disk
            if os.path.exists(f):
                zf.write(f, f"Self-Reference-Quantum-Rag-main/{f}")
                print(f"[+] Local disk version added: {f}")
            else:
                print(f"[-] WARNING: File not found in git OR disk: {f}")

if __name__ == "__main__":
    build_zip()
    print("Done!")
