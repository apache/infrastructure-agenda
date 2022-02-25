import datetime

import werkzeug.routing


class DateConverter(werkzeug.routing.BaseConverter):
    """Extracts a date from the path and validates it"""

    regex = r'\d{4}_\d{2}_\d{2}'

    def to_python(self, value):
        try:
            return datetime.datetime.strptime(value, '%Y_%m_%d').date()
        except ValueError:
            raise werkzeug.routing.ValidationError()

    def to_url(self, value):
        return value.strftime('%Y_%m_%d')
