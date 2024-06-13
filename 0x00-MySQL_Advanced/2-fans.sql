-- SORT THE NUMBER OF FANS FOR EACH BANK BASED ON ORIGIN

SELECT origin, sum(fans) as nb_fans from metal_bands GROUP BY origin ORDER BY nb_fans DESC;
