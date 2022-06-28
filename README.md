# module_testing_plots

Plots input and output noise for modules tested through itsdaq.

Works for R1, R2, R4 and R5 sensors though R5 sensors may need reversal of channels for proper plotting (at least at TRIUMF)

It should be noted that line 34 should be uncommented PPA modules and line 35 for prototype modules.

Command to run is (windows):

```
python plot_module_noise.py --run_numbers <list of run numbers> --sensor_type <module number> --labels <List of commnents>
```

Example:
```
python plot_module_noise.py --run_numbers 1424, 1436 --sensor_type R4 --labels "TRIUMF Box", "Diamond Box"
```
