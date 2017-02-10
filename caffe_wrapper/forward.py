#!/usr/bin/env python
import caffe
import json
import transformer as t
from preprocessor import Preprocessor
from PIL import Image

def transform_input(input, type, size):
    if (type == "image"):
        image_data = []
        if (len(input) != size[0]*size[1]*size[2]):
            return image_data

        for x in range(len(input) - 3):
            if ((x + 1) % 3) == 0:
                image_data.append((input[x], input[x + 1], input[x + 2]))

        image = Image.new('RGB', (size[0], size[1]))
        image.putdata(image_data)
        return image.getdata()
    else:
        return input

def compute(input, transformer, net):
    input_name = net.inputs[0]
    all_outputs = net.forward_all(blobs=net.outputs, **{input_name: input})
    return all_outputs[net.outputs[0]][0].astype(float)

def run(name, input, type, size):
    # Pre-load caffe model
    model_def = '/home/ec2-user/server/models/%s/deploy.prototxt' % name
    pretrained_model = '/home/ec2-user/server/models/%s/deploy.caffemodel' % name
    net = caffe.Net(model_def, pretrained_model, caffe.TEST)

    # Transform input
    input = transform_input(input, type, size)

    # Generate transformer from data
    net_steps_file = open('/home/ec2-user/server/caffe_wrapper/models.json')
    net_steps_json = json.load(net_steps_file)
    transformer_steps = net_steps_json["transformer"]
    transformer = t.get_transformer(net, transformer_steps)

    # Preprocess input
    preprocess_steps = net_steps_json["preprocess"]
    preprocessor = Preprocessor(net, transformer, input)
    input = preprocessor.preprocess(preprocess_steps)

    # Forward propogate and return
    return compute(input, transformer, net)
