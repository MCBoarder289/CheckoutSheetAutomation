# How To: https://cx-freeze.readthedocs.io/en/latest/distutils.html
# From CMD: python setup.py build

import sys
from cx_Freeze import setup, Executable
import os.path

# tcl library key error: https://stackoverflow.com/questions/35533803/keyerror-tcl-library-when-i-use-cx-freeze
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# Dependencies are automatically detected, but it might need fine tuning.

build_exe_options = {'include_files': [os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                                       os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')],
                     'packages': ["numpy"]  # numpy was missing as a dependency
                     }

"""
options = {  # {"packages": ["os"], "excludes": ["tkinter"]}
    {
        'include_files': [
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')
         ],
    },
}
"""

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name="PDFtoExcelConverter",
        version="0.1",
        description="For Making Easier Rosters!",
        options={"build_exe": build_exe_options},
        executables=[Executable("PDFtoExcel.py", base=base)])
