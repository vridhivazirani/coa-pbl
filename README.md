# I/O Data Transfer Techniques
### Studio Shodwe · Computer Organization and Architecture PBL

A full interactive web platform simulating and comparing three I/O data transfer techniques: **Programmed I/O**, **Interrupt-Driven I/O**, and **DMA (Direct Memory Access)**.

---

## Project Structure

```
COA-pbl/
├── index.html             # Main multi-page interactive app
├── simulation.html        # Simulation explanation, algorithm & Python code
├── results.html           # Charts, data table & key findings
├── style.css              # All styling
├── script.js              # All JavaScript (simulation, visualizer, quiz, nav)
│
├── data/
│   └── simulation-data.json   # Pre-computed results for all 7 data sizes
│
├── python/
│   └── io_simulation.py       # Original Python simulation model
│
├── images/
│   ├── architecture.png       # I/O system architecture diagram
│   └── results_graph.png      # Performance comparison graph
│
├── README.md
└── vercel.json            # Vercel deployment config
```

---

## Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Splash screen + 11-page interactive app |
| Simulation | `/simulation` | Algorithm, pseudocode & Python source |
| Results | `/results` | Charts, data table & findings |

---

## Simulation Model

| Constant | Value | Description |
|----------|-------|-------------|
| `TRANSFER_RATE` | 100 MB/s | Base bus speed |
| `INTERRUPT_OVERHEAD` | 0.002s | Per interrupt cost |
| `CONTEXT_SWITCH` | 0.001s | State save/restore |
| `DMA_INIT_TIME` | 0.0005s | DMA setup (one-time) |
| `INTERRUPT_BLOCK_SIZE` | 10 MB | Data per interrupt |
| `PIO_CPU_FACTOR` | 0.68 | CPU active fraction |
| `DMA_EFF_RATE` | 97 MB/s | DMA effective throughput |

---

## Running the Python Simulation

```bash
cd python
python io_simulation.py
```

This will print the results table and export updated `data/simulation-data.json`.

---

## Deploying to Vercel

1. Push this folder to a GitHub repository
2. Go to [vercel.com](https://vercel.com) → **New Project**
3. Import your GitHub repo
4. Leave all settings as default (static site, no build command)
5. Click **Deploy**

Your site will be live at `https://your-project.vercel.app`

---

## What We Built

- **Live simulation** — Python model ported to JS, real-time slider 1MB–1GB
- **Bus visualizer** — Step-by-step animation of data transfer on the system bus
- **4-view chart system** — Built with Canvas API, no libraries
- **Smart recommendation engine** — Auto-selects best method per workload
- **Interactive quiz** — 6 COA questions with explanations
- **COA Glossary** — 9 key terms defined

---

*Studio Shodwe — COA Project*
