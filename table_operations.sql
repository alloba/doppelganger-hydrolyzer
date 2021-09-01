create table if not exists  connection_data
(
    "source"   TEXT,
    "target"   TEXT,
    "distance" NUMBER
);

create table if not exists rgb_averages
(
    "source"   TEXT,
    "r"   NUMBER,
    "g"   NUMBER,
    "b"   NUMBER
);

drop table if exists connection_data;
drop table if exists rgb_averages;