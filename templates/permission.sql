-- name: list-permissions
SELECT * FROM permission ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-permissions
SELECT count(id) from permission;


-- name: get-permission-by-id^
SELECT * FROM permission where id = :id;


-- name: delete-permission-by-id<!
DELETE FROM permission where id = :id RETURNING id;


-- name: add-permission<!
INSERT INTO permission (
    "name",
    "uri",
    "description",
    "method",
    "status"
)
VALUES (
    :name,
    :uri,
    :description,
    :method,
    :status
)
RETURNING id, created;


-- name: update-permission-by-id<!
UPDATE
    permission
SET
    "name" = :name,
    "uri" = :uri,
    "description" = :description,
    "method" = :method,
    "status" = :status
WHERE id = :id
RETURNING updated;
