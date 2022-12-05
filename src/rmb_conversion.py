#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time  : 2022/12/5 23:14
# @Author: lionel

import re

MONEY_PATTERN = '([0-9,，.]+?)[百千万亿]'
UPPER_DIGITS = '[壹贰叁肆伍陆柒捌玖拾一二三四五六七八九十两俩]'
UPPER_MONEY_PATTERN = '([零壹贰叁肆伍陆柒捌玖拾佰仟万亿一二三四五六七八九十百千两俩]+?)[元圆]' \
                      '[零]?([壹贰叁肆伍陆柒捌玖一二三四五六七八九两俩])角[零]?([壹贰叁肆伍陆柒捌玖一二三四五六七八九两俩])分'
UPPER_MONEY_PATTERN2 = '([零壹贰叁肆伍陆柒捌玖拾佰仟万亿一二三四五六七八九十百千两俩]+?)[元圆][零]?([壹贰叁肆伍陆柒捌玖一二三四五六七八九两俩])角'
UPPER_MONEY_PATTERN3 = '([零壹贰叁肆伍陆柒捌玖拾佰仟万亿一二三四五六七八九十百千两俩]+?)[元圆][零]?([壹贰叁肆伍陆柒捌玖一二三四五六七八九两俩])分'
UPPER_MONEY_PATTERN4 = '([零壹贰叁肆伍陆柒捌玖拾佰仟万亿一二三四五六七八九十百千两俩]+?)[元圆]'
UPPER_MONEY_PATTERN5 = '([壹贰叁肆伍陆柒捌玖一二三四五六七八九两俩][零壹贰叁肆伍陆柒捌玖拾佰仟万亿一二三四五六七八九千两俩]{1,})'
CHINESE_DIGITS = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖', '拾', '俩',
                  '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '两']
CHINESE_UNITS = ['拾', '佰', '仟', '万', '亿', '千', '百', '十']
UPPER_TO_LOWER = {'零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '拾': 10, '一': 1,
                  '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '两': 2, '俩': 2, '1': 1,
                  '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}


def is_number(text):
    if not text:
        return False, text
    if len(re.findall('\.', text)) > 1 \
            or re.findall('^[，,.]', text) \
            or re.findall('[.，,]$', text):
        return False, text
    if re.findall('^[0-9.,，]+$', text):
        text = re.sub('[，,]', '', text)
        return True, text
    return False, text


def qian_money_parse(text):
    digit = 0.0
    if not text:
        return None
    for ele in re.finditer('(.*?)[千仟]', text):
        start, end = ele.span()
        key = re.sub('[千仟]$', '', ele.group())
        if key.isdigit():
            digit += 1000.0 * int(key)
        else:
            key = re.sub('^零', '', key)
            if key in UPPER_TO_LOWER.keys():
                digit += 1000.0 * UPPER_TO_LOWER[key]
            else:
                return -1
        text = text[end:]
        break
    if not text:
        return digit

    for ele in re.finditer('(.*?)[百佰]', text):
        start, end = ele.span()
        key = re.sub('[百佰]$', '', ele.group())
        if key.isdigit():
            digit += 100.0 * int(key)
        else:
            key = re.sub('^零', '', key)
            if key in UPPER_TO_LOWER.keys():
                digit += 100.0 * UPPER_TO_LOWER[key]
            else:
                return -1
        text = text[end:]
        break
    if not text:
        return digit

    for ele in re.finditer('(.*?)[十拾]', text):
        start, end = ele.span()
        key = re.sub('[十拾]$', '', ele.group())
        if key.isdigit():
            digit += 10.0 * int(key)
        else:
            key = re.sub('^零', '', key)
            if key in UPPER_TO_LOWER.keys():
                digit += 10.0 * UPPER_TO_LOWER[key]
            elif not key:
                digit += 10.0 * 1
            else:
                return -1
        text = text[end:]
        break
    if not text:
        return digit

    key = re.sub('^零', '', text)
    if key in UPPER_TO_LOWER.keys():
        digit += UPPER_TO_LOWER[key]
    else:
        return -1
    return digit


def wan_money_parse(text):
    digit = 0.0
    if not text:
        return None
    for ele in re.finditer('(.*?)万', text):
        start, end = ele.span()
        key = re.sub('万$', '', ele.group())
        flag, key = is_number(key)
        if flag:
            digit += pow(10, 4) * float(key)
        else:
            tmp_digit = qian_money_parse(key)
            if not tmp_digit or tmp_digit == -1:
                return -1
            else:
                digit += pow(10, 4) * tmp_digit
        text = text[end:]
    if not text:
        return digit
    tmp_digit = qian_money_parse(text)
    if tmp_digit == -1:
        return -1
    else:
        digit += tmp_digit
    return digit


def yi_money_parse(text):
    digit = 0.0
    if not text or not re.findall(UPPER_DIGITS, text):
        return None
    for ele in re.finditer('(.*?)亿', text):
        start, end = ele.span()
        key = re.sub('亿$', '', ele.group())
        flag, key = is_number(key)
        if flag:
            digit += pow(10, 8) * float(key)
        else:
            tmp_digit = wan_money_parse(key)
            if not tmp_digit or tmp_digit == -1:
                return -1
            else:
                digit += pow(10, 8) * tmp_digit
        text = text[end:]
    if not text:
        return digit
    tmp_digit = wan_money_parse(text)
    if tmp_digit == -1:
        return -1
    else:
        digit += tmp_digit
    return digit


def money_parse(text):
    if not text:
        return None
    digit = 0.0
    yuan = None
    if re.findall(UPPER_MONEY_PATTERN, text):
        yuan, jiao, fen = tuple(re.findall(UPPER_MONEY_PATTERN, text)[0])
        jiao, fen = re.sub('^零', '', jiao), re.sub('^零', '', fen)
        if jiao in UPPER_TO_LOWER.keys():
            digit += 0.1 * UPPER_TO_LOWER[jiao]
        else:
            return -1
        if fen in UPPER_TO_LOWER.keys():
            digit += 0.01 * UPPER_TO_LOWER[fen]
        else:
            return -1
    elif re.findall(UPPER_MONEY_PATTERN2, text):
        yuan, jiao = tuple(re.findall(UPPER_MONEY_PATTERN2, text)[0])
        jiao = re.sub('^零', '', jiao)
        if jiao in UPPER_TO_LOWER.keys():
            digit += 0.1 * UPPER_TO_LOWER[jiao]
        else:
            return -1
    elif re.findall(UPPER_MONEY_PATTERN3, text):
        yuan, fen = tuple(re.findall(UPPER_MONEY_PATTERN3, text)[0])
        fen = re.sub('^零', '', fen)
        if fen in UPPER_TO_LOWER.keys():
            digit += 0.01 * UPPER_TO_LOWER[fen]
        else:
            return -1
    elif re.findall(UPPER_MONEY_PATTERN4, text):
        yuan = re.findall(UPPER_MONEY_PATTERN4, text)[0]
    elif re.findall(UPPER_MONEY_PATTERN5, text):
        yuan = re.findall(UPPER_MONEY_PATTERN5, text)[0]
    flag, yuan = is_number(yuan)
    if flag:
        digit += float(yuan)
        return digit
    if yuan:
        tmp_digit = yi_money_parse(yuan)
        if tmp_digit and tmp_digit != -1:
            digit += tmp_digit
            return digit
    return -1


def money_uniform(origin_money):
    amount = None
    punish_money = re.findall('^([0-9.]+)亿$', origin_money)
    if punish_money:
        flag, money = is_number(punish_money[0])
        if flag:
            amount = float(money) * 10000
            return amount
    punish_money = re.findall('^([0-9.]+)万$', origin_money)
    if punish_money:
        flag, money = is_number(punish_money[0])
        if flag:
            amount = float(money)
            return amount
    punish_money = re.findall('^([0-9.]+)[千仟]$', origin_money)
    if punish_money:
        flag, money = is_number(punish_money[0])
        if flag:
            amount = float(money) * 0.1
            return amount
    punish_money = re.findall('^([0-9.，]+)$', origin_money)
    if punish_money:
        flag, money = is_number(punish_money[0])
        if flag:
            amount = float(money) / 10000
            return amount
    return amount


if __name__ == '__main__':
    print(money_parse('一亿三万零贰拾'))
