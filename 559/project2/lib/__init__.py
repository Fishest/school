'''
Project 2 - Viola Jones / PCA
-----------------------------------------------------------
'''
import logging

# ------------------------------------------------------------------ #
# The following is to prevent "no attached handler" messages
# ------------------------------------------------------------------ #
class NullHandler(logging.Handler):
    def emit(self, record):
        pass

h = NullHandler()
logging.getLogger("project").addHandler(h)
