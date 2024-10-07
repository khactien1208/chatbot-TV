import random


responses = [
    "Cảm ơn bạn đã phản hồi. Chúng tôi sẽ xem xét và phản hồi sớm nhất có thể.",
    "Tôi rất tiếc vì sự bất tiện này. Chúng tôi sẽ nhanh chóng giải quyết vấn đề của bạn."
]
def random_string():
    return random.choice(responses)