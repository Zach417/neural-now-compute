import caffe
import parseutils as pu
from PIL import Image
from StringIO import StringIO

class Preprocessor(object):
    def __init__(self, net, transformer, input):
        self.net = net
        self.transformer = transformer
        self.input = input

    def resize(self, size):
        im = Image.new('RGB', size)
        im.putdata(self.input)
        imr = im.resize(size, resample=Image.BILINEAR)
        fh_im = StringIO()
        imr.save(fh_im, format='JPEG')
        fh_im.seek(0)
        img_data_rs = bytearray(fh_im.read())
        return caffe.io.load_image(StringIO(img_data_rs))

    def crop(self):
        H, W, _ = self.input.shape
        _, _, h, w = self.net.blobs['data'].data.shape
        h_off = max((H - h) / 2, 0)
        w_off = max((W - w) / 2, 0)
        return self.input[h_off:h_off + h, w_off:w_off + w, :]

    def preprocess(self, steps):
        # execute steps
        for x in range(len(steps)):
            step = steps[x]

            # get params from step
            params = []
            for y in range(len(step["parameters"])):
                param = step["parameters"][y]
                value = pu.get_param_value(param)
                params.append(value)

            # execute step
            method = getattr(self, step["method"])
            self.input = method(*params)

        self.input = self.transformer.preprocess('data', self.input)
        self.input.shape = (1,) + self.input.shape
        return self.input

