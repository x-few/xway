-- name: get-user-login-record
SELECT * FROM login ORDER BY id desc LIMIT :limit OFFSET :offset where uid = :uid;


-- name: count-user-login-record
SELECT count(id) from login where uid = :uid;


-- name: add-login-record<!
INSERT INTO login (uid, host) VALUES (:uid, :host) RETURNING id, created;


-- name: get-login-record-by-id^
SELECT * FROM users where id = :id;
