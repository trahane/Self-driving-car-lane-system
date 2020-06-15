<h2>Introduction:</h2>
<p>
I wanted to make some kind of autonomous system simulation. Initially, I was unsure what kind of autonomous system. In consideration with time period given. I took some inspiration from Tesla’s autopilot system and MIT’s deeptraffic system.
The idea behind it was, making a car drive through lanes by avoiding traffic.
It is actually a classification problem. There are cars incoming in each lane. And the autonomous car is classifying which would be the best lane to take.
</p>
<p>
The implementation is pretty simple and the motivation behind is not to build the best A.I. that was ever created. But to understand some basic concepts and applying them.
</p>

<h2>Implementation:</h2>
<p>
As I was making a simulation, I have way less input than the actual real-time roads. So, I just wanted to mimic that scenario. I am using a simple 2-layer neural network with back-propagation. For this task I am using a sigmoid activation function. The current system performs more like an expert system. I am using python as my tool for implementation. For all the dependences used please check usage below.
</p>

<h3>Structure of NN:</h3>
<table>
<tr>
    <th>Input</th>
    <th>Layer 1</th>
    <th>Layer 2</th>
    <th>Output</th>
  </tr>
  <tr>
    <td>Data</td>
    <td>7x5 weights</td>
    <td>5x1 weights</td>
    <td>1 neuron</td>
  </tr>
</table>

<h3>Input:</h3>
<table>
  <tr>
    <td>Left Edge</td>
    <td>Left Lane</td>
    <td>Mid Lane</td>
    <td>Right Lane</td>
    <td>Right Edge</td>
    <td>Bias</td>
    <td>Current Position</td>
  </tr>
</table>


<h3>Output:</h3>
<table>
<tr>
    <th>Value</th>
    <th>Action</th>
  </tr>
  <tr>
    <td>0.1</td>
    <td>Do nothing</td>
  </tr>
  <tr>
    <td>0.2</td>
    <td>Go one lane right</td>
  </tr>
  <tr>
    <td>0.3</td>
    <td>Go one lane left</td>
  </tr>
  <tr>
    <td>0.4</td>
    <td>Go two lane right</td>
  </tr>
  <tr>
    <td>0.5</td>
    <td>Go two lane left</td>
  </tr>
</table>


<h2>Usage:</h2>
<p>
USE PYTHON 3.5+

Dependences:
1.	pygame
2.	numpy

Run:
1.	extract all files in one folder
2.	change paths in the car_d.py (if required)
3.	If all dependences are installed, just run car_d.py using
python car_d.py
4.	To control use arrow keys left and right.
5.	To use autonomous mode press spacebar.
</p>

![alt text](https://github.com/trahane/Self-driving-car-lane-system/blob/master/showcase%20output.png?raw=true)
