show databases;
use project;
#understanding data:
select count(*) from rapidorides; # 50000
select * from rapidorides;
describe rapidorides;

# data cleaning
select count(*) from rapidorides where ride_status='cancelled';
set sql_safe_updates=0;
update rapidorides set ride_charge=0 where ride_status='cancelled';
update rapidorides set misc_charge=0 where ride_status='cancelled';
update rapidorides set total_fare=0 where ride_status='cancelled';
update rapidorides set payment_method='cancelled' where ride_status='cancelled';

# to check whether all null values are handled:
SELECT COUNT(*) FROM rapidorides WHERE ride_charge IS NULL OR misc_charge IS NULL OR total_fare IS NULL
OR payment_method IS NULL;
#feature engineering:
alter table rapidorides add column distance_category text;
update rapidorides set distance_category = case
    when distance < 5 then 'short' 
    when distance between 5 and 15 then 'medium' 
    else 'long' 
end;
select * from rapidorides;

# analysis:
#total revenue and avg revenue: based on services: 
SELECT services,SUM(total_fare) AS total_revenue,AVG(total_fare) AS avg_fare
FROM rapidorides WHERE payment_method != 'cancelled' GROUP BY services order by total_revenue desc;
-- bike	7432783.949999977	547.8575919510561
-- auto	6099731.319999989	548.83312218823
-- cab economy	5006233.040000004	547.2489112374294
-- parcel	3686514.150000007	546.3930858159192
-- bike lite	2387720.589999999	544.1478099361893

SELECT distance_category,SUM(total_fare) AS total_revenue, AVG(total_fare) AS avg_revenue
FROM rapidorides WHERE payment_method != 'cancelled' GROUP BY distance_category order by total_revenue desc;
-- long	17559047.229999907	546.6531935493884
-- medium	5064196.179999989	550.1571080934264
-- short	1989739.6400000001	546.9322814733371

#Calculate the percentage of canceled rides versus completed rides for an overview of ride success.
SELECT ride_status, COUNT(*) AS count,(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM rapidorides)) AS percentage
FROM rapidorides GROUP BY ride_status;
-- completed	44964	89.92800
-- cancelled	5036	10.07200

# Find peak times of the day for rides 
SELECT HOUR(time) AS ride_hour,COUNT(*) AS ride_count
FROM rapidorides WHERE payment_method != 'cancelled'
GROUP BY HOUR(time) ORDER BY ride_count DESC limit 10;
-- hour  count
-- 11	1972
-- 9	1965
-- 8	1907
-- 10	1907
-- 21	1898
-- 5	1897
-- 7	1892
-- 18	1891
-- 13	1889
-- 17	1888
SELECT dayname(`date`) AS ride_day,COUNT(*) AS ride_count FROM rapidorides
WHERE payment_method != 'cancelled'
GROUP BY ride_day ORDER BY ride_count DESC;
# monday is most with 6679, tuesday-6659
#least count:Sunday 5916,Saturday 5913

# which payment method the is most used
SELECT payment_method,COUNT(*) AS method_count FROM rapidorides 
WHERE payment_method != 'cancelled' GROUP BY payment_method ORDER BY method_count DESC;
# paytm-11315
# minimum-qr scan 11156

#Find the most common pickup and drop-off locations by counting occurrences of source and destination.
SELECT source, COUNT(*) AS pickup_count FROM rapidorides
GROUP BY source ORDER BY pickup_count desc;
#most:Kothanur Landing	23

SELECT destination, COUNT(*) AS destination_count FROM rapidorides
GROUP BY destination ORDER BY destination_count desc;
#most:Gottigere Landing	 23

#Compare auto and cab services in terms of average fare, ride duration, and distance to understand performance differences.
SELECT services,AVG(total_fare) AS avg_fare, AVG(duration) AS avg_duration,AVG(distance) AS avg_distance
FROM rapidorides WHERE payment_method != 'cancelled' GROUP BY services;
-- cab economy	547.2489112374294	, 64.1835	, 25.498173371228646
-- auto	548.83312218823	, 65.0436	, 25.531251574590613
-- parcel	546.3930858159192	, 64.4175	, 25.649845857418182
-- bike lite	544.1478099361893, 	63.9724	, 25.646166818596235
-- bike	547.8575919510561	, 64.0363, 	25.353877791700263

    

             


