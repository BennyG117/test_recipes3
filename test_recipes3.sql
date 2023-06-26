
SELECT * FROM users;

SELECT * FROM users
LEFT JOIN recipes
ON recipes.user_id = user.id
WHERE users.id = id;

SELECT * FROM recipes;




INSERT INTO shows (name, description, instructions, date_cooked, under_30_minutes, user_id)
VALUES ('pop-tarts', 'on-the-go breakfast foor or sweet treat', 'throw in the toaster then eat, or just open and eat', 'June 24th, 2023', "Yes", '1');

INSERT INTO shows (title, network, release_date, description, user_id)
VALUES ('Stranger Things', 'Netflix', NOW(), "Fantasy Thriller show that takes place in the 80s", '1');

DELETE FROM shows WHERE id = 3;

INSERT INTO shows (title, network, release_date, description, user_id)
VALUES ('Stranger Things', 'Netflix', NOW(), "Fantasy Thriller show that takes place in the 80s", '3');