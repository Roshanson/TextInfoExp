# encoding:utf-8
import xlwt
import os


class Write2File:
    def __init__(self):
        pass

    @staticmethod
    def append(filepath, content):
        if filepath is not None:
            with open(filepath, "a") as f:
                f.write(content)

    @staticmethod
    def write(filepath, content):
        if filepath is not None:
            with open(filepath, "w") as f:
                f.write(content)

    @staticmethod
    def write_contents(filepath, contents):
        if os.path.exists(filepath):
            os.remove(filepath)

        if isinstance(contents, list) and isinstance(contents[0], tuple):
            wb = xlwt.Workbook()
            ws = wb.add_sheet("Sheet 1")

            for i, (head, content) in enumerate(contents):
                ws.write(0, i, head)
                ws.write(1, i, content)

            wb.save(filepath)
        elif isinstance(contents, list) and isinstance(contents[0], list) and isinstance(contents[0][0], tuple):
            wb = xlwt.Workbook()
            ws = wb.add_sheet("Sheet 1")

            i = 0
            # write the head
            for j, (head, _) in enumerate(contents[0]):
                ws.write(i, j, head)

            # write the content
            for a_content in contents:
                i += 1
                for j, (_, content) in enumerate(a_content):
                    ws.write(i, j, content)

            wb.save(filepath)
        else:
            print("The output format is wrong!")

    @staticmethod
    def write_results(origin_labels, classify_labels, filepath):
        wb = xlwt.Workbook()
        sh = wb.add_sheet("results")
        for i in range(len(origin_labels)):
            sh.write(i, 0, origin_labels[i])
            sh.write(i, 1, int(classify_labels[i]))
        wb.save(filepath.split(".")[0] + "_label.xls")


def get_accuracy(origin_labels, classify_labels, parameters):
    assert len(origin_labels) == len(classify_labels)

    print 'result'
    print classify_labels
    print len(classify_labels)

    print 'ori'
    print origin_labels
    print len(origin_labels)

    xls_contents = []

    xls_contents.extend([("train num", parameters[0]), ("test num", parameters[1])])
    xls_contents.append(("feature num", parameters[2]))

    pos_right, pos_false = 0, 0
    neg_right, neg_false = 0, 0
    for i in range(len(origin_labels)):
        if origin_labels[i] == 1:
            if classify_labels[i] == 1:
                pos_right += 1         # 负负11
            else:
                neg_false += 1         # 负正10
        else:
            if classify_labels[i] == 0:
                neg_right += 1         # 正正00
            else:
                pos_false += 1         # 正负01
    xls_contents.extend([("neg-right", neg_right), ("neg-false", neg_false)])
    xls_contents.extend([("pos-right", pos_right), ("pos-false", pos_false)])

    print (neg_right, pos_right, neg_false, pos_false)

    pos_precision = float(pos_right) / (pos_right + pos_false) * 100
    pos_recall = float(pos_right) / (pos_right + neg_false) * 100
    pos_f1 = 2 * pos_precision * pos_recall / (pos_precision + pos_recall) if pos_precision + pos_recall != 0 else 1
    xls_contents.extend([("pos-precision", pos_precision), ("pos-recall", pos_recall), ("pos-f1", pos_f1)])

    neg_precision = float(neg_right) / (neg_right + neg_false) * 100
    neg_recall = float(neg_right) / (neg_right + pos_false) * 100
    neg_f1 = 2 * neg_precision * neg_recall / (neg_precision + neg_recall) if neg_precision + neg_recall != 0 else 1
    xls_contents.extend([("neg-precision", neg_precision), ("neg-recall", neg_recall), ("neg-f1", neg_f1)])

    total_recall = float(neg_right + pos_right) / (neg_right + neg_false + pos_right + pos_false) * 100
    xls_contents.append(("total-recall", total_recall))

    print("    pos-right\tpos-false\tneg-right\tneg-false\tpos-precision\tpos-recall\t"
          "pos-f1\tneg-precision\tneg-recall\tneg-f1\ttotal-recall")
    print("    " + "---" * 45)
    print("    %8d\t%8d\t%8d\t%8d\t%8.4f\t%8.4f\t%8.4f\t%8.4f\t%8.4f\t%8.4f\t%8.4f" %
          (pos_right, pos_false, neg_right, neg_false, pos_precision, pos_recall,
           pos_f1, neg_precision, neg_recall, neg_f1, total_recall))

    return xls_contents
