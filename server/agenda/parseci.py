#!/usr/bin/env python
#
# parseci -- parse committee-info.txt
#

import re
import sys

RE_NAME = re.compile(r'([A-Za-z0-9+ -.]+?)  +([A-Z].*?) +<.*')

PERIOD_A = 'January'      # January, April, July, October
PERIOD_B = 'February'     # February, May, August, November
PERIOD_C = 'March'        # March, June, September, December
PERIOD_ALL = 'Next'  # Note all reports expected next month

MONTH_MAP = [
             PERIOD_A, PERIOD_B, PERIOD_C,
             PERIOD_A, PERIOD_B, PERIOD_C,
             PERIOD_A, PERIOD_B, PERIOD_C,
             PERIOD_A, PERIOD_B, PERIOD_C,
             ]


def parse_info(fp):
    lines = [s.split("#")[0].strip() for s in fp.readlines()]

    # parse the committee names and VPs
    c = []
    gather_proj = False
    gather_rot = None
    for line in lines:
        if line.startswith('NAME'):
            gather_proj = True
        elif not line:
            gather_proj = False  # stop gathering
        elif gather_proj and not line.startswith('--'):
            m = RE_NAME.match(line)
            if not m:
                print('BAD:', line)
            else:
                c.append({'name': m.group(1).lower(),
                          'chair': m.group(2),
                          'reporting': None})

        if line.startswith(PERIOD_A):
            gather_rot = PERIOD_A
        elif line.startswith(PERIOD_B):
            gather_rot = PERIOD_B
        elif line.startswith(PERIOD_C):
            gather_rot = PERIOD_C
        elif line.startswith(PERIOD_ALL):
            gather_rot = PERIOD_ALL
        elif line.startswith('==='):
            gather_rot = None
        elif gather_rot:
            if line.startswith('---'):
                pass
            elif not line:
                gather_rot = None  # stop gathering
            else:
                rot = None
                for committee in c:
                    if committee['name'].lower() == line.lower():
                        if committee['reporting'] and gather_rot != PERIOD_ALL:
                            print('DUPLICATED REPORTING PERIOD: ', line)
                        else:
                            rot = gather_rot
                            committee['reporting'] = rot.lower()
                        break
                if rot is None:  
                    print('BAD:', line)

    return c


if __name__ == '__main__':
    parse_info(sys.stdin)
