function docx_to_markdown
    pandoc $argv[1] -f docx -t markdown -o $argv[1]
end

