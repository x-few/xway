-- name: get-user-login-record
SELECT * FROM login_record ORDER BY id desc LIMIT :limit OFFSET :offset where uid = :uid;


-- name: count-user-login-record
SELECT count(id) from login_record where uid = :uid;


-- name: add-login-record<!
INSERT INTO login_record (uid, host) VALUES (:uid, :host) RETURNING id, created;


-- name: get-login-record-by-id^
SELECT * FROM login_record where id = :id;
