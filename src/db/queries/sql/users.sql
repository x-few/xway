-- name: get-all-user
SELECT id, username, email, created, updated, status FROM users;


-- name: add-user<!
INSERT INTO users (username, email, salt, password, status)
VALUES (:username, :email, :salt, :password, :status)
RETURNING
    id, created, updated;