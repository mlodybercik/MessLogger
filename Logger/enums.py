from enum import IntEnum

class LogType(IntEnum):
    NONE = 0 #           "default"
    TEXT = 1 #           to arr
    LOG_TO_CONSOLE = 2 # log to console
    LIVE_LOG = 3 #       to live file stream
    DUMP_CONTENTS = 4 #   dump whole arr
