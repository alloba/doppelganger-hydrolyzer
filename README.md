# Doppelganger Hydrolyzer

This project is meant to categorize and find similarities between a dataset of videos.

This is an offshoot project created as a way to gather more information about a dataset that I have been collecting 
for a bit now. Basically a large uncategorized bunch of video files. 

## Approach 

Naive implementation is going to win the day here initially. The first idea I pulled out of a think about it was to 
take the average color of each frame of a video, and store this information. This would survive differest aspect ratios 
and resolutions decently enough, and if I make the data accessible via relative position on a timeline instead of literal
position of the frame, the issue of different runtimes can be sidestepped a bit. 

Although also, probably don't want to rule out runtimes and sizes entirely. maybe something to think about as things 
develop more. To start with it'll be fine maybe. 

Supporting libraries seem to be relatively few in number. I'm not really about writing a binary decoder for 
whatever video file is getting worked on, so something more plug and play. In that regard there seems to be a 
couple of things that make use of ffmpeg, and some approaches with opencv. 

I kind of like the idea of using something one layer deeper like ffmpeg, but I'm not sure if it gives a good 
avenue to keep things loaded into memory the way I want for data operations. OpenCV would definitely do the job, 
but it weighs a metric tonne. Not clear installation instructions for Mac either, honestly. 

MoviePy might be a nice simple solution. It's very oriented towards video editing though.

## Misc Notes

- Data set is 18.6 GB at time of writing. 
- Slightly over 5000 files in the dataset.
- some videos fail to process. This is probably due to a bug(?) in versions of ffmpeg. 
  the file has a goofed image buffer or whatever, and it errors out. 
  ffmpeg itself can bypass this with a flag (`-max_muxing_queue_size 9999`), but this really doesn't trickle down 
  to the opencv usage. and workarounds with the os environment seem to not work either. 
    - trying the conda version of opencv to see if it uses a newer version of ffmpeg without the issue. (didnt)
    - `ffmpeg -vsync drop -i broken.webm -vcodec copy new.webm`
