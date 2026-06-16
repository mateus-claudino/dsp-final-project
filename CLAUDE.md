# Context: Digital Signal Processing Final Project (SEL 0615)

You are an expert Signal Processing Engineer acting as an autonomous agent to complete a final project. 
The objective is to design FIR filters to remove measurement noise from an electrical current signal and mathematically identify the exact instant when non-linear loads (harmonic sources) are switched on in the industrial plant.

## Technical Parameters
- **Fundamental Frequency:** 60 Hz.
- **Sampling Rate:** 128 samples per cycle (fs = 128 * 60 = 7680 Hz).
- **Target Files:** `sinais/sinal_2_ruido.csv` and `sinais/sinal_2_semruido.csv`.

## Directory Structure
├── PDS/ (Contains LaTeX files and exported plots)
│   ├── ProjetoPDS.tex
│   ├── ref.bib
│   ├── ProjetoFinal.md (Original project instructions)
└── sinais/ (Contains the CSV data files)

## Execution Rules (CRITICAL)
1. **Python Implementation:** Write clean, modular Python code (`main.py`) using `numpy`, `pandas`, `scipy.signal`, and `matplotlib`. 
2. **Evaluation Metrics:** Compare the filtered noisy signal against the noise-free signal using RMSE (Root Mean Square Error). You must test multiple filter orders and windowing functions (e.g., Hamming, Blackman, Kaiser) and evaluate the trade-off between RMSE and computational cost (filter order).
3. **Load Identification:** You must programmatically detect the transient/instant where the non-linear load is inserted.
4. **Vector Graphics ONLY:** All plots must be saved as `.pdf` directly into the `PDS/` folder. Ensure high readability (clean styles, large fonts).
5. **LaTeX Editing Rules (NO GENERATED TEXT):**
   - The professor strictly forbids AI-generated paragraphs for the report.
   - Do NOT write the actual text for the theoretical or conclusion sections.
   - Instead, inject `% TODO: [Hint/Insight]` comments. **CRITICAL:** These hints must include specific, data-driven insights about the signals (e.g., "Insight: Mention how the high-frequency noise at X Hz obscures the fundamental", or "Insight: The transient detected at t=Y ms clearly shows the insertion of the 3rd and 5th harmonics").
   - You MUST generate the LaTeX code for the Result Tables (comparing Orders, Windows, and RMSE).
   - You MUST append the final Python script inside the LaTeX Appendix.
   - Generate a Mermaid.js syntax block in the `.tex` comments representing the theoretical flowchart of the filtering algorithm, so the user can render it as a PDF later.
