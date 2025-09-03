import subprocess
import sys
import os


def check_data_exists():
    processed_dir = "data/processed"

    if not os.path.exists(processed_dir):
        return False

    csv_files = [f for f in os.listdir(processed_dir) if f.endswith(".csv")]
    return len(csv_files) > 0


def run_dashboard():
    if not check_data_exists():
        print("Dados processados não encontrados!")
        print("Execute primeiro:")
        print("1. python src.data_collector")
        print("2. python src.data_pipeline")
        return

    print("🚀 Iniciando dashboard...")
    print("📱 O dashboard abrirá em: http://localhost:8501")
    print("🛑 Para parar: Ctrl+C no terminal")

    # Executar Streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])


if __name__ == "__main__":
    run_dashboard()
