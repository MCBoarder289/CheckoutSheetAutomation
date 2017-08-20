# How To: https://cx-freeze.readthedocs.io/en/latest/distutils.html
# From CMD: cd to the project directory, then on mac run: python3 setup-mac.py build

# ALSO - did some strange manually copy/pasting of QT's framework that I'll outline:
# Went and found the Python.Framework in my usr/local/Cellar directory
# Pasted that in the /Library/Frameworks directory
# Had to get the site-packages directory from Cellar and put them in the Library/Frameworks/Python.framework folder
# Had to find the QT frameworks located in /usr/local/lib/python3.6/site-packages/PyQt5/Qt/lib...
# Then manually copied those in /usr/local/Cellar/python3/3.6.2/Frameworks/Python.framework/Versions/3.6/lib
# Still get strange error on not having QtGamepad.framework, which won't create standalone .app
# but the executable will open a console window, then the window we need, so it's at least testable/manageable

# To get around the opening of the terminal window, deliver the whole build folder, and then create an AppleScript
# that saves as an application. See the site below:
# http://brizzled.clapper.org/blog/2008/10/22/wrapping-an-executable-inside-a-mac-os-x-application/

import sys
from cx_Freeze import setup, Executable
import os.path

# tcl library key error: https://stackoverflow.com/questions/35533803/keyerror-tcl-library-when-i-use-cx-freeze
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
# os.environ['PYQT5_LIBRARY'] = '/usr/local/lib/python3.6/site-packages/PyQt5'

# Dependencies are automatically detected, but it might need fine tuning.

build_exe_options = {'include_files': ['/usr/local/lib/python3.6/site-packages/PyQT5',
                                       '/usr/local/lib/python3.6/site-packages/PyQT5/Qt/lib'],
    
                     #                  os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')],
                     # 'includes': ['qtpy'],
                     'excludes': ['tcl', 'ttk', 'tkinter', 'Tkinter'],
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
