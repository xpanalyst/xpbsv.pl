import bitsv
import os
import time
import secrets
import requests
import colorama as color
import termcolor as colors
color.init()


def cls():

    """ Czyści okno konsoli """
    
    os.system('cls' if os.name=='nt' else 'clear')


def logo():

    """ Logo """

    print(colors.colored("\t   ___ _ _            _                       _ ", "yellow"))
    print(colors.colored("\t  / __(_) |_ ___ ___ (_)_ __  _____   ___ __ | |", "yellow"))
    print(colors.colored("\t /__\// | __/ __/ _ \| | '_ \/ __\ \ / / '_ \| |", "yellow"))
    print(colors.colored("\t/ \/  \ | || (_| (_) | | | | \__ \\  V /| |_) | |", "yellow"))
    print(colors.colored("\t\_____/_|\__\___\___/|_|_| |_|___/ \_(_) .__/|_|", "yellow"))
    print(colors.colored("\t                                       |_|      ", "yellow"))
    print(" ")


def info():

    """ Logo + Menu wyboru """

    wybor = None
    while wybor != "4":
        print(colors.colored("\t   ___ _ _            _                       _ ", "yellow"))
        print(colors.colored("\t  / __(_) |_ ___ ___ (_)_ __  _____   ___ __ | |", "yellow"))
        print(colors.colored("\t /__\// | __/ __/ _ \| | '_ \/ __\ \ / / '_ \| |", "yellow"))
        print(colors.colored("\t/ \/  \ | || (_| (_) | | | | \__ \\  V /| |_) | |", "yellow"))
        print(colors.colored("\t\_____/_|\__\___\___/|_|_| |_|___/ \_(_) .__/|_|", "yellow"))
        print(colors.colored("\t                                       |_|      ", "yellow"))
        print(" ")
        print("\t   MENU")
        print(colors.colored("\t1. Samouczek", "green"))
        print(colors.colored("\t2. Stwórz nowy klucz prywatny", "red"))
        print(colors.colored("\t3. Wyślij wiadomość", "cyan"))
        print("\t4. Wyjście")
        print(" ")
        wybor = str(input("\tWybieram: "))
        if wybor == "1":
            cls()
            logo()
            krok_1()
        elif wybor == "2":
            cls()
            logo()
            krok_2()
        elif wybor == "3":
            cls()
            logo()
            krok_3()
            

def krok_3():

    """ Wysyłanie wiadomości do blockchain BSV """

    print(colors.colored("\n\t[WYSYŁANIE WIADOMOŚCI]", "magenta"))
    
    chain = None
    while chain != "test" or chain != "main" or chain != "wyjscie":
        chain = str(input("\n\tDo jakiej sieci chcesz wysłać wiadomość? (main/test/wyjscie) "))
        if chain == "wyjscie":
            info()
        elif chain == "test" or chain == "main":
            print("\tWybrałeś sieć [", chain, "]")
            break
        
    tekst = str(input("\tWpisz tutaj treść jaką chcesz wysłać i potwierdź 'enter': "))
    print("\tTwoja wiadomość wygląda tak: [", tekst, "]")
    
    odp_1 = str(input("\tCzy chcesz ją wysłać? (tak/nie) "))
    if odp_1.lower() == "nie":
        input("\tTo wracamy do menu :)")
        info()
    elif odp_1.lower() == "tak":
        potwierdzenie = None
        while potwierdzenie != "tak":
            private_key = str(input("\tWprowadź klucz prywatny i potwierdź 'enter' : ")) #  Tu wprowadzasz swój klucz prywatny
            print(colors.colored("\t--------------------------------------------------------------------------------------------------", "yellow"))
            print("\t", private_key)
            print(colors.colored("\t--------------------------------------------------------------------------------------------------", "yellow"))
            potwierdzenie = str(input("\n\tCzy klucz jest prawidłowy? (tak/nie) "))
        try:
            key = bitsv.Key.from_hex(private_key, network=chain) #  Klucz publiczny + klucz prywatny
            saldo = key.get_balance('bsv') #  Saldo adresu 
        except ValueError:
            print(colors.colored("\tValueError: non-hexadecimal number found in fromhex() arg at position 1", "red"))
            input("\t'Enter' by wyjść do menu..")
            cls()
            info()
        if float(saldo) == 0.0: #  Jeżeli saldo wynosi 0 BSV
           print(colors.colored("\tNie możesz wysłać wiadomości. Musisz mieć dodanie saldo.", "red"))
           key = None #  Adres publiczny ma wartość None
           private_key = None #  Klucz prywatny ma wartośc None
           input("\t'Enter' by wyjść do menu..")
           cls()
           info()
        else: #  Jeżeli saldo jest większe od 0
            cls() #  Wymaż konsolę
            logo()
            list_of_pushdata = [bytes.fromhex('6d01'), tekst.encode('utf-8')] #  Wygeneruj wiadomość
            key.send_op_return(list_of_pushdata, fee=0) #  Wyślij wiadomość
            print(colors.colored("\n\t[Wiadomość została wysłana!]", "green"))
            private_key = None # Zastąp klucz prywatny wartością None
            print(colors.colored("\n\tSprawdzam hash transakcji..", "yellow"))
            time.sleep(5) #  Odczekaj 5 sekund na pobranie transakcji z blockchain
            unspend = key.get_unspents() #  Sprawdź niepotwierdzone/wysłane
            txid_x = unspend[0]
            txid = str(txid_x)
            lis_0 = txid.find("'")
            one_id = txid[(lis_0 + 1):(lis_0 + 65)] #  Wygeneruj tylko hash transakcji
            while not unspend: #  Jeżeli nie ma jeszcze niewydanych/niepotwierdzonych odczekaj 5 sekund i powtórz zapytanie
                time.sleep(5)
                unspend = key.get_unspents()
                txid_x = unspend[0]
                txid = str(txid_x)
                lis_0 = txid.find("'")
                one_id = txid[(lis_0 + 1):(lis_0 + 65)]
            key = None #  Zastąp adres publiczny wartością None
            print("\tHash Twojej transakcji --> ", one_id)
            input("\n\tTo wracamy do menu :)")
            cls()
            info()
    else:
        input("\tTo wracamy do menu :)")
        cls()
        info()
    


def krok_2():

    """ Tworzenie klucza prywatnego """

    print(colors.colored("\n\t[TWORZENIE NOWEGO KLUCZA PRYWATNEGO]", "magenta"))
    print("\n\tKlucz prywatny tworzony jest z pomocą modułu 'secrets' języka programowania Python.")
    print(colors.colored("\tBezpieczeństwo takiego klucza to szyfrowanie 256 bitowe. ", "yellow"))
    print(colors.colored("\tRozłącz się z internetem.", "red"))
    print("\tTeraz naciśnij 'enter' by utworzyć nowy klucz prywatny.")
    input()

    bits = secrets.randbits(256) #  Tworzenie klucza prywatnego
    bits_hex = hex(bits)
    private_key = bits_hex[2:]
    print(colors.colored("\n\t--------------------------------------------------------------------------------------------------", "yellow"))
    print("\tTwój klucz prywatny to:", private_key) #  Klucz prywatny
    print(colors.colored("\t--------------------------------------------------------------------------------------------------", "yellow"))
    print(colors.colored("        *Skopiuj i Zapisz swój klucz prywatny*", "red"))
    
    print(colors.colored("\n\tPołącz się z internetem.", "yellow"))
    print("\tTeraz naciśnij 'enter' by sprawdzić listę adresów publicznych.")
    input()
    status_url = check_conn() #  Sprawdź połączenie z internetem
    while status_url != 200:
        status_url = check_conn()
        print(colors.colored("\n\t[*]Brak połączenia z siecią..[*]", "red"))
        input("\tNaciśnij 'enter' i sprawdź ponownie.. ")
    cls() #  Wyczyść okno konsoli
    logo()
    print(colors.colored("\n\t[TWORZENIE NOWEGO KLUCZA PRYWATNEGO]", "magenta"))
    new_key_main = bitsv.Key.from_hex(private_key, network="main") #  Adres publiczny MAIN
    new_key_test = bitsv.Key.from_hex(private_key, network="test") #  Adres publiczny TEST
    new_key_stn = bitsv.Key.from_hex(private_key, network="stn") #  Adres publiczny STN
    print(colors.colored("\n\t--------------------------------------------------------------------------------------------------", "yellow"))
    print("\tTwój adres publiczny w sieci MAINNET to:", new_key_main.address)
    print("\tTwój adres publiczny w sieci TESTNET to:", new_key_test.address)
    print("\tTwój adres publiczny w sieci STN to:", new_key_stn.address)
    print(colors.colored("\t--------------------------------------------------------------------------------------------------", "yellow"))
    private_key = None #  Zastąp klucz prywatny wartością None
    odpowiedz = None #  Zastąp adres publiczny wartością None
    while odpowiedz != "tak":
        odpowiedz = str(input("\n\tCzy wrócić do MENU? (tak) "))
    cls()
    info()
    
    

def check_conn():

    """ Sprawdza połączenie z internetem """

    print("\tSprawdzam połączenie..")
    try:
        url = "https://api.whatsonchain.com/v1/bsv/test/woc"
        response = requests.get(url)
        status_url = response.status_code
        
    except:
        status_url = None
        
    return status_url
    


def krok_1():

    """ Samouczek """
    
    print(colors.colored("\n\t[SAMOUCZEK]", "magenta"))
    print("""\n\tTen niewielki program, jest małym portfelem za pomocą którego możesz wysyłać wiadomości
        do blockchaina BitcoinSV. Fakt, mógł mieć dość ciekawy interfejs graficzny ale jestem zwolennikiem
        prostoty,dlatego działa w konsoli. Pomimo tego posiada potrzebne funkcje, które dają mozliwość bliższego
        poznania i działania z blockchain.
        Pierwszą rzeczą jaką zrobimy to założenie nowego klucza prywatnego ale SPOKOJNIE.
        Zrobimy to na łańcuchu testowym :)""")
    
    odpowiedz = None
    while odpowiedz != "test":
        odpowiedz = str(input("\n\tW jakiej sieci chcesz założyć klucz prywatny? (wpisz 'test' i potwierdz 'enter') "))
        if odpowiedz.lower() == "test":
            cls()
            logo()
            chain = "test"
            print(colors.colored("\n\t[KROK 1]", "cyan"))
            print(colors.colored("\n\tWybrałeś sieć TESTNET.", "green"))
            print("\tTo jeszcze nic nie oznacza, narazie wszystko dzieje się lokalnie na Twoim komputerze.")
            print("\tKlucz prywatny tworzony jest z pomocą modułu 'secrets' języka programowania Python.")
            print(colors.colored("\tBezpieczeństwo takiego klucza to szyfrowanie 256 bitowe. ", "yellow"))
            print("\tModuł 'secrets' jest znacznie bezpieczniejszy, ponieważ czerpie entropię bezpośrednio z systemu operacyjnego.")
            print("\tTa przypadkowość jest często zbierana ze źródeł sprzętowych,")
            print("\tzróżnicowania hałasu wentylatora lub dysku twardego,")
            print("\talbo z istniejących wcześniej, takich jak ruchy myszy, kliknięcia itp.")
            print("\tWynik takiego RNG (random number generator) jest znacznie trudniejszy do odtworzenia.")
            print("\tNie możesz go odtworzyć, znając czas powstania lub mając seed, ponieważ - nie ma seed!")
            print("\tKlucz prywatny który zaraz utworzymy, może być również użyty w sieci MAIN")
            print("\tto dlatego, że jest bez znaczenia do jakieś sieci go utworzysz - po prostu tworzysz nowy klucz.")
            print("\tMożesz teraz rozłączyć na chwilę swoje połączenie z internetem, by poczuć się bezpieczniej.")
            print("\tTeraz naciśnij 'enter' by utworzyć nowy klucz prywatny.")
            input()
            cls()
            logo()
            tworzenie_klucza_prywatnego(chain)

                  

def tworzenie_klucza_prywatnego(chain):

    """ Tworzy klucz prywatny """

    bits = secrets.randbits(256)
    bits_hex = hex(bits)
    private_key = bits_hex[2:]
    
    print(colors.colored("\n\t[KROK 2]", "cyan"))
    print("\n\tTwój klucz prywatny to:", private_key)
    print(colors.colored("        *Skopiuj i Zapisz swój klucz prywatny*", "red"))
    print("\tTeraz musimy sprawdzić, adres publiczny i saldo ale do tego potrzeba już połączenia z internetem")
    input("\tJeśli jesteś połączony z siecią, wciśnij 'enter'")
    
    status_url = check_conn()
    while status_url != 200:
        status_url = check_conn()
        print(colors.colored("\t[*]Brak połączenia z siecią..[*]", "red"))
        input("\tNaciśnij 'enter' i sprawdź ponownie.. ")
    cls()
    logo()
    conn(chain, private_key)



def conn(chain, private_key):

    """ Sprawdza adres publiczny i saldo """

    new_key = bitsv.Key.from_hex(private_key, network=chain)
    saldo = new_key.get_balance('bsv')
    print(colors.colored("\n\t[KROK 3]", "cyan"))
    print("\n\tBrawo! Twój adres publiczny w sieci TESTNET to:", new_key.address)
    print("\tSaldo twojego portfela wynosi", saldo, "BSV")
    print("\tZauważ, że adres portfela wygląda nieco inaczej.")
    print("\tTo dlatego, że jest adresem publicznym w sieci testowej")
    print("\tMożesz go sprawdzić, wchodząc na stronę https://whatsonchain.com/, wybrać sieć TEST,")
    print("\tlub wejśc bezpośrednio na https://test.whatsonchain.com/ i wkleić adres publiczny")
    odpowiedz = None
    while odpowiedz != "tak":
        odpowiedz = str(input("\n\tCzy chcesz przejść do [Krok 4]? (tak) "))
    cls()
    logo()
    print(colors.colored("\n\t[KROK 4]", "cyan"))
    print("\n\tTeraz zasilimy Twój adres publiczny [", new_key.address, "]")
    print("\tWejdź na stronę https://test.whatsonchain.com/ i z zakładki 'Tools' wybierz 'Faucet'.")
    print("\tWklej swój adres publiczny, rozwiąż reCAPTCHTA i naciśnij 'Roll!'")
    print("\tPewnie zobaczyłeś, że otrzymałeś testowe BSV. OK. Teraz to sprawdźmy tutaj.")
    print("\tNaciśnij enter by sprawdzić saldo.")
    while float(saldo) == 0.0:
        print("\tSaldo twojego portfela wynosi", saldo, "BSV")
        print("\tSprawdzam połączenie..")
        saldo = new_key.get_balance('bsv')
        input("\tNaciśnij enter by sprawdzić ponownie.")
    if float(saldo) > 0.0:
        cls()
        logo()
        print(colors.colored("\n\tDobra wiadomość!", "green"))
        print("\tSaldo twojego portfela wynosi", saldo, "BSV")
        input("\tTeraz wciśnij 'enter' by przejść do wysłania wiadomości.")
        cls()
        logo()
        wysylka_wiadomosci(new_key)



def wysylka_wiadomosci(new_key):

    """ Wysyła wiadomość do blockchain """

    print(colors.colored("\n\t[KROK 5]", "cyan"))
    print("\n\tNasze saldo testowe jest dodatnie. Teraz wyślemy naszą pierwszą wiadomość do blockchain.")
    tekst = str(input("\tWpisz tutaj treść jaką chcesz wysłać i naciśnij 'enter': "))
    print("\tTwoja wiadomość wygląda tak: [", tekst, "]")
    input("\tTeraz naciśnij enter by ją wysłać.")
    list_of_pushdata = [bytes.fromhex('6d01'), tekst.encode('utf-8')]
    new_key.send_op_return(list_of_pushdata, fee=0)
    print(colors.colored("\n\tWiadomość została wysłana!", "green"))
    print("\tTeraz sprawdź swój adres publiczny [", new_key.address, "] w blockchain i zobacz co wysłałeś.")
    odpowiedz = None
    while odpowiedz != "tak":
        odpowiedz = str(input("\tCzy wrócić do MENU? (tak) "))
    cls()
    info()



# start
info()
print("\n\tDo widzenia!")
input()


