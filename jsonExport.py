import io
from pandas import read_json


def json_to_txt(json):
    df = read_json(json)

    f_str = io.StringIO()
    f_str.write(df.to_string())
    f_str.seek(0)  # move cursor to beginning
    return f_str
