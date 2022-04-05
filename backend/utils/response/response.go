package response

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"github.com/x-few/xway/backend/utils/constant"
)

type Result struct {
	Status int       `json:"status"`
	Data interface{} `json:"data"`
}

type PageResult struct {
	Status int       `json:"status"`
	Data interface{} `json:"data"`
	Total    int64   `json:"total"`
}

func Response(c *gin.Context, status int, data interface{},
	total, httpStatusOptional ...int) {

	httpStatus := http.StatusOK
	if len(httpStatusOptional) > 0 {
		httpStatus = httpStatusOptional[0]
	}

	if total == nil {
		c.JSON(httpStatus, Result{
			status,
			data,
		})
	} else {
		c.JSON(httpStatus, Result{
			status,
			data,
			total,
		})
	}
}

func Ok(c *gin.Context, data interface{}, totalOptional ...int64) {
	total := nil
	if len(totalOptional) > 0 {
		total = totalOptional[0]
	}

	Response(c, constant.RESPONSE_STATUS_OK, data, total)
}

func Err(c *gin.Context, data interface{}, httpStatusOptional ...int) {
	total := nil
	if len(totalOptional) > 0 {
		total = totalOptional[0]
	}

	Response(c, constant.RESPONSE_STATUS_ERR, data, nil, httpStatusOptional)
}
