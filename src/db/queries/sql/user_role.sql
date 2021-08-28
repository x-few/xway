-- name: list-user_roles
SELECT * FROM user_role ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-user_roles
SELECT count(id) from user_role;


-- name: get-user_role-by-id^
SELECT * FROM user_role where id = :id;


-- name: delete-user_role-by-id<!
DELETE FROM user_role where id = :id RETURNING id;


-- name: add-user_role<!
INSERT INTO user_role (
    "user_id",
    "role_id"
)
VALUES (
    :user_id,
    :role_id
)
RETURNING id, created;


-- name: update-user_role-by-id<!
UPDATE
    user_role
SET
    "user_id" = :user_id,
    "role_id" = :role_id
WHERE id = :id
RETURNING updated;
