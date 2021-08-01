-- name: list-login-record
SELECT * FROM login_record where uid = :uid ORDER BY id desc LIMIT :limit OFFSET :offset;


-- name: count-login-record
SELECT count(id) from login_record where uid = :uid;


-- name: add-login-record<!
INSERT INTO login_record (uid, host, type, token) VALUES (:uid, :host, :type, :token) RETURNING id, created;


-- name: get-login-record-by-id^
SELECT * FROM login_record where id = :id;
