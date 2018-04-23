import numpy as np
import parse_data



class generator:

    def __init__(self, x, y):
        x = x
        y = y


    def gen_mem(self, batch_size):
        """
        generator for training on gpu
        :param batch_size:
        :return:
        """
        while(True):
            batch_x = []
            batch_y = []
            for i in range(batch_size):
                # get the random index
                i = np.random.randint(0, len(self.x))
                # add the example
                batch_x.append( np.asarray(self.x[i]))
                batch_y.append(np.asarray(self.y[i]))
            yield np.array(batch_x), np.array(batch_y)

