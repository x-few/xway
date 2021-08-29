-- name: list-role-permissions
SELECT * FROM role_permission ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-role-permissions
SELECT count(id) from role_permission;


-- name: get-role-permission-by-id^
SELECT * FROM role_permission where id = :id;


-- name: delete-role-permission-by-id<!
DELETE FROM role_permission where id = :id RETURNING id;


-- name: add-role-permission<!
INSERT INTO role_permission (
    "role_id",
    "permission_id"
)
VALUES (
    :role_id,
    :permission_id
)
RETURNING id, created;


-- name: update-role-permission-by-id<!
UPDATE
    role_permission
SET
    "role_id" = :role_id,
    "permission_id" = :permission_id
WHERE id = :id
RETURNING updated;
