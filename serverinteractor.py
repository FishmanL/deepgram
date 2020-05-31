import requests


if __name__ == "__main__":
    with open("test.wav", "rb") as f:
        files = {'file': f}
        r = requests.post('http://127.0.0.1:5000/post', files=files)
        print(r)
