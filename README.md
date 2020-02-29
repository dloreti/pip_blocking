# pip_blocking
pip_blocking is a python prototype to test the performance of four different methods to compute the worst-case plocking time of a task under the prescriptions of Priority Inheritance Protocol (PIP). We suppose that tasks are served under uniprocessor fixed-priority scheduling.

## Getting started
Download IBM ILOG CPLEX Optimization Studio 12.9 from https://www.ibm.com/products/ilog-cplex-optimization-studio and follow the installation instructions.
Also, follow the instructions of https://www.ibm.com/support/knowledgecenter/SSSA5P_12.6.2/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/Python_setup.html to set up the python API for CPLEX

## User Guide
The file `generator.py` reports some useful functions to synthetically generate a benchmarck of applications for the evaluation.

`background.py` reports the state-of-the-art procedures to compute the worst-case blocking time. In particular, `def buttazzo(app : Application)` implements the technique of:

Giorgio C. Buttazzo. 2011. Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications, Third Edition. Real-Time Systems Series, Vol. 24. Springer. https://doi.org/10.1007/978-1-4614-0676-1

The function `def rajkumar(app : Application)` implements the technique of:

Ragunathan Rajkumar. 1991. Synchronization in Real-Time Systems: A Priority Inheritance Approach. Kluwer Academic
Publishers, Norwell, MA, USA.

The file `loreti_faldella.py` implements two Binary Linear Programming based approaches reported in:

Eugenio Fadella and Daniela Loreti, Precise Worst-case Blocking Time of Tasks under Priority Inheritance Protocol. Submitted to IEEE Trans. on Computers in 2020.

The function `def schedule(app: Application, n: int, Qn : list)` of file `scheduler.py` evaluates the feasibility of the solution (in terms of the possibility that a block chaining as the one on the solution can actually occur) provided by any method.

You can use `compute_n_store.py` to launch the comparison. The file `computeY_n_store.py` can be used to call `schedcat` and compute the results of Yang et al.'s method reported in:

M. Yang, A. Wieder, and B. B. Brandenburg, Global real-time semaphore protocols: A survey, unified analysis, and compari- son, in IEEE Real-Time Systems Symposium, RTSS, 2015, pp. 1–12.

In order to execute `computeY_n_store.py` you have to first download the github repository of `schedcat` (https://github.com/brandenburg/schedcat) and store it into the lib folder of this project. Since `schedcat` only works with python 2.7, be sure to launch `computeY_n_store.py` with it. All other python script in this project run with python 3.

The results will be saved in the `apps` directory. Then, you can use `load_n_plot.py` to visualize the results.
