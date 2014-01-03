# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
from __future__ import absolute_import
import re
import json

from svtplay_dl.service import Service
from svtplay_dl.utils import get_http_data, subtitle_tt
from svtplay_dl.fetcher.rtmp import download_rtmp
from svtplay_dl.fetcher.hls import download_hls

class Urplay(Service):
    supported_domains = ['urplay.se', 'ur.se']

    def get(self, options, url):
        data = get_http_data(url)
        data = re.search(r"urPlayer.init\((.*)\);", data)
        match = re.search(r"urPlayer.init\((.*)\);", data)
        if not match:
            log.error("Can't find json info")
            sys.exit(2)
        data = match.group(1)
        jsondata = json.loads(data)
        subtitle = jsondata["subtitles"].split(",")[0]
        basedomain = jsondata["streaming_config"]["streamer"]["redirect"]
        http = "http://%s/%s" % (basedomain, jsondata["file_html5"])
        #hds = "%s%s" % (http, jsondata["streaming_config"]["http_streaming"]["hds_file"])
        hls = "%s%s" % (http, jsondata["streaming_config"]["http_streaming"]["hls_file"])
        rtmp = "rtmp://%s/%s" % (basedomain, jsondata["streaming_config"]["rtmp"]["application"])
        path = "mp%s:%s" % (jsondata["file_flash"][-1], jsondata["file_flash"])
        options.other = "-v -a %s -y %s" % (jsondata["streaming_config"]["rtmp"]["application"], path)
        if options.hls:
            download_hls(options, hls, http)
        else:
            download_rtmp(options, rtmp)
        if options.subtitle:
            if options.output != "-":
                data = get_http_data(subtitle)
                subtitle_tt(options, data)
