-- create procedure for student Correction
DELIMITER //

DELIMITER //
CREATE PROCEDURE AddBonus (IN users_id INT, IN project_name VARCHAR(255), IN scores INT)
BEGIN
   DECLARE project_id INT;
   SELECT id INTO project_id FROM projects WHERE name = project_name;
   IF project_id IS NULL THEN
      INSERT INTO projects (name) VALUES (project_name);
      SET project_id = LAST_INSERT_ID();
   END IF;

   INSERT INTO corrections (user_id, project_id, score) VALUES (users_id, project_id, scores);
END;
//
