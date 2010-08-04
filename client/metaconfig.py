# -*- coding: utf-8 -*-
#
#            metaconfig.py is part of MetaDoc (Client).
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

import os
import sys
import logging

def write_sample_config():
    """Creates a default configuration file.
    Used if the config file is missing to create a base to work from.

    """
    SCRIPT_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
    f = open(os.path.join(SCRIPT_PATH, "metadoc.conf"), "w")
    f.write("# This is a sample configuration file for MetaDoc\n")
    f.write("# It uses Python's ConfigParser, see\n")
    f.write("#\thttp://docs.python.org/library/configparser.html\n")
    f.write("# for details.\n")
    f.write("\n# The standard MetaDoc section\n")
    f.write("[MetaDoc]\n")
    f.write("host  = https://localhost/metadoc_api/\n")
    f.write("key   = userkey.pem\n")
    f.write("cert  = usercert.pem\n")
    f.write("trailing_slash = True\n")
    f.write("valid = False\n")
    f.write("site_name = SITENAME\n")
    f.write("ca_certs = ca_certs.pem\n")
    f.close()

def test_config(vals):
    """Tests configuration file to see that it contains the necessary 
    information to run the script.

    @param vals: Dictionary of configuration values.
    @type vals: dict
    @return: bool indicating proper configuration.

    """
    if 'valid' in vals:
        if not bool_conf_value(vals['valid'], True):
            print "The config is not valid. "
            print ("You need to explicitly set the "
                    "config-switch 'valid' to 'True'.")
            print "You can also remove the switch completely from the file"
            print ""
            print ("It is included as a fail-safe to stop "
                    "auto-configured programs from running.")
            logging.critical("Configuration file not set to valid. "
                    "Please make sure configuration file is correct and "
                    "set 'valid' to 'True'.")
            return False
    if 'host' not in vals or vals['host'] == "":
        print "Need a valid host. Aborting"
        logging.critical("Configuration file missing 'host'.")
        return False
    if 'cert' not in vals or vals['cert'] == "":
        print "Need path to the certificate to use for AuthN/AuthZ. Aborting"
        logging.critical("Configuration file missing path to certificate.")
        return False
    else:
        if not os.access(vals['cert'], os.R_OK):
            print "cert file is not a file or not readable for user."
            logging.critical("cert file is not a file or not readable "
                        "for user")
            return False
    if 'key' not in vals or vals['key'] == "":
        print "Need path to the privatekey to use for AuthN/AuthZ. Aborting"
        logging.critical("Configuration file missing path to private key.")
        return False
    else:
        if not os.access(vals['key'], os.R_OK):
            print "key file is not a file or not readable for user."
            logging.critical("key file is not a file or not readable "
                        "for user")
            return False
    if 'site_name' not in vals or vals['site_name'] == "":
        print "Missing site name in configuration file. Aborting"
        logging.critical("Configuration file missing site name.")
        return False
    if 'ca_certs' not in vals or vals['ca_certs'] == "":
        print "Missing ca_certs in configuration. Aborting."
        logging.critical("Missing ca_certs in configuration.")
    else:
        if not os.access(vals['ca_certs'], os.R_OK):
            print "ca_certs file is not a file or not readable for user."
            logging.critical("ca_certs file is not a file or not readable "
                        "for user")
            return False
    return True

def bool_conf_value(val, default=False):
    """Attempts to convert a string value from configuration to a boolean.

    @param val: Configuration value
    @type val: str
    @param default: Default return value if unable to properly convert.
    @type default bool
    @return: bool

    """
    if val.lower() in ('true', 'yes'):
        return True
    elif val.lower() in ('false', 'no'):
        return False
    return default
