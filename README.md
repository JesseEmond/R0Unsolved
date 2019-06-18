# R0Unsolved
Tool to help pick a next challenge to do on
[RingZer0](https://ringzer0ctf.com/challenges), based on the heuristic that more
solves means that a challenge is likely easier to solve. Weights the number of
solves by the number of points for the challenge.

Note:
- Uses Python 3;
- Relies on HTML parsing, so relatively brittle;
- Doesn't take into account challenges that have other challenges as a prerequisite;
- Implicitly doesn't promote new/newer challenges, but they might still be worth trying;
- Learning is the most important part of R0, so don't take this tool ordering too seriously. :)

## Example
```
> python unsolved_r0.py 2574
  Score  Name                             Id    # Solves    # Points
-------  -----------------------------  ----  ----------  ----------
   1088  Linux x64 shellcoding level 4   132         136           8
   1032  Linux x64 shellcoding level 3   131         172           6
    972  Linux x64 shellcoding level 6   134          81          12
    950  Linux x64 shellcoding level 5   133          95          10
    950  Quote of the day reloaded        38         190           5
    892  Linux x64 shellcoding level 2   128         223           4
    840  Size DOES matter                 78         120           7
    840  The useless search tool         123         105           8
    792  Hot Single Mom                  158         132           6
    672  PHP Jail 5                      227         112           6
```

Guess I should get started on that shellcoding track...

## Setup
Uses Python 3.
```
pip install --user -r requirements.txt
```

## Usage
```
> python unsolved_r0.py -h
usage: unsolved_r0.py [-h] [--points-weight POINTS_WEIGHT] [-n MAX_CHALLENGES]
                      userid

Lists the unsolved challenges on R0 (using the given user ID), sorted to help
pick the next unsolved challenge that has the most solves, weighted by points.

positional arguments:
  userid                User ID (from your profile URL).

optional arguments:
  -h, --help            show this help message and exit
  --points-weight POINTS_WEIGHT
                        Weight contributed by the challenge points to the
                        sorting score.
  -n MAX_CHALLENGES, --max-challenges MAX_CHALLENGES
                        Max number of challenges to display. Set to high
                        number to display all.
```
