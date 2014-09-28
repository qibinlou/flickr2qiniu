import qiniu.conf
import qiniu.rs
import qiniu.io
import os


class QiniuUploader(object):
    """Qiniu Uploader to upload flickr images"""
    def __init__(self, opts):
        self.opts = opts
        qiniu.conf.ACCESS_KEY = opts["ak"]
        qiniu.conf.SECRET_KEY = opts["sk"]

    def upload_images(self):
        policy = qiniu.rs.PutPolicy(self.opts["bucket"])
        uptoken = policy.token()
        dir = 'tmp'
        files = os.listdir(dir)
        for file in files:
            if not file.endswith(".jpg"):
                continue

            ret, err = qiniu.io.put_file(uptoken, file, dir + "/" + file)
            if err is not None:
                print "err", err
            else:
                print "success", ret



    def upload_flickr_json(self):
        policy = qiniu.rs.PutPolicy(self.opts["bucket"])
        uptoken = policy.token()
        dir = 'tmp'
        files = os.listdir(dir)
        for file in files:
            if not file.endswith(".json"):
                continue
            ret, err = qiniu.rs.Client().delete(self.opts["bucket"], file)
            ret, err = qiniu.io.put_file(uptoken, file, dir + "/" + file)
            if err is not None:
                print "err", err
            else:
                print "success", ret

    def start(self):
        # self.upload_images()
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
