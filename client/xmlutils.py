import logging
import os
import sys

# lxml import
lxml = True
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree
    from xml.parsers.expat import ExpatError
    lxml = False

def element_from_string(data):
    if lxml:
        try:
            data = etree.fromstring(data)
        except etree.XMLSyntaxError, e:
            logging.error("Invalid XML data. Error: %s" % e)
            return False
    else:
        try:
            data = etree.fromstring(data)
        except ExpatError, e:
            logging.error("Invalid XML data. Error: %s" % e)
            return False
    return data

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
