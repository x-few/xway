-- name: get-all-users
SELECT * FROM users ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-all-users
SELECT count(id) from users;


-- name: add-user<!
INSERT INTO users (username, email, salt, password, status, creator)
VALUES (:username, :email, :salt, :password, :status, :creator)
RETURNING id, created, updated;


-- name: get-user-by-id^
SELECT * FROM users where id = :id;


-- name: get-user-by-username^
SELECT * FROM users where username = :username;


-- name: get-user-by-email^
SELECT * FROM users where email = :email;


-- name: delete-user-by-id<!
DELETE FROM users where id = :id RETURNING id;


-- name: update-user-by-id<!
UPDATE
    users
SET username        = :username,
    email           = :email,
    salt            = :salt,
    password        = :password,
    status          = :status
WHERE id = :id
RETURNING
    updated;