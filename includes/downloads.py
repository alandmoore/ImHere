"""
Functions related to downloading application data.
"""
import sys
if sys.version_info.major < 3:
    from StringIO import StringIO
else:
    from io import StringIO
import csv
from datetime import date


def create_csv(headers, data):
    fh = StringIO()
    csvfile = csv.writer(fh)
    csvfile.writerow(headers)
    xstr = lambda s: s is not None and s or ""
    for row in data:
        output_row = [xstr(row[header])
                      for header in headers]
        csvfile.writerow(output_row)
    return fh.getvalue()


def data_dump_csv(db_model):
    csv_data = db_model.customer_dump()
    csv_headers = db_model.table_headers("customers_rept")

    data = create_csv(csv_headers, csv_data)
    headers = {
        "Content-Disposition":
        "attachment; filename=signin_sheet_data-{}.csv".format(
            date.today().isoformat()
        )
    }
    mimetype = "text/csv"

    return data, headers, mimetype
