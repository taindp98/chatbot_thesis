import re

DEFINE_COMPARE = {}
DEFINE_COMPARE['lte'] = ["thấp","thap","thấp hơn","thap hon","giảm","tuột","nhỏ","nhỏ hơn","dưới","dưới mức","ít","ít hơn","tới","toi","đến","den","cỡ","khoảng","tầm","khoang","tam","đạt","được","dat","duoc","dc","đc"]
DEFINE_COMPARE['gte'] = ["cao","cao hơn","tren","cao hon","tăng","trên","trên mức","nhiều","nhiều hơn","từ","tu"]

def catch_point(mess):

    compare_flag = 'lte'
    for key in list(DEFINE_COMPARE.keys()):
        for value in DEFINE_COMPARE[key]:
            if (mess.find(value) != -1):
                compare_flag = key
            else:
                continue

    define_regex_point = r"[-+]?\d*\.\d+|\d+"
    list_point_regex = re.findall(define_regex_point,mess)
    list_point_float = [float(item) for item in list_point_regex]
    list_point_sort = sorted(list_point_float)

    list_point_res = []
    if len(list_point_sort) == 1:
        if compare_flag == 'lte':
            if list_point_sort[0] < 100 and list_point_sort[0] >= 30:
                list_point_res.append(float(30))
                list_point_res.append(list_point_sort[0])

            elif list_point_sort[0] < 1000 and list_point_sort[0] >= 100:
                list_point_res.append(float(100))
                list_point_res.append(list_point_sort[0])
            elif list_point_sort[0] < 30:
                list_point_res.append(float(0))
                list_point_res.append(list_point_sort[0])
        else:
            if list_point_sort[0] < 100 and list_point_sort[0] >= 30:
                list_point_res.append(list_point_sort[0])
                list_point_res.append(float(100))

            elif list_point_sort[0] < 1000 and list_point_sort[0] >= 100:
                list_point_res.append(list_point_sort[0])
                list_point_res.append(float(1000))
            elif list_point_sort[0] < 30:
                list_point_res.append(list_point_sort[0])
                list_point_res.append(float(30))

    elif len(list_point_sort) > 1:
        if len(list_point_sort) == 2:
            list_point_res = list_point_sort.copy()
        else:
            list_point_res.append(list_point_sort[-2])
            list_point_res.append(list_point_sort[-1])

    return list_point_res

# mess = 'điểm ngành nào tầm điểm không ạ'
# confirm_obj = catch_point(mess)
# print(confirm_obj)
