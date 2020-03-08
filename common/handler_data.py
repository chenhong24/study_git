import re
from common.handleconfig import conf


class CaseData:
    """专门用来保存执行过程中提取出来给其他用例用的数据"""
    pass


def replace_data(s):
    r1 = r"#(.+?)#"
    while re.search(r1, s):
        res = re.search(r1, s)
        data = res.group()
        key = res.group(1)
        try:
            # s = s.sub(r1, conf.get("test_data", key), s, 1)
            s = s.replace(data, conf.get("test_data", key))
        except Exception:
            s = s.replace(data, getattr(CaseData, key))
            # s = s.sub(r1, getattr(CaseData, key), s, 1)
    return s


if __name__ == '__main__':
    pass


