import requests
import logging

# Настройка логирования
logging.basicConfig(filename='test_service.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

recommendations_url = "http://127.0.0.1:8000"
events_store_url = "http://127.0.0.1:8020"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


class RecommendationTester:
    def __init__(self, recommendations_url, events_store_url, headers):
        self.recommendations_url = recommendations_url
        self.events_store_url = events_store_url
        self.headers = headers

    def fetch_recommendations(self, user_id):
        params = {"user_id": user_id, 'k': 10}

        # Запрос оффлайн рекомендаций
        try:
            resp_offline = requests.post(self.recommendations_url + "/recommendations_offline", headers=self.headers, params=params)
            resp_offline.raise_for_status()
            recs_offline = resp_offline.json()["recs"]
            logging.info(f'Fetched offline recommendations for user {user_id}: {recs_offline}.')
        except requests.exceptions.RequestException as e:
            logging.error(f'Error fetching offline recommendations for user {user_id}: {e}')
            recs_offline = []

        # Запрос онлайн рекомендаций
        try:
            resp_online = requests.post(self.recommendations_url + "/recommendations_online", headers=self.headers, params=params)
            resp_online.raise_for_status()
            recs_online = resp_online.json()["recs"]
            logging.info(f'Fetched online recommendations for user {user_id}: {recs_online}.')
        except requests.exceptions.RequestException as e:
            logging.error(f'Error fetching online recommendations for user {user_id}: {e}')
            recs_online = []

        # Запрос смешанных рекомендаций
        try:
            resp_blended = requests.post(self.recommendations_url + "/recommendations", headers=self.headers, params=params)
            resp_blended.raise_for_status()
            recs_blended = resp_blended.json()["recs"]
            logging.info(f'Fetched blended recommendations for user {user_id}: {recs_blended}.')
        except requests.exceptions.RequestException as e:
            logging.error(f'Error fetching blended recommendations for user {user_id}: {e}')
            recs_blended = []

        return recs_offline, recs_online, recs_blended

    def log_events(self, user_id, event_item_ids):
        for event_item_id in event_item_ids:
            try:
                resp = requests.post(self.events_store_url + "/put", 
                                     headers=self.headers, 
                                     params={"user_id": user_id, "track_id": event_item_id})
                resp.raise_for_status()  
                logging.info(f'Successfully logged event {event_item_id} for user {user_id}.')
            except requests.exceptions.RequestException as e:
                logging.error(f'Error logging event {event_item_id} for user {user_id}: {e}')

    def test_user_recommendations(self, user_id):
        logging.info(f'Testing recommendations for user_id: {user_id}')
        recs_offline, recs_online, recs_blended = self.fetch_recommendations(user_id)
        print(f"Offline Recommendations: {recs_offline}")
        print(f"Online Recommendations: {recs_online}")
        print(f"Blended Recommendations: {recs_blended}")

# Пример использования

tester = RecommendationTester(recommendations_url, events_store_url, headers)

# Сценарии тестирования
test_users = {
    "user_no_recommendations": 1,
    "user_no_online_history": 1374577,
    "user_with_online_history": 1133
}

# Зададим историю последних действий для пользователя с онлайн-историей
user_id = test_users["user_with_online_history"]
event_item_ids = [589498, 590262, 590303, 99262, 590262, 590303, 99262]
tester.log_events(user_id, event_item_ids)

# Тестирование для всех пользователей
for user_key, user_id in test_users.items():
    tester.test_user_recommendations(user_id)