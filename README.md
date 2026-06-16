## Project Objectives (Group B1-B4 Track)
Our group is responsible for the **FIR (Finite Impulse Response)** filtering track. Our core objectives are:
* **Filter Design:** Project and implement FIR filters to process noisy signals.
* **Error Minimization:** Minimize the RMSE (Root Mean Square Error) when comparing our filtered signal against the provided noise-free baseline signal.
* **Parameter Optimization:** Test various filter orders and windowing techniques to find the optimal balance between signal clarity and computational cost.
* **Algorithm Implementation:** Develop a generalized function that can apply these FIR filters to signals of any length.

## Repository Structure
```text
dsp-final-project/
│
├── signals/        # CSV files (e.g., sinal_N_semruido, sinal_N_ruido)
├── src/            # Source code for our FIR filter functions
├── docs/           # LaTeX source files for the final report
└── README.md       # Project overview and workflow rules

```

## Deliverables

By the end of this project, this repository will house our two main deliverables:

1. The final functional script (Python or MATLAB).
2. The final project report written in LaTeX (using the provided e-Disciplinas template).

## Collaborative Git Workflow

Since multiple people are working on this repository, we are using a **Feature Branch Workflow** to prevent merge conflicts and keep the `main` branch stable.

**⚠️ STOP: Do not push directly to the `main` branch!** Follow these steps for every new feature, bug fix, or analysis script.

### 1. Update your local environment

Always start by pulling the latest changes from the remote `main` branch:

```bash
git checkout main
git pull origin main

```

### 2. Create a new branch

Create a new branch for your specific task. Use a descriptive name so the team knows exactly what you are working on.

```bash
git checkout -b type/short-description

```

**Naming conventions:**

* `feature/` - for new additions (e.g., `feature/fir-windowing-tests`)
* `fix/` - for bug fixes (e.g., `fix/rmse-calculation`)
* `docs/` - for documentation/LaTeX updates (e.g., `docs/latex-intro`)

### 3. Make changes and commit

Write your code, test your outputs against the noise-free signals, and commit your changes. Write clear commit messages.

```bash
git add .
git commit -m "Implement RMSE calculation function for FIR outputs"

```

### 4. Push your branch

Push your newly created branch to GitHub:

```bash
git push -u origin your-branch-name

```

### 5. Open a Pull Request (PR)

1. Go to the repository on GitHub.
2. Click the green **Compare & pull request** button for your branch.
3. Briefly describe your code (e.g., "Tested a Hamming window with order 50, computational cost looks good").
4. Request a review from at least one teammate.
5. Once approved, the branch will be merged into `main`.
""")

