Generating MRC workouts
-----------------------

I still need to figure out a reasonable format for specifying the workouts. Best thought so far is a 
text file consisting of a series of lines of either Intervals or Repeat directives. This will lend itself 
to a web page form interface.

Interval format
---------------

Line I minutes percentFTP

Repeat format
-------------

Line R repeat_from_line repeat_to_line repetitions

Example
-------

    1 I 10 75
    2 I 0.5 100
    3 I 1 65
    4 R 2 3 5
    5 I 5 75
    6 I 10 100
    7 I 3 65
    8 R 6 7 3
    9 I 5 60

