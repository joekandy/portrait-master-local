#  Portrait Master FLUX - Installazione Locale

Installa **Portrait Master FLUX** sul tuo PC per generare ritratti professionali AI in locale. Supporta sia **GPU** che **CPU** con rilevamento automatico dell'hardware.

##  **Installazione Automatica (1-Click)**

###  **Windows**
1. Scarica: **[ install.bat](https://raw.githubusercontent.com/joekandy/portrait-master-local/main/install.bat)**
2. Clicca destro  **"Esegui come amministratore"**
3. Scegli **GPU** o **CPU** quando richiesto
4. Attendi installazione (~10-30 minuti)

###  **Mac /  Linux**
`ash
curl -sSL https://raw.githubusercontent.com/joekandy/portrait-master-local/main/install.sh | bash
`

###  **Installazione Manuale**
`ash
git clone https://github.com/joekandy/portrait-master-local.git
cd portrait-master-local
python install.py
`

##  **Requisiti di Sistema**

###  **Requisiti Minimi (CPU)**
- **OS:** Windows 10+, macOS 10.15+, Linux Ubuntu 18.04+
- **RAM:** 8GB (16GB raccomandati)
- **Spazio:** 50GB liberi
- **Processore:** Intel i5 / AMD Ryzen 5+

###  **Requisiti GPU**
- **NVIDIA:** GTX 1660+ (6GB VRAM) o RTX series
- **AMD:** RX 6600+ (8GB VRAM)
- **Apple:** M1/M2/M3 (GPU integrata)
- **VRAM:** 6GB+ raccomandati

##  **Modalità di Funzionamento**

| Modalità | Tempo | Qualità | Hardware |
|----------|-------|---------|----------|
| **GPU NVIDIA** | 15-30s | Massima | RTX 3060+ |
| **GPU AMD** | 1-2 min | Ottima | RX 6600+ |
| **Apple Silicon** | 1-3 min | Ottima | M1/M2/M3 |
| **CPU Intel/AMD** | 5-15 min | Buona | i5/Ryzen 5+ |

##  **Come Usare**

### 1. **Avvio**
- **Windows:** Doppio click su **Portrait Master** (desktop)
- **Mac/Linux:** Comando portrait-master nel terminale

### 2. **Generazione**
1. Apri browser su http://localhost:8188
2. Carica workflow **"Portrait_Basic"**
3. Inserisci prompt (es: "professional headshot")
4. Clicca **"Queue Prompt"**

### 3. **Parametri**
- **Steps:** 20 (GPU) / 10 (CPU)
- **Resolution:** 768x1024 standard
- **CFG:** 1.0-2.0

##  **Problemi Comuni**

###  **GPU non rilevata**
`ash
python launcher.py --force-gpu
`

###  **Memoria insufficiente**
`ash
python launcher.py --lowvram --cpu-fallback
`

###  **Modelli mancanti**
`ash
python install.py --download-models
`

##  **Performance**

| Hardware | Tempo (768x1024) | VRAM/RAM |
|----------|------------------|----------|
| RTX 4090 | ~15 sec | 12GB |
| RTX 3080 | ~25 sec | 8GB |
| M3 Max | ~90 sec | 16GB |
| CPU i7 | ~8 min | 16GB |

##  **Esempi Prompt**

- **Business:** "professional headshot, corporate attire, office background"
- **Artistic:** "portrait with dramatic lighting, vintage style"  
- **Fashion:** "fashion model, studio lighting, magazine quality"

##  **Supporto**

- **Issues:** [GitHub Issues](https://github.com/joekandy/portrait-master-local/issues)
- **Wiki:** [Guida Completa](https://github.com/joekandy/portrait-master-local/wiki)

---

 **Crea ritratti AI professionali sul tuo PC!** 
