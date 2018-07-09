# -*- coding: utf8 -*-
"""
auto_groupfolder.py

Description : Librairie to interact with Nextcloud Group folders.

App groupfolders : https://github.com/nextcloud/groupfolders
"""
__author__ = "Alexandre BRIT (@britaxx)"
__maintainer__ = "Alexandre BRIT"

import urllib3
import json
import logging
import certifi
import xml.etree.ElementTree as ET

# Logging
formatter = logging.Formatter(
    "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

console = logging.StreamHandler()
console.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(console)

try:
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass

_http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where())
base_url = 'https://nextcloud.example.com'
base_uri = '/apps/groupfolders/folders'


def _make_request(url, method='GET', data={}):
    '''
        Make request
    '''
    headers = urllib3.util.make_headers(
        basic_auth='ADMIN:PASSWORD')
    headers['OCS-APIRequest'] = 'true'
    r = _http.request(method, url, fields=data, headers=headers)
    return r.data


def _get_mount_point(id):
    '''
        Get groupfolder
        ret : element
    '''
    data = _get_all_mount_point()
    for element in data:
        if element.get('id') == str(id):
            return element
    return {}


def _get_all_mount_point():
    '''
        List all groupfolders
        ret :
                [{
                'id': XXX,
                'mount_point' : XXXx
                }, ...]
    '''
    data = _make_request(base_url + base_uri)
    root = ET.fromstring(data)

    parse_resp = ET.fromstring(data)
    meta = parse_resp.find('meta')
    status = meta.find('status').text
    if status != 'ok':
        logger.error('Error, when list all groups folders')
        return False
    result = []
    #root = xml.getroot()
    for child in root.iter("element"):
        group_set = []
        for groups in child.find('groups'):
            for i in groups.iter():
                group_set.append(i.tag)
        tmp = {
            'id': child.find('id').text,
            'mount_point': child.find('mount_point').text,
            'groups': group_set
        }
        result.append(tmp)
    return result


def _create_mount_point(element):
    '''
        Create groupfolders
        element : groupfolder {'mount_point': 'XXX'}
        ret : element or  False
    '''
    folder_name = element.get('mount_point', None)
    if not folder_name:
        logger.error('Error, element doesn\'t have mount_point')
        return False
    value = {'mountpoint': folder_name}
    data = _make_request(base_url + base_uri, method='POST', data=value)

    parse_resp = ET.fromstring(data)
    meta = parse_resp.find('meta')
    data = parse_resp.find('data')
    status = meta.find('status').text
    if status != 'ok':
        logger.error('Error, when creating folder {0}'.format(folder_name))
        return False

    id = data.find('id').text
    result = _get_mount_point(id)
    logger.info('Create mount_point {0}'.format(result))

    # Set default quota to 1Go
    _set_quota_mount_point(element, 1024 * 1024 * 1024)

    return result


def _delete_mount_point(element):
    '''
        Delete groupfolders
        element : groupfolder {'mount_point': 'XXX', 'id': 19}
        ret : True or Flase
    '''
    id = str(element.get('id', None))
    if not id.isnumeric():
        return False
    data = _make_request(base_url + base_uri + '/' + id, method='DELETE')
    logger.info('Delete mount_point {0} with id {1}'.format(
        element.get('mount_point'), id))
    return True


def _set_quota_mount_point(element, quota):
    '''
        Set Quota (in octet) on groupfolder
        ret : True or False
    '''
    id = str(element.get('id', None))
    if not id.isnumeric():
        return False
    url = base_url + base_uri + '/' + id + '/quota'
    value = {'quota': quota}
    data = _make_request(url, method='POST', data=value)

    parse_resp = ET.fromstring(data)
    meta = parse_resp.find('meta')
    status = meta.find('status').text
    if status == 'ok':
        return True
    folder_name = element.get('mount_point', None)
    logger.error('Error, when set quota on folder {0}'.format(folder_name))
    return False


def _set_group_mount_point(element, group):
    '''
        Set Groups permission on groupfolder
        var :
            element == group folder
            groups == Group's name as string
        ret : True or False
    '''
    id = str(element.get('id', None))
    if not id.isnumeric():
        return False

    url = base_url + base_uri + '/' + id + '/groups'
    value = {'group': str(group)}
    data = _make_request(url, method='POST', data=value)

    parse_resp = ET.fromstring(data)
    meta = parse_resp.find('meta')
    status = meta.find('status').text
    if status == 'ok':
        return True
    folder_name = element.get('mount_point', None)
    logger.error('Error, when try to set permission on folder {0} with groups {1}'.format(
        folder_name, str(group)))
    return False


def _delete_group_mount_point(element, group):
    '''
        Delete Group permission on groupfolder
        This function delete all group.
        ret : True or False
    '''
    id = str(element.get('id', None))
    if not id.isnumeric():
        return False

    url = base_url + base_uri + '/' + id + '/groups/' + group
    data = _make_request(url, method='DELETE')

    parse_resp = ET.fromstring(data)
    meta = parse_resp.find('meta')
    status = meta.find('status').text
    if status == 'ok':
        return True
    folder_name = element.get('mount_point', None)
    logger.error('Error, when try to delete permission on folder {0}'.format(
        folder_name, groups))
    return False


def _set_permission_mount_point():
    # Don't need for the moment
    return
