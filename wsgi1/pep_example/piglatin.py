#
# pig latin 형식으로 문자열을 바꿔주는 메소드
# https://www.geeksforgeeks.org/encoding-word-pig-latin/
#
# @author      Seongeun Yu (s3ich4n@gmail.com)
# @date        2021/11/28 16:27 created.
# @modified    2021/11/28 16:27 modified.
# @copyright   Subject to the copyright of the above link.
#


def is_vowel(c):
    return (c == 'A' or c == 'E' or c == 'I' or
            c == 'O' or c == 'U' or c == 'a' or
            c == 'e' or c == 'i' or c == 'o' or
            c == 'u')


def piglatin(s):
    # the index of the first vowel is stored.
    length = len(s)
    index = -1
    for i in range(length):
        if is_vowel(s[i]):
            index = i
            break

    # Pig Latin is possible only if vowels
    # is present
    if index == -1:
        return "-1"

    # Take all characters after index (including
    # index). Append all characters which are before
    # index. Finally append "ay"
    #
    # 미들웨어의 마지막에, 문자열을 리턴해줘야할 때는 encode 를 해주고
    # 마지막에 인코딩 재-세팅시 처리할 수 있는 형태로 주어야한다.
    #
    return (s[index:] + s[0:index] + "ay").encode("UTF-8")
