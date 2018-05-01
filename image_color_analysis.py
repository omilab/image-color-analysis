from __future__ import print_function

from sklearn.cluster import KMeans
import numpy as np
import time
from PIL import Image
import os
from PIL import ImageDraw


'''
@param images_path: Images' directory from which the function creates collage
@return: Object of type PIL.Image 
'''
def images_collage(images_path):
    startTime = time.time()

    # load images from the folder
    images = []
    for image_name in os.listdir(images_path):
        images.append(Image.open(images_path + '/' + image_name))

    # calculate the total height and the max width of the collage
    total_height = sum(img.size[1] for img in images)
    max_width = max(img.size[0] for img in images)

    # create a collage with alpha channel
    # every image will be placed below the previous one
    collage = Image.new('RGBA', (max_width, total_height))
    y = 0
    for img in images:
        collage.paste(img, (0, y))
        y += img.size[1]

    endTime = time.time()

    print ('creating collage time: ', endTime - startTime)
    print ('total_height: ', total_height)
    print ('max_width: ', max_width)

    # print the collage
    # collage.show()
    return collage

'''
@param collage: Object of type PIL.Image 
@param clusters: Number of clusters (k) for k-mean  (=final number of colors in the histogram)
@return: Object of type KMeans model
'''
def k_means(collage,clusters = 5):
    startTime = time.time()
    # conevrt the collage to a color array (total_height X max_width X 4)
    collage_array = np.array(collage)

    # reshape the array
    collage_array = collage_array.reshape((collage_array.shape[0] * collage_array.shape[1], 4))

    # remove all transparent colors
    collage_array = collage_array[~np.all(collage_array == 0, axis=1)]

    # fit k-means model with 5 clusters
    kmeans_model = KMeans(n_clusters=clusters)
    kmeans_model.fit(collage_array)

    endTime = time.time()
    print ('fitting model time: ', endTime - startTime)
    return kmeans_model

'''
@param kmeans_model: Object of type KMeans model 
@param bar_save_path: The file name for the color bar image
@return: Object of type PIL.Image 
'''
def colors_bar(kmeans_model, color_bar_save_path ):
    # create a histogram of the number of clusters
    numLabels = np.arange(0, len(np.unique(kmeans_model.labels_)) + 1)
    (hist, _) = np.histogram(kmeans_model.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    startX = 0

    # create a bar image that displays the most used colors
    im = Image.new('RGB', (300, 300), (0, 0, 0))
    dr = ImageDraw.Draw(im)

    for (percent, color) in sorted(zip(hist, kmeans_model.cluster_centers_), key=lambda t: t[0], reverse=True):
        endX = startX + (float(percent) * 300)
        dr.rectangle([int(startX), 0, int(endX), 300], fill=tuple(map(int, color)))
        startX = endX

    im.save(color_bar_save_path)
    return im

'''
@param images_path: Images' directory from which the function creates collage
@param colors_bar_path: The file path for the color bar image, default = 'colors_bar.png' in current dir
@param clusters: Number of clusters (k) for k-mean, default = 5
'''
def analyze_folder(images_path, colors_bar_path ='colors_bar.png' , clusters=5 ):
    collage = images_collage(images_path)
    model = k_means(collage, clusters)
    color_bar_image = colors_bar(model, colors_bar_path)
    color_bar_image.show()