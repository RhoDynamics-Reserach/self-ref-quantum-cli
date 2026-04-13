import os
import zipfile
import shutil
from datetime import datetime

def clean_artifacts(root_dir):
    """Recursively removes all __pycache__ and build artifacts."""
    print(f"[*] Starting deep cleanup of {root_dir}...")
    for root, dirs, files in os.walk(root_dir):
        for d in list(dirs):
            if d in ["__pycache__", ".pytest_cache"]:
                path = os.path.join(root, d)
                shutil.rmtree(path)
                print(f"    [-] Deleted: {path}")

def bundle_supplementary_materials():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_artifacts(base_dir)
    
    output_filename = os.path.join(base_dir, 'RhoDynamics_Supplementary_Materials.zip')
    
    files_to_zip = [
        'setup.py',
        'README.md',
        os.path.join('src', 'quantum_rag_layer', 'math_engine.py'),
        os.path.join('src', 'quantum_rag_layer', 'agent_model.py'),
        os.path.join('src', 'quantum_rag_layer', 'rag_engine.py'),
        os.path.join('src', 'quantum_rag_layer', 'encoding.py'),
        os.path.join('src', 'quantum_rag_layer', 'middleware.py'),
        os.path.join('src', 'quantum_rag_layer', 'hardware_connector.py'),
        os.path.join('src', 'quantum_rag_layer', 'config.json'),
        os.path.join('src', 'quantum_rag_layer', '__init__.py'),
        os.path.join('tests', 'test_calibration.py'),
        os.path.join('tests', 'test_drift.py'),
        os.path.join('tests', 'test_scientific_benchmark.py'),
        os.path.join('tests', 'generate_academic_plots.py'),
        os.path.join('tests', 'generate_circuit_diagram.py'),
        os.path.join('tests', 'run_academic_benchmark.py'),
        os.path.join('tests', 'final_hardware_benchmark.py'),
        os.path.join('tests', 'academic_methods_results.md'),
        os.path.join('tests', 'validation_report.md'),
        os.path.join('tests', 'results', 'qpu_final_benchmark.json'),
        os.path.join('tests', 'results', 'qpu_final_proof.json'),
        os.path.join('tests', 'results', 'final_evolution_plot.png'),
        os.path.join('tests', 'results', 'self_ref_circuit.png'),
        os.path.join('tests', 'results', 'qcs_graph.png'),
        os.path.join('tests', 'results', 'formal_benchmark_statistics.md'),
    ]

    # PRE-FLIGHT INTEGRITY CHECK
    print("[*] Performing Pre-flight Integrity Check...")
    missing = [f for f in files_to_zip if not os.path.exists(os.path.join(base_dir, f))]
    if missing:
        print("!"*60)
        print("[FATAL ERROR] Bundle Integrity Violation!")
        print(f"The following {len(missing)} files are missing from the workspace:")
        for m in missing:
            print(f"  - {m}")
        print("!"*60)
        print("[FAIL] Please run generation scripts (calibration, benchmark, plots) before bundling.")
        return

    print(f"[*] Packaging {len(files_to_zip)} artifacts into Reviewer-Proof Supplementary Bundle...")
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            full_path = os.path.join(base_dir, file)
            zipf.write(full_path, arcname=file)
            print(f"  [+] Included: {file}")
                
    print("="*60)
    print(f"[*] SUCCESS: Academic dataset packaged successfully!")
    print(f"[*] Location: {output_filename}")
    print("="*60)

if __name__ == "__main__":
    bundle_supplementary_materials()
