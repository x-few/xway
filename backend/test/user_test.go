package test

import (
	// "net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestUser(t *testing.T) {
	resp := NewRequest("POST", "/api/v1/login", nil, nil)

	assert.Equal(t, 200, resp.Code)
}
