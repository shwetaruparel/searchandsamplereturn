[//]: # (Image References)
[image_0]: ./images/test_dataset.jpg
[image_1]: ./images/Recorded_testdata.jpg
[image_2]: ./images/obs_map.jpg
[image_3]: ./images/diff_img.jpg
[image_4]: ./images/sim_conf.jpg
[image_5]: ./images/auto_run.jpg

*Created on Tue Jul 31 12:15:54 2018
@author: Shweta*

# Notebook Anaysis

## Testing on the provided test data. 
### The function in the notebook were run as is on the provided test data set
"""
![alt text][image_0]

"""
## Testing on the simulator run recorded data.
### The functions in the notebook were run on the recorded data
"""
![alt text][image_1]

"""
### The function perspect_transform was changed to return an image(masked) to map pixels for obstacles

***Note: masked = cv2.warpPerspective(np.ones_like(img[:,:,0]), M, (img.shape[1], img.shape[0])) #Create an image containing all 1's for obstacle channel(img[:,:,0])
        return warped, masked

***Note: obs_map =np.invert(np.invert(threshed)+masked) - This statement is used to invert the color thresholded navigable map andthen added to masked image and inverted back to map the pixel poitions for obstacles leaving the navigable pixels as is .

`The images below shows the colour thresholded navigable pixels and colour thresholded obstacle pixels` 
![alt text][image_2]


### Added one more function to find the colour thresholded image to map pixels for golden rocks

"""

    def rocks_thresh (img, rgb_thresh=(110, 110, 50)):  
    rock_pix = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] < rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    rock_select = np.zeros_like(img[:,:,1])
    rock_select[rock_pix] = 1
    # Return the binary image
    return rock_select
"""

***Note: Called this function to map rock details
rock_map = rocks_thresh(warped)

### Modified process_image to map identifiable navigable terrain , obstacles and rock to worldmap
"""
    ## After obtaining the colour thresholded image for navigable terrain , obstacles and for rock, the rover coordinates are calculated 
      and then pixels to world map.The data worldmap is updated with the mapped pixels.##
    
"""

    xpix, ypix = rover_coords(threshed)
    obs_xpix,obs_ypix = rover_coords(obs_map)
    rock_xpix,rock_ypix = rover_coords(rock_map)
    worldmap = np.zeros((200, 200))
    scale = 10
    x_world, y_world = pix_to_world(xpix, ypix, data_xpos, 
                                data_ypos, data_yaw, 
                                data.worldmap.shape[0], scale)
    obs_x_world, obs_y_world = pix_to_world(obs_xpix, obs_ypix, data_xpos, 
                                data_ypos, data_yaw, 
                                data.worldmap.shape[0], scale)
    
    
    data.worldmap[y_world, x_world,2] = 255
    data.worldmap[obs_y_world, obs_x_world,0] =255
    rock_map = rocks_thresh(warped)

    if rock_map.any():
        rock_xpix, rock_ypix = rover_coords(rock_map)
        rock_x_world, rock_y_world = pix_to_world(rock_xpix, rock_ypix, data_xpos, 
                                data_ypos, data_yaw, 
                                data.worldmap.shape[0], scale)
        rock_dist, rock_angles = to_polar_coords(rock_xpix, rock_ypix)

        rock_idx = np.argmin(rock_dist)
        rock_xcen = rock_x_world[rock_idx]
        rock_ycen = rock_y_world[rock_idx]
        data.worldmap[rock_ycen, rock_xcen, 1]+=1
        
     ### Adding Analyses and plotting it on output image
         tot_nav_pix = np.float(len((data.worldmap[:,:,2].nonzero()[0])))
    # Next figure out how many of those correspond to ground truth pixels
    good_nav_pix = np.float(len(((data.worldmap[:,:,2] > 0) & (data.ground_truth[:,:,1] > 0)).nonzero()[0]))
    # Next find how many do not correspond to ground truth pixels
    bad_nav_pix = np.float(len(((data.worldmap[:,:,2] > 0) & (data.ground_truth[:,:,1] == 0)).nonzero()[0]))
    # Grab the total number of map pixels
    tot_map_pix = np.float(len((data.ground_truth[:,:,1].nonzero()[0])))
    # Calculate the percentage of ground truth map that has been successfully found
    perc_mapped = round(100*good_nav_pix/tot_map_pix, 1)
    # Calculate the number of good map pixel detections divided by total pixels 
    # found to be navigable terrain
    if tot_nav_pix > 0:
        fidelity = round(100*good_nav_pix/(tot_nav_pix), 1)
    else:
        fidelity = 0

    cv2.putText(output_image,"Mapped"+str(perc_mapped), (20, 20), 
                cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1)
    cv2.putText(output_image,"Fidelity"+str(fidelity), (20, 30), 
                cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 255, 255), 1)


"""

    check the image below that contains the original image , warped image , colour thresholded image 
![alt text][image_3]

## Output Test Data Video with analyses

***The output data video can be found in the output folder.

# Autonomous Navigation and Mapping

### Filled in the perception_step(Rover)  [Global Rover was giving some error , so I had to pass the object ]
   1) Defined source and destination points for perspective transform with bottom offset set to 10
   2) Applied perspective transform over the image recieved from the rover camera with source and destination set
   3) Applied color threshold to identify navigable terrain/obstacles/rock samples
    
    """
          threshed = color_thresh(warped)
          obs_map =np.invert(np.invert(threshed)+masked) [I tried different method using np.invert]
          rock_map = rocks_thresh(warped)
    """
   4) Updated Rover.vision_image (this will be displayed on left side of screen)    
      
      """
      
            Rover.vision_image[:,:,0] = obs_map
            Rover.vision_image[:,:,2] = threshed*255
      """
      
   5) Converted map image pixel values to rover-centric coords
   6) Converted rover-centric pixel values to world coordinates
   7) Updated Rover worldmap (to be displayed on right side of screen)

        """
        
            Rover.worldmap[y_world, x_world,2] =255
            Rover.worldmap[obs_y_world, obs_x_world, 0] =255
            nav_pix =Rover.worldmap[:,:,2]>0
            Rover.worldmap[nav_pix,0]=0
    
        """
    8) Converted rover-centric pixel positions to polar coordinates
     Update Rover pixel distances and angles
   
     """   
        dist, angles = to_polar_coords(xpix, ypix)
        mean_dir = np.mean(angles)
    
        Rover.nav_dists = dist
        Rover.nav_angles = angles
    
    """
   9)Returned the rover object with everything updated.
   
   ### Filled in the desicion_step(Rover)
   
       Check if there is enough navigation area available:
           Check if set to 'forward' mode:
               Check if navigation vision angle is > than maximum stop forward length:
                   Steer the Rover to +15/-15 to the mean of the vision area
                   Check if Rover Velocity < Maximum velocity:
                       Set Throttle  = Max Throttle
                   else:
                       Just Coast (Throttle = 0)
                       
                   Check if the rover navigable distance length is less than 5000 :
                       slow down set throttle to 0.2
                       
                   Check if Rock is traced:
                       Slow down throttle set to 0.2
                       Set the steer towards the rock location +15/-15                       
                       Rover.steer = np.clip(np.mean(Rover.rock_angles * 180/np.pi), -15, 15) 

               Else Check if the len of navigation angles is < than stop_forward OR Length of Navigation distance <1000:
                       Coast Throttle set to 0
                       Apply brakes = 10
                       set the mode to 'stop'
        
           Else Check if Rover set to 'stop' mode:
                   Check if Rover velocity is > 0.2
                        Make sure to set throttle = 0
                        Apply brakes = 10
                        Try to steer +=-15
                    Else Check if Rover velocity <=0.2:
                        Check if the navigation angles < Go forward :
                                Set Throttle = 0
                                Release the brakes = 0
                                Keep Steering +=-15
                         Else Check if navigation angles > Go Forward:
                                 Release the brake = 0
                                 Set the steer to +15/-15 to the mean of navigation angles
                                 Set the mode to 'forward'
       
       Else  Check if no navigation angles is available :                          
           Try to move back set throttle = -1
           Set steer +=-15
           release the brake = 0
           Set the mode to 'forward'
           
       Check if Rover is near sample and is not pcking up :
           Set the send pickup flag
           Set the steer  = 0
           Apply brakes = 10
           Set the mode to 'stop'
         
 ### Driving Rover 
 
 #### Autonomous driving
 1) Run drive_rover.py
 2) Open the simulator on Windows ,  check the image linked below to see the configuration
 3) The telemetry data is recieved as frames (images) per second.Rover is updated with the current telemetry data , like position, pitch, 
     yaw, roll, velocity, near sample, picking up, sample count.
 4) Then the Rover updated data with image is sent for perspective transform and decision making.
 5) The output image is created by checking the worldmap and plotting on the ground map. Th ground map is overlapped with navigable pixels 
    and obstacles . if any rock is seen the rover turns to that direction and when it is near objective it is stop to pick the rock. Every 
    rock location is checked against the sample location and if rock is detected within 3 
    meters of known sample position, it is plotted on the groud map.
 6) Rover is able to map between 60-80 % . The maximum mapped result was around 99.1%. Fidelity sometimes reaches 60% and then it reduces 
    down to 40-44%. It is able to locate the rocks and pick them up.It also plots the located rock , but not all the times . Sometimes it 
    collects the rock but unable to plot it on the map.
    
### Issues and  Improvements
 1) Runs smoothly , but when Rover dashes into a big rock or moves over small rocks then the rover is not able to come out and move ahead 
    most of the times.
 2) Many a times the rock is located and gets collected but it is not plotted.
 3) Sometimes the Rover just get stuck and doesnot even move manually , seems to be simulator issue.
 4) It navigates the same terrain multiple times , so it needs to be flagged that the already navigated terrain should not be navigated 
    again.
 5) collecting rock sample is not a problem , but need to bring to the middle after collecting all needs to be worked upon.
 
 
### Images 
1)Simulator Configuration 
![alt text][image_4]


2)Image of the Rover in autonomous mode
![alt text][image_5]


    
   






