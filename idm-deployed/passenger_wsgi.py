import sys, os

INTERP = "/home/example/demo-covid-idm/env/bin/python"

if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

from app import app as application