from players import player_stats
from links import links
from games import games
import pandas as pd
import constants
from time import sleep
import random

def executor():
    lks = links()
    all_leagues = lks.getLeagues()
    leagues = []
    for league in all_leagues:
        #if 'England-Premier-League' in league:
        if 'England-Premier-League' in league or 'Germany-Bundesliga' in league and 'Germany-Bundesliga-II' not in league:
            leagues.append(league)
    l = []
    c = 0
    for i in leagues:
        lks.getIn(i)
        if c == 0:
            lks.accept()
        else:
            pass
        sleep(random.randint(3,5))
        l.append(lks.linkgetter())
        sleep(random.randint(3,5))
        c+=1

    s = []
    for i in l:
        for j in i:
            if j not in s:
                s.append(j)
    l = s
    print("There are: " + str(len(l)) + " links")
    print(l)


    df_lis = list()
    b = 0
    l = list(l)

    gms = games()

    def execute(link, lis):
        gms.get_link(link)
        dic = gms.table(link)
        lis.append(dic)

    for link in l[b:]:
        try:
            execute(link, df_lis)
            b += 1
            total = len(l)
            print(str(b) + " links have been executed, " + str(total - b) + " to go")
        except Exception as ex:
            print(ex)
            if b > 300:
                gms.driver.quit()
                for link in l[a:]:
                    try:
                        execute(link, df_lis)
                        b += 1
                        total = len(l)
                        print(str(b) + " links have been executed, " + str(total - b) + " to go")
                    except Exception as ex:
                        print(ex)
                        continue
            else:
                continue
    df = pd.DataFrame(df_lis)
    df.to_csv('games.csv', index = False)

    pst_links = gms.pst_links


    player_stats_df = pd.DataFrame()
    a = 0
    pst = player_stats()
    for link in pst_links:
        try:
            pst.get_link(link)

            if a == 0:
                pst.accept()
            else:
                pass
            sleep(random.randint(3, 8))
            soup = pst.get_soup()
            player_stats_df = player_stats_df.append(pst.table('home', soup, link))
            player_stats_df = player_stats_df.append(pst.table('away', soup, link))
            a += 1
            print('Executed ' + str(a) + ' links')

        except Exception as ex:
            print(ex)
            continue
    player_stats_df.to_csv('player_stats.csv', index = False)



if __name__ == '__main__':
    executor()