import os
import zipfile

def bundle_supplementary_materials():
    # We are in ROOT/tests/bundle_supplementary.py
    # base_dir should be ROOT/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_filename = os.path.join(base_dir, 'RhoDynamics_Supplementary_Materials.zip')
    
    # Updated paths to reflect the Reviewer-Proofed structure
    files_to_zip = [
        # Manifests
        'setup.py',
        'README.md',
        
        # Source (Standard Package)
        os.path.join('src', 'quantum_rag_layer', 'math_engine.py'),
        os.path.join('src', 'quantum_rag_layer', 'agent_model.py'),
        os.path.join('src', 'quantum_rag_layer', 'rag_engine.py'),
        os.path.join('src', 'quantum_rag_layer', 'encoding.py'),
        os.path.join('src', 'quantum_rag_layer', 'middleware.py'),
        os.path.join('src', 'quantum_rag_layer', 'hardware_connector.py'),
        os.path.join('src', 'quantum_rag_layer', 'config.json'),
        os.path.join('src', 'quantum_rag_layer', '__init__.py'),
        
        # Comprehensive Pytests (Verified Peer-Review Ready)
        os.path.join('tests', 'test_calibration.py'),
        os.path.join('tests', 'test_drift.py'),
        os.path.join('tests', 'test_scientific_benchmark.py'),
        os.path.join('tests', 'generate_academic_plots.py'),
        os.path.join('tests', 'generate_circuit_diagram.py'),
        
        # Scientific Results & Formal Reports
        os.path.join('tests', 'academic_methods_results.md'),
        os.path.join('tests', 'validation_report.md'),
        os.path.join('tests', 'results', 'qpu_final_benchmark.json'),
        os.path.join('tests', 'results', 'final_evolution_plot.png'),
        os.path.join('tests', 'results', 'self_ref_circuit.png'),
        os.path.join('tests', 'results', 'qcs_graph.png'),
    ]

    print(f"[*] Packaging {len(files_to_zip)} artifacts into Reviewer-Proof Supplementary Bundle...")

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            full_path = os.path.join(base_dir, file)
            if os.path.exists(full_path):
                # Add file to zip keeping the relative path
                zipf.write(full_path, arcname=file)
                print(f"  [+] Included: {file}")
            else:
                print(f"  [!] Missing file (skipped): {file}")
                
    print("="*60)
    print(f"[*] SUCCESS: Academic dataset packaged successfully!")
    print(f"[*] Location: {output_filename}")
    print("="*60)

if __name__ == "__main__":
    bundle_supplementary_materials()
