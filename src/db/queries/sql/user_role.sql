-- name: list-user-roles
SELECT * FROM user_role ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-user-roles
SELECT count(id) from user_role;


-- name: get-user-role-by-id^
SELECT * FROM user_role where id = :id;


-- name: delete-user-role-by-id<!
DELETE FROM user_role where id = :id RETURNING id;


-- name: add-user-role<!
INSERT INTO user_role (
    "id",
    "user_id",
    "role_id"
)
VALUES (
    :id,
    :user_id,
    :role_id
)
RETURNING id, created;


-- name: update-user-role-by-id<!
UPDATE
    user_role
SET
    "user_id" = :user_id,
    "role_id" = :role_id
WHERE id = :id
RETURNING updated;
