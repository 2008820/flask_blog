package main

import (
	"net/http"
	"time"
)

func main() {
	url := "http://0.0.0.0:5000"
	for i:=0; i< 10000; i++ {
		go http.Get(url)
	}
	time.Sleep(time.Second)
}
