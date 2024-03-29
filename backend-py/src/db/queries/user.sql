-- name: list-user
SELECT * FROM users ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-user$
SELECT count(*) from users;


-- name: add-user<!
INSERT INTO users (
    id,
    username,
    email,
    salt,
    password,
    status,
    type,
    creator
)
VALUES (
    :id,
    :username,
    :email,
    :salt,
    :password,
    :status,
    :type,
    :creator
)
RETURNING
    id,
    created,
    updated;


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