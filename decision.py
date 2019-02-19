import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward':           
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                print ('Rover navigation Forward mode')

                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)                 # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                    #Rover.vel = Rover.max_vel
                else: # Else coast
                    Rover.throttle = 0
            
                if (len(Rover.nav_dists) < 5000):
                    Rover.throttle= 0.2
                                  
                Rover.brake = 0               

                if(Rover.rock_traced):
                    Rover.throttle = 0.2
                    Rover.steer = np.clip(np.mean(Rover.rock_angles * 180/np.pi), -15, 15) 
                                    # Set steering to average angle clipped to the range +/- 15
                print ('All Clear','vel =',Rover.vel)
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward or len(Rover.nav_dists)<700:
                    # Set mode to "stop" and hit the brakes!
                    print('lot of rocks in stop_forward')
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                  #  Rover.steer =-15
                    Rover.mode = 'stop'
                                                
        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop'and not Rover.near_sample:
            print ("What do I do in stop",'vel-',Rover.vel)
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                #Rover.steer = 0 
                #Rover.mode = 'forward'
            elif Rover.vel <=0.2:
                if len(Rover.nav_angles)< Rover.go_forward:
                    print("I am trying to get some vision")
                    Rover.throttle = 0
                    Rover.brake = 0
                    Rover.steer +=-15 
                elif len(Rover.nav_angles)>=Rover.go_forward:
                   # Rover.throttle = Rover.throttle_set
                    print("Got some vision")
                    Rover.brake = 0
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15) 
                    Rover.mode = 'forward'
            # If we're in stop mode but still moving keep braking
        
    # even if no modifications have been made to the code
    else:
        print('Oops no navigation terrain')
        Rover.throttle = -1
        #Rover.vel = -0.6
        Rover.steer +=-15               #Rover.steer = 0
        Rover.brake = 0
        Rover.mode = 'forward'
    
    # If in a state where want to pickup a rock send pickup command
    if (Rover.near_sample and not Rover.picking_up):

        Rover.send_pickup = True
        Rover.steer = 0
        Rover.brake = Rover.brake_set
       # Rover.picking_up = True
        Rover.mode = 'stop'
        
    
    return Rover