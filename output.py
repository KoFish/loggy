import io


class Output(io.BufferedWriter):
    _prev_nl = True
    _line_count = 0

    def __init__(self, console, old):
        self._out = old
        self._console = console
        self.write_raw = old.write

    def _remove_cr(self, row):
        if '\r' in row:
            string, rest = row.split('\r', 1)
            string = self._remove_cr(rest) + string[len(rest):]
            return string
        return row

    def _normalize_rows(self, rows, columns):
        new_rows = []
        for row in rows:
            row = self._remove_cr(row)
            while row:
                crow, row = row[:columns], row[columns:]
                new_rows.append(crow)
        if not new_rows:
            return ['']
        return new_rows

    def write(self, string):
        endnl = string.endswith('\n')
        string = string[:-1] if endnl else string
        lines, columns = self._console.get_size()
        rows = string.split('\n')
        rows = self._normalize_rows(rows, columns)
        if not Output._prev_nl:
            self._out.write(rows[0])
            rows = rows[1:]
        erows = enumerate(rows, Output._line_count)
        Output._line_count += len(rows)
        self._out.write('\n'.join("{0[1]}".format(each) for each in erows))
        if endnl:
            self._out.write('\n')
        else:
            self._out.flush()
        Output._prev_nl = endnl

    def get_current_row(self):
        return self._line_count

    def flush(self):
        self._out.flush()

