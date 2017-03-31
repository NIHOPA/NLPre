
def pipeline_function(func):

    class joint(object):

        def __init__(self, *args, **kwargs):
            # Set any function arguments for calling
            self.kwargs = kwargs

        def __call__(self, x):
            return func(x, **self.kwargs)

    return joint
