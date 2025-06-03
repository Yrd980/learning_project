package case_go

import (
	"fmt"
	"regexp"
	"strings"
)

const (
	TOKEN_EOF = iota
	TOKEN_VAR_PREFIX
	TOKEN_LEFT_PAREN
	TOKEN_RIGHT_PAREN
	TOEKN_EQUAL
	TOKEN_QUOTE
	TOKEN_DUOQUOTE
	TOKEN_NAME
	TOKEN_PRINT
	TOKEN_IGNORED
)

var tokenNameMap = map[int]string{
	TOKEN_EOF:         "EOF",
	TOKEN_VAR_PREFIX:  "$",
	TOKEN_LEFT_PAREN:  "(",
	TOKEN_RIGHT_PAREN: ")",
	TOKEN_EQUAL:       "=",
	TOKEN_QUOTE:       "\"",
	TOKEN_DUOQUOTE:    "\"\"",
	TOKEN_NAME:        "Name",
	TOKEN_PRINT:       "print",
	TOKEN_IGNORED:     "Ignored",
}

var keywords = map[string]int{
	"print": TOKEN_PRINT,
}

var regexName = regexp.MustCompile(`^[_\d\w]+`)

type Lexer struct {
	sourceCode       string
	lineNum          int
	nextToken        string
	nextTokenType    int
	nextTokenLineNum int
}

func NewLexer(sourceCode string) *Lexer {
	return &Lexer{sourceCode, 1, "", 0, 0}
}

func (lexer *Lexer) GetLineNum() int {
	return lexer.lineNum
}

func (lexer *Lexer) nextSouceCodeIs(s string) bool {
	return strings.HasPrefix(lexer.sourceCode, s)
}

func (lexer *Lexer) skipSourceCode(n int) {
	lexer.sourceCode = lexer.sourceCode[n:]
}

func (lexer *Lexer) isIgnored() bool {
	isIgnored := false
	isNewLine := func(c byte) bool {
		return c == '\r' || c == '\n'
	}
	isWhitespace := func(c byte) bool {
		switch c {
		case '\t', '\n', '\v', '\f', '\r', ' ':
			return true
		}
		return false
	}

	for len(lexer.sourceCode) > 0 {
		if lexer.nextSouceCodeIs("\r\n") || lexer.nextSouceCodeIs("\n\r") {
			lexer.skipSourceCode(2)
			lexer.lineNum += 1
			isIgnored = true
		} else if isNewLine(lexer.sourceCode[0]) {
			lexer.skipSourceCode(1)
			lexer.lineNum += 1
			isIgnored = true
		} else if isWhitespace(lexer.sourceCode[0]) {
			lexer.skipSourceCode(1)
			isIgnored = true
		} else {
			break
		}
	}
	return isIgnored
}

func (lexer *Lexer) scan(regex *regexp.Regexp) string {
	if token := regexp.FindString(lexer.sourceCode); token != "" {
		lexer.skipSourceCode(len(token))
		return token
	}
	panic("unreachable!")
}

func (lexer *Lexer) scanName() string {
	return lexer.scan(regexName)
}

func (lexer *Lexer) scanBeforeToken(token string) string {
	s := strings.Split(lexer.sourceCode,token)
	if len(s) < 2 {
		panic("unreachable!")
	}
	lexer.skipSourceCode(len(s[0]))
	return s[0]
}

func isLetter(c byte) bool {
	return c >= 'a' && c <= 'z' || c >= 'A' && c <= 'Z'
}

func (lexer *Lexer) MatchToken() (lineNum int, tokenType int, token string) {

	if lexer.isIgnored() {
		return lexer.lineNum, TOKEN_IGNORED, tokenNameMap[TOKEN_IGNORED]
	}

	if len(lexer.sourceCode) == 0 {
		return lexer.lineNum, TOKEN_EOF, tokenNameMap[TOKEN_EOF]
	}

	switch lexer.sourceCode[0] {
	case '$':
		lexer.skipSourceCode(1)
		return lexer.lineNum, TOKEN_VAR_PREFIX, tokenNameMap[TOKEN_VAR_PREFIX]
	case '(':
		lexer.skipSourceCode(1)
		return lexer.lineNum, TOKEN_LEFT_PAREN, tokenNameMap[TOKEN_LEFT_PAREN]
	case ')':
		lexer.skipSourceCode(1)
		return lexer.lineNum, TOKEN_RIGHT_PAREN, tokenNameMap[TOKEN_RIGHT_PAREN]
	case '=':
		lexer.skipSourceCode(1)
		return lexer.lineNum, TOEKN_EQUAL, tokenNameMap[TOEKN_EQUAL]
	case '"':
		if lexer.nextSouceCodeIs("\"\"") {
			lexer.skipSourceCode(2)
			return lexer.lineNum, TOKEN_DUOQUOTE, tokenNameMap[TOKEN_DUOQUOTE]
		}
		lexer.skipSourceCode(1)
		return lexer.lineNum, TOKEN_QUOTE, tokenNameMap[TOKEN_QUOTE]
	}

	if lexer.sourceCode[0] == '_' || isLetter(lexer.sourceCode[0]) {
		token := lexer.scanName()
		if tokenType, isMatch := keywords[token]; isMatch {
			return lexer.lineNum, tokenType, token
		} else {
			return lexer.lineNum, TOKEN_NAME, token
		}
	}

	err := fmt.Sprintf("MatchToken(): syntax error near '%s' at line %d.", lexer.sourceCode, lexer.lineNum)
	panic(err)
}

func (lexer *Lexer) GetNextToken() (lineNum int, tokenType int, token string) {
	if lexer.nextTokenLineNum > 0 {
		lineNum = lexer.nextTokenLineNum
		tokenType = lexer.nextTokenType
		token = lexer.nextToken
		lexer.lineNum = lexer.nextTokenLineNum
		lexer.nextTokenLineNum = 0
		return
	}
	return lexer.MatchToken()
}

func (lexer *Lexer) NextTokenIs(tokenType int) (lineNum int, token string) {
	nowLineNum, nowTokenType, nowToken := lexer.GetNextToken()
	if tokenType != nowTokenType {
		err := fmt.Sprintf("NextTokenIs(): syntax error near '%s', expected token: {%s} but got {%s}.", tokenNameMap[nowTokenType], tokenNameMap[nowTokenType], nowLineNum)
		panic(err)
	}
	return nowLineNum, nowToken
}

func (lexer *Lexer) LookAheadAndSkip(expectedType int) {
	nowLineNum := lexer.lineNum
	lineNum, tokenType, token := lexer.GetNextToken()
	if tokenType != expectedType {
		lexer.lineNum = nowLineNum
		lexer.nextTokenLineNum = lineNum
		lexer.nextTokenType = tokenType
		lexer.nextToken = token
	}
}

func (lexer *Lexer) LookAhead() int {
	if lexer.nextTokenLineNum > 0 {
		return lexer.nextTokenType
	}

	nowLineNum := lexer.lineNum
	lineNum, tokenType, token := lexer.GetNextToken()
	lexer.lineNum = nowLineNum
	lexer.nextTokenLineNum = lineNum
	lexer.nextTokenType = tokenType
	lexer.nextToken = token
	return tokenType
}

