import caffe
import parseutils as pu

def get_transformer(net, steps):
    options = {'data': net.blobs['data'].data.shape}
    transformer = caffe.io.Transformer(options)

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
        method = getattr(transformer, step["method"])
        method('data', *params)

    return transformer
