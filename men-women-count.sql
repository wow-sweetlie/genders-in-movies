SELECT sum("Men") as men, sum("Women") as women, count("Id") as movies
FROM movie_gender
WHERE "Fetched" = True  and "Valid" = True and "Unset" = 0;
