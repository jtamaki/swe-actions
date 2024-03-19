import adoc_validator

def test_validate_encoding():
    raw = '文字列'.encode(encoding='utf-8')
    errors = adoc_validator.validate_encoding('filename.adoc', raw)
    assert len(errors) == 0

    raw = '文字列'.encode(encoding='shift_jis')
    errors = adoc_validator.validate_encoding('filename.adoc', raw)
    assert len(errors) == 1
    assert errors[0].line == 0
    assert errors[0].message == 'File encoding is not UTF-8'

    raw = '文字列'.encode(encoding='euc_jp')
    errors = adoc_validator.validate_encoding('filename.adoc', raw)
    assert len(errors) == 1
    assert errors[0].line == 0
    assert errors[0].message == 'File encoding is not UTF-8'

def test_validate_line_ending():
    lines = [
        'LF\n',
        'LF\n',
        'LF\n',
    ]
    errors = adoc_validator.validate_line_ending('filename.adoc', lines)
    assert len(errors) == 0

    lines = [
        'LF\n',
        'CRLF\r\n',
        'LF\n',
    ]
    errors = adoc_validator.validate_line_ending('filename.adoc', lines)
    assert len(errors) == 1
    assert errors[0].line == 2
    assert errors[0].message == 'File line endings are not LF'

    lines = [
        'LF\n',
        'LF\n',
        'CR\r',
    ]
    errors = adoc_validator.validate_line_ending('filename.adoc', lines)
    assert len(errors) == 1
    assert errors[0].line == 3
    assert errors[0].message == 'File line endings are not LF'

def test_validate_char():
    lines = [
        '全角スペース　',
    ]
    errors = adoc_validator.validate_char('filename.adoc', lines)
    assert len(errors) == 1
    assert errors[0].line == 1
    assert errors[0].message == 'Contains invalid char(full width space)'

    lines = [
        '全角開きカッコ（',
        '全角閉じカッコ）',
    ]
    errors = adoc_validator.validate_char('filename.adoc', lines)
    assert len(errors) == 2
    assert errors[0].line == 1
    assert errors[0].message == 'Contains invalid char(full width paren)'
    assert errors[1].line == 2
    assert errors[1].message == 'Contains invalid char(full width paren)'

    lines = [
        '全角英字Ａ',
        '全角英字Ｂ',
        '全角英字Ｚ',
        '全角英字ａ',
        '全角英字ｂ',
        '全角英字ｚ',
    ]
    errors = adoc_validator.validate_char('filename.adoc', lines)
    assert len(errors) == 6
    assert errors[0].line == 1
    assert errors[0].message == 'Contains invalid char(full width alphabet)'
    assert errors[1].line == 2
    assert errors[1].message == 'Contains invalid char(full width alphabet)'
    assert errors[2].line == 3
    assert errors[2].message == 'Contains invalid char(full width alphabet)'
    assert errors[3].line == 4
    assert errors[3].message == 'Contains invalid char(full width alphabet)'
    assert errors[4].line == 5
    assert errors[4].message == 'Contains invalid char(full width alphabet)'
    assert errors[5].line == 6
    assert errors[5].message == 'Contains invalid char(full width alphabet)'

    lines = [
        '全角数字０',
        '全角数字１',
        '全角数字９',
    ]
    errors = adoc_validator.validate_char('filename.adoc', lines)
    assert len(errors) == 3
    assert errors[0].line == 1
    assert errors[0].message == 'Contains invalid char(full width numeric)'
    assert errors[1].line == 2
    assert errors[1].message == 'Contains invalid char(full width numeric)'
    assert errors[2].line == 3
    assert errors[2].message == 'Contains invalid char(full width numeric)'

    lines = [
        '全角記号！',
        '全角記号“',
        '全角記号”',
        '全角記号＃',
        '全角記号＄',
        '全角記号％',
        '全角記号＆',
        '全角記号‘',
        '全角記号’',
        '全角記号＊',
        '全角記号＋',
        '全角記号，',
        '全角記号．',
        '全角記号／',
        '全角記号：',
        '全角記号；',
        '全角記号＜',
        '全角記号＝',
        '全角記号＞',
        '全角記号？',
        '全角記号＠',
        '全角記号［',
        '全角記号￥',
        '全角記号］',
        '全角記号＾',
        '全角記号＿',
        '全角記号‘',
        '全角記号｛',
        '全角記号｜',
        '全角記号｝',
        '全角記号～',
    ]
    errors = adoc_validator.validate_char('filename.adoc', lines)
    assert len(errors) == 31
    assert errors[0].line == 1
    assert errors[0].message == 'Contains invalid char(full width symbol)'
    assert errors[-1].line == 31
    assert errors[-1].message == 'Contains invalid char(full width symbol)'

def test_validate_multiple_whitespaces():
    lines = [
        '1つの 半角スペース',
        '2つの  半角スペース',
        '3つの   半角スペース',
    ]
    errors = adoc_validator.validate_multiple_whitespaces('filename.adoc', lines)
    assert len(errors) == 2
    assert errors[0].line == 2
    assert errors[0].message == 'Multiple consecutive whitespaces'
    assert errors[1].line == 3
    assert errors[1].message == 'Multiple consecutive whitespaces'

def test_validate_multiple_empty_lines():
    lines = [
        '\n',        
        '1つの空行\n',
        '\n',
        '1つの空行\n',
        '1つの空行\n',
        '\n',
    ]
    errors = adoc_validator.validate_multiple_empty_lines('filename.adoc', lines)
    assert len(errors) == 0

    lines = [
        '\n',        
        '\n',        
        '2つの空行\n',
        '\n',
        '2つの空行\n',
        '2つの空行\n',
        '\n',
        '\n',
    ]
    errors = adoc_validator.validate_multiple_empty_lines('filename.adoc', lines)
    assert len(errors) == 2
    assert errors[0].line == 2
    assert errors[0].message == 'Multiple consecutive empty lines'
    assert errors[1].line == 8
    assert errors[1].message == 'Multiple consecutive empty lines'

    lines = [
        '\n',        
        '\n',        
        '\n',
        '3つの空行\n',
        '\n',
        '3つの空行\n',
        '3つの空行\n',
        '\n',
        '\n',
        '\n',
    ]
    errors = adoc_validator.validate_multiple_empty_lines('filename.adoc', lines)
    assert len(errors) == 4
    assert errors[0].line == 2
    assert errors[0].message == 'Multiple consecutive empty lines'
    assert errors[1].line == 3
    assert errors[1].message == 'Multiple consecutive empty lines'
    assert errors[2].line == 9
    assert errors[2].message == 'Multiple consecutive empty lines'
    assert errors[3].line == 10    
    assert errors[3].message == 'Multiple consecutive empty lines'

def test_validate_blank_line_at_file_end():
    lines = [
        '改行で終わる\n',
        '改行で終わる\n',
        '改行で終わる\n',
    ]
    errors = adoc_validator.validate_blank_line_at_file_end('filename.adoc', lines)
    assert len(errors) == 0

    lines = [
        '改行で終わっていない\n',
        '改行で終わっていない\n',
        '改行で終わっていない',
    ]
    errors = adoc_validator.validate_blank_line_at_file_end('filename.adoc', lines)
    assert len(errors) == 1
    assert errors[0].line == 3
    assert errors[0].message == 'File does not end with a newline'
