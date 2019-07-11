# Inter-vehicle Communication and Alert on Veering Away from Lane

A head-on collision prevention system for 2-lane roads (e.g. Route 90).  
When a vehicle veers away from its lane to the opposite one for any reason, an alert will be sent to other drivers within 200m.

## Demo

Car A send warning messages to the white car on the left side.

![ezgif com-video-to-gif](https://user-images.githubusercontent.com/40145410/60893513-b5fc7e00-a269-11e9-833b-4dee98f71fd7.gif)

## The main idea

● Establishing client – server.


● Identifying a veering away from lanes at any given moment.


● Current location pinpointing at any given moment.

## client–server
The server will wait for client requests, whereby each client represents a vehicle.  
Once the server receives a request, it will store the created connection in the database and open a new thread to listen to data from that vehicle at any given moment.  
At any given moment, each vehicle sends:  
1. Its location.  
2. Whether or not it veered away from its lane.


To the other threads (vehicles) connected to the network.  
These two actions are done simultaneously. I will explain this further at a later stage.

Each vehicle will receive real-time updates on the location of other vehicles and test whether there is a vehicle that has veered away from its lane nearby; an alert will be sent if such vehicle is found.





## Identifying a veering away from lanes

We will identify broken white lines on the road in every frame captured by the vehicle’s camera.  
When broken white lines appear to the left of the frame, the vehicle is in its lane (remember: this is a 2-lane road only).  
When veering away from a lane, the broken white lines that were previously to the left of the frame will now be near the center of the frame.  
During a full overtaking of the lane, the broken white lines will be to the right of the frame.


### Color Selection

 The images are loaded in RGB color space

![Input](https://user-images.githubusercontent.com/40145410/60889291-63b75f00-a261-11e9-99fb-2d0dea3e0da4.jpg)


#### Converted from RGB to HSL color space


The main advantage of HSL is that it makes it easy to select a color quickly.


![HSL](https://user-images.githubusercontent.com/40145410/60889309-6ca83080-a261-11e9-8789-5f2b532c74f9.jpg)



For more details: https://www.nixsensor.com/what-is-hsl-color/

#### Selecting _only_ white colors in the images using the HSL channels

![white_mask](https://user-images.githubusercontent.com/40145410/60889343-7b8ee300-a261-11e9-8dd9-b911b66b86d1.jpg)

### Edge Detection

#### Converted to Grayscale

The images should be converted into gray scaled ones in order to detect edges in the images.

![gray](https://user-images.githubusercontent.com/40145410/60889392-919ca380-a261-11e9-91fe-eb7dcc1abe31.jpg)


#### Gaussian Blur

To smooth out rough edges.

![smooth_image](https://user-images.githubusercontent.com/40145410/60889407-9b260b80-a261-11e9-8c81-3d44cd52e823.jpg)

 
#### Canny Edge Detection

To find edges in the image
 
![detect_edges](https://user-images.githubusercontent.com/40145410/60889447-af6a0880-a261-11e9-811f-7f49ac8de084.jpg)

 
 
### Region of Interest 
      
   We are need to check only part of the image.
   
   So we need to create mask and use "and" bitwise operator with the result of the previous step.

#### Create mask
 
  We are interested in the white area in the image only.
  
  ![ROI_mask](https://user-images.githubusercontent.com/40145410/60889474-bee95180-a261-11e9-84f3-8ef394b678f5.jpg)

   
 **Then use _"and"_ bitwise operator**
   
![lane_only](https://user-images.githubusercontent.com/40145410/60889496-ca3c7d00-a261-11e9-8645-0a09b17ef88e.jpg)

#### And now lets look at the left side(.4 of the frame) and right side(.6 of the frame) of of the frame:
 
 ![left_side](https://user-images.githubusercontent.com/40145410/61053404-2506dd80-a3f6-11e9-8941-83c978efc465.PNG)  ![right_side](https://user-images.githubusercontent.com/40145410/61053408-26d0a100-a3f6-11e9-98a9-533e2ea67029.PNG)
 
 


## Current location pinpointing at any given moment

For full details:  
https://codeburst.io/how-i-understood-getting-accurate-geolocation-using-python-web-scraping-and-selenium-7967d721587a


