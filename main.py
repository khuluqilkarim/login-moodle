import requests
from bs4 import BeautifulSoup
from config import username, password

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
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

def ComingupEvent(session):
    url = "https://elearning.ittelkom-sby.ac.id/calendar/view.php?view=upcoming"
    response = session.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    events = soup.find_all('div', class_='description')

    results = []
    for event in events:
        masterSoup = BeautifulSoup(str(event), "html.parser")
        date_and_time = masterSoup.find('div', class_='col-xs-11').text
        course_info1 = masterSoup.find_all('div', class_='col-xs-11')[2].text
        try:
            course_info2 = masterSoup.find_all('div', class_='col-xs-11')[3].text
        except:
            course_info2 = ""
        if course_info2 != "":
            results.append({'dateline':date_and_time, 'course_info':course_info2})
        else: 
            results.append({'dateline':date_and_time, 'course_info':course_info1})

    printTable(results)
    
def printTable(results):
    print(bcolors.BOLD + "Tugas Kampus It Telkom Surabaya\n" + bcolors.ENDC)
    for result in results:
        if filterString(result['dateline']):
            print(bcolors.WARNING + f"{bcolors.BOLD} {result['dateline']} : {result['course_info']} {bcolors.ENDC}") 
        else:
            print(f"{bcolors.BOLD} {result['dateline']} : {result['course_info']} {bcolors.ENDC}")

def filterString(string):
    return "ini" in string

def main():
    isLogin, session = Login()
    if isLogin:
        print(bcolors.BOLD+bcolors.OKGREEN+"Connected to Moodle Success"+ bcolors.ENDC)
        ComingupEvent(session)
    else:
        print("Login Failed")

if __name__ == "__main__":
    main()
