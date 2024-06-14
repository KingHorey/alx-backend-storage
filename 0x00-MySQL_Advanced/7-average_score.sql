-- CREATE PROCEDURE

DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser (IN users_id INT)
BEGIN
   DECLARE avg_score FLOAT;
   SELECT AVG(score) INTO avg_score FROM corrections WHERE user_id = users_id;
   UPDATE users
   SET average_score = avg_score WHERE id = users_id;
END;
//
DELIMITER ;
