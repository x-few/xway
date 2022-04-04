package main

import (
	"fmt"
	"time"
	"log"
	"syscall"

	"github.com/fvbock/endless"

	"github.com/x-few/xway/backend/global"
	"github.com/x-few/xway/backend/initialize"

)

func main() {
	// initialize
	global.VIPER = initialize.Viper(&global.CONFIG)
	db, err := initialize.Database()
	if err != nil {
		log.Fatal("init database failed: ", err)
	}

	global.DB = db

	err = initialize.Tables(global.DB)
	if err != nil {
		log.Fatal("init table failed: ", err)
	}

	fmt.Println("config = ", global.CONFIG)

	// TODO init middlewares

	// init router
	router := initialize.Router()

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
        log.Printf("Actual pid is %d", syscall.Getpid())
    }

	err = server.ListenAndServe()
    if err != nil {
        log.Printf("Server err: %v", err)
    }
}
