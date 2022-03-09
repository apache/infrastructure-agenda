#!../venv/bin/python

import re
import datetime

import click


@click.command()
@click.argument('file')
@click.option('--section', '-s', default=0, type=int)
def main(file, section):
    parsed_file = AgendaParser(file)

    print(parsed_file.contents)


class AgendaParser(object):

    def __init__(self, file):
        raw_sections = self._parse_sections(file)
        self.meta = {'date': self._parse_meeting_date(raw_sections[0]['data'])}
        self.contents = {'roll_call': self._parse_roll_call(raw_sections[2]['data']),
                         'previous_minutes': self._parse_last_minutes(raw_sections[3]['data'])
                         }

    def __repr__(self):
        return f"<ParsedAgenda: {self.meta['date']}>"

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
        section_pattern = r'^[ |\d]\d\.\s(.*)$'
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
