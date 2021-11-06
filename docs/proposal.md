# Project Proposal

## 1. Motivation & Objective

In this project, we are trying to compare the performance of partitioning of control of the robot across different devices. Since the computing power of embedded devices may not be good enough for intense computation, we are going to do the control algorithm either on the edge device or the embedded device. However, in order for the edge device to perform the computation, it will need to communicate with the embedded device. This communication adds overhead which may offset the gains from higher performance. 

We will explore this problem with a particular use case. We will have a robot which is designed to avoid obstacles in a hallway. In the real world, this robot would likely have a camera to detect obstacles and avoid them. However, since our focus is on the performance impacts of moving the control algorithms, we will simplify this problem. 

We are going to utilize the built-in color sensor and proximity sensor for obstacle detection. The proximity sensor can help us to detect the distance between the obstacles and the robot. The color sensor will identify what kind of obstacles it is.
For example, if there’s a person (a yellow obstacle) in front of the robot, the robot should try to maintain a safer distance from him. On the other hand, if there’s a non-human obstacle (a blue obstacle), the robot can get closer to it.

One real world application is a robot that can be controlled by itself and manually outside of the building. However, after getting into the building, there are two cases of how the robot moves. The first case is that the building trusts the robot, and allows the robot to control itself. Another case is that the building does not trust the robot and does not allow it to roam inside the building, it would take the control of the robot and navigate it to avoid obstacles. Our project will evaluate the performance of the robot in both of these cases.


## 2. State of the Art & Its Limitations

One widely used design pattern is networked robotics. Networked robotics is a system which has several robots which communicate with each to share data and computational load. It is commonly used in factory environments such as assembly lines [4]. One limitation of this approach is that the computation resources are limited to the installed computational units on the robot. This means that the types of computations that one can perform are limited.

Cloud robotics is another design pattern which addresses this limited computational power problem [4]. With cloud robotics, a significant portion of the computation is done on the cloud. If the system ever needs more computational resources, one can simply provision more cloud resources which makes it possible to perform very expensive computations. However, this approach suffers from higher latency and availability issues due to network service interruptions.


## 3. Novelty & Rationale

Our approach will compare the performance of the control algorithm when it is computed on the edge device versus when it is computed on the robot. This is different from previous work since previous work focused on having computation in the cloud or moving certain tasks to the cloud while other tasks stay on the robot [4]. In our case, the entire control algorithm will either be in the robot or the edge device.

This is also different from Imai and Kubo’s paper on cloud-based motion control [1] because this project involves both motion control based on data gathered by the sensors on the robot. This increases the latency of the control loop because it needs to first receive the data, process it and then send back controls to the motors. 

## 4. Potential Impact

First of all, it could help us to have a better understanding of the performance of partitioning of control of the robot in different ways. As a result, we can choose the optimal approach whenever we want to implement projects similar to this one. Additionally, we can have a better understanding of whether edge device based control of a robot is feasible at all in certain applications.

Another impact is that it can help us have a better understanding of the specific use case involving the robot and the building. If the robot is outside of the building, it controls itself. However, after it gets into the building, things might be different. If the building does not trust the robot, which means that the building does not allow the robot to move by itself, it would take the control of the robot and navigate it to avoid the obstacles. Our project will create a solution to a simplified version of this problem and evaluate its performance. Our project will also produce strategies to optimize the edge device based control. 


## 5. Challenges

One challenge is minimizing latency of communication between the robot and the edge device. There is a risk that the latency will be too large and moving the computation to the edge device will make the system not responsive enough to avoid obstacles in real time.
Another challenge would be creating a simple control algorithm for the robot. One risk is that our control algorithm will not be effective enough for the robot to navigate the hallway.

Lastly, we have the challenge of training a model to detect the obstacle type using the color sensor. If this model is not accurate and robust enough, then our robot will not be able perform its task properly.


## 6. Requirements for Success

We will need an Arduino Nano 33 BLE, a motor controller, two Motors and a Raspberry Pi.

The Arduino Nano 33 BLE will communicate with the Raspberry Pi using Bluetooth Low Energy. We chose this technology because the Arduino and Raspberry Pi already have a BLE chip on the board. Additionally, we will not be transmitting a lot of data. If we discover this approach is infeasible, we will attempt to use Zigbee.

We will also need to program the Arduino to control the motors through the motor controller.

We will also need to train a neural network to identify obstacles based on color. Lastly, we will need to implement a simple control algorithm for the robot.



## 7. Metrics of Success

We will need to optimize the edge device code to compensate for the communication overhead. One metric of success would be speed of the control loop in the edge device case compared to the speed of the control loops on the embedded device case. If the edge device case’s speed is similar to the embedded device case’s speed, then we successfully optimized the edge device control of the robot.

One metric for success is the quality of our comparison between the performance of the four cases and being able to explain the differences in their performances. 

Lastly, one important criteria for success is whether the robot will be able to navigate in the hallway without running into obstacles.

## 8. Execution Plan

1. Programming the robot to read raw sensor data and control motors.
2. Train a neural network to identify obstacles with the color sensor on the arduino.
3. Implement a simple algorithm for navigating the robot in the hallway with obstacles.
4. Programming the robot to send sensor data and accept commands.
5. Programming the edge device to receive sensor data and send commands
6. Determining a method to measure the speed of the control loop
7. Testing the robot in both control modes in a simple environment.

Tim will work on 2, 3 and 6. Neil will work on 1, 4 and 5. Both of us will work together on 7. 


## 9. Related Work

### 9.a. Papers

Cloud-based remote motion control over FTTH networks for home robotics [1] implements a cloud system that controls a motor over the internet. One key result is that it determined the maximum allowed latency for effective motor control. This is relevant to our project because we are also doing control of motors through another device.The final result that the maximum allowed latency was 20 ms can be relevant to us when designing our system.

Fruit identification using Arduino and TensorFlow [2] introduces the way how we can implement object detection with the built-in color sensor and proximity sensor, and use Tensorflow [3] to train a model for object detection.

Cloud robotics: architecture, challenges and applications [4] is relevant because it defines a model for determining whether a computation should be done on a cloud device or on a robot. Our project involves evaluating the performance of doing work on an edge device instead of the robot and comparing it with performing the computation on the robot itself. Thus this model can be useful to us.


### 9.b. Datasets

We are not planning to use any existing data sets.

### 9.c. Software

* Tensorflow Lite
* Arduino
* Arm® Mbed™ OS
* Raspbian


## 10. References

[1] R. Imai and R. Kubo, "Cloud-based remote motion control over FTTH networks for home robotics," 2014 IEEE 3rd Global Conference on Consumer Electronics (GCCE), 2014, pp. 565-566, doi: 10.1109/GCCE.2014.7031107. https://ieeexplore.ieee.org/document/7031107

[2] Dominic, P. & Sandeep, M. (2019, November 7). Fruit identification using Arduino and TensorFlow. ARDUINO TEAM. https://blog.arduino.cc/2019/11/07/fruit-identification-using-arduino-and-tensorflow/

[3] 
Martín Abadi, Ashish Agarwal, Paul Barham, Eugene Brevdo,
Zhifeng Chen, Craig Citro, Greg S. Corrado, Andy Davis,
Jeffrey Dean, Matthieu Devin, Sanjay Ghemawat, Ian Goodfellow,
Andrew Harp, Geoffrey Irving, Michael Isard, Rafal Jozefowicz, Yangqing Jia,
Lukasz Kaiser, Manjunath Kudlur, Josh Levenberg, Dan Mané, Mike Schuster,
Rajat Monga, Sherry Moore, Derek Murray, Chris Olah, Jonathon Shlens,
Benoit Steiner, Ilya Sutskever, Kunal Talwar, Paul Tucker,
Vincent Vanhoucke, Vijay Vasudevan, Fernanda Viégas,
Oriol Vinyals, Pete Warden, Martin Wattenberg, Martin Wicke,
Yuan Yu, and Xiaoqiang Zheng.
TensorFlow: Large-scale machine learning on heterogeneous systems,
2015. Software available from tensorflow.org.

[4] Guoqiang,  H., & Weepeng, T., & Yonggang,  W.. (2012). Cloud robotics: architecture, challenges and applications. IEEE Network. 26(3). https://ieeexplore.ieee.org/abstract/document/6201212

