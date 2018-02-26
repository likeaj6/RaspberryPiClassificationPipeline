import tensorflow as tf
from xception import xception, xception_arg_scope

slim = tf.contrib.slim

def preprocess_for_eval(image, height, width, central_fraction=0.875, scope=None):
    """Prepare one image for evaluation.
    If height and width are specified it would output an image with that size by
    applying resize_bilinear.
    If central_fraction is specified it would cropt the central fraction of the
    input image.
    Args:
    image: 3-D Tensor of image. If dtype is tf.float32 then the range should be
      [0, 1], otherwise it would converted to tf.float32 assuming that the range
      is [0, MAX], where MAX is largest positive representable number for
      int(8/16/32) data type (see `tf.image.convert_image_dtype` for details)
    height: integer
    width: integer
    central_fraction: Optional Float, fraction of the image to crop.
    scope: Optional scope for name_scope.
    Returns:
    3-D float Tensor of prepared image.
    """
    with tf.name_scope(scope, 'eval_image', [image, height, width]):
        if image.dtype != tf.float32:
            image = tf.image.convert_image_dtype(image, dtype=tf.float32)
        # Crop the central region of the image with an area containing 87.5% of
        # the original image.
        if central_fraction:
            image = tf.image.central_crop(image, central_fraction=central_fraction)

        if height and width:
            # Resize the image to the specified height and width.
            image = tf.expand_dims(image, 0)
            image = tf.image.resize_bilinear(image, [height, width],
                                           align_corners=False)
            image = tf.squeeze(image, [0])
        image = tf.subtract(image, 0.5)
        image = tf.multiply(image, 2.0)
        return image

def load_model(sess):

    """

    Load TensorFlow model

    Args:
        sess: TensorFlow session

    """
    print("Loading model...")

    placeholder = tf.placeholder(shape=[None, image_size, image_size, 3], dtype=tf.float32, name = 'Placeholder_only')

    #Now create the inference model but set is_training=False
    with slim.arg_scope(xception_arg_scope()):
        logits, end_points = xception(placeholder, num_classes = NUM_CLASSES, is_training = False)

    # #get all the variables to restore from the checkpoint file and create the saver function to restore
    variables_to_restore = slim.get_variables_to_restore()

    #Just define the metrics to track without the loss or whatsoever
    probabilities = end_points['Predictions']
    predictions = tf.argmax(probabilities, 1)
    saver = tf.train.Saver()
    saver.restore(sess, '/model.ckpt') # specify here which model to restore
    return predictions
