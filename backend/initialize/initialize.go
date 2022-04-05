package initialize

import (
	"fmt"
	"log"

	"github.com/gin-gonic/gin"

	"github.com/x-few/xway/backend/global"
)

func Initialize() *gin.Engine {
	// initialize
	global.VIPER = Viper(&global.CONFIG)
	db, err := Database()
	if err != nil {
		log.Fatal("init database failed: ", err)
	}

	global.DB = db

	err = Tables(global.DB)
	if err != nil {
		log.Fatal("init table failed: ", err)
	}

	fmt.Println("config = ", global.CONFIG)

	err = Snowflake()
	if err != nil {
		log.Fatal("init snowflake failed: ", err)
	}

	// TODO init middlewares

	// init router
	router := Router()

	return router
}
