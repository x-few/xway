package snowflake

import (
	"time"

	"github.com/x-few/xway/backend/global"
)

// Get unique id from Twitter's Snowflake
func GetID() uint64 {
	sleep := 1
	for {
		id, err := global.SF.NextID()
		if err == nil {
			return id
		}

		time.Sleep(time.Duration(sleep) * time.Millisecond)
		sleep *= 2
	}
}
