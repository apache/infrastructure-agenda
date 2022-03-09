#!../venv/bin/python

import re
import datetime

import click


@click.command()
@click.argument('file')
@click.option('--section', '-s', default=0, type=int)
def main(file, section):
    parsed_file = AgendaParser(file)

    print(parsed_file)


class AgendaParser(object):

    def __init__(self, file):
        self._sections = self._parse_sections(file)
        self._date = self._parse_meeting_date(self._sections[0]['data'])

    def __repr__(self):
        return f"<ParsedAgenda: {self._date.date()}>"

    @staticmethod
    def _parse_meeting_date(section):
        return datetime.datetime.strptime(section[2], '%B %d, %Y')

    @staticmethod
    def _parse_sections(file_name):
        sections = [{'name': 'head', 'data': []}]
        section_num = 0
        section_pattern = r'^[ |\d]\d\.\s(.*)$'
        with open(file_name, "r") as fp:

            for line in fp.readlines():
                match = re.search(section_pattern, line)
                if match is not None:
                    section_num += 1
                    sections.append({'name': match.group(1).replace(" ", "_").lower(),
                                     'data': []})
                else:
                    line = line.strip()
                    if line:
                        sections[section_num]['data'].append(line)

        return sections


if __name__ == "__main__":
    main()
