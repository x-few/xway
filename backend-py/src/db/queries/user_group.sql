-- name: list-user-groups
SELECT * FROM user_group ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-user-groups$
SELECT count(*) from user_group;


-- name: get-user-group-by-id^
SELECT * FROM user_group where id = :id;


-- name: delete-user-group-by-id<!
DELETE FROM user_group where id = :id RETURNING id;


-- name: add-user-group<!
INSERT INTO user_group (
    "id",
    "name",
    "description",
    "creator"
)
VALUES (
    :id,
    :name,
    :description,
    :creator
)
RETURNING id, created;


-- name: update-user-group-by-id<!
UPDATE
    user_group
SET
    "name" = :name,
    "description" = :description
WHERE id = :id
RETURNING updated;
