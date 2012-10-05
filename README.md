Generating MRC workouts
-----------------------

This script will take a workout description and output a computrainer compatible .mrc file

Usage
-----
    gdunn@ni:/home/gdunn/src/mrcgen$ ./mrcgen.py ftp-development.txt        
    [COURSE HEADER]
    VERSION = 2
    UNITS =  METRIC
    DESCRIPTION =  FTP bread and butter
    FILE NAME = ftp-development.mrc
    MINUTES PERCENTAGE
    [END COURSE HEADER]
    [COURSE DATA]
    0.000000 75.000000
    10.000000 75.000000
    10.000000 85.000000
    30.000000 85.000000
    30.000000 65.000000
    34.000000 65.000000
    34.000000 85.000000
    54.000000 85.000000
    54.000000 65.000000
    58.000000 65.000000
    58.000000 50.000000
    64.000000 50.000000
    [END COURSE DATA]



Example
-------
    2, METRIC, PreSeason Week 1: Tuesday Interval
    1 x ([10, 75], 
      5 x ([0.5, 100], [0.5, 65]), 
      [5, 75], 
      3 x ([10, 100], [3, 65]), 
      [5, 60])

Explanation
-----------

Line 1 of the file must be:
MRC Version, METRIC or ENGLISH, description of the workout (no commas!)

The remainer of the file describes the workout:

1 x (the workout) : you can change the "1" to "2" if you want to do the workout twice, for example

where "the workout" is a list of intervals, so the workout in the example has

Interval 1: [10, 75] = 10 minutes at 75% FTP

Interval 2: 5 x ([0.5, 100], [0.5, 65]) = 30 seconds at 100% FTP, 30 seconds at 65% FTP, repeated 5 times

Interval 3: [5, 75] = 5 minutes at 75% FTP

Interval 4: 3 x ([10, 100], [3, 65]) = 10 minutes at 100% FTP, 3 minutes at 65% FTP, repeated 3 times

Interval 5: [5, 60] = 5 minutes at 60% FTP

Another Example
---------------
    2, METRIC, FTP bread and butter
    1 x ([10, 75],
      2 x ([20, 85], [4, 65]),
      [6, 50])
