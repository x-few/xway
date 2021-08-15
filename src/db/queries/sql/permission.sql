-- name: list-permissions
SELECT * FROM permission ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-permissions
SELECT count(id) from permission;


-- name: get-permission-by-id^
SELECT * FROM permission where id = :id;


-- name: delete-permission-by-id<!
DELETE FROM permission where id = :id RETURNING id;



