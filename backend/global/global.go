package global

import (
	"gorm.io/gorm"
	"github.com/spf13/viper"
	"github.com/sony/sonyflake"

	"github.com/x-few/xway/backend/model/config"
)

var (
	DB     	*gorm.DB
	CONFIG  config.Config
	VIPER   *viper.Viper
	SF      *sonyflake.Sonyflake
)
