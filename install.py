#!/usr/bin/env python3
"""
Portrait Master FLUX - Local Installation Script
Installa automaticamente Portrait Master con rilevamento GPU/CPU
Supporta Windows, Mac, Linux
"""

import os
import sys
import platform
import subprocess
import json
import time
import shutil
from pathlib import Path
import urllib.request
import argparse

# Configurazione colori
class Colors:
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_step(message):
    print(f"{Colors.CYAN} {message}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN} {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW} {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED} {message}{Colors.END}")

def print_header():
    print(f"{Colors.WHITE}{Colors.BOLD}")
    print(" Portrait Master FLUX - Installazione Locale")
    print("=" * 50)
    print(f"{Colors.END}")

def detect_system():
    """Rileva sistema operativo e architettura"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "windows", machine
    elif system == "darwin":
        return "macos", machine
    elif system == "linux":
        return "linux", machine
    else:
        return "unknown", machine

def detect_gpu():
    """Rileva GPU disponibili"""
    gpu_info = {
        "nvidia": False,
        "amd": False,
        "apple_silicon": False,
        "intel": False
    }
    
    system, machine = detect_system()
    
    # Rileva Apple Silicon
    if system == "macos" and ("arm64" in machine or "aarch64" in machine):
        gpu_info["apple_silicon"] = True
        return gpu_info
    
    # Rileva NVIDIA
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            gpu_info["nvidia"] = True
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    
    # Rileva AMD su Linux
    if system == "linux":
        try:
            result = subprocess.run(["lspci"], capture_output=True, text=True)
            if "VGA" in result.stdout and "AMD" in result.stdout:
                gpu_info["amd"] = True
        except:
            pass
    
    return gpu_info

def check_python_version():
    """Verifica versione Python compatibile"""
    version = sys.version_info
    if version.major != 3 or version.minor < 8:
        print_error(f"Python 3.8+ richiesto. Attuale: {version.major}.{version.minor}")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro} OK")
    return True

def check_git():
    """Verifica Git disponibile"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print_success("Git disponibile")
        return True
    except:
        print_error("Git non trovato! Installa Git per continuare")
        return False

def install_pytorch(gpu_info, force_cpu=False):
    """Installa PyTorch appropriato per il sistema"""
    
    print_step("Installazione PyTorch...")
    
    # Determina comando pip per PyTorch
    if force_cpu or not any(gpu_info.values()):
        # CPU only
        pip_cmd = [
            sys.executable, "-m", "pip", "install",
            "torch==2.1.0+cpu",
            "torchvision==0.16.0+cpu", 
            "torchaudio==2.1.0+cpu",
            "--index-url", "https://download.pytorch.org/whl/cpu"
        ]
        print_step("Modalità CPU selezionata")
        
    elif gpu_info["nvidia"]:
        # NVIDIA GPU
        pip_cmd = [
            sys.executable, "-m", "pip", "install",
            "torch==2.1.0+cu118",
            "torchvision==0.16.0+cu118",
            "torchaudio==2.1.0+cu118",
            "--index-url", "https://download.pytorch.org/whl/cu118"
        ]
        print_step("Modalità NVIDIA GPU selezionata")
        
    elif gpu_info["apple_silicon"]:
        # Apple Silicon
        pip_cmd = [
            sys.executable, "-m", "pip", "install",
            "torch==2.1.0",
            "torchvision==0.16.0",
            "torchaudio==2.1.0"
        ]
        print_step("Modalità Apple Silicon selezionata")
        
    else:
        # Fallback to CPU
        pip_cmd = [
            sys.executable, "-m", "pip", "install",
            "torch==2.1.0+cpu",
            "torchvision==0.16.0+cpu",
            "torchaudio==2.1.0+cpu", 
            "--index-url", "https://download.pytorch.org/whl/cpu"
        ]
        print_step("Fallback a modalità CPU")
    
    try:
        subprocess.run(pip_cmd, check=True)
        print_success("PyTorch installato")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Errore installazione PyTorch: {e}")
        return False

def install_dependencies():
    """Installa dipendenze Python"""
    
    print_step("Installazione dipendenze core...")
    
    core_deps = [
        "numpy<2",
        "pillow>=9.5.0",
        "opencv-python-headless>=4.8.0",
        "transformers>=4.25.0",
        "accelerate>=0.21.0",
        "safetensors>=0.3.1",
        "diffusers>=0.21.0",
        "psutil",
        "einops",
        "pyyaml",
        "scipy",
        "tqdm",
        "huggingface-hub",
        "requests",
        "aiohttp"
    ]
    
    for dep in core_deps:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f" {dep}")
        except subprocess.CalledProcessError:
            print_warning(f"Errore installazione {dep}")
    
    print_success("Dipendenze installate")

def setup_comfyui():
    """Installa e configura ComfyUI"""
    
    print_step("Setup ComfyUI...")
    
    comfyui_dir = Path("ComfyUI")
    
    # Clone ComfyUI se non esiste
    if not comfyui_dir.exists():
        try:
            subprocess.run([
                "git", "clone", 
                "https://github.com/comfyanonymous/ComfyUI.git"
            ], check=True)
            print_success("ComfyUI clonato")
        except subprocess.CalledProcessError:
            print_error("Errore clonazione ComfyUI")
            return False
    else:
        print_success("ComfyUI già presente")
    
    # Installa requirements ComfyUI
    req_file = comfyui_dir / "requirements.txt"
    if req_file.exists():
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "-r", str(req_file)
            ], check=True)
            print_success("Requirements ComfyUI installati")
        except subprocess.CalledProcessError:
            print_warning("Errore requirements ComfyUI")
    
    return True

def setup_custom_nodes():
    """Installa custom nodes essenziali"""
    
    print_step("Installazione custom nodes...")
    
    nodes_dir = Path("ComfyUI/custom_nodes")
    nodes_dir.mkdir(parents=True, exist_ok=True)
    
    essential_nodes = [
        ("ComfyUI-Manager", "https://github.com/ltdrdata/ComfyUI-Manager.git"),
        ("ComfyUI_essentials", "https://github.com/cubiq/ComfyUI_essentials.git"),
        ("rgthree-comfy", "https://github.com/rgthree/rgthree-comfy.git"),
        ("was-node-suite-comfyui", "https://github.com/WASasquatch/was-node-suite-comfyui.git")
    ]
    
    for node_name, repo_url in essential_nodes:
        node_path = nodes_dir / node_name
        
        if not node_path.exists():
            try:
                subprocess.run([
                    "git", "clone", repo_url, str(node_path)
                ], check=True, capture_output=True)
                print(f" {node_name}")
                
                # Installa requirements del nodo se presenti
                req_file = node_path / "requirements.txt"
                if req_file.exists():
                    subprocess.run([
                        sys.executable, "-m", "pip", "install",
                        "-r", str(req_file)
                    ], capture_output=True)
                    
            except subprocess.CalledProcessError:
                print_warning(f"Errore installazione {node_name}")
        else:
            print(f" {node_name} (già presente)")
    
    print_success("Custom nodes installati")

def download_models():
    """Scarica modelli FLUX essenziali"""
    
    print_step("Setup modelli FLUX...")
    
    models_dir = Path("ComfyUI/models")
    
    # Crea directory modelli
    (models_dir / "unet").mkdir(parents=True, exist_ok=True)
    (models_dir / "vae").mkdir(parents=True, exist_ok=True)
    (models_dir / "clip").mkdir(parents=True, exist_ok=True)
    
    print_warning("I modelli FLUX (~50GB) devono essere scaricati manualmente da:")
    print(" https://huggingface.co/black-forest-labs/FLUX.1-dev")
    print(" Posiziona i file in ComfyUI/models/")
    print("   - flux1-dev.safetensors  unet/")
    print("   - ae.safetensors  vae/")
    print("   - clip_l.safetensors, t5xxl_fp16.safetensors  clip/")
    
    return True

def create_launcher():
    """Crea script launcher"""
    
    print_step("Creazione launcher...")
    
    # Script launcher per Windows
    launcher_bat = """@echo off
cd /d "%~dp0"
echo  Avvio Portrait Master FLUX...
python launcher.py %*
pause
"""
    
    with open("Portrait Master.bat", "w") as f:
        f.write(launcher_bat)
    
    print_success("Launcher creato")

def create_desktop_shortcut():
    """Crea collegamento desktop (Windows)"""
    
    system, _ = detect_system()
    
    if system == "windows":
        try:
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "Portrait Master.lnk"
            
            # Comando PowerShell per creare collegamento
            ps_cmd = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{Path.cwd() / 'Portrait Master.bat'}"
$Shortcut.WorkingDirectory = "{Path.cwd()}"
$Shortcut.IconLocation = "shell32.dll,14"
$Shortcut.Save()
'''
            
            subprocess.run([
                "powershell", "-Command", ps_cmd
            ], capture_output=True)
            
            print_success("Collegamento desktop creato")
            
        except:
            print_warning("Impossibile creare collegamento desktop")

def main():
    """Funzione principale"""
    
    parser = argparse.ArgumentParser(description="Installa Portrait Master FLUX")
    parser.add_argument("--cpu", action="store_true", help="Forza modalità CPU")
    parser.add_argument("--gpu", action="store_true", help="Forza modalità GPU")
    parser.add_argument("--clean", action="store_true", help="Pulizia installazione")
    
    args = parser.parse_args()
    
    print_header()
    
    # Verifica prerequisiti
    if not check_python_version():
        return False
    
    if not check_git():
        return False
    
    # Rileva hardware
    print_step("Rilevamento hardware...")
    system, machine = detect_system()
    gpu_info = detect_gpu()
    
    print(f" Sistema: {system.title()} ({machine})")
    
    if gpu_info["nvidia"]:
        print(" GPU NVIDIA rilevata")
    elif gpu_info["apple_silicon"]:
        print(" Apple Silicon rilevato")
    elif gpu_info["amd"]:
        print(" GPU AMD rilevata")
    else:
        print(" Solo CPU disponibile")
    
    # Conferma installazione
    if not args.cpu and not args.gpu:
        if any(gpu_info.values()):
            use_gpu = input("\n GPU rilevata. Usare GPU? (s/n): ").lower().startswith('s')
        else:
            use_gpu = False
            print(" Modalità CPU selezionata automaticamente")
    else:
        use_gpu = args.gpu and not args.cpu
    
    print_step("Inizio installazione...")
    
    # Installazione componenti
    steps = [
        ("PyTorch", lambda: install_pytorch(gpu_info, force_cpu=not use_gpu)),
        ("Dipendenze", install_dependencies),
        ("ComfyUI", setup_comfyui),
        ("Custom Nodes", setup_custom_nodes),
        ("Modelli", download_models),
        ("Launcher", create_launcher),
        ("Shortcut", create_desktop_shortcut)
    ]
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                print_error(f"Errore in: {step_name}")
                return False
        except Exception as e:
            print_error(f"Errore {step_name}: {e}")
            return False
    
    # Completamento
    print()
    print_success(" INSTALLAZIONE COMPLETATA!")
    print()
    print(" Per avviare Portrait Master:")
    print("   - Windows: Doppio click su 'Portrait Master' (desktop)")
    print("   - Mac/Linux: python launcher.py")
    print()
    print(" Interfaccia web: http://localhost:8188")
    print(" Workflow: Carica 'Portrait_Basic_Local.json'")
    print(" Modelli: Scarica da HuggingFace in ComfyUI/models/")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("Premi Invio per uscire...")
    except KeyboardInterrupt:
        print_error("\n Installazione interrotta")
    except Exception as e:
        print_error(f"Errore generale: {e}")
        input("Premi Invio per uscire...")
