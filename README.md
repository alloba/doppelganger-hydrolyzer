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

## Misc Notes

- Data set is 18.6 GB at time of writing. 
- Slightly over 5000 files in the dataset.


