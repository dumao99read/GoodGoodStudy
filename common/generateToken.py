"""生成token"""



def split_into_pairs(key_word):
    if len(key_word) % 2 != 0:
        raise ValueError('必须为偶数个。')
    return [key_word[i:i+2] for i in range(0, len(key_word), 2)]
def generate_token(key_word):
    pair_list = split_into_pairs(key_word)
    token_list = []
    for numbers in pair_list:
        if int(numbers) > 26:
            temp_list = list(numbers)
            for number in temp_list:
                token_member = chr(int(number) + 64)
                token_list.append(token_member)
        else:
            token_member = chr(int(numbers) + 64)
            token_list.append(token_member)
    token = ''.join(token_list)
    return token

if __name__ == '__main__':
    key_word = '2027'
    token = generate_token(key_word)
    print(token)