# Import Libraries
import cv2
import sys
from random import randint

# Tracker Types
tracker_types = ['BOOSTING',
                 'MIL',
                 'KCF',
                 'TLD',
                 'MEDIANFLOW',
                 'GOTURN',
                 'MOSSE',
                 'CSRT']

# Define trackers by name
def tracker_name(tracker_type):
    # Create trackers by name with if statement
    if tracker_type == tracker_types[0]:
        tracker = cv2.TrackerBoosting_create()
    elif tracker_type == tracker_types[1]:
        tracker = cv2.TrackerMIL_create()
    elif tracker_type == tracker_types[2]:
        tracker = cv2.TrackerKCF_create()
    elif tracker_type == tracker_types[3]:
        tracker = cv2.TrackerTLD_create()
    elif tracker_type == tracker_types[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif tracker_type == tracker_types[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif tracker_type == tracker_types[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif tracker_type == tracker_types[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('No tracker found')
        print('Choose from these trackers: ')
        for tr in tracker_types:
            print(tr)
            
    # return
    return tracker

if __name__ == '__main__':
    print("Default tracking algorithm MOSSE \n"
        "Available algorithms are: \n")
    for tr in tracker_types:
        print(tr)
        
    tracker_type = 'MOSSE'
    # Create a video capture
    cap = cv2.VideoCapture('Video/Vehicles.mp4')
    # Read first frame
    success, frame = cap.read()
    
    # Quit if failure
    if not success:
        print('Cannot read the video')
    
    # Select boxes and colors
    rects = []
    colors = []
    
    # While loop
    while True:
    
        # draw rectangles, select ROI, open new window
        rect_box = cv2.selectROI('MultiTracker', frame)
        rects.append(rect_box)
        colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
        print('Press q to stop selecting boxes and start multitracking')
        print('Press any key to select another box')
        
        
        #close window
        if cv2.waitKey(0) & 0xFF == 113:
            break
        
    # print message
    print(f'Selected boxes {rects}')
    
    
    # Create multitracker
    multi_tracker = cv2.MultiTracker_create()
    
    # Initialize multitracker
    for rect_box in rects:
        multi_tracker.add(tracker_name(tracker_type),
                         frame,
                         rect_box)
    
    #Video and Tracker
    # while loop
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        # update location objects
        success, boxes = multi_tracker.update(frame)
        
        # draw the objects tracked
        for i, newbox in enumerate(boxes):
            pts1 = (int(newbox[0]),
                   int(newbox[1]))
            pts2 = (int(newbox[0] + newbox[2]),
                   int(newbox[1] + newbox[3]))
            cv2.rectangle(frame,
                         pts1,
                         pts2,
                         colors[i],
                         2,
                         1)
        
        # display frame
        cv2.imshow('Multitracker', frame)
    
        # Close the frame
        if cv2.waitKey(30) & 0xFF == 27:
            break
    
    # Release and Destroy
    cap.release()
    cv2.destroyAllWindows()

