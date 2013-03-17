# -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
" NINJA-IDE Time Tracker "
__version__ = ' 0.1 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 20/04/2013 '
__prj__ = ' timetracker '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from os import path
from subprocess import call

from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QDockWidget
from PyQt4.QtGui import QPushButton

try:
    from PyKDE4.kdecore import *
    from PyKDE4.kparts import *
except ImportError:
    pass

from ninja_ide.core import plugin


# constants
TRACK_FILE = path.abspath(path.join(path.expanduser("~"),
             '.kde/share/apps/ktimetracker/ktimetracker.ics'))


###############################################################################


class Main(plugin.Plugin):
    " dock Class "
    def initialize(self):
        " Init Class dock "
        self.dock = QDockWidget()
        self.dock.setFeatures(QDockWidget.DockWidgetFloatable |
                                           QDockWidget.DockWidgetMovable)
        self.dock.setWindowTitle(__doc__)
        self.dock.setStyleSheet('QDockWidget::title{text-align: center;}')
        self.boton = QPushButton(QIcon.fromTheme("document-open-recent"),
                                 'Edit Track', self.dock)
        self.boton.setToolTip('Edit iCal: ' + TRACK_FILE)
        try:
            self.factory = KPluginLoader("ktimetrackerpart").factory()
            self.part = self.factory.create(self)
            self.part.setReadWrite(True)
            self.part.closeUrl()
            self.part.openUrl(KUrl(str(TRACK_FILE)))
            self.boton.clicked.connect(lambda: call('xdg-open ' + TRACK_FILE,
                                                    shell=True))
            self.dock.setWidget(self.part.widget())
        except:
            self.dock.setWidget(QLabel(""" <center>
            <h3>ಠ_ಠ<br> ERROR: Please, install kTimeTracker App ! </h3><br>
            <br><i> (Sorry, cant embed non-Qt Apps). </i><center>"""))
        self.misc = self.locator.get_service('misc')
        self.misc.add_widget(self.dock, QIcon.fromTheme("user-away"), __doc__)


###############################################################################


if __name__ == "__main__":
    print(__doc__)
