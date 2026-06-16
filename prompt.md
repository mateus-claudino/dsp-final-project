Read the CLAUDE.md file for the project constraints and rules, and read PDS/ProjetoFinal.md for the original instructions. I want you to execute the entire pipeline autonomously.

  Please follow these steps in order:

  Step 1: Signal Analysis & Processing (Python)
  Create main.py in the root folder. Load the CSV files, calculate the time vector (fs=7680 Hz), and write a robust FIR filter
  function. Test at least 3 different windowing methods and 3 different filter orders. Calculate the RMSE for each combination.
  Programmatically identify the exact sample/time when the non-linear load is inserted.

  Step 2: Plot Generation
  Generate high-quality, vectorized .pdf plots saving them to PDS/. I need at least:

      A plot comparing the noisy signal, the noise-free signal, and the best-filtered signal.

      A plot highlighting the exact moment the non-linear load is switched on.

  Step 3: LaTeX Integration
  Modify PDS/ProjetoPDS.tex directly:

      Insert the generated .pdf figures into the document with proper captions.

      Create a beautifully formatted \begin{table} that tabulates the RMSE, Filter Order, and Windowing methods tested.

      Include the final main.py code in the Appendix section using a verbatim or listings environment.

      Provide the Mermaid code for the algorithm's flowchart as a commented block in the 'Fundamentação Teórica' section.

      Crucial: Leave detailed % TODO: comments in the 'Fundamentação Teórica', 'Análise dos Sinais', and 'Conclusões' sections. These
  comments must provide deep, technical insights about the signal behavior, the harmonic content, the trade-off between filter order
  and delay, and the specific characteristics of the transient you detected, so I have strong data to write the text myself.

  Execute all steps and let me know when the .tex file is fully updated and ready for my manual writing.