# Abstract

Lossy compression is a commonly used technique in different fields, especially embedded devices. However, its effects on object classification still need to be investigated. In this project, we analyzed the effects of lossy compression of images on the object detection model. We tradeoff of model accuracy and latency of sending images over a network and performing the compression. We analyzed four different compression algorithms on our image dataset and collected the request time and model accuracy. We found that the bicubic downscaling algorithm minimized the system’s latency because the downscaling computational time was the most significant term in the overall latency. Additionally, we found that the bilinear downscaling algorithm caused the smallest reduction in model accuracy, even when the image was downscaled 10x. Overall we found the bicubic and bilinear algorithms had a reasonable tradeoff between latency and model accuracy.

# Team

* Ting Chun Chou \#1 
* Neil Prajapati \#2 

# Required Submissions

* [Proposal](proposal)
* [Midterm Checkpoint Presentation Slides](https://docs.google.com/presentation/d/1Kj6vXsNdJutJDV4BZEIuXOJpnmdhZLw2z4csMEBuo5k/edit?usp=sharing)
* [Final Presentation Slides](https://docs.google.com/presentation/d/1V2OVSa5LZTNG0FJv18XL8g6pz3JAFtowmMsRv8NLZq0/edit?usp=sharing&fbclid=IwAR0qmA8rdiBYomJ_Bepoh37TKnOYXAL5bWgdPSHlGLqhFDC780pcVHYM-BM)
* [Final Report](report)
