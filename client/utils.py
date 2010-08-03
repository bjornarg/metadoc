# -*- coding: utf-8 -*-
#
#            utils.py is part of MetaDoc (Client).
#
# All of MetaDoc is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# MetaDoc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MetaDoc.  If not, see <http://www.gnu.org/licenses/>.
lxml = False

import logging
import datetime
import time
import re
import sys
import os
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
else:
    lxml = True
    

import version
import metadoc
from cacher import Cacher

def _singleton(cls):
    """ Decorator creating a singleton """
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@_singleton
class UniqueID(object):
    """ Singleton class to create unique IDs. """
    def __init__(self):
        """ Starts the ID counter at 0. """
        self.last_id = 0
    def get_id(self):
        """ Increments the ID counter and returns it. 
        
        @return: str on the form "_%d"
        
        """
        self.last_id = self.last_id + 1
        return "_%i" % self.last_id


def check_response(element_tag, md, xml_data, cache_data=True):
    """ Wrapper function for the 
    L{MetaDoc.check_response<metadoc.MetaDoc.check_response>} function that 
    catches any errors raised and logs them.

    @param element_tag: Element tag name
    @type element_tag: str
    @param md: Document sent that created I{xml_data} response
    @type md: L{MetaDoc}
    @param xml_data: Data returned from server when I{md} was sent.
    @type xml_data: str
    @param cache_data: Indicates whether or not I{md} should be cached
                       in case of a error in I{xml_data}.
    @type cache_data: bool

    """
    try:
        md.check_response(xml_data)
    except metadoc.NoReceiptReturnedError, nr:
        logging.error("Server returned no receipt for \"%s\" data." % 
                        element_tag)
        if cache_data:
            logging.info("Caching data for \"%s\"." % element_tag)
            Cacher(element_tag, md)
        else:
            logging.warning("--no-cache handle passed, not caching data.")
    except metadoc.InvalidXMLResponseError, ir:
        logging.error("Server returned invalid receipt for \"%s\" data." %
                        element_tag)
        if cache_data:
            logging.info("Caching data for \"%s\"." % element_tag)
            Cacher(element_tag, md)
        else:
            logging.warning("--no-cache handle passed, not caching data.")
    except metadoc.NotAllAcceptedError, nar:
        logging.error("Not all elements accepted for \"%s\" data." % 
                        element_tag)
        sys.stderr.write("Not all elements were accepted by the server.\n")
        sys.stderr.write("Check MetaDoc Client log file for more information.")
        if cache_data:
            logging.info("Caching data for \"%s\"." % element_tag)
            Cacher(element_tag, md)
        else:
            logging.warning("--no-cache handle passed, not caching data.")

def date_to_rfc3339(date):
    """ Converts a datetime.datetime object or time.time() to RFC3339 string. 
    
    """
    if isinstance(date, float) or isinstance(date, int):
        date = datetime.datetime.fromtimestamp(date)
    if not isinstance(date, datetime.datetime):
        return False
    date_str = "%Y-%m-%dT%H:%M:%S"
    if date.tzinfo is not None:
        timedelta = (date.dst() or date.utcoffset())
        timedelta = timedelta.days * 86400 + timedelta.seconds
    else:
        it = time.mktime(date.timetuple())
        if time.localtime(it).tm_isdst:
            timedelta = -time.altzone
        else:
            timedelta = -time.timezone
    zone_prefix = "-"
    if timedelta >= 0:
        zone_prefix = "+"
    offset = "%s%02d:%02d" % (zone_prefix, abs(timedelta/3600), abs(timedelta%3600/60))
    return "%s%s" % (date.strftime(date_str), offset)

def rfc3339_to_date(date_str):
    """ Converts a string to datetime.datetime object if string is a valid
    RFC3339 date.

    Returns False for any string that is not valid RFC3339.
    
    """
    rfc3339_match = r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:([+]|[-])(\d{2}):(\d{2})|(Z))$"
    match = re.match(rfc3339_match, date_str.strip())
    if match is None:
        return False
    try:
        dt_obj = datetime.datetime(
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
            int(match.group(4)),
            int(match.group(5)),
            int(match.group(6)),
            )
    except ValueError:
        # If any values outside allowed range (e.g. month 15), a ValueError
        # is raised by datetime.datetime() and we have an invalid date.
        return False
    if match.group(7) is not None and match.group(8) is not None \
        and match.group(9) is not None:
        if int(match.group(8))*60+int(match.group(9)) >= 1439:
            return False
    if match.group(10) is not None and match.group(10) != "Z":
        return False
        
    return dt_obj

def check_version(server_version):
    """ Checks whether server and client versions are the same. 

    Stops program execution on different major versions, logs critical error.
    Logs warning on different minor versions.
    Logs debug info on different bugfix versions.

    """
    client_version = version.__version__
    (cmajor, cminor, cbug) = client_version.split(".")
    (smajor, sminor, sbug) = server_version.split(".")
    if cmajor != smajor:
        logging.critical(("Client has different major version from server. "
                "Server version: %s. Client version: %s.") % 
                (server_version, client_version))
        sys.stderr.write(("Client has different major version from server. \n"
                "Server version: %s. Client version: %s.\n"
                "Terminating MetaDoc Client.") %
                (server_version, client_version))
        sys.exit(2)
    elif cminor != sminor:
        logging.warning(("Client has different minor version from server. "
                "Server version: %s. Client version: %s.") % 
                (server_version, client_version))
    elif cbug != sbug:
        logging.debug(("Client has different bugfix version from server. "
                "Server version: %s. Client version: %s.") % 
                (server_version, client_version))

def dtd_validate(xmldoc):
    """Validates the XML document against the MetaDoc DTD.

    If lxml is unavailable, the function will not be able to do DTD 
    validation. Will log an error message and return no errors so that 
    the script can proceed.

    @param xmldoc: XML document
    @type xmldoc: str
    @return: list of DTD validation errors.

    """
    if lxml:
        SCRIPT_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
        dtd_file = os.path.join(SCRIPT_PATH, "MetaDoc.dtd")
        dtd = etree.DTD(dtd_file)
        valid = dtd.validate(xmldoc)
        if valid:
            return []
        else:
            ret = []
            for error in dtd.error_log.filter_from_errors():
                ret.append(error)
            return ret
    else:
        logging.warning(("Could not load lxml python library, "
            "unable to do XML Validation."))
        return []
