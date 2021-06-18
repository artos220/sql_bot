from xml.etree.ElementTree import Element, SubElement, tostring
from pyodbc import connect

from config import CONNECTION, SQL_TELEGRAM_WRAP_PROC


def sp_telegram_wrap(data):
    user = data[0]
    rtype = data[1]

    root = Element('root')
    SubElement(root, 'v').text = data[2] if len(data) > 2 else ''
    # SubElement(root, 'v2').text = data[3] if len(data) > 3 else ''
    values = tostring(root).decode()

    conn = connect(CONNECTION)
    cursor = conn.cursor()

    cursor.execute(SQL_TELEGRAM_WRAP_PROC, (user, rtype, values))
    result = cursor.fetchval()

    conn.close()
    return result
