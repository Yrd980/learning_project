package case_go

import (
	"errors"
	"fmt"
)

type GlobalVariables struct {
	Variables map[string]string
}

func NewGlobalVariables() *GlobalVariables {
	var g GlobalVariables
	g.Variables = make(map[string]string)
	return &g
}

func Execute(code string) {
	var ast *SourceCode
	var err error

	g := NewGlobalVariables()

	if ast, err = parse(code); err != nil {
		panic(err)
	}

	if err = resolveAST(g, ast); err != nil {
		panic(err)
	}
}

func resolveAST(g *GlobalVariables, ast *SourceCode) error {
	if len(ast.Statements) == 0 {
		return errors.New("no statements found in the source code")
	}

	for _, statement := range ast.Statements {
		if err := resolveStatement(g, statement); err != nil {
			panic(err)
		}
	}
	return nil
}

func resolveStatement(g *GlobalVariables, statement Statement) error {
	if assignment, ok := statement.(*Assignment); ok {
		return resolveAssignment(g, assignment)
	} else if print, ok := statement.(*Print); ok {
		return resolvePrint(g,print)
	} else {
		return fmt.Errorf("unknown statement type: %T", statement)
	}
}

func resolveAssignment(g *GlobalVariables, assignment *Assignment) error {
	varName := ""
	if varName = assignment.Variable.Name; varName == "" {
		return errors.New("variable name cannot be empty")
	}
	g.Variables[varName] = assignment.String
	return nil
}

func resolvePrint(g *GlobalVariables, print *Print) error {
	varName := ""
	if varName = print.Variable.Name; varName == "" {
		return errors.New("variable name cannot be empty")
	}
	str := ""
	ok := false
	if str, ok = g.Variables[varName]; !ok {
		return fmt.Errorf("variable '%s' not found", varName)
	}
	fmt.Println(str)
	return nil
}

