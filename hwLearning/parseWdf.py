
def check_multi_func(string_list):
    stack = []
    index_list = []
    result = []
    for i, char in enumerate(string_list):
        temp_char = string_list[i]
        if string_list[i] == '(':
            stack.append(temp_char)  # 记录一个括号标识
        elif temp_char == ')' and stack:
            stack.pop()  # 弹出一个括号标识
        elif temp_char == ',' and not stack:
            index_list.append(i)  # 如果逗号不在括号内，则记录它的索引位置


    index_start = 0
    if index_list:  # 如果index_list中记录了括号外逗号的索引位置，就根据索引拆分出各函数，添加到result列表中
        for index_end in index_list:
            single_func = string_list[index_start:index_end]
            result.append(single_func)
            index_start += index_end + 1
            result.append(string_list[index_end + 1:])  # 例如3个函数，只会有2个逗号，这一行就能获取到最后一个函数
        return result
    else:
        result.append(string_list)
        return result  # 如果index_list中没有记录到括号外逗号，就说明string_list是一个单函数
