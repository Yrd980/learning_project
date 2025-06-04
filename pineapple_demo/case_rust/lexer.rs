use std::collections::HashMap;

#[derive(Clone,Copy,PartialEq,Debug)]
pub enum TokenType {
    Eof,
    VarPrefix,
    LeftBracket,
    RightBracket,
    Equal
    String,
    Name,
    Print,
    Ignored,
    None,
}

#[derive(Clone,Debug)]
pub struct Token(pub TokenType, pub usize, pub Option<String>);

pub struct Lexer {
    source: Vec<String>,
    line: usize,
    ptr: usize,
    pub next_token_info: TokenType,
    next_token: Token,
    keywords: HashMap<String, TokenType>,
}

impl Lexer {
    pub fn new(source: String) -> Self {
        let mut hash = HashMap::new();
        hash.insert("print".to_string(), TokenType::Print);
        Lexer {
            source: source.split('\n').map(|s| s.to_string()).collect(),
            line: 0,
            ptr: 0,
            next_token_info: TokenType::None,
            next_token: Token(TokenType::None, 0, None),
            keywords: hash,
        }
    }
}

fn scan_name(&self, s:&str, start: usize) -> (usize, String) {
    let codes = &s[start..];
    let mut i = 0;
    for c in codes.chars() {
        match c {
            '_' | 'a' ..= 'z' | 'A' ..= 'Z' | '0' ..= '9' => i += 1
            _ => break,
        }
    }
    (i, codes[0..i].to_string())
}

fn scan_string(&self, s:&str, start: usize) -> (usize, String) {
    let codes = &s[start..];
    let mut i = 0;
    for c in codes.chars() {
        match c {
            '"' => break,
            _ => i += 1,
        }
    }
    (i + 1, codes[0..i].to_string())
}
