### Image Color Analysis

This color analysis tool was built to support a data visual analytics method for the study of  national Webs. It was initially used to analyze the changing colors of the former Yugoslav domain, .yu, during the Kosovo War. For more information please refer to:

Ben-David, A., Amram, A., & Bekkerman, R. (in press). [The Colors of the National Web: Visual Data Analysis of the Historical Yugoslav Web Domain](https://www.academia.edu/30508702/The_colors_of_the_national_Web_visual_data_analysis_of_the_historical_Yugoslav_Web_domain._Int_J_Digit_Libr_2016_._doi_10.1007_s00799-016-0202-6). *Internation Journal on Digital Libraries*.
 

The method can be readily applied to any other national Web (or Web archive), and, in fact, to any folder of images.

The following is a tutorial for using the tool on a given folder of images. We will compare the color histogram of Google images results to "Donald Trump" and "Hillary Clinton" (as of November 2016). Two demo folders are included in this tutorial.

### Tools
There are 2 ways to run this tool
1. Use "Jupyter Notebook".
2. Install image-color-analysis as package

#### "Jupyter Notebook"

##### Preparations

1. Please Download and install [Anaconda, version Python 2.7](https://www.continuum.io/downloads).
2. Please 'download zip' the project folders from [Github](https://github.com/omilab/image-color-analysis/archive/master.zip).
3. Unzip the folder

##### A  Step by Step Guide for using the tool

1. In Anaconda, open "Jupyter Notebook".
2. When notebook opens - it automatically opens your default browser and shows your file directory. 
3. Open your downloaded and extracted folder.
4. Open the file "image_color_analysis.ipynb".

##### Now, let's have some fun!

The script in the file you just opened is divided into three sections:

1. Building a collage from all the images.
2. Fitting a K-Means clustering model (identifying clusters of colors in the images).
3. Creating a color histogram that summarizes the color histogram of the images.

Although the code is annotated, below is an explanation of each section.

###### Part 1: Creating a collage

In this section, we first specify the location of an images folder and load the images. Then, we create a collage from all the images. This is done by calculating the maximal width of all images and the sum of the heights of all images. Finally, it creates a new image with an alpha channel. That is, all images are arranged one below the other, and the empty spaces between them are marked as transparent.

Click the 'run' button to start this procedure. When it's done, it prints the time it took to build the collage (this give a good indication of the process when analyzing a large corpus). The generated collage pops up. You may want to view or save it.
 

###### Part 2: Building a K-Means model and running it on the collage

In order to calculate and identify clusters of colors in the dataset, we first need to convert the images into a numerical representation - a color array. The array has four dimensions: Red, Green, Blue (RGB) and Alpha (the transparent color we added to mark the empty spaces in the previous section).
Subsequently, the collage is represented as a matrix of the total height * total width * 4(that is, RGB+A).

Since KMeans does not work on a matrix, we need to transform it into a continuous, one-dimensional layer. For example, if the maximum height of the collage is 100, and the maximum width is 400, instead of representing the collage as a 100 * 400 * 4, it is represented as one line of the sum: 160,000.

Finally, we remove all transparent colors, as they are not necessary for the calculation, and we fit the model. In the code, we specify 5 clusters, but this number can be changed.

Click the 'run' button to start this procedure. When it's done, it prints the time it took to build the collage. (The larger your collage is and the larger the number of clusters, the longer it will take to complete).


###### Part 3: Generating the color histogram

This section calculates the proportion of colors for each section. Then, it normalizes the histogram, so that the proportions sum to 1.
Finally, it generates an image that puts the width of each color in a histogram.
1.for each cluster, calculate the proportion of each color.

Click the 'run' button to start this procedure. The resulting histogram that pops up summarizes the color composition of your corpus!


###### N.B.

this is the bit of code where you may change the name of the demo folder to your own folder of images:

folder = 'YOUR FOLDER'

This is the bit of code where you may change the number of clusters (=colors in the histogram):

kmeans_model = KMeans(n_clusters=YOUR NUMBER)

#### Install image-color-analysis

##### Preparations

1. Please Download and install python 3.6
2. Install the package
```
pip install image-color-analysis
```
3. Create new python file and import the package
```
from image_color_analysis import *
```
##### Now, let's have some fun!
The package has 4 functions:
1. image_collage
2. k_means
3. colors_bar
4. analyze_folder

###### image_collage: Creating a collage
 The function creates a collage of all the images in a folder.
 The function receives directory/folder path.
 The function return a collage as image (object's type: PIL.Image).

 ```python
import image_color_analysis

folder = 'YOUR FOLDER'
image = image_color_analysis.images_collage(folder)
 # print the collage
image.show()

 # save the image in png format (you can choose another format as well)
image.save('collage.png')
```

in order to load the image:
 ```python
from PIL import Image
im = Image.open('collage.png')
```

###### k_means: Building a K-Means model
The function find a k-mean model for a collage.
The function receives collage image (object PIL.Image) and number of clusters (default value = 5).
The function returns the model it create (object's type: KMeans)

 ```python
import image_color_analysis

folder = 'YOUR FOLDER'
image = image_color_analysis.images_collage(folder)
# train model with 5 clusters (k=5)
model_5_clusters = image_color_analysis.k_means(image)
# train model with 8 clusters (k=8)
model_8_clusters = image_color_analysis.k_means(image, 8)
```

if you want to save the model to a file and load it later:

 ```python
import image_color_analysis
import pickle
folder = 'YOUR FOLDER'
image = image_color_analysis.images_collage(folder)
# train model with 5 clusters (k=5)
model_5_clusters = image_color_analysis.k_means(image)
# save the model
model_file_name = 'model.pkl'
pickle.dump(model_5_clusters, open(model_file_name, 'wb'))

# load the model
loaded_model = pickle.load(open(model_file_name, 'rb'))

```

###### colors_bar: Generating the color histogram
Then the function creates a color bar image from a KMeans model and save it to a file.
The function receives model(object sklearn.cluster.Kmeans) and file path (path and file name for saving the color bar image).
The function return a color bar image (object's type: PIL.Image).
 ```python
import image_color_analysis

folder = 'YOUR FOLDER'
image = image_color_analysis.images_collage(folder)
# train model with 5 clusters (k=5)
model_5_clusters = image_color_analysis.k_means(image)
color_bar_path = "new_color_bar.png"
color_bar_image = image_color_analysis.colors_bar(model_5_clusters,color_bar_path)
 # print the color bar
color_bar_image.show()
```

###### analyze_folder:
This function run all the functions , creates color bar and presents it to the user.
The function receives:
 1. directory/folder path of images
 2. optional - file' name to save the color bar( default = 'colors_bar.png' in current dir)
 3. optional - number of clusters in k-means (default - 5)

 ```python
import image_color_analysis

folder = 'YOUR FOLDER'
# 5 clusters and and create file  'colors_bar.png'
image_color_analysis.analyze_folder(folder)

# 7 clusters and and create file  'new_colors_bar.jpg'
image_color_analysis.analyze_folder(folder, 'new_colors_bar.jpg', 7)
```