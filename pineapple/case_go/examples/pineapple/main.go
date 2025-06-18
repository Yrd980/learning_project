package main

import (
	"os"
	"fmt"
	"case_go/src"
)

func main() {
	args := os.Args
	if len(args) != 2 {
		fmt.Println("Usage: %s filename\n", args[0])
		return
	}
	filename := args[1]
	code, err := os.ReadFile(filename)
	if err != nil {
		fmt.Println("error reading file:", err)
		return
	}

	case_go.Execute(string(code))
}
