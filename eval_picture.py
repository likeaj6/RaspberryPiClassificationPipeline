import tensorflow as tf
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# ['tf' or 'keras']
LIBRARY = 'TENSORFLOW'
NUM_CLASSES = 6


def runModel(sess, image, predict):
    start_time = time.time()
    print("Now running predictions...")

    test_pred = sess.run(predict)
    # timing
    print("ML 'runModel': --- %s seconds ---" % (time.time() - start_time))
    print("Preditions complete.")
    print(test_pred)
    return test_pred
