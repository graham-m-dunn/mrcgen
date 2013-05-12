Generating MRC workouts
-----------------------

This script exists on Google AppEngine, and will take a workout description and output a computrainer compatible .mrc file

Example
-------
    Fill in:
    Version = 2, 
    Units = METRIC
    Description = PreSeason Week 1: Tuesday Interval
    Workout = 
    1 x ([10, 75], 
      5 x ([0.5, 100], [0.5, 65]), 
      [5, 75], 
      3 x ([10, 100], [3, 65]), 
      [5, 60])

Another Example
---------------
    2, METRIC, FTP bread and butter
    1 x ([10, 75],
      2 x ([20, 85], [4, 65]),
      [6, 50])
