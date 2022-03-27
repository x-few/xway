package initialize

import (
    "gorm.io/gorm"
    "gorm.io/driver/postgres"

    "github.com/x-few/xway/backend/global"
)

func GormConfig() *gorm.Config {
	config := &gorm.Config{ DisableForeignKeyConstraintWhenMigrating: true }

	return config
}

func Postgres() *gorm.DB {
    config := global.CONFIG.Database
    if config.Dbname == "" {
        return nil
    }

    pgsqlConfig := postgres.Config{
        DSN:                  config.Dsn(),
        PreferSimpleProtocol: false,
    }
    if db, err := gorm.Open(postgres.New(pgsqlConfig), GormConfig()); err != nil {
        return nil
    } else {
        sqlDB, _ := db.DB()
        sqlDB.SetMaxIdleConns(config.MaxIdleConns)
        sqlDB.SetMaxOpenConns(config.MaxOpenConns)
        return db
    }
}

func Mysql() *gorm.DB {
    return nil
}

func Database() *gorm.DB {
    switch global.CONFIG.Database.Type {
    case "postgres":
        return Postgres()
    case "mysql":
        return Mysql()
    default:
        return Postgres()
    }
}
