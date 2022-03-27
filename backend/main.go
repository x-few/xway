package main

import (
	"fmt"

	"github.com/gin-gonic/gin"

	"github.com/x-few/xway/backend/global"
	"github.com/x-few/xway/backend/initialize"
)

func main() {
	// initialize
	global.VIPER = initialize.Viper(&global.CONFIG)
	global.DB = initialize.Database()

	fmt.Println("config = ", global.CONFIG)

	// init router
	router := gin.Default()
	router.GET("/hello", func(c *gin.Context) {
		c.String(200, "world")
	})

	// start server
	router.Run(":" + global.CONFIG.Server.Port)
}
