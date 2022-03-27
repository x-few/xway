package main

import (
	"fmt"
	"time"
	"log"
	"syscall"

	"github.com/gin-gonic/gin"
	"github.com/fvbock/endless"

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
	address := fmt.Sprintf("%s:%d",
		global.CONFIG.Server.Host,
		global.CONFIG.Server.Port)

	// router.Run(address)
	server := endless.NewServer(address, router)

	server.ReadHeaderTimeout = 20 * time.Second
	server.ReadTimeout = 20 * time.Second
	server.WriteTimeout = 20 * time.Second
	server.MaxHeaderBytes = 1 << 20

	server.BeforeBegin = func(add string) {
		global.MASTER_PID = syscall.Getpid()
        log.Printf("Actual pid is %d", syscall.Getpid())
    }

	err := server.ListenAndServe()
    if err != nil {
        log.Printf("Server err: %v", err)
    }
}
