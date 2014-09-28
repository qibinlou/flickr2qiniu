import urllib, urllib2
import json
import os
import datetime
import time

class FlickrReader(object):
    """docstring for FlickrReader"""
    def __init__(self, arg):
        super(FlickrReader, self).__init__()
        self.url = arg

    def get_data(self):
        c = urllib.urlopen(self.url)
        content = c.readlines()
        return ''.join(content)

    def parse_data(self, content):
        content = content[15: -1]
        items = json.loads(content)
        # print items
        return items

    def get_items(self, data):
        source = data["items"]
        items = []
        for item in source:
            items.append(item["media"]["m"])
        print items
        return items, source

    def _get_name_from_url(self, url):
        return url.split('/')[-1]

    def save_images_to_local(self, dir, urlList):
        import shutil

        if os.path.isdir(dir) or os.path.exists(dir):
            shutil.rmtree(dir)
        time.sleep(1)
        os.mkdir(dir)
        prefix = time.strftime('%Y%m%d',time.localtime(time.time())) + "_"
        for url in urlList:
            filename = prefix + self._get_name_from_url(url)
            try:
                urllib.urlretrieve(url, dir + "/" + filename)
            except:
                print filename, "not found"
        print "images all save to local files!"

    def save_desc_to_local(self, dir, source):
        items = []
        host = ''  # Your qiniu domain. e.g. http://louqibin.qiniudn.com/
        prefix = host + time.strftime('%Y%m%d',time.localtime(time.time())) + "_"
        for s in source:
            item = {}
            item["title"] = s["title"]
            item["link"] = s["link"]
            item["date"] = s["date_taken"]
            item["url"] = prefix + self._get_name_from_url(s["media"]["m"])
            items.append(item)
        with open(dir + "/" + "flickr.json", "w") as fout:
            fout.write(json.dumps(items))
        print "flickr.json generated"


    def run(self):
        print "running..."
        content = self.get_data()
        items = self.parse_data(content)
        items, source = self.get_items(items)
        self.save_images_to_local('tmp', items)
        self.save_desc_to_local('tmp', source)



if __name__ == "__main__":
    uid = ""  # Your flickr id. eg. 99791876@N07
    url = "http://api.flickr.com/services/feeds/photos_public.gne?id=%s&format=json" % (uid)  # Format can be json, xml, plain text, rss, etc.
    reader = FlickrReader(url)
    reader.run()