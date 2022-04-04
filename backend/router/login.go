package router

import (
	"github.com/gin-gonic/gin"

	"github.com/x-few/xway/backend/api"
)

func InitLoginRouter(Router *gin.RouterGroup) {
	Router.POST("/login", api.Login)
}
