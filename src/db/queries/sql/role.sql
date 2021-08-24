-- name: list-roles
SELECT * FROM role ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-roles
SELECT count(id) from role;


-- name: get-role-by-id^
SELECT * FROM role where id = :id;


-- name: delete-role-by-id<!
DELETE FROM role where id = :id RETURNING id;


-- name: add-role<!
INSERT INTO role (
    "name",
    "description"
)
VALUES (
    :name,
    :description
)
RETURNING id, created;


-- name: update-role-by-id<!
UPDATE
    role
SET
    "name" = :name,
    "description" = :description
WHERE id = :id
RETURNING updated;
