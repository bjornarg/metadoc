#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#            mapi.py is part of MetaDoc (Client).
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
"""Runs the synchronization procedure

Description
===========
    Information sent and recieved depends on handles passed to mapi.py.
    If mapi.py is run without any handles it will attempt to send any cached 
    information to the server.

Usage
=====
    -h, --help              Displays this help message
    -v, --verbose           Verbose mode, outputs loads of stuff
    -q, --quiet             Quiet mode, outputs nothing except
                            critical errors
    -e                      Send event data
    -c                      Send config data
    -s                      Send software data
    -t                      Send SPODTest data
    -u                      Fetch user data
    -a                      Fetch allocation data
    -p                      Fetch project data
    -l <log level>          Sets log level, availible levels are:
    --loglevel=<log level>  debug, info, warning, error, critical
    -n, --no-cache          Will not send any cached data.
    --dry-run               Does a dry run, not sending or fetching any data.
                            Run with verbose to see input and output that would 
                            be sent.
    --all                   Sends and fetches all data, equal to -ecsuap.
    --send-all              Sends all data, equal to -ecs.
    --fetch-all             Fetches all data, equal to -uap.

"""
lxml = False

import ConfigParser
import logging
import logging.handlers
import sys
import os
import getopt
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
    from xml.parsers.expat import ExpatError
else:
    lxml = True
import urllib2
import StringIO
import datetime

import metahttp 
import metadoc
import utils
import xmlutils
from metaconfig import write_sample_config, test_config, bool_conf_value
from metadoc import MetaDoc
from metaelement import MetaElement
from cacher import Cacher

# Classes that send information to server
from events.definition import Events
from configuration.definition import Configuration
from software.definition import Software
from spodtest.definition import SPODTest

# Classes that retrieve information from server
from allocations.definition import Allocations
from users.definition import Users
from projects.definition import Projects



def get_element_processor(element, send_cache, verbose, dryrun):
    """Gets an instance of element that contains cached data, depending on 
    arguments passed.

    Will skip any cached data if send_cache is False or dryrun is True.

    @param element: Element class that should be fetched.
    @type element: L{MetaElement} sub class.
    @param send_cache: Indicates whether cache should be included.
    @type send_cache: bool
    @param verbose: Indicates whether or not the script runs in verbose mode.
    @type verbose: bool
    @param dryrun: Indicates whether the script is doing a dry run.
    @type dryrun: bool
    @return: L{MetaElement} sub class. The sub class is given by the element 
            parameter.

    """
    if dryrun or not send_cache:
        return element()
    if send_cache:
        c = Cacher(element.xml_tag_name)
        cached_data = c.get_cache()
        if cached_data is not None:
            if element.resend_cache:
                element_processor = element.from_xml_element(cached_data, 
                                                                element)
            else:
                logging.info(("Found cached data for \"%s\", but element "
                    "type declares not to resend this cache. "
                    "Removing cache.") % element.xml_tag_name)
                c.remove_cache()
                element_processor = element()
            if element_processor is None:
                logging.error(("Found cached data for \"%s\", but unable to "
                    "load. Check file \"%s\" for possible errors. "
                    "Continuing without cached data") % 
                                (element.xml_tag_name, c.file_path))
                element_processor = element()
            else:
                # We have successfully loaded the cached data.
                if element.resend_cache:
                    logging.debug(("Succesfully loaded cache for \"%s\", "
                        "removing cached file \"%s\".") % 
                        (element.xml_tag_name, c.file_path))
                    c.remove_cache()
        else:
            logging.debug(("Found no cached data for \"%s\".") % 
                            element.xml_tag_name)
            element_processor = element()
    return element_processor

def send_element(element, conf, send_cache, dryrun, verbose, cache_only):
    """Attempts to gather and send information defined by element to server.

    If send_cache is True or dryrun is False, cache will be ignored.
    If cache_only is True, only cache is checked and no new data is gathered.


    @param element: Element class that should be fetched.
    @type element: L{MetaElement} sub class.
    @param conf: Configuration dictionary.
    @type conf: dict
    @param send_cache: Indicates whether cache should be included.
    @type send_cache: bool
    @param dryrun: Indicates whether the script is doing a dry run.
    @type dryrun: bool
    @param verbose: Indicates whether or not the script runs in verbose mode.
    @type verbose: bool
    @param cache_only: Indicates whether to send only cache for this element.
    @type cache_only: bool

    """
    if dryrun and cache_only:
        # We're doing a dry run and we've reached the cached items
        return
    m = MetaDoc(conf.get("site_name"))
    element_processor = get_element_processor(element, send_cache, 
                                                verbose, dryrun)
    if not cache_only:
        # If we're doing cache only, we've reached the possible_send_elements
        # loop and do not want or need to remove elements from it anymore.
        site_element = element.site_handler()
        site_element.populate()
        element_processor.add_elements(site_element.fetch())
    m.reg_meta_element(element_processor)
    # Build URL
    url = "%s%s" % (conf['host'], element.url)
    if bool_conf_value(conf.get('trailing_slash',"")):
        url = "%s/" % url

    # Check to see if there is any content to transfer in the MetaDoc.
    if m.has_content():
        if verbose:
            print "-" * 70
            print "Connecting to host: %s" % url
            print "Using key: %s" % conf['key']
            print "Using certificate: %s" % conf['cert']
            print "-" * 70
            print "Sent data:\n%s" % ("-" * 70)
            print m.get_xml(pretty=True)

        if not dryrun:
            server_response = utils.send_document(url, 
                conf['key'], 
                conf['cert'],
                m)
            if server_response is False:
                if not send_cache:
                    logging.warning("Could not send data to server, "
                        "but running with --no-cache, so data was not cached.")
                else:
                    Cacher(element.xml_tag_name, m)
            else:
                if verbose:
                    print "%s\nRecieved data:\n%s" % ("-" * 70, "-" * 70)
                    print server_response
                    print "-" * 70
                utils.check_response(element.xml_tag_name, 
                                        m, 
                                        server_response,
                                        send_cache)
    else:
        if verbose and not cache_only:
            print "No data to send for \"%s\"." % element.xml_tag_name
        logging.info(("No data to send for \"%s\".") % element.xml_tag_name)

def fetch_element(element, conf, verbose):
    url = "%s%s" % (conf['host'], element.url)
    if bool_conf_value(conf.get('trailing_slash',"")):
        url = "%s/" % url
    if verbose:
        print "-" * 70
        print "Connecting to host: %s" % url
        print "Using key: %s" % conf['key']
        print "Using certificate: %s" % conf['cert']
        print "-" * 70
    server_response = utils.send_document(url, conf['key'], conf['cert'])
    if server_response is False:
        sys.stderr.write("Unable to fetch data from \"%s\".\n" %
                            url)
        sys.stderr.write("See log for more information.\n")
    else:
        if verbose:
            print "%s\nRecieved data:\n%s" % ("-" * 70, "-" * 70)
            print server_response
        data = xmlutils.element_from_string(server_response)
        if data is False:
            sys.stderr.write(("Got response from server at url \"%s\", "
                            "but unable to parse. \nError message: %s\n") % 
                            (url, e))
        else:
            # Check for valid according to DTD:
            utils.check_version(data.attrib.get("version"))
            dtd_validation = xmlutils.dtd_validate(data)
            if len(dtd_validation) == 0:
                logging.debug(("Data returned from \"%s\" validated to "
                                "DTD.") % url)
                found_elements = data.findall(
                                element.xml_tag_name
                                )
                sub_elements = []
                for found_element in found_elements:
                    sub_elements.append(MetaElement.from_xml_element(
                                        found_element, element)
                                        )
                element.update_handler(sub_elements).process()
            else:
                logging.error(("XML recieved for \"%s\" did not "
                            "contain valid XML according to DTD.") % 
                            element.xml_tag_name)
                sys.stderr.write(("Received XML document from server "
                            "on url \"%s\", but did not validate "
                            "against DTD.\n") % url)
                sys.stderr.write("Logging with \"debug\" will show "
                            "validation errors.\n")
                dtd_errors = ""
                for error in dtd_validation:
                    dtd_errors = "%s\n%s" % (dtd_errors, error)
                logging.debug("XML DTD errors: %s" % dtd_errors)


def main():
    """Main execution. """
    optstr = "hvqectaspunl:"
    optlist = ['help', 'dry-run', 'loglevel=', 'no-cache', 
                'send-all', 'fetch-all', 'all']
    SCRIPT_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
    # Default settings
    # Will be altered depending on passed options
    verbose = False
    dryrun = False
    send_cache = True
    # These lists contain all elements that might be sent or fetched.
    possible_send_elements = [Events, Configuration, Software,SPODTest]
    possible_fetch_elements = [Allocations, Users, Projects,]
    # Information to send
    send_elements = []
    # Fetch information from server
    fetch_elements = []

    LOG_LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    log_level = logging.WARNING

    try:
        opts, args = getopt.getopt(sys.argv[1:], optstr, optlist)
    except getopt.GetoptError, goe:
        print str(goe)
        print __doc__
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print __doc__
            sys.exit()
        elif opt == '-v':
            verbose = True
        elif opt == '-q':
            a = StringIO.StringIO()
            sys.stdout = a
        elif opt == '-e':
            send_elements.append(Events)
        elif opt == '-c':
            send_elements.append(Configuration)
        elif opt == '-s':
            send_elements.append(Software)
        elif opt == '-t':
            send_elements.append(SPODTest)
        elif opt == '-u':
            fetch_elements.append(Users)
        elif opt == '-a':
            fetch_elements.append(Allocations)
        elif opt == '-p':
            fetch_elements.append(Projects)
        elif opt == '--dry-run':
            dryrun = True
        elif opt in ('-l', '--loglevel'):
            log_level = LOG_LEVELS.get(arg.lower(), logging.WARNING)
        elif opt in ('-n', '--no-cache'):
            send_cache = False
        elif opt == '--send-all':
            send_elements.extend(possible_send_elements)
            possible_send_elements = []
        elif opt  == '--fetch-all':
            fetch_elements.extend(possible_fetch_elements)
            possible_fetch_elements = []
        elif opt == '--all':
            fetch_elements.extend(possible_fetch_elements)
            possible_fetch_elements = []
            send_elements.extend(possible_send_elements)
            possible_send_elements = []

    log_file = datetime.datetime.strftime(datetime.datetime.now(), 
                "/var/log/mapi/metadoc.client.%Y-%m-%d.log")
    # Might get an error due to not having access to log directory.
    try:
        logging.basicConfig(level=log_level, 
            format=LOG_FORMAT,
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=log_file 
            )
    except IOError, ioerr:
        sys.stderr.write(("Unable to open log file for writing, "
            "please check permissions "
            "for \"%s\".\n") % log_file)
        sys.stderr.write("Error message: %s\n" % ioerr)
        sys.exit(2)
    

    conf = ConfigParser.ConfigParser()
    conf.read(os.path.join(SCRIPT_PATH, "metadoc.conf"))
    v = []
    vals = {}
    try:
        v = conf.items("MetaDoc")
    except ConfigParser.NoSectionError as nose:
        print "Need a configuration-file. "
        print "A sample file has been created for you in metadoc.conf"
        print "Please edit this file carefully and re-run the program."
        logging.info("Creating default configuration file.")
        write_sample_config()
        return

    vals = dict(v)

    if not test_config(vals):
        # test_config() prints/logs any errors
        return

    # ready for main processing.
    logging.info("Running mapi.py with handles %s." % " ".join(sys.argv[1:]))

    for element in send_elements:
        if element in possible_send_elements:
            possible_send_elements.remove(element)
        send_element(element, vals, send_cache, dryrun, verbose, False)

    # Checking if we have any cached items that should be sent
    for element in possible_send_elements:
        send_element(element, vals, send_cache, dryrun, verbose, True)
        

    if not dryrun:
        for element in fetch_elements:
            fetch_element(element, vals, verbose)
    else:
        logging.info("Doing dryrun, wont send any data")

if __name__ == "__main__":
    main()
