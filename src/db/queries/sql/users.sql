-- name: get-all-user
SELECT id, username, email, created, updated, status FROM users;


-- name: add-user<!
INSERT INTO users (username, email, salt, password, status)
VALUES (:username, :email, :salt, :password, :status)
RETURNING
    id, created, updated;


-- name: get-user-by-id^
SELECT id, username, email, salt, password, status, created, updated FROM users where id = :id;


-- name: get-user-by-username^
SELECT id, username, email, salt, password, status, created, updated FROM users where username = :username;


-- name: get-user-by-email^
SELECT id, username, email, salt, password, status, created, updated FROM users where email = :email;

