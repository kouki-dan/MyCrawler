

import urllib.request
import xml.dom.minidom
import re

class YoutubeCrawler(object):
  def __init__(self, first_videoids):
    self.first_videoids = first_videoids
    self.base_url = "http://gdata.youtube.com/feeds/api/videos/{}"

  def crawl(self, depth):
    pass
  def _fetch_videodata__from_videoid(self, videoid):
    """
    >>> crawler = YoutubeCrawler([])
    >>> crawler._fetch_videodata__from_videoid("6bM5SzQFpZQ")
    {...}
    """
    
    videodata_url = self.base_url.format(videoid)
    video_info_xml = urllib.request.urlopen(videodata_url).read()
    video_info_doc = xml.dom.minidom.parseString(video_info_xml)
    video_comment_xml = urllib.request.urlopen(videodata_url+"/comments").read()
    video_comment_doc = xml.dom.minidom.parseString(video_comment_xml)

    video_info = {}
    video_info["url"] = video_info_doc.getElementsByTagName("media:player")[0].getAttribute("url")
    video_info["title"] = video_info_doc.getElementsByTagName("title")[0].childNodes[0].data

    video_info["comments"] = []
    for comment in video_comment_doc.getElementsByTagName("content"):
      video_info["comments"].append(comment.childNodes[0].data)

    video_info["related_videoids"] = self._fetch_related_videoids(videoid)
    return video_info

  def _fetch_related_videoids(self, from_videoid):
    related_videoids_container = []
    related_videodata = self.base_url.format(from_videoid) + "/related"
    related_videos_xml = urllib.request.urlopen(related_videodata).read()
    related_videos_doc = xml.dom.minidom.parseString(related_videos_xml)
    related_videos = related_videos_doc.getElementsByTagName("entry")
    for related_video in related_videos:
      url = related_video.getElementsByTagName("id")[0].childNodes[0].data
      related_videoid = self._get_videoid_from_url(url)
      related_videoids_container.append(related_videoid)
    return related_videoids_container

  def _get_videoid_from_url(self, url):
    """
    >>> crawler = YoutubeCrawler([])
    >>> crawler._get_videoid_from_url("http://gdata.youtube.com/feeds/api/videos/6bM5SzQFpZQ")
    '6bM5SzQFpZQ'
    """
    videoid_re = re.search("/([\w]*)$", url)
    videoid = videoid_re.group(1)
    return videoid

if __name__ == "__main__":
  import doctest
  doctest.testmod(
      optionflags = (doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
  )


