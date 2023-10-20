from concurrent.futures import ThreadPoolExecutor
import requests  # pip install requests


class RequestSender:
    HEADER = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Authorization": "Bearer P9TYiQJkTpaM0HRfeteZomBs6rXjL7Cu",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Connection": "keep-alive",
    }

    BASE_URL = "https://student.otm.uz/rest/v1/data/student-list?limit=50"
    PAGES_COUNT = 90 # Bu raqamni esa aslida apiga bir marta bog'lanish orqali sonini aniqlash kerak. (Erinchoqlik qilmaysiz)

    def __init__(self):
        self.session = requests.Session()

    def send_request(self, url):
        response = self.session.get(url, headers=self.HEADER)
        print(f"Response from {url.split('=')[-1]}: page status code is {response.status_code}")
        return response.json()

    def send_requests(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = [executor.submit(self.send_request, f"{self.BASE_URL}&page={page}") for page in
                       range(1, self.PAGES_COUNT + 1)]

            # for result in results:
            #     result.result()


if __name__ == "__main__":
    sender = RequestSender()
    sender.send_requests()
