# -*- coding: utf-8 -*-

from subprocess import call
from builder import settings
from builder.utils import popen, gettext as _
import logging
import os

def abuild_path(pkgname):
    return os.path.join(settings.ABUILD_PATH, pkgname, 'ABUILD')


def print_graph(packages, fname, highlight=[]):
    data = ["digraph G {"]
    data.extend(['\t"{0}" [fontcolor = red, color = red];'.format(pkgname) \
            for pkgname in highlight])
    for package in packages:
        data.extend(['\t"{0}" -> "{1}";'.format(d, pkgname) \
                        for d in package.deps])
    data.append("}")
    data = '\n'.join(data)
    with open('{0}.dot'.format(fname), 'w') as f:
        f.write(data)
    call(["dot", "-Tpng", "-O{0}.dot".format(fname)])
    return data;


def is_blacklist(p):
    return p in settings.BLACKLIST_PACKAGES


def get_multipkg_set(pkgname):
    abuild = abuild_path(pkgname)
    if not os.path.exists(abuild):
        logging.debug(_("GET_ERROR: No such file %s"), abuild)
        return [pkgname];

    data, error = popen("./get_subpackages.sh", abuild)
    return filter(None, data.splitlines())



def get_deps(pkgname):
    """This function called when build_deps were not specified.
This means that package depends only on generic build-essential packages.
ATM, this is a hack. The code below that was commented out were designed
to get package deps from online repository. At this time, we should avoid it.
"""
    logging.debug(_("Build deps for package %s were not specified. It is ABUILD problem probably"))
    return [];
    #$ret = array('glibc-solibs', 'gcc');
    #~ debug("API CALL $pkgname");
    #~ $handle = popen("wget -qO- 'http://api.agilialinux.ru/get_dep.php?n=" . urlencode($pkgname) . "'", 'r');
    #~ $data = fread($handle, 65536);
    #~ debug("RAW API DATA ($pkgname): $data");
    #~ pclose($handle);
    #~ if (trim(preg_replace("/\n/", '', $data))=="") return array();
    #~ $deps = explode("\n", trim($data));
    #~ $ret = array();
    #~ foreach($deps as $d) {
        #~ if (!isBlacklist($d)) $ret[] = $d;
    #~ }
    #~ return $ret;


def print_array(array, log_callback):
    """Prints array elements (used for output results)"""
    if not array:
        logging.debug(_('ZERO-LENGTH ARRAY'))
        return

    array = ["{0}{1}".format(
        '[{0}] '.format(number) if settings.NUMERATE else '',
        item) for number, item in enumerate(array)]
    log_callback('\n'.join(array))



def filter_dupes(array):
    """Filter dupes in array. Removes 2nd and others entries of each dupe items"""
    return list(set(array))