package initialize

import (
    "errors"
    "regexp"

    "gorm.io/gorm"
    "gorm.io/driver/postgres"

    "github.com/x-few/xway/backend/global"
    "github.com/x-few/xway/backend/model"
)

func GormConfig() *gorm.Config {
	config := &gorm.Config{ DisableForeignKeyConstraintWhenMigrating: true }

	return config
}

func Postgres() (*gorm.DB, error) {
    config := global.CONFIG.Database
    if config.Dbname == "" {
        return nil, errors.New("dbname is empty")
    }

    pgsqlConfig := postgres.Config{
        DSN:                  config.Dsn(),
        PreferSimpleProtocol: false,
    }

    db, err := gorm.Open(postgres.New(pgsqlConfig), GormConfig())

    if err != nil {
        matched, _ := regexp.MatchString(`SQLSTATE 3D000`, err.Error())
        if ! matched {
            return nil, err
        }

        // database does not exist, created it
        newPgsqlConfig := postgres.Config{
            DSN:                  config.DsnWithoutDBName(),
            PreferSimpleProtocol: false,
        }

        db, err = gorm.Open(postgres.New(newPgsqlConfig), GormConfig())
        if err != nil {
            return nil, err
        }

        err = db.Exec("CREATE DATABASE " + config.GetDBName()).Error
        if err != nil {
            return nil, err
        }

        // TODO: should i close the previous db?

        db, err = gorm.Open(postgres.New(pgsqlConfig), GormConfig())
        if err != nil {
            return nil, err
        }
    }

    sqlDB, _ := db.DB()
    sqlDB.SetMaxIdleConns(config.MaxIdleConns)
    sqlDB.SetMaxOpenConns(config.MaxOpenConns)
    return db, nil
}

func Mysql() (*gorm.DB, error) {
    return nil, nil
}

func Database() (*gorm.DB, error) {
    switch global.CONFIG.Database.Type {
    case "postgres":
        return Postgres()
    case "mysql":
        return Mysql()
    default:
        return Postgres()
    }
}

func Tables(db *gorm.DB) error {
    return db.AutoMigrate(
        model.Users{},
        model.KVConfigs{},
    )
}
