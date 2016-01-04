import os
import sys
from qiniu import *


class QiniuUploader(object):
    """Qiniu Uploader to upload flickr images"""
    def __init__(self, opts):
        self.opts = opts
        self.q = Auth(opts["ak"], opts["sk"])
        self.token = self.q.upload_token(opts["bucket"])
        self.bucket = BucketManager(self.q)

    def upload_images(self):
        dir = 'tmp'
        files = os.listdir(dir)
        for file in files:
            if not file.endswith(".jpg"):
                continue
            ret, err = self.bucket.delete(self.opts["bucket"], file)
            ret, err = put_file(self.token, file, dir + '/' + file)
            if err is not None:
                print >> sys.stderr, "err:", err
            else:
                print "success", ret



    def upload_flickr_json(self):
        dir = 'tmp'
        files = os.listdir(dir)
        for file in files:
            if not file.endswith(".json"):
                continue
            ret, err = self.bucket.delete(self.opts["bucket"], file)
            ret, err = put_file(self.token, file, dir + '/' + file)
            if err is not None:
                print >> sys.stderr, "err!!!:", err
            else:
                print "success", ret

    def start(self):
        self.upload_images()
        self.upload_flickr_json()
        print "all work is done."

if __name__ == '__main__':
    opts = {
        "ak" : "",                  # Your Qiniu ACCESS_KEY
        "sk" : "",                  # Your Qiniu SECRET_KEY
        "bucket" : ""               # Your Qiniu bucket where you want to store your flickr images
    }
    uploader = QiniuUploader(opts)
    uploader.start()
