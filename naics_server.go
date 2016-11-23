package main

import (
	"flag"
	"log"
	"net/http"
)

func main() {
	var prod = flag.Bool("production", false, "determines whether to run in production mode")
	flag.Parse()

	var port = ":7000"
	if *prod {
		port = ":80"
	}

	// Simple static webserver:
	log.Fatal(http.ListenAndServe(port, http.FileServer(http.Dir("./"))))
}
