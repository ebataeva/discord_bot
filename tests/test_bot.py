import unittest
from api.huggingface_api import HuggingFaceClient

class TestHuggingFaceClient(unittest.TestCase):
    def test_generate_image(self):
        client = HuggingFaceClient()
        prompt = "Тестовый промт"
        try:
            image_data = client.generate_image(prompt)
            self.assertIsNotNone(image_data)
        except Exception as e:
            self.fail(f"Ошибка при вызове API: {e}")

if __name__ == '__main__':
    unittest.main()