import configparser

config = configparser.ConfigParser()
r = config.read('.settings.ini')

TOKEN = config['DEFAULT']['token']
CONNECTION = config['DEFAULT']['db_connection_string']
USERS = config['DEFAULT']['users'].split()

SQL_TELEGRAM_WRAP_PROC = 'SET NOCOUNT ON;' \
                         'DECLARE @result nvarchar(max);' \
                         'exec core.dbo.telegram_wrap @user=?, @rtype=?, @value=?, @result = @result OUTPUT;' \
                         'select @result as result;'
