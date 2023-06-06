import pandas as pd
import numpy as np

def open_file(file_name):
    try:
        with open(file_name, 'r') as file:
            print("Đang xử lý...")
            # Thực hiện xử lý tệp tin ở đây
    except FileNotFoundError:
        print("Không tìm thấy tệp:", file_name)

def kiemtrahople(file_name):
    valid_lines = []
    invalid_count = 0  # Số dòng dữ liệu không hợp lệ

    with open(file_name, 'r') as file:
        lines = file.readlines()

        # Báo cáo tổng số dòng dữ liệu được lưu trữ trong tệp
        total_lines = len(lines)
        print("Tổng số dòng dữ liệu được lưu trữ trong tệp:", total_lines)

        # Kiểm tra từng dòng dữ liệu
        for line in lines:
            line = line.strip()
            data = line.split(',')

            # Kiểm tra độ dài dữ liệu
            if len(data) != 26:
                print("Bài nộp không hợp lệ, không đủ 26 kí tự:", line)
                invalid_count += 1
                continue

            # Kiểm tra ID của sinh viên
            student_id = data[0]
            if not (student_id.startswith('N') and student_id[1:].isdigit() and len(student_id) == 9):
                print("Bài nộp không hợp lệ, ID không đúng:", line)
                invalid_count += 1
                continue

            # Dòng dữ liệu hợp lệ, thêm vào danh sách valid_lines
            valid_lines.append(line)

    # Báo cáo tổng số dòng dữ liệu hợp lệ trong tệp
    valid_count = len(valid_lines)
    print("Tổng số dòng dữ liệu hợp lệ trong tệp:", valid_count)

    # In tổng số dòng dữ liệu không hợp lệ
    print("Tổng số dòng dữ liệu không hợp lệ trong tệp:", invalid_count)

    return valid_lines


def chamdiem(valid_lines, file_name, key="B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"):
    # Đọc dữ liệu từ tệp
    with open(file_name, 'r') as file:
        data = file.readlines()

    answers = [line.strip().split(',') for line in valid_lines]

    scores = []
    skipped_questions = {}
    wrong_answers = {}

    key = key.split(',')

    # Tính điểm cho từng học sinh
    for i in range(len(answers)):
        answer = answers[i]
        score = 0
        skipped_count = 0
        wrong_count = 0

        # Kiểm tra từng câu trả lời
        for j in range(1, len(answer)):
            if answer[j] == '':
                skipped_count += 1
                # Lưu các câu hỏi bị bỏ qua
                if j not in skipped_questions:
                    skipped_questions[j] = 0
                skipped_questions[j] += 1
            elif answer[j] == key[j - 1]:
                score += 4
            else:
                score -= 1
                wrong_count += 1
                # Lưu các câu hỏi bị trả lời sai
                if j not in wrong_answers:
                    wrong_answers[j] = 0
                wrong_answers[j] += 1

        scores.append(score)

    # Thống kê số liệu và in kết quả
    if scores:
        num_students = len(scores)
        max_score = max(scores)
        min_score = min(scores)
        total_score = sum(scores)
        average_score = total_score / num_students
        score_range = max_score - min_score

        sorted_scores = sorted(scores)
        median = 0

        # Tính toán trung vị
        if num_students % 2 == 0:
            middle1 = num_students // 2
            middle2 = middle1 - 1
            median = (sorted_scores[middle1] + sorted_scores[middle2]) / 2
        else:
            middle = num_students // 2
            median = sorted_scores[middle]

        # In kết quả thống kê
        print("Số lượng sinh viên đạt điểm cao (>80 điểm):", len([score for score in scores if score > 80]))
        print("Điểm trung bình:", round(average_score, 3))
        print("Điểm cao nhất:", max_score)
        print("Điểm thấp nhất:", min_score)
        print("Miền giá trị của điểm:", score_range)
        print("Giá trị trung vị:", round(median, 3))

        print("Các câu hỏi bị học sinh bỏ qua nhiều nhất:")
        max_skipped = max(skipped_questions.values()) if skipped_questions else 0
        for question, count in skipped_questions.items():
            if count == max_skipped:
                skip_rate = count / num_students * 100
                print(f"Số thứ tự câu hỏi: {question} - Số lượng học sinh bỏ qua: {count} - Tỷ lệ bị bỏ qua: {round(skip_rate, 3)}%")

        print("Các câu hỏi bị học sinh trả lời sai nhiều nhất:")
        max_wrong = max(wrong_answers.values()) if wrong_answers else 0
        for question, count in wrong_answers.items():
            if count == max_wrong:
                wrong_rate = count / num_students * 100
                print(f"Số thứ tự câu hỏi: {question} - Số lượng học sinh trả lời sai: {count} - Tỷ lệ trả lời sai: {round(wrong_rate, 3)}%")

    else:
        print("Không có dữ liệu hợp lệ để thống kê.")

    # Trả về điểm cho từng sinh viên
    return scores

def ketqua(file_name, valid_lines, scores):
    if scores:
        answers = [line.strip().split(',') for line in valid_lines]

        # Lấy số ID của từng học sinh
        student_ids = [answer[0] for answer in answers]

        # Ghi kết quả vào tệp
        output_file = file_name.replace('.txt', '_grades.txt')
        with open(output_file, 'w') as file:
            for i in range(len(scores)):
                file.write(f"{student_ids[i]},{scores[i]}\n")

        return output_file

    else:
        return None

def main():
    file_name = input("Nhập class: ") + '.txt'

    open_file(file_name)
    valid_lines = kiemtrahople(file_name)
    scores = chamdiem(valid_lines, file_name)
    if scores:
        ketqua(file_name, valid_lines, scores)

main()

