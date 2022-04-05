
package api

import (
	"github.com/gin-gonic/gin"
)

func GetUserList(c *gin.Context) {
	c.String(200, "hello list")
}

func GetUserInfo(c *gin.Context) {
	c.String(200, "hello info")
}

func AddUser() {

}
