package test

import (
	"io"
	// "fmt"
	"bytes"
	"net/http"
	"encoding/json"
	"net/http/httptest"

	"github.com/gin-gonic/gin"

	"github.com/x-few/xway/backend/initialize"
	"github.com/x-few/xway/backend/global"
	test_utils "github.com/x-few/xway/backend/utils/test"
)

var engine *gin.Engine

func ReinitDB() {
	// clean all data in db
	err := test_utils.CleanDB(global.DB)
	if err != nil {
		panic(err)
	}

	err = initialize.Tables(global.DB)
	if err != nil {
		panic(err)
	}
}

func init() {
	router := initialize.Initialize()

	ReinitDB()

	engine = router
}

func Encode(v interface{}) io.Reader {
	buf := new(bytes.Buffer)
	_ = json.NewEncoder(buf).Encode(v)
	return buf
}

func NewRequest(method string, path string, body interface{},
	headers map[string]string) *httptest.ResponseRecorder {

	req, _ := http.NewRequest(method, path, Encode(body))

	for k, v := range headers {
		req.Header.Add(k, v)
	}

	w := httptest.NewRecorder()
	engine.ServeHTTP(w, req)

	// var result map[string]interface{}
	// fmt.Println("--- request --- w.Body = ", w.Body)
	// fmt.Println("--- request --- w.Body.Bytes() = ", w.Body.Bytes())
	// json.Unmarshal(w.Body.Bytes(), &result)
	// // _ = json.NewDecoder(w.Body).Decode(&result)

	// fmt.Println("--- request ---")
	// for key, value := range result {
	// 	// Each value is an interface{} type, that is type asserted as a string
	// 	fmt.Println(key, value)
	// }

	// world := result["world"].(map[string]interface{})
	// for key2, value2 := range world {
	// 	// Each value is an interface{} type, that is type asserted as a string
	// 	fmt.Println(key2, value2)
	// }

	return w
}
