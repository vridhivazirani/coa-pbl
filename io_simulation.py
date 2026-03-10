# io_simulation.py — Studio Shodwe · COA Project
# Simulates and compares Programmed I/O, Interrupt-Driven I/O, and DMA
# Subject: Computer Organization and Architecture (PBL)

import math
import json

# ── Constants ──────────────────────────────────────────────────────────────────
TRANSFER_RATE        = 100     # MB/s — base bus transfer speed
INTERRUPT_OVERHEAD   = 0.002   # seconds per interrupt received
CONTEXT_SWITCH       = 0.001   # seconds per context switch (save/restore CPU state)
DMA_INIT_TIME        = 0.0005  # seconds — one-time DMA controller setup
INTERRUPT_BLOCK_SIZE = 10      # MB per interrupt block
PIO_POLL_OVERHEAD    = 0.15    # 15% extra time due to busy-wait polling
PIO_CPU_FACTOR       = 0.68    # CPU active fraction during polling (idle gaps exist)
DMA_EFF_RATE         = 97      # Effective MB/s for DMA (reduced by bus arbitration)

DATA_SIZES = [1, 10, 50, 100, 250, 500, 1000]  # MB

# ── Programmed I/O ─────────────────────────────────────────────────────────────
# CPU continuously polls the status register until I/O is complete.
# No interrupt hardware needed. CPU is blocked the entire time.
def simulate_programmed_io(size_mb):
    base_time  = size_mb / TRANSFER_RATE
    poll_time  = base_time * PIO_POLL_OVERHEAD  # extra overhead from busy-wait loop
    total_time = base_time + poll_time
    cpu_time   = total_time * PIO_CPU_FACTOR    # CPU has idle gaps during bus stalls
    throughput = size_mb / total_time
    cpu_util   = (cpu_time / total_time) * 100
    return {
        "total_time": round(total_time, 5),
        "cpu_time":   round(cpu_time, 5),
        "throughput": round(throughput, 2),
        "cpu_util":   round(cpu_util, 2)
    }

# ── Interrupt-Driven I/O ───────────────────────────────────────────────────────
# CPU initiates I/O and continues other work. Device sends interrupt when ready.
# CPU only involved during ISR execution (context switch + handler).
def simulate_interrupt_io(size_mb):
    transfer_time = size_mb / TRANSFER_RATE
    n_interrupts  = max(1, math.floor(size_mb / INTERRUPT_BLOCK_SIZE))
    overhead      = n_interrupts * (INTERRUPT_OVERHEAD + CONTEXT_SWITCH)
    total_time    = transfer_time + overhead
    cpu_time      = overhead   # CPU only active during ISR handling
    throughput    = size_mb / total_time
    cpu_util      = (cpu_time / total_time) * 100
    return {
        "total_time":   round(total_time, 5),
        "cpu_time":     round(cpu_time, 5),
        "throughput":   round(throughput, 2),
        "cpu_util":     round(cpu_util, 4),
        "n_interrupts": n_interrupts
    }

# ── DMA (Direct Memory Access) ─────────────────────────────────────────────────
# CPU sets up DMA controller then steps aside. DMA manages bus and transfers data
# directly between memory and device. CPU only interrupted at completion.
def simulate_dma(size_mb):
    total_time = size_mb / DMA_EFF_RATE  # slightly reduced by bus arbitration
    cpu_time   = DMA_INIT_TIME           # CPU only used for setup
    throughput = size_mb / total_time
    cpu_util   = (cpu_time / total_time) * 100
    return {
        "total_time": round(total_time, 5),
        "cpu_time":   round(cpu_time, 5),
        "throughput": round(throughput, 2),
        "cpu_util":   round(cpu_util, 4)
    }

# ── Run Simulation ─────────────────────────────────────────────────────────────
def run_simulation(export_json=False):
    results = []

    print("=" * 90)
    print("  I/O DATA TRANSFER TECHNIQUES — SIMULATION RESULTS")
    print("  Studio Shodwe · Computer Organization and Architecture PBL")
    print("=" * 90)
    print(f"\n{'Size':>7} | {'PIO Total':>10} | {'PIO CPU':>10} | {'INT Total':>10} | {'INT CPU':>10} | {'DMA Total':>10} | {'DMA CPU':>10}")
    print("-" * 90)

    for size in DATA_SIZES:
        p = simulate_programmed_io(size)
        n = simulate_interrupt_io(size)
        d = simulate_dma(size)

        label = f"{size}MB" if size < 1000 else "1GB"
        print(f"{label:>7} | {p['total_time']:>9.4f}s | {p['cpu_time']:>9.4f}s | "
              f"{n['total_time']:>9.4f}s | {n['cpu_time']:>9.4f}s | "
              f"{d['total_time']:>9.4f}s | {d['cpu_time']:>9.5f}s")

        results.append({
            "data_size_mb":   size,
            "programmed_io":  p,
            "interrupt_io":   n,
            "dma":            d
        })

    print("\n" + "=" * 90)
    print("  RECOMMENDATION SUMMARY")
    print("=" * 90)
    print("  - Small  data (<5MB):    Programmed I/O  — no setup overhead")
    print("  - Medium data (5-80MB):  Interrupt I/O   — CPU free between transfers")
    print("  - Large  data (>80MB):   DMA             — CPU nearly 0% utilized")
    print("=" * 90)

    if export_json:
        output = {
            "project": "I/O Data Transfer Techniques",
            "team": "Studio Shodwe",
            "constants": {
                "transfer_rate_mbps":       TRANSFER_RATE,
                "interrupt_overhead_s":     INTERRUPT_OVERHEAD,
                "context_switch_s":         CONTEXT_SWITCH,
                "dma_init_time_s":          DMA_INIT_TIME,
                "interrupt_block_size_mb":  INTERRUPT_BLOCK_SIZE,
                "pio_poll_overhead_factor": PIO_POLL_OVERHEAD,
                "pio_cpu_active_factor":    PIO_CPU_FACTOR,
                "dma_effective_rate_mbps":  DMA_EFF_RATE
            },
            "results": results
        }
        with open("data/simulation-data.json", "w") as f:
            json.dump(output, f, indent=2)
        print("\n  Results saved to data/simulation-data.json")

    return results

if __name__ == "__main__":
    run_simulation(export_json=True)
