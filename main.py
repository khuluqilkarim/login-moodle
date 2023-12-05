import requests
from bs4 import BeautifulSoup
from config import username, password

def Login():
    url = "https://elearning.ittelkom-sby.ac.id/login/index.php"
    
    with requests.Session() as session:
        response = session.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        loginToken = soup.find('input', {'name': 'logintoken'}).get('value')

        data = {
            'anchor': '',
            'logintoken' : loginToken,
            'username' : username,
            'password' : password
        }
        
        r_post = session.post(url, data=data)
        
        return "Dasbor" in r_post.text,session


def main():
    if Login():
        print("Login Success")
    else:
        print("Login Failed")

if __name__ == "__main__":
    main()
