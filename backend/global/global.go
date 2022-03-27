package global

import (
	"gorm.io/gorm"
	"github.com/spf13/viper"

	"github.com/x-few/xway/backend/config"
)

var (
	DB     	*gorm.DB
	CONFIG 	config.Config
	VIPER 	*viper.Viper
)
