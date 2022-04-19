import re
import datetime

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


class AgendaParser(object):

    # Regex patterns for various lines in the agenda. These are used
    # as both stop/start for the _parse_fragment() method.
    #
    # Note: technically, we could precompile them, but this entire
    # parse is sub-second.
    # TODO: precompile these even if just for self-doc purposes

    P_SECTION = r'^[ |\d]\d\.\s(.*)$'

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

    # Header
    RE_AGENDA_DATE = re.compile(r"(\w+\s\d{1,2},\s\d{4})")

    # Committee reports
    RE_REPORT_META = re.compile(r'\w+\.\sApache\s(.*?)\sProject\s\[(.*?)(?:\s\/\ (.*?))?\]')
    RE_REPORT_ATTACH = re.compile(r'See\sAttachment\s(\w+)')
    RE_REPORT_APPROVALS = re.compile(r'approved:\s(.*)')

    # Attachments
    RE_ATTACHMENT = re.compile(r"^Attachment\s(\w+)\:\s(.*?)\s+\[(.*?)\]")

    def __init__(self, file):
        raw_sections = self._parse_sections(file)
        with open(file, 'r') as fp:
            self._data = fp.readlines()

        self._idx = self._create_index(self._data, self.P_SECTION)

        self.date = self._parse_meeting_date(self._get_section(S_HEADER))
        self.last_minutes = self._parse_last_minutes(self._get_section(S_MINUTES))
        self.reports = self._parse_committee_reports(self._get_section(S_REPORTS))
        self.attachments = self._parse_attachments()

        ## TODO: convert the following to use self._create_index() and compiled patterns like the above
        #self.roll_call = self._parse_roll_call(raw_sections[S_ROLL_CALL]['data'])
        self.executive_officer_reports = self._parse_exec_officer_reports(raw_sections[S_EXEC_REPORTS]['data'])
        self.additional_officer_reports = self._parse_add_officer_reports(raw_sections[S_OFFICER_REPORTS]['data'])
        self.orders = self._parse_special_orders(raw_sections[S_ORDERS]['data'])

    def __repr__(self):
        return f"<ParsedAgenda: {self.date}>"

    def _parse_attachments(self):
        attachments = [ ]
        data = self._get_section(S_ATTACHMENTS)

        id = None
        title = None
        reporter = None
        content = [ ]

        for line in data:
            m = self.RE_ATTACHMENT.search(line)
            if m:
                if id:
                    attachments.append((id, title, reporter, "".join(content)))
                    content = [ ]
                id = m.group(1)
                title = m.group(2)
                reporter = m.group(3)
            elif re.search(r'-{41}', line):
                pass
            else:
                content.append(line)

        if id:
            attachments.append((id, title, reporter, "".join(content)))

        return attachments

    def _parse_special_orders(self, data):
        orders = [ ]

        title = None
        content = [ ]

        for line in data:
            m = re.search(r'^\w+\.\s(.*)$', line)
            if m:
                if title:
                    orders.append((title, content))
                    content = [ ]
                title = m.group(1)
            else:
                content.append(line)

        if title:
            orders.append((title, content))

        return orders

    def _parse_committee_reports(self, data):
        reports = [ ]

        project = None
        owner = None
        shepherd = None
        attachment = None
        approvals = None

        for line in data:
            m = self.RE_REPORT_META.search(line)
            if m:
                if project:
                    reports.append((project, owner, shepherd, attachment, approvals))
                    attachment = None
                    approvals = None
                project = m.group(1)
                owner = m.group(2)
                shepherd = m.group(3)
            m = self.RE_REPORT_ATTACH.search(line)
            if m:
                attachment = m.group(1)
            m = self.RE_REPORT_APPROVALS.search(line)
            if m:
                temp_list = [sig.strip() for sig in m.group(1).split(",")]
                approvals = tuple(temp_list)
            ## TODO: figure out how to grab comments here

        if project:
            reports.append((project, owner, shepherd, attachment, approvals))

        return reports

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
        ## TODO: need to parse out officer names here
        ## TODO: need to parse possible status messages in each report
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

    def _parse_meeting_date(self, data):
        date_str = self.RE_AGENDA_DATE.search("".join(data))
        return datetime.datetime.strptime(date_str.group(1), '%B %d, %Y').date()

    @staticmethod
    def _create_index(data, pattern):
        line_num = 1
        idx = [line_num]
        for line in data:
            m = re.search(pattern, line)
            if m:
                idx.append(line_num)
            line_num += 1
        idx.append(idx[-1] + 7)
        return idx

    def _get_section(self, section):
        if section == S_HEADER:
            s_start = 0
            s_end = self._idx[S_CALL_TO_ORDER] - 1
        elif section == S_ROLL_CALL:
            s_start = self._idx[S_ROLL_CALL]
            s_end = self._idx[S_MINUTES] - 1
        elif section == S_MINUTES:
            s_start = self._idx[S_MINUTES]
            s_end = self._idx[S_EXEC_REPORTS] - 1
        elif section == S_REPORTS:
            s_start = self._idx[S_REPORTS]
            s_end = self._idx[S_ORDERS] - 1
        elif section == S_ATTACHMENTS:
            s_start = self._idx[S_ATTACHMENTS]
            s_end = -1
        else:
            s_start = 0
            s_end = 0
        return self._data[s_start:s_end]

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