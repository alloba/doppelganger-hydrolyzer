-- distances of less than 500 are strong candidates for being either the exact same entire file, or the exact same video.
-- although this is not guaranteed to be the case.
-- anything below 15000 i'd say gets close to being the same general primary color scheme. being generous.
-- at max distance, you tend to be purely looking at bright/white as a primary color vs dark/black between the two files.
select * from connection_data c
where c.source is not c.target
order by c.distance
limit 5000;


-- Interesting Features --

-- pure black being registered is not very common, these are generally either fade ins or outs in the video.
select count(source), * from rgb_averages where b is 0 and g is 0 and r is 0 group by source;

-- These are not always duplicates, but they kind of tend to be.
select * from connection_data where distance is 0 and source is not target;

-- DATA CLEANING --
delete from rgb_averages where source == 'source'; -- import errors. should be fixed now, but keeping query for a bit.
delete from connection_data where distance == 0 and connection_data.source is connection_data.target; -- these are distance-to-self. not needed.
delete from connection_data where source not in (select avgs.source from rgb_averages avgs); --distances of corrupt files. invalid data points.

