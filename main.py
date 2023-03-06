import requests
from requests.models import Response
from colorama import init, Fore
from typing import List

def append_file(line: str, output: str) -> None:
    with open(output, 'a') as f:
        f.write(line)
        f.write('\n')

def get_phone_number(cpf: str) -> str:
    response: Response = requests.get(f'api.example.com/cpf/{cpf}')
    response_json = response.json()
    if response_json['status'] == 'success':
        ddd: str = response_json['result']['ddd']
        phone: str = response_json['result']['telefone']
        print(f'{Fore.GREEN}Telefone {Fore.WHITE}{ddd} {phone}{Fore.GREEN} encontrado')
        return f'{ddd} {phone}'
    else:
        print(f'{Fore.RED}Telefone não encontrado')
        return 'Não encontrado'


def parse_file(filename: str) -> List[str]:
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines


def main() -> None:
    print()

    while True:
        print(f'{Fore.MAGENTA}[@] Input Filename?')
        filename: str = input(f'{Fore.YELLOW}-> {Fore.WHITE}')
        if not filename.endswith('.txt'):
            filename += '.txt'
        try:
            filesize: int = len(open(filename, 'r').readlines())
            print(f'{Fore.GREEN}File {Fore.WHITE}{filename}{Fore.GREEN} found with {Fore.WHITE}{filesize}{Fore.GREEN} lines')
            print()
            break
        except FileNotFoundError:
            print(f'{Fore.RED}File {Fore.WHITE}{filename}{Fore.RED} not found')
            print()
            continue

    while True:
        print(f'{Fore.MAGENTA}[@] Output Filename?')
        output: str = input(f'{Fore.YELLOW}-> {Fore.WHITE}')
        if not output.endswith('.txt'):
            output += '.txt'

        try:
            open(output, 'r').close()
            print(f'{Fore.RED}File {Fore.WHITE}{output}{Fore.RED} already exists')
            print()
            continue
        except FileNotFoundError:
            print()
            break

    for line in parse_file(filename):
        line: str = line.strip()

        if line:
            parse: List[str] = line.split('|')
            cpf: str = parse[0].split('CPF: ')[1].strip()
            phone_field: str = parse[-1].split('Telefone: ')[1].strip()
    
            ddd: str = phone_field.split(' ')[0].strip()
            phone: str = phone_field.split(' ')[1].strip()
    
            if phone[0] == '9':
                print(f'{Fore.GREEN}Telefone {Fore.WHITE}{phone}{Fore.GREEN} já está no formato correto')
                append_file(line, output)
            else:
                print()
                print(f'{Fore.YELLOW}↓↓↓ Formatando telefone {Fore.WHITE}{phone}')
                formated_phone: str = get_phone_number(cpf) 
                line: str = line.replace(phone_field, formated_phone)
                append_file(line, output)   


if __name__ == '__main__':
    init(autoreset=True)
    try:
        print(f'''
    {Fore.CYAN}                  _,-'|
    {Fore.CYAN}           ,-'._  |
    {Fore.CYAN} .||,      |####\ |
    {Fore.CYAN}\.`',/     \####| |
    {Fore.CYAN}= ,. =      |###| |              {Fore.MAGENTA}   combolist phone validator
    {Fore.CYAN}/ || \    ,-'\#/,'`.                  {Fore.MAGENTA}           v1.0
    {Fore.CYAN}  ||     ,'   `,,. `.                {Fore.MAGENTA}         by @edermxf
    {Fore.CYAN}  ,|____,' , ,;' \| |        
    {Fore.CYAN} (3|\    _/|/'   _| |        
    {Fore.CYAN}  ||/,-''  | >-'' _,\\           {Fore.YELLOW}           [what is this?]
    {Fore.CYAN}  ||'      ==\ ,-'  ,'   {Fore.YELLOW}   this script convert landline numbers to mobile numbers
    {Fore.CYAN}  ||       |  V \ ,|      {Fore.RED}      the responsability of the use of this script is yours
    {Fore.CYAN}  ||       |    |` |     
    {Fore.CYAN}  ||       |    |   \            {Fore.GREEN}               [examples]
    {Fore.CYAN}  ||       |    \    \           {Fore.GREEN}   input filename => combolist.txt
    {Fore.CYAN}  ||       |     |    \          {Fore.GREEN}output filename => combolist_validated.txt
    {Fore.CYAN}  ||       |      \_,-'
    {Fore.CYAN}  ||       |___,,--")_\\
    {Fore.CYAN}  ||         |_|   ccc/
    {Fore.CYAN}  ||        ccc/
      ''')
        main()
    except KeyboardInterrupt:
        print()
        print(f'{Fore.RED}Exiting...')
        exit()