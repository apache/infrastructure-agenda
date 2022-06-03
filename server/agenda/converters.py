import datetime

import werkzeug.routing


class DateConverter(werkzeug.routing.BaseConverter):
    """Extracts a date from the path and validates it"""

    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise werkzeug.routing.ValidationError()

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')
