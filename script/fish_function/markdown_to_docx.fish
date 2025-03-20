function markdown_to_docx
    if not test -f $argv[1]
        echo "请提供一个有效的 Markdown 文件"
        return 1
    end

    set input_file $argv[1]
    set output_file (basename $input_file .md).docx
    pandoc $input_file -o $output_file

    echo "转换完成，输出文件为: $output_file"
end

