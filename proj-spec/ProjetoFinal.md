## Final Project

In a certain industrial plant in the Southeast Region of Brazil, there are non-linear electrical loads used in production processes (rectifiers, inverters, DC motor drives) that draw harmonic currents. At the beginning of the workday, the factory operates only with linear loads (RLC), and at certain times of the day, the non-linear loads are switched on.

A meter located at the connection point between the factory and the utility's medium-voltage grid records the current demanded by the installation in one of its phases at a sampling rate of **128 samples per cycle**, as illustrated in Figure 1. The fundamental frequency is **60 Hz**.

**Figure 1: Current signal read by the meter** *(Note: Figure not included in text)*

The engineering department was assigned to develop a digital signal processing routine to remove measurement noise and identify the instant when non-linear loads (harmonic sources) are inserted. 

To carry out this activity you must **use the files “sinal_2_semruido” and “sinal_2_ruido”** that are on folder sinais/.

### Exercises

**a)** Design FIR (Finite Impulse Response) filters to be applied to the noisy signal in order to minimize the RMSE (Root Mean Square Error) relative to the noise-free signal. Implement the filters as a Python or MATLAB function so they can be applied to any signal size.

**b)** Test different filter orders and windowing methods. Determine the most suitable parameters for the problem. Take into account the computational cost when sizing the filter orders.

### What you must submit:

* The Python script developed in the exercise.
* The project report written in LaTeX, using the template provided on PDS/ProjetoPDS.tex.