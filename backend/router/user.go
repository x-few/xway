package router

import (
	"github.com/gin-gonic/gin"

	"github.com/x-few/xway/backend/api"
)

func InitUserRouter(Router *gin.RouterGroup) {
	userRouter := Router.Group("user")
	{
		userRouter.GET("", api.GetUserList)
		userRouter.GET(":id", api.GetUserInfo)
	}
}
