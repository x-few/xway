package initialize

import (
	"github.com/gin-gonic/gin"

	"github.com/x-few/xway/backend/router"
)

func Router() *gin.Engine {
	r := gin.Default()

	g := r.Group("/api")
	v1 := g.Group("/v1")

	{
		router.InitLoginRouter(v1)
		router.InitUserRouter(v1)
	}

	return r
}
