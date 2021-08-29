-- name: list-login-logs
SELECT * FROM login_log where user_id = :user_id ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-login-logs
SELECT count(id) from login_log where user_id = :user_id;


-- name: get-login-log-by-id^
SELECT * FROM login_log where id = :id;


-- name: delete-login-log-by-id<!
DELETE FROM login_log where id = :id RETURNING id;


-- name: add-login-log<!
INSERT INTO login_log (
    "user_id",
    "host",
    "type",
    "status"
)
VALUES (
    :user_id,
    :host,
    :type,
    :status
)
RETURNING id, created;
