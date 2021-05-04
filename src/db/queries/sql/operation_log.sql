
-- name: get-oplog-by-owner
SELECT id, op, path, new, old, owner, creator, created, updated FROM operation_log where owner = :owner ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-oplog-by-owner
SELECT count(id) from operation_log where owner=:owner;


-- name: add-oplog<!
INSERT INTO operation_log (op, path, new, old, owner, creator)
VALUES (:op, :path, :new::jsonb, :old::jsonb, :owner, :creator)
RETURNING id, created, updated;