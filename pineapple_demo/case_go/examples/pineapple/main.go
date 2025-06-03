package main

import (
	"os"
	"fmt"
	"io/ioutil"
  "github.com/karminski/pineapple/src"
)

func main() {
	args := os.Args
	if len(args) != 2 {
		fmt.Println("Usage: %s filename\n", args[0])
		return
	}
	filename := args[1]
	code, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println("error reading file:", err)
		return
	}

	pineapple.Execute(string(code))
}
