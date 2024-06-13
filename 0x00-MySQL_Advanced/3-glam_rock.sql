-- RETURN NUMBER OF BAN WITH GLAM_ROCK AS STYLE

SELECT band_name, IFNULL(split - formed, 2022 - formed) as lifespan from metal_bands WHERE style REGEXP '.*Glam rock.*' ORDER BY lifespan DESC;
