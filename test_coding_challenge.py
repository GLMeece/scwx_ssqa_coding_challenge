import logging
import os
import platform
import random
import sqlite3

from faker import Faker

# - - - - - - - - - - - - - - - - - - SETUP - - - - - - - - - - - - - - - - - -

fake = Faker()

logging.getLogger("faker").setLevel(logging.ERROR)
LOGFILE = "scwx_rc_test.log"
test_log_file_path = os.getcwd() + f"/reports/{LOGFILE}"
os.makedirs(os.path.dirname(test_log_file_path), exist_ok=True)
# If you want to append the log, change the "w" to an "a"
open(test_log_file_path, "w").close()

# Setup logging format
log_format = '%(asctime)s | %(filename)s:%(lineno)d > %(message)s'
logging.basicConfig(
    filename=test_log_file_path,
    format=log_format,
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG
)
LOG = logging.getLogger()

# Fake malware processes
windows_malware_list = [
    "winlogon.exe", "jusched.exe", "10aba34-5619.tmp", "CDProxyServ.exe",
    "svchost.exe", "VistaDrive.exe", "$hp2F63.tmp", "csrss.exe",
    "services.exe", "SearchSettings.exe"
]

linux_malware_list = [
    "CrossRat", "GoScanSSH", "RubyMiner", "Erebus", "HandOfThief", "Jellyfish",
    "Heur", "Mayhem", "Chapro", "Wirenet"
]


def return_malware():
    """Return malware list per platform"""
    if platform.system() == "Windows":
        return windows_malware_list
    else:
        return linux_malware_list

# - - - - - - - - - - - - - - - - HELPER CLASS - - - - - - - - - - - - - - - -


class RedShawl:
    """Very limited emulation of an endpoint agent"""

    def __init__(self):
        self.rs_db_file = "red_shawl.db"
        self.pid = random.randrange(99999)
        self.name = fake.pystr()
        self.username = fake.first_name()
        self.status = 'running'

    def _random_malware(self):
        return random.choice(return_malware())

    def proc_name_is_malware(self):
        self.name = self._random_malware()

    def _sqllite_db_create(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            table_exists = """SELECT count(name) FROM sqlite_master
                WHERE type='table' AND name='proc_vals'"""
            cursor.execute(table_exists)
            if cursor.fetchone()[0] != 1:
                LOG.info("DB doesn't exist - let's create it!")
                create_table = \
                    """CREATE TABLE proc_vals
                    (recid INTEGER PRIMARY KEY, pid INTEGER, name TEXT,
                    username TEXT, status TEXT)"""
                cursor.execute(create_table)
            else:
                LOG.info("DB already exists")
        except sqlite3.Error as error:
            LOG.error("SQLlite error:", error)
        finally:
            if (conn):
                conn.close()

    def sqllite_write(self, write_vals):
        try:
            self._sqllite_db_create(self.rs_db_file)
            conn = sqlite3.connect(self.rs_db_file)
            write_cursor = conn.cursor()
            sql_stmnt = "INSERT INTO proc_vals(pid, name, username, status) " \
                "VALUES (?,?,?,?)"
            write_cursor.execute(sql_stmnt, write_vals)
            conn.commit()
        except sqlite3.Error as error:
            LOG.error("SQLlite error:", error)
        finally:
            if (conn):
                conn.close()

    def sqllite_read(self, sqllite_read):
        try:
            self._sqllite_db_create(self.rs_db_file)
            conn = sqlite3.connect(self.rs_db_file)
            read_cursor = conn.cursor()
            read_cursor.execute(sqllite_read)
            record = read_cursor.fetchall()
            read_cursor.close()
            return record
        except sqlite3.Error as error:
            LOG.error("SQLlite error:", error)


def test_db():
    """Tests the DB existence/connection
    
    Only run if this file is executed directly - """
    red_shawl_obj = RedShawl()
    pid = random.randrange(99999)
    name = fake.pystr()
    username = fake.first_name()
    status = 'running'
    print("Attempting to write to DB...")
    red_shawl_obj.sqllite_write([pid, name, username, status])
    print("Did we write to dB? Let's check...")
    select_sql = f"""SELECT pid, name, username, status FROM proc_vals
                WHERE PID = {pid};"""
    select_record = red_shawl_obj.sqllite_read(select_sql)[0]
    print(select_record)


# - - - - - - - - - - - - - - - - TEST CLASSES - - - - - - - - - - - - - - - -


class TestSensorReturn:
    """Testing what is returned by sensor."""

    def test_has_name(self):
        """Verify process name is returned"""
        rs_obj = RedShawl()
        rs_dict = vars(rs_obj)
        LOG.debug(f"Is `name` a valid proc name? : '{rs_dict['name']}'")
        assert "name" in rs_dict

    def test_has_pid(self):
        """Verify PID is valid integer"""
        rs_obj = RedShawl()
        rs_dict = vars(rs_obj)
        LOG.debug(f"Is `pid` a valid integer? : '{rs_dict['pid']}'")
        assert "pid" in rs_dict
        assert isinstance(rs_dict['pid'], int)

    def test_pid_nonzero(self):
        """Verify returned PID is > 0"""
        rs_obj = RedShawl()
        rs_dict = vars(rs_obj)
        LOG.debug(f"Is `pid` > 0? : '{rs_dict['pid']}'")
        assert rs_dict['pid'] > 0

    def test_status_running(self):
        """Verify process is actually running"""
        rs_obj = RedShawl()
        rs_dict = vars(rs_obj)
        LOG.debug(f"Is `status` 'running'? : '{rs_dict['status']}'")
        assert rs_dict['status'] == "running"

    def test_proc_is_malware(self):
        """Looking for valid malware process"""
        rs_obj = RedShawl()
        rs_obj.proc_name_is_malware()
        rs_dict = vars(rs_obj)
        LOG.debug(f"Is proc `name` malware? : '{rs_dict['name']}'")
        malware_set = return_malware()
        assert rs_dict['name'] in malware_set

    def test_proc_is_not_malware(self):
        """Verifying *not* malware process"""
        rs_obj = RedShawl()
        rs_dict = vars(rs_obj)
        LOG.debug(f"Is proc `name` *not* malware? : '{rs_dict['name']}'")
        malware_set = return_malware()
        assert rs_dict['name'] not in malware_set[0]


# class TestBreakPoints:
#     """Break points - what might go wrong?"""

#     def test_no_connection(self):
#         faux_procname = ""

#     def test_two(self):
#         x = "hello"
#         assert hasattr(x, "check")


class TestDatabaseWrites:
    """Does DB reflect what is expected?"""

    def test_values_written_in_db(self):
        """Verifies that a proc record written to the database aligns with
        what 'Red Shawl' is reporting.
        
        Normally, this functionality would be within the connection class..."""
        rs_obj = RedShawl()
        rs_dict = vars(rs_obj)
        write_vals = [
            rs_dict['pid'], rs_dict['name'], rs_dict['username'],
            rs_dict['status']
        ]
        rs_obj.sqllite_write(write_vals)
        find_new_record = f"""SELECT COUNT(*) FROM proc_vals
                WHERE PID = {rs_dict['pid']};"""
        record_count, = rs_obj.sqllite_read(find_new_record)[0]
        LOG.debug(f"record_count: '{record_count}'")
        assert record_count > 0


if __name__ == "__main__":
    """If called directly, tests the DB connection"""
    test_db()
