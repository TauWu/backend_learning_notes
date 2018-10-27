package handler

import (
	"fmt"
	"net/http"
)

func testHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "This is a test handler.")
}
