#!/usr/bin/env python3
"""
Portrait Master FLUX - Launcher
Avvia ComfyUI con configurazione ottimale
"""

import os
import sys
import subprocess
import webbrowser
import time
import argparse
from pathlib import Path

def detect_gpu():
    """Rileva GPU disponibili"""
    try:
        # Testa NVIDIA
        result = subprocess.run(["nvidia-smi"], capture_output=True)
        if result.returncode == 0:
            return "nvidia"
    except:
        pass
    
    # Testa Apple Silicon
    if sys.platform == "darwin":
        import platform
        if "arm64" in platform.machine().lower():
            return "apple"
    
    return "cpu"

def start_comfyui(args):
    """Avvia ComfyUI con parametri ottimali"""
    
    comfyui_path = Path("ComfyUI")
    if not comfyui_path.exists():
        print(" ComfyUI non trovato! Esegui install.py prima")
        return False
    
    os.chdir(comfyui_path)
    
    # Comando base
    cmd = [sys.executable, "main.py", "--listen", "0.0.0.0", "--port", "8188"]
    
    # Rileva modalità
    if args.cpu:
        gpu_mode = "cpu"
    elif args.gpu:
        gpu_mode = detect_gpu()
    else:
        gpu_mode = detect_gpu()
    
    # Aggiungi parametri specifici
    if gpu_mode == "cpu" or args.cpu:
        cmd.append("--cpu")
        print(" Modalità CPU")
    elif gpu_mode == "nvidia":
        if args.lowvram:
            cmd.extend(["--lowvram", "--cpu-vae"])
        print(" Modalità NVIDIA GPU")
    elif gpu_mode == "apple":
        cmd.append("--mps")
        print(" Modalità Apple Silicon")
    
    print(" Avvio ComfyUI...")
    print(f" Directory: {comfyui_path.absolute()}")
    print(f" Comando: {' '.join(cmd)}")
    
    try:
        # Avvia ComfyUI
        process = subprocess.Popen(cmd)
        
        # Attendi avvio (più tempo per CPU)
        wait_time = 20 if gpu_mode == "cpu" else 10
        print(f" Attendi {wait_time} secondi per l'avvio...")
        time.sleep(wait_time)
        
        # Apri browser
        url = "http://localhost:8188"
        print(f" Apertura browser: {url}")
        webbrowser.open(url)
        
        print("\n Portrait Master FLUX avviato!")
        print(" Interfaccia web: http://localhost:8188") 
        print(" Documentazione: Carica un workflow dalla lista")
        print("  Premi Ctrl+C per fermare")
        print("-" * 50)
        
        # Aspetta terminazione
        process.wait()
        
    except KeyboardInterrupt:
        print("\n Arresto Portrait Master...")
        process.terminate()
    except Exception as e:
        print(f" Errore avvio: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Portrait Master FLUX Launcher")
    parser.add_argument("--cpu", action="store_true", help="Forza modalità CPU")
    parser.add_argument("--gpu", action="store_true", help="Forza modalità GPU")
    parser.add_argument("--lowvram", action="store_true", help="Modalità bassa VRAM")
    parser.add_argument("--mps", action="store_true", help="Usa Apple MPS")
    
    args = parser.parse_args()
    
    print(" Portrait Master FLUX - Launcher")
    print("=" * 40)
    
    if not start_comfyui(args):
        input("Premi Invio per uscire...")

if __name__ == "__main__":
    main()
