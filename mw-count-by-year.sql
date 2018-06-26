SELECT sum("Men") as men, sum("Women") as women, "Year" as year
FROM movie_gender
WHERE "Fetched" = True  and "Valid" = True and "Unset" = 0
GROUP BY "Year"
ORDER BY "Year"
