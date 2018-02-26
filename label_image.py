# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import os
from sys import exit
import matplotlib.pyplot as plt

import argparse
import sys

import cv2

import readline, glob

from scipy import misc, ndimage

import numpy as np
import tensorflow as tf

def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)
    # print(graph.get_operations())
    return graph

def read_tensor_from_image_file(file_name, input_height=299, input_width=299,
				input_mean=0, input_std=255):
    input_name = "file_reader"
    output_name = "normalized"
    file_reader = tf.read_file(file_name, input_name)
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(file_reader, channels = 3,
                                       name='png_reader')
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(tf.image.decode_gif(file_reader,
                                                  name='gif_reader'))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
    else:
        image_reader = tf.image.decode_jpeg(file_reader, channels = 3,
                                        name='jpeg_reader')
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0);
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)

    return result

def prep_numpy(frame, input_height=299, input_width=299):
    frame = cv2.resize(frame, (input_height, input_width), interpolation=cv2.INTER_CUBIC)
    # adhere to TS graph input structure
    numpy_frame = np.asarray(frame)
    numpy_frame = cv2.normalize(numpy_frame.astype('float'), None, -0.5, .5, cv2.NORM_MINMAX)
    np_final = np.expand_dims(numpy_frame, axis=0)
    return np_final

def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label

def fileWalk(directory, destPath, sess, input_operation, output_operation, file_name, input_height, input_width, input_mean, input_std, plot):
    try:
        os.makedirs(destPath)
    except OSError:
        if not os.path.isdir(destPath):
            raise
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if len(file) <= 4 or file[-4:] not in ['.jpg', '.png', 'jpeg']:
             # or file[-4:] != '.jpg':
                continue
            file_name = os.path.join(subdir, file)
            print('CURRENT FILE: ', file_name)
            title = infer_image(sess, input_operation, output_operation, file_name, input_height, input_width, input_mean, input_std)
            if plot:
                plot_image(title, file_name, False, plot)


def plot_image(title, image, show, save):
    if isinstance(image, str):
        image = plt.imread(file_name)
    img_plot = plt.imshow(image)
    plt.style.use('ggplot')
    #Set up the plot and hide axes
    plt.title(title)
    img_plot.axes.get_yaxis().set_ticks([])
    img_plot.axes.get_xaxis().set_ticks([])
    if show:
        plt.show()
    if save:
        plt.savefig('./predictions/' + file_name+'_prediction.png')

def infer_image(sess, input_operation, output_operation, image, input_height, input_width, input_mean, input_std):
    if isinstance(image, str):
        t = read_tensor_from_image_file(file_name,
                                      input_height=input_height,
                                      input_width=input_width,
                                      input_mean=input_mean,
                                      input_std=input_std)
    else:
        t = image
    start_time = time.time()

    results = sess.run(output_operation.outputs[0],
                  {input_operation.outputs[0]: t})


    results = np.squeeze(results)

    top_k = results.argsort()[-6:][::-1]

    print("Finished in : --- %s seconds ---" % (time.time() - start_time))

    for i in top_k:
        print(labels[i], results[i])
    category = ''
    if labels[top_k[0]] in ['plastic', 'metal', 'glass']:
        category = 'recycle'
    if labels[top_k[0]] in ['cardboard', 'paper']:
        category = 'compost'
    if labels[top_k[0]] == 'trash':
        category = 'trash'
    print(category)
    human_string = category + '\n' + str(labels[top_k[0]]) + ':' + str(results[top_k[0]]*100) + '%' + '\n' + str(labels[top_k[1]]) + ':' + str(results[top_k[1]]*100) + '%'
    return human_string


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

def grabVideoFeed(camera):
    grabbed, frame = camera.read()
    return frame if grabbed else None

def setUpCamera():
    camera = cv2.VideoCapture(0)
    return camera

def setUpArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to be processed")
    parser.add_argument("--graph", help="graph/model to be executed")
    parser.add_argument("--labels", help="name of file containing labels")
    parser.add_argument("--input_height", type=int, help="input height")
    parser.add_argument("--input_width", type=int, help="input width")
    parser.add_argument("--input_mean", type=int, help="input mean")
    parser.add_argument("--input_std", type=int, help="input std")
    parser.add_argument("--input_layer", help="name of input layer")
    parser.add_argument("--output_layer", help="name of output layer")
    parser.add_argument("--plot", help="plot/save image and prediction")
    parser.add_argument("--filewalk", help="label all images in directory")
    parser.add_argument("--livestream", help="feed image directly from webcam")
    return parser.parse_args()

if __name__ == "__main__":
    file_name = "./test.jpg"
    model_file = \
    "./transferInceptionResV2_50EpochsRun1.pb"
    label_file = "labels.txt"
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255
    filewalkPath = ''
    input_layer = "input_1"
    output_layer = "output_node0"

    setUpArgs()

    plot = False
    args = setUpArgs()

    if args.graph:
        model_file = args.graph
    if args.image:
        file_name = args.image
    if args.labels:
        label_file = args.labels
    if args.input_height:
        input_height = args.input_height
    if args.input_width:
        input_width = args.input_width
    if args.input_mean:
        input_mean = args.input_mean
    if args.input_std:
        input_std = args.input_std
    if args.input_layer:
        input_layer = args.input_layer
    if args.output_layer:
        output_layer = args.output_layer
    if args.filewalk:
        filewalkPath = args.filewalk
    if args.plot:
        plot = True

    graph = load_graph(model_file)

    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)

    aborted = False

    input_name = 'import/' + input_layer
    output_name = 'import/' + output_layer
    input_operation = graph.get_operation_by_name(input_name);
    output_operation = graph.get_operation_by_name(output_name);
    labels = load_labels(label_file)
    while not aborted:
        with tf.Session(graph=graph) as sess:
            if args.image:
                infer_image(sess, input_operation, output_operation, file_name, input_height, input_width, input_mean, input_std, plot)
            if args.livestream:
                while True:
                    camera = setUpCamera()
                    frame = grabVideoFeed(camera)
                    if frame is None:
                        raise SystemError('Issue grabbing the frame')
                    cv2.imshow('Main', frame)
                    np_final = prep_numpy(frame)

                    key = cv2.waitKey(32)
                    if key == 32:
                        title = infer_image(sess, input_operation, output_operation, np_final, input_height, input_width, input_mean, input_std)
                        plot_image(title, frame, show=True, save=False)
                        # sess.close()
                        # exit(1)
                camera.release()
                cv2.destroyAllWindows()
            if filewalkPath == '':
                print('input file name of image: ')
                file_name = input()
                if file_name == '\x1b':
                    aborted = True
                title = infer_image(sess, input_operation, output_operation, file_name, input_height, input_width, input_mean, input_std)
                if plot:
                    plot_image(title, file_name, plot, plot)
            else:
                fileWalk(filewalkPath, './predictions/', sess, input_operation, output_operation, file_name, input_height, input_width, input_mean, input_std, plot)
