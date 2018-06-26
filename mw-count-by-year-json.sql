SELECT array_to_json(array_agg(row_to_json(t)))
FROM(
  SELECT sum("Men") as men, sum("Women") as women, count("Id") as movies, "Year" as year
  FROM movie_gender
  WHERE "Fetched" = True  and "Valid" = True and "Unset" = 0 and "Year" >= 1930
  GROUP BY "Year"
  ORDER BY "Year"
) t;
