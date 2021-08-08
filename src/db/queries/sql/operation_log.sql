-- name: count-all-oplog
SELECT count(id) from operation_log;


-- name: get-all-oplog
SELECT id, op, path, new, old, creator, created, updated FROM operation_log ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: get-oplog-by-id
SELECT id, op, path, new, old, creator, created, updated FROM operation_log and id > :id ORDER BY id desc;


-- name: add-oplog<!
INSERT INTO operation_log (op, path, new, old, creator)
VALUES (:op, :path, :new::jsonb, :old::jsonb, :creator)
RETURNING id, created, updated;