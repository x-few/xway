package test

import (
	"testing"
	// "reflect"

	"github.com/stretchr/testify/assert"

	"github.com/x-few/xway/backend/utils/snowflake"
)

func TestSnowflake(t *testing.T) {
	h := make(map[uint64]bool)
	for i := 0; i < 1024; i++ {
		id := snowflake.GetID()
		assert.IsType(t, uint64(0), id)
		assert.Greater(t, id, uint64(1))
		assert.NotContains(t, h, id)
		h[id] = true
	}
}
