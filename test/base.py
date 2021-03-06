#coding:utf-8
import constant
import os, sys
sys.path.insert(0, constant.PROJECT_DIR)
import time
import logging
import tornado.web
from tornado.testing import AsyncHTTPTestCase
import server
server.logger = logging.getLogger('Robot')
stream_hd = logging.StreamHandler()
stream_hd.setFormatter(server.log_format)
server.logger.addHandler(stream_hd)
server.logger.setLevel(logging.WARNING)

from urllib import urlencode
from tornado.escape import utf8
from tornado.httpclient import HTTPRequest as TornadoHTTPRequest
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.escape import json_decode
import tornado.ioloop
from service.base import HTTPRequest
from lib import base_util
import copy
import tornado.gen
import urllib
import uuid

from database.models import Novel, Chapter

class BaseTestCase(AsyncHTTPTestCase):
    '测试基类'
    
    def setUp(self):
        
        AsyncHTTPTestCase.setUp(self)
        Novel.objects.all().delete()
        Chapter.objects.all().delete()
    
    def get_app(self):

        return server.Application()
    
    def get_new_ioloop(self):
        
        return tornado.ioloop.IOLoop.instance()
    
    def get_http_client(self):
        
        return SimpleAsyncHTTPClient(self.io_loop)
    
    def common_internal_request(self, path, params={}, body=None, headers={}, method='GET', timeout=10):
        '通用的内部接口请求'
        
        _params = copy.deepcopy(params)
        _headers = copy.deepcopy(headers)
        url = '%s?%s' %(self.get_url(path), urllib.urlencode({'pid': 'testcase', 'guid': 'test'}))
        request = HTTPRequest(url, params=_params, headers=_headers, body=body, method=method, request_timeout=timeout)
        self.http_client.fetch(request, self.stop)
        response = self.wait(timeout=timeout)
        return response
    
    def common_json_request(self, path, params={}, body=None, headers={}, method='GET', timeout=10):
        'response为json的请求'
        
        response = self.common_internal_request(path, params=params, body=body, headers=headers, method=method, timeout=timeout)
        self.assertEqual(response.code, 200)
        return json_decode(response.body)

    def pprint(self, data):
        base_util.pprint(data)
    
    def add_novel(self, name):
        '添加一个novel'

        id = uuid.uuid4().hex
        Novel.objects.create(**{
            'id': id,
            'name': name, 
            'createtime': int(time.time()),
            'status': 0
        })
        return Novel.objects.get(id=id)
    
    def add_chapter(self, novel, title, pageid):
        '新增一个chapter'

        id = uuid.uuid4().hex
        Chapter.objects.create(**{
            'id': id,
            'title': title,
            'pageid': pageid,
            'novel': novel,
        })
        return Chapter.objects.get(id=id)

