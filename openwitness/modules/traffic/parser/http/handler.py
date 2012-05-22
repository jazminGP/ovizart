#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import dpkt
import gzip
import StringIO
import os
import tempfile
import urllib2
from lxml.html import fromstring
from openwitness.modules.traffic.parser.tcp.handler import Handler as TcpHandler
from openwitness.modules.traffic.log.logger import Logger

class Handler(TcpHandler):
    def __init__(self):
        super(Handler, self).__init__()
        self.log = Logger("HTTP Protocol Handler", "DEBUG")
        self.log.message("HTTP protocol handler called")

#    def read_http(self, tcp):
#        request = self.check_request(tcp)
#        if request:
#            request_dict = {'method': request.method, 'uri': request.uri, 'headers': request.headers, 'version': request.version}
#            return {'request': request_dict}
#        else:
#            response = self.check_response(tcp)
#            if response:
#                response_dict = {'headers': response.headers, 'status': response.status, 'body': response.body, 'version': response.version}
#                return {'response': response_dict, 'tcp_id': tcp.id}
#            return False
#
#    def check_request(self, tcp):
#        data = tcp.data
#        try:
#            return dpkt.http.Request(data)
#        except dpkt.UnpackError:
#            return False

#    def check_response(self, tcp):
#        data = tcp.data
#        try:
#            return dpkt.http.Response(data)
#        except dpkt.UnpackError:
#            return False
#
#    def get_html(self, response_dict):
#        #response will be the dictionary response created after the read_http runs
#        html = None
#        headers = response_dict['headers']
#        body = response_dict['body']
#        if 'content-encoding' in headers and headers['content-encoding'] == 'gzip':
#            data = StringIO.StringIO(body)
#            gzipper = gzip.GzipFile(fileobj = data)
#            html = gzipper.read()
#        else:
#            html = body
#        return html
#
#    def save_html(self, html, path):
#        html_dir = "/".join([path, "html"])
#        if not os.path.exists(path):
#            os.mkdir(html_dir)
#        html_list = os.listdir(html_dir)
#        if not html_list:
#            stream_name = "0.html"
#        else:
#            # the html names will be under html directory with the increasing order as 0.html, 1.html for each flow
#            names = map(lambda x: int(x.split(".")[0]), html_list)
#            names.sort()
#            stream_name = str(names[-1] + 1) + ".html"
#        stream_path = "/".join([html_dir, stream_name])
#        htmlfile = open(stream_path, 'w')
#        htmlfile.write(html)
#        htmlfile.close()
#        return stream_path
#
#    def get_js(self, path, tcp):
#        # get the path of html file
#        base = os.path.dirname(path)
#        js_dir = "js"
#        js_dir_path = "/".join([base, js_dir])
#        if not os.path.exists(js_dir_path):
#            os.mkdir(js_dir_path)
#        doc = fromstring(path)
#        # first the header part
#        header = doc.header
#        scripts = header.cssselect('script')
#        for script in scripts:
#            # check whether it defines a src
#            items = script.items()
#            if items:
#                #[('src', 'index_files/adnet_async.js'), ('type', 'text/javascript')]
#                # i should do something for these files to, need the requested url
#                js_status = False
#                src_status = False
#                src = None
#                for item in items:
#                    if 'type' in item and 'text/javascript' in item:
#                        js_status = False
#                    if 'src' in item:
#                        src_status = True
#                        src = item[1]
#
#                if js_status and src_status:
#                    file_name = src.split("/")[-1]
#                    url = "/".join([tcp.dst_ip, src])
#                    u = urllib2.urlopen(url)
#                    path = "/".join([js_dir_path, file_name])
#                    localFile = open(path, 'w')
#                    localFile.write(u.read())
#                    localFile.close()
#
#            else:
#                # text between script headers
#                txt = script.text()
#                data = StringIO.StringIO(txt)
#                # create a file and save it
#                tmp = tempfile.NamedTemporaryFile(mode="w+", dir=js_dir_path, delete=False)
#                tmp.write(data)
#                tmp.close()
#
#    def read_http_log(self, path):
#        # first check whether there is an http.log created
#        result = []
#        full_path = "/".join([path, "http.log"])
#        if os.path.exists(full_path):
#            f = open(full_path, "r")
#            for line in f.readlines():
#                if line.startswith("#"):
#                    continue
#                else:
#                    data = line.split()
#                    # src ip, sport, dst ip, dport
#                    result.append(data[2:6])
#        else:
#            return False
#
#        return result

    def read_dat_files(self, path):
        result = []
        files = os.listdir(path)
        for f in files:
            f_path = "/".join([path, f])
            if os.path.isdir(f_path):
                continue
            #contents_192.168.1.5:42825-62.212.84.227:80_orig.dat
            name = f.split("_")
            extension = name[-1].split(".")[-1]
            if extension == "dat":
                communication = name[1].split("-")
                source = communication[0].split(":")
                destination = communication[1].split(":")
                source.extend(destination)
                result.append(source)
            else:
                continue

        return result


    def get_flow_ips(self,path):
        return self.read_dat_files(path)