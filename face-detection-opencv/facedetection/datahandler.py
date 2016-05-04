# -*- coding: utf-8 -*-
# Copyright (C) 2016 Canonical
#
# Authors:
#  Didier Roche
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import datetime
import logging
import os
import sqlite3

from tools import Singleton, get_data_path, suppress

logger = logging.getLogger(__name__)


class DataHandler(object):
    """Retrieve and store face data handling"""
    __metaclass__ = Singleton

    def __init__(self):
        self._conn = sqlite3.connect(os.path.join(get_data_path(), 'faces_detect.sqlite'))
        c = self._conn.cursor()
        with suppress(sqlite3.OperationalError):
            c.execute("CREATE TABLE FacesDetect(Timestamp DATETIME, Number INTEGER);")
            self._conn.commit()
        c.execute("SELECT * FROM FacesDetect ORDER BY Timestamp")
        self.face_detect_data = c.fetchall()
        logger.debug("Found {}".format(self.face_detect_data))

    def add_one_facedetect_entry(self, timestamp, count):
        """Add one face detect datapoint at timestamp"""
        logger.info("Add new data point: {} at {}".format(count, datetime.datetime.utcfromtimestamp(timestamp).isoformat()))
        c = self._conn.cursor()
        c.execute("INSERT INTO FacesDetect VALUES({}, {})".format(timestamp, count))
        self._conn.commit()
        self.face_detect_data.append((timestamp, count))
