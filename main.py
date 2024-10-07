import json
import re
import random_responses


# Tải dữ liệu JSON
def load_json(file):
    with open(file,  'r', encoding='utf-8') as bot_responses:
        return json.load(bot_responses)


# Lưu trữ dữ liệu JSON
response_data = load_json("data.json")

def get_response(input_string):
    # Kiểm tra nếu đầu vào trống hoặc chỉ chứa khoảng trắng
    if not input_string.strip():
        return "Tôi có thể giúp gì cho bạn."

    input_string_lower = input_string.lower().strip()

    # 1. Kiểm tra xem đầu vào có khớp với bất kỳ cụm từ nào trong 'user_input' không (Exact Match)
    for response in response_data:
        for phrase in response.get("user_input", []):
            if input_string_lower == phrase.lower():
                return response.get("bot_response", "Xin lỗi, tôi không hiểu bạn nói gì.")

    # 2. Nếu không có exact match, tiếp tục với phương pháp đánh giá dựa trên từ khóa
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string_lower)
    split_message = [word for word in split_message if word]  # Loại bỏ các chuỗi rỗng
    score_list = []

    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response.get("required_words", [])
        user_input_keywords = response.get("user_input", [])

        # Kiểm tra xem có chữ yêu cầu nào không ?
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

            # Số lượng từ yêu cầu phải khớp với số lượng từ trong 'required_words'
            if required_score == len(required_words):
                for word in split_message:
                    if word in user_input_keywords:
                        response_score += 1
            else:
                # Nếu không đủ từ yêu cầu, bỏ qua phản hồi này
                response_score = 0
        else:
            # Nếu không có từ yêu cầu, đánh giá dựa trên số từ trùng khớp
            for word in split_message:
                if word in user_input_keywords:
                    response_score += 1

        # Thêm điểm vào danh sách
        score_list.append(response_score)

    if not score_list:
        return random_responses.random_string()

    # Tìm phản hồi có điểm cao nhất
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    if best_response > 0:
        return response_data[response_index].get("bot_response", "Xin lỗi, tôi không hiểu bạn nói gì.")

    # Nếu không có phản hồi phù hợp, trả về một phản hồi ngẫu nhiên
    return random_responses.random_string()


while True:
    user_input = input("You: ")
    print("Bot:", get_response(user_input))


