import requests, pandas, math, os

def main():
    print("\n"+30 * "-"+"MENU"+ 30 * "-")
    print("Chose one of the following options")
    print("1 - Player Details")
    print("2 - Clan info")
    print("3 - Combat Level Calculator")
    print("4 - Exit")
    print(64 * "-")
    while True:
        try:
            choice = int(input("> "))
        except ValueError:
            print("Invalid Option")
            continue
        else:
            break
    if choice==1:
        os.system('cls')
        PlayerDetails()
    elif choice==2:
        os.system('cls')
        Claninfo()
    elif choice==3:
        os.system('cls')
        CombatLvlCalc()
    elif choice==4:
        loop=False
    else:
        print("Wrong option selection. Enter any key to try again...\n")
        main()

def PlayerDetails():
    
    username = input("Enter a username: ")
    
    runedata = requests.get("https://apps.runescape.com/runemetrics/profile/profile?user=" + username + "&activities=20")
    print("Name: " + runedata.json()["name"])
    print("Total Skill Level: " + str(runedata.json()["totalskill"]))
    print("Combat Level: " + str(runedata.json()["combatlevel"]))
    print("Logged in: " + runedata.json()["loggedIn"])

    for activities in runedata.json()["activities"]:
        print(activities["date"])
        print(activities["details"])
        print(activities["text"]+"\n")
    main()

def Claninfo():
    clanname = input("Enter clan name: ")

    # reading csv file from url  
    data = pandas.read_csv("http://services.runescape.com/m=clan-hiscores/members_lite.ws?clanName=" + clanname, "utf-8", engine="python") 
  
    # dropping null value columns to avoid errors 
    data.dropna(inplace = True) 
  
    # new data frame with split value columns 
    new = data["Clanmate, Clan Rank, Total XP, Kills"].str.split(",", n = 3, expand = True)
  
    # making separate column from new data frame 
    data["Clanmate"]= new[0] 
    data["Clan Rank"]= new[1]
    data["Total XP"]= new[2]
    data["Kills"]= new[3]
  
    # Dropping old Name columns 
    data.drop(columns =["Clanmate, Clan Rank, Total XP, Kills"], inplace = True) 
  
    # df display 
    print(data)
    main()

def CombatLvlCalc():
    username = input("Enter a username: ")
    print("")
    
    # Get json data and assign skill level to variables
    runedata = requests.get("https://apps.runescape.com/runemetrics/profile/profile?user=" + username + "&activities=20")
    for skillvalues in runedata.json()["skillvalues"]:
        if skillvalues["id"] == 0:
            attack = skillvalues["level"]
            print("Current Attack: " +str(attack))
        elif skillvalues["id"] == 1:
            defence = skillvalues["level"]
            print("Current Defence: " +str(defence))
        elif skillvalues["id"] == 2:
            strength = skillvalues["level"]
            print("Current Strength: " +str(strength))
        elif skillvalues["id"] == 3:
            constitution = skillvalues["level"]
            print("Current Constitution: " +str(constitution))
        elif skillvalues["id"] == 4:
            ranged = skillvalues["level"]
            print("Current Ranged: " +str(ranged))
        elif skillvalues["id"] == 5:
            prayer = skillvalues["level"]
            print("Current Prayer: " +str(prayer))
        elif skillvalues["id"] == 6:
            magic = skillvalues["level"]
            print("Current Magic: " +str(magic))
        elif skillvalues["id"] == 23:
            summoning = skillvalues["level"]
            print("Current Summoning: " +str(summoning))

    # This will be used several times:
    attstr = attack + strength

    # Used formula, with every subcalculation being floored:
    # 1/4 * [1.3 * Max(Att+Str, 2*Mag, 2*Rng) + Def + Hp + Pray/2 + Summ/2]
    # The weight of pray/summ for example is 1/8, that of def/hp is 1/4 etc.
    combatlvl = ((max(attstr, 2*magic, 2*ranged)) * 13/10 + defence + constitution + math.floor(prayer/2) + math.floor(summoning/2))/4
    HpDef = math.ceil((1 - (combatlvl % 1)) * 4)
    PraySumm = math.ceil((1 - (combatlvl % 1)) * 8)

    if attstr >= 2*magic and attstr >= 2*ranged:
        AttStr = math.ceil((1 - (combatlvl % 1)) / 0.325)
        Mage = math.ceil((attstr - magic * 2 ) / 2 + (1 - (combatlvl % 1 )) / 0.65)
        Range = math.ceil((attstr - ranged * 2) / 2 + (1 - (combatlvl % 1)) / 0.65)
    else:
        # calculate att/str levels needed for combat level up:
        # first calculate how many levels to get to make your combat melee-based, then add the amount of levels needed from there.
        AttStr = max(ranged, magic) * 2 - attstr + math.ceil((1 - (combatlvl % 1)) / 0.325)

        # store this value in variable Mage first: assume mage-based combat first
        Mage = math.ceil(( 1 - (combatlvl % 1)) / 0.65 )
        if ranged > magic:
            # move the calculated value to variable Range: the combat is range-based
            Range = Mage
            # same logic for melee: amount of levels to get mage-based combat PLUS levels to another cb from there
            Mage = ranged - magic + Range
        else:
            # same logic again
            Range = magic - ranged + Mage

    print("\nYour current combat level is " + str(math.floor(combatlvl)) + ".\nFor level " + str(math.floor(combatlvl) + 1) + " you need one of the folowing:\n")
    print("- " + str(HpDef) + " Constitution or Defence levels")
    print("- " + str((prayer % 2 == 0 and PraySumm+1 or PraySumm)) + " Prayer levels")
    print("- " + str((summoning % 2 == 0 and PraySumm+1 or PraySumm)) + " Summoning levels")
    print("- " + str(AttStr) + " Attack or Strength levels")
    print("- " + str(Mage) + " Magic levels")
    print("- " + str(Range) + " Ranged levels")
    main()

if __name__ == "__main__":
    print("Welcome to RuneTracker by HexEditHD")
    main()