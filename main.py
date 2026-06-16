import sys
import logging
import numpy as np
import pandas as pd
from scipy.signal import firwin, filtfilt, freqz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

FS = 7680.0        # Hz — 128 samples/cycle × 60 Hz
FC = 600.0         # Low-pass cutoff (Hz): preserves up to 10th harmonic, rejects broadband noise
OUTPUT_DIR = Path("PDS")

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_signal(path: str) -> np.ndarray:
    return pd.read_csv(path, header=None)[0].values


# ---------------------------------------------------------------------------
# FIR filter design and application
# ---------------------------------------------------------------------------

def design_fir(numtaps: int, window, cutoff: float = FC, fs: float = FS) -> np.ndarray:
    """Window-based linear-phase FIR low-pass filter (Type I for odd numtaps).

    Group delay of the causal implementation: (numtaps - 1) / 2 samples.
    At fs=7680 Hz and numtaps=128, this is 63/7680 ≈ 8.2 ms.
    filtfilt cancels this delay for offline evaluation; lfilter with explicit
    index shift must be used for causal/real-time deployment.
    """
    return firwin(numtaps, cutoff, window=window, fs=fs)


def apply_filter(signal: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Zero-phase FIR filtering via forward-backward pass (filtfilt).
    Doubles effective roll-off order; suitable for offline RMSE evaluation.
    """
    return filtfilt(b, 1.0, signal)


def rmse(filtered: np.ndarray, reference: np.ndarray) -> float:
    return float(np.sqrt(np.mean((filtered - reference) ** 2)))


# ---------------------------------------------------------------------------
# Transient (non-linear load insertion) detection
# ---------------------------------------------------------------------------

def detect_transient(signal: np.ndarray, fs: float, window_samples: int = 128):
    """Rolling RMS energy estimator with maximum-gradient detector.

    Computes 1-cycle (128-sample) rolling RMS using the cumulative-sum trick
    (O(N) complexity). The sample with the steepest positive RMS gradient
    marks the non-linear load insertion onset.

    Returns
    -------
    idx : int   — detected sample index in the original signal
    t   : float — corresponding time in seconds
    rms : ndarray — rolling RMS array (length N - window_samples)
    """
    sq = signal ** 2
    cs = np.cumsum(sq)
    # Sliding window sum: cs[i] - cs[i - window_samples]
    window_sums = np.empty(len(sq) - window_samples + 1)
    window_sums[0] = cs[window_samples - 1]
    window_sums[1:] = cs[window_samples:] - cs[:-window_samples]
    rms_arr = np.sqrt(window_sums / window_samples)

    grad = np.diff(rms_arr)
    # argmax gives the index inside grad; shift back to original signal index
    peak_in_grad = int(np.argmax(grad))
    # peak_in_grad + 1 aligns to the right edge of the window where the jump ends;
    # subtract window_samples // 2 to approximate the onset midpoint.
    idx = peak_in_grad + window_samples // 2
    return idx, idx / fs, rms_arr


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------

def _save_pdf(fig: plt.Figure, name: str) -> Path:
    path = OUTPUT_DIR / name
    fig.savefig(path, format="pdf", bbox_inches="tight")
    plt.close(fig)
    log.info("Saved %s", path)
    return path


def plot_comparison(
    t: np.ndarray,
    noisy: np.ndarray,
    clean: np.ndarray,
    filtered: np.ndarray,
    best_label: str,
    best_rmse: float,
) -> Path:
    """Three-panel time-domain comparison plot."""
    fig, axes = plt.subplots(3, 1, figsize=(8, 9), sharex=True)

    axes[0].plot(t * 1000, noisy, color="#888888", linewidth=0.6, alpha=0.85)
    axes[0].set_ylabel("Corrente (A)", fontsize=11)
    axes[0].set_title("Sinal com Ruído de Medição", fontsize=11)
    axes[0].grid(True, linestyle="--", linewidth=0.4)

    axes[1].plot(t * 1000, clean, color="#1f4e79", linewidth=0.9)
    axes[1].set_ylabel("Corrente (A)", fontsize=11)
    axes[1].set_title("Sinal Sem Ruído (Referência)", fontsize=11)
    axes[1].grid(True, linestyle="--", linewidth=0.4)

    axes[2].plot(t * 1000, filtered, color="#c0392b", linewidth=0.9)
    axes[2].set_ylabel("Corrente (A)", fontsize=11)
    axes[2].set_xlabel("Tempo (ms)", fontsize=11)
    axes[2].set_title(
        f"Sinal Filtrado — {best_label}  |  RMSE = {best_rmse:.5f}", fontsize=11
    )
    axes[2].grid(True, linestyle="--", linewidth=0.4)

    fig.tight_layout(pad=1.5)
    return _save_pdf(fig, "fig_comparison.pdf")


def plot_transient(
    t: np.ndarray,
    filtered: np.ndarray,
    rms_arr: np.ndarray,
    transient_idx: int,
    transient_time: float,
) -> Path:
    """Two-panel plot: filtered signal + rolling RMS with transient marker."""
    t_rms = np.arange(len(rms_arr)) / FS  # rolling RMS has different length

    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=False)

    # Top: full filtered signal with vertical transient marker
    axes[0].plot(t * 1000, filtered, color="#1f4e79", linewidth=0.8)
    axes[0].axvline(
        x=transient_time * 1000,
        color="#e74c3c",
        linestyle="--",
        linewidth=1.4,
        label=f"Transitório: t = {transient_time * 1000:.2f} ms (amostra {transient_idx})",
    )
    axes[0].set_ylabel("Corrente (A)", fontsize=11)
    axes[0].set_title("Sinal Filtrado — Detecção de Inserção de Carga Não-Linear", fontsize=11)
    axes[0].legend(fontsize=9, loc="upper left")
    axes[0].grid(True, linestyle="--", linewidth=0.4)
    axes[0].set_xlabel("Tempo (ms)", fontsize=11)

    # Bottom: rolling RMS with gradient peak marker
    axes[1].plot(t_rms * 1000, rms_arr, color="#27ae60", linewidth=0.9)
    axes[1].axvline(
        x=transient_time * 1000,
        color="#e74c3c",
        linestyle="--",
        linewidth=1.4,
    )
    axes[1].set_ylabel("RMS Deslizante (A)", fontsize=11)
    axes[1].set_xlabel("Tempo (ms)", fontsize=11)
    axes[1].set_title("RMS Deslizante (janela = 1 ciclo = 128 amostras)", fontsize=11)
    axes[1].grid(True, linestyle="--", linewidth=0.4)

    fig.tight_layout(pad=1.5)
    return _save_pdf(fig, "fig_transient.pdf")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    log.info("Loading signals — fs=%.0f Hz, fc=%.0f Hz", FS, FC)
    noisy = load_signal("sinais/sinal_2_ruido.csv")
    clean = load_signal("sinais/sinal_2_semruido.csv")
    assert len(noisy) == len(clean), "Signal length mismatch"
    N = len(noisy)
    t = np.arange(N) / FS
    log.info("N=%d samples, duration=%.4f s (~%.1f cycles)", N, N / FS, N / (FS / 60))

    # --- FFT spectrum summary (informational) ---
    freqs = np.fft.rfftfreq(N, d=1.0 / FS)
    noise_spectrum = np.abs(np.fft.rfft(noisy - clean))
    peak_noise_freq = freqs[np.argmax(noise_spectrum)]
    log.info("Peak noise energy at %.1f Hz (choose fc=%.0f Hz to reject)", peak_noise_freq, FC)

    # --- FIR filter test matrix ---
    windows = [
        ("hamming",           "Hamming"),
        ("blackman",          "Blackman"),
        (("kaiser", 8.6),     "Kaiser (β=8.6)"),
    ]
    numtaps_list = [32, 64, 128]  # orders 31, 63, 127

    results = []
    print(f"\n{'Window':<20} {'Taps':>6} {'RMSE':>12}")
    print("-" * 42)
    for taps in numtaps_list:
        for win_param, win_name in windows:
            b = design_fir(taps, win_param)
            filtered = apply_filter(noisy, b)
            err = rmse(filtered, clean)
            group_delay_ms = (taps - 1) / 2 / FS * 1000
            results.append({
                "window": win_name,
                "win_param": win_param,
                "numtaps": taps,
                "order": taps - 1,
                "rmse": err,
                "group_delay_ms": group_delay_ms,
                "filtered": filtered,
            })
            print(f"{win_name:<20} {taps:>6} {err:>12.6f}")

    # --- Select best configuration ---
    best = min(results, key=lambda r: r["rmse"])
    log.info(
        "Best filter: %s, %d taps (order %d), RMSE=%.6f, group delay=%.2f ms",
        best["window"], best["numtaps"], best["order"], best["rmse"], best["group_delay_ms"],
    )

    # --- Transient detection ---
    tr_idx, tr_time, rms_arr = detect_transient(best["filtered"], FS)
    log.info(
        "Transient detected: sample %d, t=%.4f s (%.2f ms), cycle ~%.1f",
        tr_idx, tr_time, tr_time * 1000, tr_time * 60,
    )
    # Cross-validate on clean signal
    tr_idx_clean, tr_time_clean, _ = detect_transient(clean, FS)
    log.info(
        "Cross-validation on clean signal: sample %d, t=%.4f s",
        tr_idx_clean, tr_time_clean,
    )

    # --- Plots ---
    OUTPUT_DIR.mkdir(exist_ok=True)
    plot_comparison(t, noisy, clean, best["filtered"], best["window"], best["rmse"])
    plot_transient(t, best["filtered"], rms_arr, tr_idx, tr_time)

    # --- Structured summary for LaTeX injection ---
    print("\n=== LATEX TABLE DATA ===")
    print(f"{'Window':<22} {'32 taps':>10} {'64 taps':>10} {'128 taps':>10}")
    print("-" * 54)
    for _, win_name in windows:
        row_vals = [r["rmse"] for r in results if r["window"] == win_name]
        vals_str = "   ".join(f"{v:.5f}" for v in row_vals)
        print(f"{win_name:<22} {vals_str}")

    print(f"\n=== TRANSIENT DETECTION ===")
    print(f"  Filtered signal: sample={tr_idx}, t={tr_time:.4f} s ({tr_time*1000:.2f} ms), cycle≈{tr_time*60:.2f}")
    print(f"  Clean signal:    sample={tr_idx_clean}, t={tr_time_clean:.4f} s ({tr_time_clean*1000:.2f} ms), cycle≈{tr_time_clean*60:.2f}")
    print(f"\n=== BEST FILTER ===")
    print(f"  Window: {best['window']}")
    print(f"  Taps: {best['numtaps']} (order {best['order']})")
    print(f"  RMSE: {best['rmse']:.6f}")
    print(f"  Group delay (lfilter): {best['group_delay_ms']:.2f} ms")


if __name__ == "__main__":
    main()
