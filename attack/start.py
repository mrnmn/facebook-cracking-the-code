import type.liniare as ln
import termcolor as prnt

#determin attack type
def start_attack(choice:str):
    attack ={
        "1":ln.start_facebook_killer,
    }
    return attack.get(choice,ln.start_facebook_killer)

#init attack
def process_choice(r:str):
    response ={
            "1":"liniar",
            "2":"random"
        }
    choice = response.get(user_choice, "liniar")
    print("initilize " + choice + " attack...")
    start_attack(str(user_choice))(str(choice))

#user configurations
if __name__ == "__main__":
    print("\n\tWellcome to fb-cracker v 1.0.1")
    print(prnt.colored("\n\t1- Liniare Attack\t2- Random Attack","green"))
    print("\n\tLiniare: Start with minimum code and increse by 1.")
    print("\n\tRandom: Generate Random codes.")
    user_choice = input("\n\tChoose attack type:")  
    process_choice(str(user_choice))

    while True:
        pass