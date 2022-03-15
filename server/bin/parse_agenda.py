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

# Report names
R_VP_W3C = 'vp_of_w3c_relations'
R_VP_LEGAL = 'apache_legal_affairs_committee'

# Officer names
O_CHAIR = 'chairman'
O_PRESIDENT = 'president'
O_SECRETARY = 'secretary'
O_EVP = 'executive_vice_president'
O_VICE_CHAIR = 'vice_chairman'


@click.command()
@click.argument('file')
@click.option('--section', '-s', default=0, type=int)
def main(file, section):
    parsed_file = AgendaParser(file)

    print(parsed_file.raw_sections[section])


class AgendaParser(object):

    def __init__(self, file):
        raw_sections = self._parse_sections(file)
        self.date = self._parse_meeting_date(raw_sections[S_HEADER]['data'])
        self.roll_call = self._parse_roll_call(raw_sections[S_ROLL_CALL]['data'])
        self.previous_minutes = self._parse_last_minutes(raw_sections[S_MINUTES]['data'])
        self.executive_officer_reports = self._parse_exec_officer_reports(raw_sections[S_EXEC_REPORTS]['data'])
        self.additional_officer_reports = self._parse_add_officer_reports(raw_sections[S_OFFICER_REPORTS]['data'])

        ### for main()
        self.raw_sections = raw_sections

    def __repr__(self):
        return f"<ParsedAgenda: {self.date}>"

    def _parse_add_officer_reports(self, data):
        ret = {}
        ret[R_VP_W3C] = \
            self._parse_fragment(data,
                                 r'A\.\ VP\ of\ W3C\ Relations',
                                 r'B\.\ Apache\ Legal\ Affairs\ Committee')

        ret[R_VP_LEGAL] = \
            self._parse_fragment(data,
                                 r'B\.\ Apache\ Legal\ Affairs\ Committee',
                                 r'C\.\ Apache\ Security\ Team\ Project')

        return ret

    def _parse_exec_officer_reports(self, data):
        # need to parse out officer names here
        # also need to parse possible status messages in each report
        ret = {}
        ret[O_CHAIR] = \
            self._parse_fragment(data,
                                 r'A\.\ Chairman\ \[.*\]',
                                 r'B\.\ President\ \[.*\]')

        ret[O_PRESIDENT] = \
            self._parse_fragment(data,
                                 r'B\.\ President\ \[.*\]',
                                 r'C\.\ Treasurer\ \[.*\]')

        ret[O_SECRETARY] = \
            self._parse_fragment(data,
                                 r'D\.\ Secretary\ \[.*\]',
                                 r'E\.\ Executive\ Vice\ President\ \[.*\]')

        ret[O_EVP] = \
            self._parse_fragment(data,
                                 r'E\.\ Executive\ Vice\ President\ \[.*\]',
                                 r'F\.\ Vice\ Chairman\ \[.*\]')

        ret[O_VICE_CHAIR] = \
            self._parse_fragment(data,
                                 r'F\.\ Vice\ Chairman\ \[.*\]',
                                 r'5\.\ Additional\ Officer\ Reports')

        return ret

    def _parse_last_minutes(self, data):
        data_str = "\n".join(data)
        ret = {}

        date_match = re.search(r'The\ meeting\ of\ (.*)', data_str)
        ret['date'] = datetime.datetime.strptime(date_match.group(1), '%B %d, %Y')
        file_match = re.search(r'See:\ (.*)', data_str)
        ret['file'] = file_match.group(1)

        # need to come back to this bit and parse it out more fully
        ret['status'] = self._parse_fragment(data,
                                             r"See: board_minutes_.*\.txt",
                                             r"\]")

        return ret

    def _parse_roll_call(self, data):
        ret = {}
        ret['directors_present'] = \
            self._parse_fragment(data,
                                 r"Directors\ \(expected\ to\ be\)\ Present\:",
                                 r"Directors\ \(expected\ to\ be\)\ Absent\:")
        ret['directors_absent'] = \
            self._parse_fragment(data,
                                 r"Directors\ \(expected\ to\ be\)\ Absent\:",
                                 r"Executive\ Officers\ \(expected\ to\ be\)\ Present\:")
        ret['officers_present'] = \
            self._parse_fragment(data,
                                 r"Executive\ Officers\ \(expected\ to\ be\)\ Present\:",
                                 r"Executive\ Officers\ \(expected\ to\ be\)\ Absent\:")

        ret['officers_absent'] = \
            self._parse_fragment(data,
                                 r"Executive\ Officers\ \(expected\ to\ be\)\ Absent\:",
                                 r"Guests\ \(expected\)\:")

        ret['guests_present'] = \
            self._parse_fragment(data,
                                 r"Guests\ \(expected\)\:",
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
