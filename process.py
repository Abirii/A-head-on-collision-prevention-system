'''
process functions:
save_to_procedure() - Save procedure images.
show_image() - Show image, press ESC to stop
break_video_to_frames() - Break a given video to frames and store them in a list. Return that list
'''

import cv2 as cv

# Show image, press ESC to stop
def show_image(string,image):
    if image is None:
        print("Failed to upload image")
        return

    while True:
        cv.imshow(string,image)
        if cv.waitKey(1) & 0xFF == 27:
            break

# Save procedure images
def save_to_procedure(file_name,file):
    file_path = 'Images/Procedure/'+file_name
    cv.imwrite(file_path,file)


#Break a given video to frames and store them in a list. Return that list
def break_video_to_frames(video):
    cap = cv.VideoCapture(video)
    # Grab the current frame.
    check, vid = cap.read()

    counter = 0
    # Initialize the value  of check variable
    check = True
    # List of frames
    frame_list = []

    while (check == True):
        # Check value is false and the last frame is None in the end of the video
        check, vid = cap.read()
        # Add each frame in the list
        frame_list.append(vid)
        counter += 1
    # Remove the last frame (None)
    frame_list.pop()
    return frame_list
