#!../venv/bin/python

import re
import datetime

import click

# Section names
S_HEADER = 0
S_CALL_TO_ORDER = 1
S_ROLL_CALL = 2
S_MINUTES = 3
S_EXEC_REPORTS = 4
S_OFFICER_REPORTS = 5
S_REPORTS = 6
S_ORDERS = 7
S_DISCUSS_ITEMS = 8
S_REVIEW_ACTION_ITEMS = 9
S_UNFINISHED_BUSINESS = 10
S_NEW_BUSINESS = 11
S_ANNOUNCEMENTS = 12
S_ADJOURNMENT = 13
S_ATTACHMENTS = 14

# Report names
R_VP_W3C = 'vp_of_w3c_relations'
R_VP_LEGAL = 'apache_legal_affairs_committee'

# Officer names
O_CHAIR = 'chairman'
O_PRESIDENT = 'president'
O_TREASURER = 'treasurer'
O_SECRETARY = 'secretary'
O_EVP = 'executive_vice_president'
O_VICE_CHAIR = 'vice_chairman'

# Roll call sections
### do we need these bits? ... seems we only need: who attended,
### extracted from minutes
RC_DIRECTORS_PRESENT = 'directors_present'
RC_DIRECTORS_ABSENT = 'directors_absent'
RC_OFFICERS_PRESENT = 'officers_present'
RC_OFFICERS_ABSENT = 'officers_absent'
RC_GUESTS_PRESENT = 'guests_present'


@click.command()
@click.argument('file')
@click.option('--section', '-s', default=0, type=int)
def main(file, section):
    parsed_file = AgendaParser(file)

    print("\n".join(parsed_file.raw_sections[S_REPORTS]['data']))


class AgendaParser(object):

    # Regex patterns for various lines in the agenda. These are used
    # as both stop/start for the _parse_fragment() method.
    #
    # Note: technically, we could precompile them, but this entire
    # parse is sub-second.

    # Section headers
    P_OFFICER_REPORTS = r'5\.\ Additional\ Officer\ Reports'

    # Roll call lines
    P_RC_DIRECTORS_PRESENT = r"Directors\ \(expected\ to\ be\)\ Present\:"
    P_RC_DIRECTORS_ABSENT = r"Directors\ \(expected\ to\ be\)\ Absent\:"
    P_RC_EXEC_PRESENT = r"Executive\ Officers\ \(expected\ to\ be\)\ Present\:"
    P_RC_EXEC_ABSENT = r"Executive\ Officers\ \(expected\ to\ be\)\ Absent\:"
    P_RC_GUESTS = r"Guests\ \(expected\)\:"

    # Executive Officer Reports
    P_CHAIR = r'A\.\ Chairman\ \[.*\]'
    P_PRESIDENT = r'B\.\ President\ \[.*\]'
    P_TREASURER = r'C\.\ Treasurer\ \[.*\]'
    P_SECRETARY = r'D\.\ Secretary\ \[.*\]'
    P_EVP = r'E\.\ Executive\ Vice\ President\ \[.*\]'
    P_VICE_CHAIR = r'F\.\ Vice\ Chairman\ \[.*\]'

    # Additional Officer Reports
    P_VP_W3C = r'A\.\ VP\ of\ W3C\ Relations'
    P_VP_LEGAL = r'B\.\ Apache\ Legal\ Affairs\ Committee'
    P_SECURITY_TEAM = r'C\.\ Apache\ Security\ Team\ Project'

    # Reports (gmxs)
    P_REPORT = r'''\s{4}\w+\.\s(?P<project>.*?)\s\[(?P<owner>.*?)(?:\s\/\s(?P<shepherd>.*?))?\]
                   \s+See\sAttachment\s(?P<attachment>\w+)
                   \s+\[(?P<status>.*?)\]'''
    # status (xs)
    P_STATUS = r'''approved:\s(?P<approvals>.*?)?\n
                   comments:\s(?P<comments>.*)'''

    def __init__(self, file):
        raw_sections = self._parse_sections(file)
        self.date = self._parse_meeting_date(raw_sections[S_HEADER]['data'])
        self.roll_call = self._parse_roll_call(raw_sections[S_ROLL_CALL]['data'])
        self.previous_minutes = self._parse_last_minutes(raw_sections[S_MINUTES]['data'])
        self.executive_officer_reports = self._parse_exec_officer_reports(raw_sections[S_EXEC_REPORTS]['data'])
        self.additional_officer_reports = self._parse_add_officer_reports(raw_sections[S_OFFICER_REPORTS]['data'])
        #self.reports = self._parse_committee_reports("\n".join(raw_sections[S_REPORTS]['data']))

        ### for main()
        self.raw_sections = raw_sections

    def __repr__(self):
        return f"<ParsedAgenda: {self.date}>"

    def _parse_committee_reports(self, data):
        ret = re.findall(self.P_REPORT, data, re.MULTILINE | re.VERBOSE | re.DOTALL)
        return ret

    def _parse_add_officer_reports(self, data):
        return {
            R_VP_W3C: self._parse_fragment(data,
                                           self.P_VP_W3C,
                                           self.P_VP_LEGAL),
            R_VP_LEGAL: self._parse_fragment(data,
                                             self.P_VP_LEGAL,
                                             self.P_SECURITY_TEAM),
        }

    def _parse_exec_officer_reports(self, data):
        # need to parse out officer names here
        # also need to parse possible status messages in each report
        ret = {}
        ret[O_CHAIR] = self._parse_fragment(data,
                                            self.P_CHAIR,
                                            self.P_PRESIDENT)

        ret[O_PRESIDENT] = self._parse_fragment(data,
                                                self.P_PRESIDENT,
                                                self.P_TREASURER)

        ret[O_TREASURER] = self._parse_fragment(data,
                                                self.P_TREASURER,
                                                self.P_SECRETARY)

        ret[O_SECRETARY] = self._parse_fragment(data,
                                                self.P_SECRETARY,
                                                self.P_EVP)

        ret[O_EVP] = self._parse_fragment(data,
                                          self.P_EVP,
                                          self.P_VICE_CHAIR)

        ret[O_VICE_CHAIR] = self._parse_fragment(data,
                                                 self.P_VICE_CHAIR,
                                                 self.P_OFFICER_REPORTS)

        return ret

    def _parse_last_minutes(self, data):
        # List of minutes to approve. Tuples: (DATE, FILENAME, CONTENT)
        minutes = [ ]

        # What have we seen/accumulated?
        min_date = None
        min_filename = None
        min_content = None

        for line in data:
            m = re.search(r'The meeting of (.*)', line)
            if m:
                if min_date:
                    minutes.append((min_date, min_filename, min_content))
                    min_filename = None
                    min_content = None
                min_date = datetime.datetime.strptime(m.group(1), '%B %d, %Y')
            else:
                m = re.search(r'See: (.*)', line)
                if m:
                    min_filename = m.group(1)

            ### TBD: do we need to capture CONTENT?

        # Parse loop done. Finish out accumulated info.
        if min_date:
            minutes.append((min_date, min_filename, min_content))

        ### need to come back to this bit and parse it out more fully.
        ### old code. Leaving for posterity and carry-forward
        if False:
         ret['status'] = self._parse_fragment(data,
                                             r"See: board_minutes_.*\.txt",
                                             r"\]")

        #print('MINUTES:', minutes)
        return minutes

    def _parse_roll_call(self, data):
        ret = {}
        ret[RC_DIRECTORS_PRESENT] = \
            self._parse_fragment(data,
                                 self.P_RC_DIRECTORS_PRESENT,
                                 self.P_RC_DIRECTORS_ABSENT)
        ret[RC_DIRECTORS_ABSENT] = \
            self._parse_fragment(data,
                                 self.P_RC_DIRECTORS_ABSENT,
                                 self.P_RC_EXEC_PRESENT)
        ret[RC_OFFICERS_PRESENT] = \
            self._parse_fragment(data,
                                 self.P_RC_EXEC_PRESENT,
                                 self.P_RC_EXEC_ABSENT)

        ret[RC_OFFICERS_ABSENT] = \
            self._parse_fragment(data,
                                 self.P_RC_EXEC_ABSENT,
                                 self.P_RC_GUESTS)

        ret[RC_GUESTS_PRESENT] = \
            self._parse_fragment(data,
                                 self.P_RC_GUESTS,
                                 r"\n")

        return ret

    @staticmethod
    def _parse_meeting_date(section):
        parsed_date = datetime.datetime.strptime(section[2], '%B %d, %Y')
        return parsed_date.date()

    @staticmethod
    def _parse_sections(file_name):
        ret = [{'name': 'head', 'data': []}]
        section_num = 0
        section_pattern = r'^[ |\d]\d\.\s(.*)$|\={12}\n(ATTACHMENTS):\n\={12}'
        with open(file_name, "r") as fp:

            for line in fp.readlines():
                match = re.search(section_pattern, line)
                if match is not None:
                    section_num += 1
                    ret.append({'name': match.group(1).replace(" ", "_").lower(),
                                'data': []})
                else:
                    line = line.strip()
                    if line:
                        ret[section_num]['data'].append(line)

        return ret

    @staticmethod
    def _parse_fragment(fragment, start_pattern, stop_pattern):
        ret = []
        capture = False
        for line in fragment:

            if re.search(stop_pattern, line):
                #print("STATE: capture->False", line)
                capture = False

            if capture is True:
                #print(f"CAPTURE: {line}")
                ret.append(line.strip())

            if re.search(start_pattern, line):
                #print("STATE: capture->True", line)
                capture = True

        return ret


if __name__ == "__main__":
    main()
