drop table if exists station_info;
drop table if exists dynamic_info;

create table station_info (
  id integer primary key,
  number integer not null,
  name text not null,
  address text not null,
  latitude integer not null,
  longitude integer not null
);

create table dynamic_info (
  id integer primary key,
  number integer not null,
  status text not null,
  bike_stands integer not null,
  available_bike_stands integer not null,
  available_bikes integer not null,
  last_update timestamp not null
);

