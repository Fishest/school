================================================================================
Computer Vision With OpenCV2
================================================================================

--------------------------------------------------------------------------------
Libraries
--------------------------------------------------------------------------------

Since version 2.2, the OpenCV library is divided into several modules:

* **opencv_core**: contains the core functionalities of the library
* **opencv_imgproc**: contains the main image processing functions.
* **opencv_highgui**: contains the image and video reading and writing functions
* **opencv_features2d**: contains the feature point detectors and descriptors
* **opencv_calib3d**: contains the camera calibration, two-view geometry estimation, and stereo functions
* **opencv_video**: contains the motion estimation, feature tracking, and foreground extraction
* **opencv_objdetect**: containing the object detection functions such as face and people
* **opencv_ml**: contains some machine learning code
* **opencv_flann**: contians computational geometry code
* **opencv_contrib**: contains contributed code
* **opencv_legacy**: contains legacy code
* **opencv_gpu**: contains gpu accelerated code

All of these modules have a header file associated with them (located in include directory):

.. code-block:: c++

    #include <opencv2/core/core.hpp>
    #include <opencv2/imgproc/imgproc.hpp>
    #include <opencv2/highgui/highgui.hpp>
    #include "cv.h" // if you see code starting with, it uses the old style

--------------------------------------------------------------------------------
Basics
--------------------------------------------------------------------------------

These are the basics of viewing and working with image files in opencv:

.. code-block:: c++

    cv::Mat image = cv::imread("img.jpg"); // store an image in a new matrix
    cv::CvSize size = image.size();        // get the size of the matrix
    std::cout << "size: " << size.height << "," << size.width << std::endl;
    std::cout << "image read correctly: " << !image.data << std::endl;

    cv::namedWindow("Original Image");   // define the viewing window
    cv::imshow("Original Image", image); // show the image
    cv::waitKey(0);                      // prevent the application from closing

    cv::Mat result;                      // apply some transformation to the image
    cv::flip(image,result, 1);           // 1:horizontal, 0:vertical, -1: both
    cv::imwrite("output.bmp", result);   // save our resulting image

    using namespace cv;                  // if you don't want to type the prefix

All the opencv containers implement reference counting, shallow copies, and
correct cleanup on destruction making them very simple to work with:

.. code-block:: c++

    cv::Mat image2, image3;
    image2 = result;                                // the two images refer to the same data
    result.copyTo(image3);                          // a new copy is created

    cv::Mat function() {                            // it is safe to return by value
        cv::Mat ima(240,320,CV_8U,cv::Scalar(100)); // create image
        return ima;                                 // return by shallow copy
    }
    cv::Mat result = function();                    // no extra memory used
    cv::Mat_<uchar> image;                          // typesafe version of image (efficient)

--------------------------------------------------------------------------------
Pixel Manipulation
--------------------------------------------------------------------------------

The following is a simple example of working with individual pixels of an opencv
`Mat` handle. It randomly whites out pixels in an image:

.. code-block:: c++

    void salt(cv::Mat &image, int n) {
        for (int k = 0; k < n; k++) {
            int i = rand() % image.cols;
            int j = rand() % image.rows;

            if (image.channels() == 1) {        // gray image
                image.at<uchar>(j,i) = 255;
            } else if (image.channels() == 3) { // color image
                image.at<cv::Vec3b>(j,i)[0] = 255;
                image.at<cv::Vec3b>(j,i)[1] = 255;
                image.at<cv::Vec3b>(j,i)[2] = 255;
            }
        }
   }

.. todo:: Page 41
