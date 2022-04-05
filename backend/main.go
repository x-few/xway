package main

import (
	"fmt"
	"time"
	"log"
	"syscall"

	"github.com/fvbock/endless"
	"github.com/gin-gonic/gin"

	"github.com/x-few/xway/backend/global"
	"github.com/x-few/xway/backend/initialize"

)


func start(Router *gin.Engine) {
	// start server
	address := fmt.Sprintf("%s:%d",
		global.CONFIG.Server.Host,
		global.CONFIG.Server.Port)

	// router.Run(address)
	server := endless.NewServer(address, Router)

	server.ReadHeaderTimeout = 20 * time.Second
	server.ReadTimeout = 20 * time.Second
	server.WriteTimeout = 20 * time.Second
	server.MaxHeaderBytes = 1 << 20

	server.BeforeBegin = func(add string) {
        log.Printf("Actual pid is %d", syscall.Getpid())
    }

	err := server.ListenAndServe()
    if err != nil {
        log.Printf("Server err: %v", err)
    }
}

func main() {
	router := initialize.Initialize()
	start(router)
}
