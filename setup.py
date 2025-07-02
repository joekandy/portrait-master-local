#!/usr/bin/env python3
"""
Portrait Master FLUX Local - Setup avanzato
Configurazioni e ottimizzazioni aggiuntive
"""

import os
import json
from pathlib import Path

def create_config():
    """Crea file di configurazione"""
    
    config = {
        "version": "1.0.0",
        "auto_launch": True,
        "default_gpu": "auto",
        "default_resolution": [768, 1024],
        "default_steps": 20,
        "default_cfg": 1.0,
        "model_paths": {
            "unet": "ComfyUI/models/unet/",
            "vae": "ComfyUI/models/vae/",
            "clip": "ComfyUI/models/clip/"
        },
        "performance": {
            "low_vram_mode": False,
            "cpu_fallback": True,
            "max_batch_size": 4
        }
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(" File di configurazione creato")

def optimize_for_system():
    """Ottimizza per il sistema corrente"""
    
    import platform
    import psutil
    
    system = platform.system()
    ram_gb = psutil.virtual_memory().total / (1024**3)
    
    print(f" Sistema: {system}")
    print(f" RAM: {ram_gb:.1f}GB")
    
    # Suggerimenti ottimizzazione
    if ram_gb < 16:
        print(" RAM limitata - Usa modalità CPU o lowvram")
    elif ram_gb >= 32:
        print(" RAM abbondante - Puoi usare batch size alto")
    
def main():
    print(" Portrait Master FLUX - Setup Avanzato")
    print("=" * 40)
    
    create_config()
    optimize_for_system()
    
    print("\n Setup completato!")

if __name__ == "__main__":
    main()
