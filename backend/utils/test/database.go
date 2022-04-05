package test

import (
	"gorm.io/gorm"
)

func CleanDB(db *gorm.DB) error {
	sql := `
		BEGIN;
		DROP SCHEMA public CASCADE;
		CREATE SCHEMA public;
		GRANT ALL ON SCHEMA public TO postgres;
		GRANT ALL ON SCHEMA public TO public;
		COMMIT;
	`
	tx := db.Exec(sql)
	if tx.Error != nil {
		return tx.Error
	}

	return nil
}
