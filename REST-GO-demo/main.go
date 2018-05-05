package main

import (
	"fmt"
	"./services"
)

func main() {
	fmt.Println("火币")
	r := services.GetKLine("btcusdt", "1min", 50)
	fmt.Println(r)
}
