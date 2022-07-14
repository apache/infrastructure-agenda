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


class AgendaParser(object):
    # TODO: DRY up the _parse_* methods
    # TODO: finish docstrings

    # Regex patterns for various lines in the agenda.

    RE_SECTION = re.compile(r'^[ |\d]\d\.\s(.*)$')
    RE_SUBSECTION = re.compile(r'^\ +\w+\.\s(.*)$')

    # Header
    RE_AGENDA_DATE = re.compile(r'(\w+\s\d{1,2},\s\d{4})')

    # Roll Call
    RE_ROLL_CALL = re.compile(r'^\ +.*:$')

    # Officer reports
    RE_EXEC_REPORT = re.compile(r'^\ {4}\w\.\ (.*?)\ \[(.*?)\]')
    RE_OFFICER_REPORT_META = re.compile(r'\w+\.\ (.*?)\ \[(.*?)(?:\s\/\ (.*?))?\]')

    # Committee reports
    RE_REPORT_META = re.compile(r'\w+\.\sApache\s(.*?)\sProject\s\[(.*?)(?:\s\/\ (.*?))?\]')
    RE_REPORT_ATTACH = re.compile(r'See\sAttachment\s(\w+)')
    RE_REPORT_APPROVALS = re.compile(r'approved:\s(.*)')

    # Discussion items
    RE_DISCUSS_ITEMS = re.compile(r' +\w+\. (.*)| +\* (.*)\:')

    # Action items
    RE_REVIEW_ACTION_ITEMS = re.compile(r' +\* (.*)\: (.*)')
    RE_REVIEW_ACTION_ITEMS_STATUS = re.compile(r' +Status\: (.*)')

    # Attachments
    RE_ATTACHMENT = re.compile(r'^Attachment\s(\w+)\:\s(.*?)\s+\[(.*?)\]')

    def __init__(self, file):
        with open(file, 'r', encoding="utf-8", errors="surrogateescape") as fp:
            self._data = fp.readlines()
        self._idx = self._create_index(self._data, self.RE_SECTION)

        self.date = self._parse_meeting_date(self._get_section(S_HEADER))
        self.call_to_order = self._parse_call_to_order(self._get_section(S_CALL_TO_ORDER))
        self.roll_call = self._parse_roll_call(self._get_section(S_ROLL_CALL))
        self.last_minutes = self._parse_last_minutes(self._get_section(S_MINUTES))
        self.exec_reports = self._parse_exec_reports(self._get_section(S_EXEC_REPORTS))
        self.officer_reports = self._parse_officer_reports(self._get_section(S_OFFICER_REPORTS))
        self.reports = self._parse_committee_reports(self._get_section(S_REPORTS))
        self.orders = self._parse_special_orders(self._get_section(S_ORDERS))
        self.discuss_items = self._parse_discuss_items(self._get_section(S_DISCUSS_ITEMS))
        self.review_action_items = self._parse_review_action_items(self._get_section(S_REVIEW_ACTION_ITEMS))
        #self.unfinished_business = self._parse_unfinished_business(self._get_section(S_UNFINISHED_BUSINESS))
        #self.new_business = self._parse_new_business(self._get_section(S_NEW_BUSINESS))
        #self.announcements = self._parse_announcments(self._get_section(S_ANNOUNCEMENTS))
        #self.adjournment = self._parse_ajournment(self._get_section(S_ADJOURNMENT))
        self.attachments = self._parse_attachments(self._get_section(S_ATTACHMENTS))

    def __repr__(self):
        return f"<ParsedAgenda: {self.date}>"

    def _parse_attachments(self, data):
        attachments = [ ]

        label = None
        title = None
        reporter = None
        content = [ ]

        for line in data:
            m = self.RE_ATTACHMENT.search(line)
            if m:
                if label:
                    attachments.append((label, title, reporter, "".join(content)))
                    content = [ ]
                label = m.group(1)
                title = m.group(2)
                reporter = m.group(3)
            elif re.search(r'-{41}', line):
                pass
            else:
                content.append(line)

        if label:
            attachments.append((label, title, reporter, "".join(content)))

        return attachments

    def _parse_review_action_items(self, data):
        items = [ ]

        assignee = None
        title = None
        status = None

        # TODO: need to grab second, third, etc... lines of title/status
        for line in data:
            m = self.RE_REVIEW_ACTION_ITEMS.search(line)
            if m:
                if assignee:
                    items.append((title, assignee, status))
                    status = None
                assignee = m.group(1)
                title = m.group(2)

            m = self.RE_REVIEW_ACTION_ITEMS_STATUS.search(line)
            if m:
                status = m.group(1)

        if assignee:
            items.append((title, assignee, status))

        return items

    def _parse_discuss_items(self, data):
        """
        '    A. Set a date for the Annual Members Meeting'
        -OR-
        '''    * Branding: I'd like to invite counsel Mark Radcliffe from DLAPiper
               to talk with the board about the risks to Apache marks and the
               importance of having sufficient education and funding for all PMCs.
               Mark is free at 11AM Pacific; I hope the board will listen.
        '''
        """
        # TODO: the RE_DISCUSS_ITEMS regex 'or' logic is not working
        items = [ ]

        title = None
        content = [ ]

        for line in data:
            m = self.RE_DISCUSS_ITEMS.search(line)
            if m:
                if title:
                    items.append((title, "".join(content)))
                    content = [ ]
                title = m.group(1)
            else:
                content.append(line)

        if title:
            items.append((title, "".join(content)))

        return items

    def _parse_special_orders(self, data):
        orders = [ ]

        title = None
        content = [ ]

        for line in data:
            m = self.RE_SUBSECTION.search(line)
            if m:
                if title:
                    orders.append((title, "".join(content)))
                    content = [ ]
                title = m.group(1)
            else:
                content.append(line)

        if title:
            orders.append((title, "".join(content)))

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
                if m.group(3):
                    shepherd = m.group(3)
                else:
                    shepherd = None
            m = self.RE_REPORT_ATTACH.search(line)
            if m:
                attachment = m.group(1)
            m = self.RE_REPORT_APPROVALS.search(line)
            if m:
                temp_list = [sig.strip() for sig in m.group(1).split(",")]
                approvals = tuple(temp_list)
            # TODO: figure out how to grab comments here

        if project:
            reports.append((project, owner, shepherd, attachment, approvals))

        return reports

    def _parse_officer_reports(self, data):
        """
        Returns the list of officer reports

            Parameters:
                data (string): a string containing the additional officer report section of the agenda

            Returns:
                officer_reports (list): (TITLE, OWNER, SHEPHERD, ATTACHMENT, APPROVALS)
        """
        officer_reports = [ ]

        title = None
        owner = None
        shepherd = None
        attachment = None
        approvals = None

        for line in data:
            m = self.RE_OFFICER_REPORT_META.search(line)
            if m:
                if title:
                    officer_reports.append((title, owner, shepherd, attachment, approvals))
                    attachment = None
                    approvals = None
                title = m.group(1)
                owner = m.group(2)
                if m.group(3):
                    shepherd = m.group(3)
                else:
                    shepherd = None
            m = self.RE_REPORT_ATTACH.search(line)
            if m:
                attachment = m.group(1)
            m = self.RE_REPORT_APPROVALS.search(line)
            if m:
                temp_list = [sig.strip() for sig in m.group(1).split(",")]
                approvals = tuple(temp_list)
            # TODO: figure out how to grab comments here

        if title:
            officer_reports.append((title, owner, shepherd, attachment, approvals))


        return officer_reports

    def _parse_exec_reports(self, data):
        """
        Returns the list of executive officer reports

            Parameters:
                data (string): a string containing the executive officer report section of the agenda

            Returns:
                exec_reports (list): (POSITION, REPORTER, CONTENT)
        """
        exec_reports = [ ]

        position = None
        reporter = None
        content = [ ]

        for line in data:
            m = self.RE_EXEC_REPORT.search(line)
            if m:
                if position:
                    exec_reports.append((position, reporter, "".join(content)))
                    reporter = None
                    content = [ ]
                position = m.group(1)
                reporter = m.group(2)
            else:
                content.append(line)

        if position:
            exec_reports.append((position, reporter, "".join(content)))

        return exec_reports

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
                    minutes.append(self.Minutes(min_date, min_filename, min_content))
                    min_filename = None
                    min_content = None
                min_date = datetime.datetime.strptime(m.group(1), '%B %d, %Y')
            else:
                m = re.search(r'See: (.*)', line)
                if m:
                    min_filename = m.group(1)

            # TBD: do we need to capture CONTENT?

        # Parse loop done. Finish out accumulated info.
        if min_date:
            minutes.append(self.Minutes(min_date, min_filename, min_content))

        #print('MINUTES:', minutes)
        return minutes

    def _parse_roll_call(self, data):
        """
        Returns lists of who is expected to attend/not-attend the meeting
            Parameters:
                data (str): a string containing the roll call section of the agenda
            Returns:
                roll_call (list): a list containing tuples with the following contents and order:
                    [directors expected to be present,
                    directors expected to be absent,
                    executive officers expected to be present,
                    executive officers expected to be absent,
                    guests expected to be present]
        """
        roll_call = [ ]

        people = [ ]

        for line in data:
            if self.RE_ROLL_CALL.search(line):
                if len(people) > 0:
                    roll_call.append(tuple(people))
                    people = [ ]
            elif line != '\n':
                people.append(line.strip())

        if len(people) > 0:
            roll_call.append(tuple(people))

        # return everything but the initial cruft that gets captured
        return roll_call[1:]

    def _parse_call_to_order(self, data):
        data_str = "".join(data)
        start_time = re.search(r'The meeting is scheduled for (.*) and will begin', data_str)
        time_zone_link = re.search(r'Other\ Time\ Zones: (.*)', data_str)

        return tuple([start_time.group(1), time_zone_link.group(1)])

    def _parse_meeting_date(self, data):
        date_str = self.RE_AGENDA_DATE.search("".join(data))
        return datetime.datetime.strptime(date_str.group(1), '%B %d, %Y').date()

    @staticmethod
    def _create_index(data, pattern):
        """
        Returns a list of line numbers where a specific pattern can be found.

            Parameters:
                data (string): a string to be searched through
                pattern (re object): a pattern to be searched for within data

            Returns:
                idx (list): a list of line numbers
        """
        line_num = 1
        idx = [line_num]
        for line in data:
            m = pattern.search(line)
            if m:
                idx.append(line_num)
            line_num += 1
        idx.append(idx[-1] + 7)
        return idx

    def _get_section(self, section):
        """
        Returns a slice of self._data based on the requested section

            Parameters:
                section (int): A number representing the requested section; likely using the
                               globals defined above.

            Returns:
                (list): a slice of self._data
        """
        s_start = 0
        s_end = 0

        if section == S_HEADER:
            s_end = self._idx[S_CALL_TO_ORDER] - 1
        elif section == S_ATTACHMENTS:
            s_start = self._idx[S_ATTACHMENTS]
            s_end = -1
        else:
            s_start = self._idx[section]
            s_end = self._idx[section + 1] - 1

        return self._data[s_start:s_end]

    class Minutes(object):

        def __init__(self, date, file, content):
            self.date = date.strftime('%B %d, %Y')
            self.file = file
            self.content = content

