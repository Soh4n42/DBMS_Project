import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image , ImageTk





root=Tk()

global match_id_matches
global home_team 
global away_team 
global home_team_score 
global away_team_score 
global age 
global jersey_no 
global player_name_player
global club_name
global match_id_played
global player_name_played
global goal 
global assists 
global yellow_card 
global red_card 
global entry_club1
global entry_player3
global player_details
global club_details
global match_details
global entry1
global played_details
global entry14
global sum_details



import mysql.connector
conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")

my_cursor=conn.cursor()
my_cursor.execute("create table if not exists club(club_name varchar(50) primary key,estd_date varchar(30),manager_name varchar(30),home_ground varchar(30))")
conn.commit()
my_cursor.execute("create table if not exists matches(match_id int primary key,home_team varchar(50),away_team varchar(50),home_team_score int,away_team_score int,foreign key (home_team) references club(club_name) on delete cascade on update cascade,foreign key (away_team) references club(club_name) on delete cascade on update cascade)")
conn.commit()
my_cursor.execute("create table if not exists player(player_name varchar(50) primary key,age int,jersey_no int,club_name varchar(50),foreign key (club_name) references club(club_name) on delete cascade on update cascade)")
conn.commit()
my_cursor.execute("create table if not exists played(match_id int,player_name varchar(50),goal int,assists int,yellow_card int,red_card int,foreign key (match_id)references matches(match_id) on delete cascade on update cascade,foreign key (player_name) references player (player_name) on delete cascade on update cascade)")
conn.commit()
my_cursor.close()
conn.close()





##########   for derived table
def exit_sum():
    
    global b3
    b3.destroy()
    b3=Frame(root,bd=3,relief=RIDGE)
    b3.place(x=10,y=570,width=760,height=220)
    button_league['state']='normal'
    button_club['state']='normal'
    button_played['state']='normal'
    button_players['state']='normal'
    

def table_summary():
    global sum_details
    scroll_x=ttk.Scrollbar(b3,orient=HORIZONTAL)
    scroll_y=ttk.Scrollbar(b3,orient=VERTICAL)
    sum_details=ttk.Treeview(b3,column=("c_name","player","g_scored","assist","yellow","red"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM,fill=X)  
    scroll_y.pack(side=RIGHT,fill=Y)
    scroll_x.config(command=sum_details.xview)
    scroll_y.config(command=sum_details.yview)
    sum_details.heading("c_name",text="Club_Name")
    sum_details.heading("player",text="Player_Name")
    #sum_details.heading("m_played",text="Matches_Played")
    sum_details.heading("g_scored",text="Goal_Scored")
    sum_details.heading("assist",text="Assists")
    sum_details.heading("yellow",text="Yellow_Cards")
    sum_details.heading("red",text="Red_Cards")

    sum_details["show"]="headings"
    sum_details.pack(fill=BOTH,expand=1)

    fetch_summary()
    button_league['state']='disabled'
    button_club['state']='disabled'
    button_played['state']='disabled'
    button_players['state']='disabled'
    button_exit_sum['state']='normal'



def fetch_summary():
    global sum_details
    import mysql.connector
    conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
    my_cursor=conn.cursor()
    my_cursor.execute("select * from goal_summary natural join assist_summary natural join yellow_card_summary natural join red_card_summary")
    rows=my_cursor.fetchall()
    for i in rows:
        sum_details.insert('','end',values=i)
    my_cursor.close()
    conn.close

    sum_details["show"]="headings"
    sum_details.pack(fill=BOTH,expand=1)




############         to add records club


club_name=StringVar()
estd_date=StringVar()
manager_name=StringVar()
home_ground=StringVar()


def add_records_club():

    import mysql.connector
    from mysql.connector import Error
    conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
    global b3
    if(club_name.get()=="" or estd_date.get()=="" or manager_name.get()=="" or home_ground.get()==""):
        response=messagebox.showerror("error","All Fields Are Required")
        return
    try:
        my_cursor=conn.cursor()
        my_cursor.execute("insert into club values(%s,%s,%s,%s)",(club_name.get(),estd_date.get(),manager_name.get(),home_ground.get()))
        conn.commit()
        b3.destroy()
        b3=Frame(root,bd=3,relief=RIDGE)
        b3.place(x=10,y=570,width=760,height=220)      
        my_cursor.close()
        conn.close
        messagebox.showinfo("Added","Record Added Successfully")
    except Error as error:
        response=messagebox.showerror("error",error) 



#### add records of player


player_name1=StringVar()
age1=StringVar()
jersey_no1=StringVar()
club_name1=StringVar()



def add_records_player():
    global age 
    global jersey_no 
    global player_name_player
    global club_name
    

    if(player_name1.get()=="" or age1.get()=="" or jersey_no1.get()=="" or club_name1.get()==""):
        response=messagebox.showerror("error","All Fields Are Required")
        return
      
    import mysql.connector
    from mysql.connector import Error
    try:
        try:
            age=int(age1.get())
            jersey_no=int(jersey_no1.get())
            player_name_player=player_name1.get()
            club_name=club_name1.get()
        except:
            response=messagebox.showerror("error","Enter Integer Values For Age And Jersey Number")
        
        conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
        my_cursor=conn.cursor()
        my_cursor.execute("insert into player values(%s,%s,%s,%s)",(player_name_player,age,jersey_no,club_name))
        conn.commit()
        my_cursor.close()
        conn.close
        messagebox.showinfo("Added","Record Added Successfully")
    except Error as error:
        response=messagebox.showerror("error",error)


###  add records of matches




match_id1=StringVar()
home_team1=StringVar()
away_team1=StringVar()
home_team_score1=StringVar()
away_team_score1=StringVar()

def add_records_matches():
    global match_id_matches
    global home_team 
    global away_team 
    global home_team_score 
    global away_team_score 
    if(match_id1.get()=="" or home_team1.get()=="" or away_team1.get()=="" or home_team_score1.get()==""or away_team_score1.get()==""):
        response=messagebox.showerror("error","All Fields Are Required")
        return

    import mysql.connector
    from mysql.connector import Error
    try:
        try:
            match_id=int(match_id1.get())
            home_team=home_team1.get()
            away_team=away_team1.get()
            home_team_score=int(home_team_score1.get())
            away_team_score=int(away_team_score1.get())
        except:
            response=messagebox.showerror("error","Enter Integer Values For match id , home_team_score and away_team_score")


        conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
        my_cursor=conn.cursor()
        my_cursor.execute("insert into matches values(%s,%s,%s,%s,%s)",(match_id,home_team,away_team,home_team_score,away_team_score))
        conn.commit()
        my_cursor.close()
        conn.close()
        messagebox.showinfo("Added","Record Added Successfully")
    except Error as error:
            response=messagebox.showerror("error",error)

###  add records of played




match_id2=StringVar()
player_name2=StringVar()
goal1=StringVar()
assists1=StringVar()
yellow_card1=StringVar()
red_card1=StringVar()

def add_records_played():
    global match_id_played
    global player_name_played
    global goal 
    global assists 
    global yellow_card 
    global red_card 

    if(match_id2.get()=="" or player_name2.get()=="" or goal1.get()=="" or assists1.get()=="" or yellow_card1.get()=="" or red_card1.get()==""):
        response=messagebox.showerror("error","All Fields Are Required")
        return

    import mysql.connector
    from mysql.connector import Error
    try:
        try:
            match_id_played=int(match_id2.get())
            player_name_played=player_name2.get()
            goal=int(goal1.get())
            assists=int(assists1.get())
            yellow_card =int(yellow_card1.get())
            red_card =int(red_card1.get())
        except:
            response=messagebox.showerror("error","Enter Integer Values For match id ,goal,assists,yellow card and red card")


        conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
        my_cursor=conn.cursor()
        my_cursor.execute("insert into played values(%s,%s,%s,%s,%s,%s)",(match_id_played,player_name_played,goal,assists,yellow_card,red_card))
        conn.commit()
        my_cursor.close()
        conn.close
        messagebox.showinfo("Added","Record Added Successfully")
    except Error as error:
            response=messagebox.showerror("error",error)



global b3
global b_matches
global b_club
global b_player
global b_matchplay


#######   Window+Title     ######


root.title("Project DBMS")
root.geometry('1520x840')
label_title=Label(root,bd=10,relief=RIDGE,text="RECORD ENTRY OF SPORT LEAGUE",fg="gold",bg="black",font=("times new roman",30,"bold"))
label_title.pack(side=TOP,fill=X)

######    Image premier league


img2=Image.open(r"F:\downloads pc\hh.JPEG")
img2=img2.resize((700,200),Image.ANTIALIAS)
photoimg2=ImageTk.PhotoImage(img2)
lbl=Label(root,image=photoimg2,bd=4,relief=RIDGE)
lbl.place(x=780,y=570,width=720,height=220)

###### Image paras logo




img1=Image.open(r"F:\downloads pc\ss.JPG")
img1=img1.resize((1080,200),Image.ANTIALIAS)
photoimg1=ImageTk.PhotoImage(img1)
lbl=Label(root,image=photoimg1,bd=3,relief=RIDGE)
lbl.place(x=410,y=70,width=1100,height=220)







#######   Frame to SHOW  TABLEs

b3=Frame(root,bd=3,relief=RIDGE)
b3.place(x=10,y=570,width=760,height=220)




###### Window for matches



#### for exit button
def exit1():
    global b_matches
    global b3
    b_matches.destroy()
    b3.destroy()
    b3=Frame(root,bd=3,relief=RIDGE)
    b3.place(x=10,y=570,width=760,height=220)
    button_league['state']='normal'
    button_club['state']='normal'
    button_played['state']='normal'
    button_players['state']='normal'
    button_exit_sum['state']='disabled'
    button_show_all['state']='normal'
    


def refresh_matches():
    global b_matches
    match_id1.set("")
    home_team1.set("")
    away_team1.set("")
    home_team_score1.set("")
    away_team_score1.set("")
    b_matches.destroy()
    box_matches()    




def box_matches():
    global b_matches
    global entry1
    

        
    
        ##########      Frame 1
        
    b_matches=LabelFrame(root,text="Details Of Matches",bd=3,relief=RIDGE)
    b_matches.place(x=415,y=75,width=1100,height=490)
    label1=Label(b_matches,text="Match Id",bg="black",fg="white",font=("Ariel",25,"bold"))
    label1.grid(row=0,column=0,padx=15,pady=15)
    label2=Label(b_matches,text="Home Team",bg="black",fg="white",font=("Ariel",25,"bold"))
    label2.grid(row=1,column=0,padx=15,pady=15)
    label3=Label(b_matches,text="Away Team",bg="black",fg="white",font=("Ariel",25,"bold"))
    label3.grid(row=2,column=0,padx=15,pady=15)
    label4=Label(b_matches,text="Home Team Score",bg="black",fg="white",font=("Ariel",25,"bold"))
    label4.grid(row=3,column=0,padx=15,pady=15)
    label5=Label(b_matches,text="Away Team Score",bg="black",fg="white",font=("Ariel",25,"bold"))
    label5.grid(row=4,column=0,padx=15,pady=15)




         #########    Entry Frame 1

    entry1=ttk.Entry(b_matches,width=15, font=('Arial 24'),textvariable=match_id1)
    entry2=ttk.Entry(b_matches,width=15, font=('Arial 24'),textvariable=home_team1)
    entry3=ttk.Entry(b_matches,width=15, font=('Arial 24'),textvariable=away_team1)
    entry4=ttk.Entry(b_matches,width=15, font=('Arial 24'),textvariable=home_team_score1)
    entry5=ttk.Entry(b_matches,width=15, font=('Arial 24'),textvariable=away_team_score1)


    entry1.grid(row=0,column=1,padx=5,pady=5)
    entry2.grid(row=1,column=1,padx=5,pady=5)
    entry3.grid(row=2,column=1,padx=5,pady=5)
    entry4.grid(row=3,column=1,padx=5,pady=5)
    entry5.grid(row=4,column=1,padx=5,pady=5)
        
       

        ####### ADD

    b3=LabelFrame(b_matches,bd=3,relief=RIDGE)
    b3.place(x=12,y=365,width=1080,height=100)
    button_add=Button(b3,text="ADD RECORDS",command=add_records_matches,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_add.grid(row=0,column=0,padx=2,pady=2)
    button_exit=Button(b3,text="EXIT",command=exit1,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_exit.grid(row=0,column=1,padx=2,pady=2)
    button_refresh=Button(b3,text="REFRESH",command=refresh_matches,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_refresh.grid(row=0,column=2,padx=2,pady=2)
    button_showtable=Button(b3,text="SHOW TABLE",command=table_matches,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_showtable.grid(row=0,column=3,padx=2,pady=2)
    button_update=Button(b3,text="UPDATE",command=update_matches,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_update.grid(row=0,column=4,padx=2,pady=2)
    button_delete=Button(b3,text="DELETE",command=delete_matches,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_delete.grid(row=0,column=5,padx=2,pady=2)



    button_league['state']='disabled'
    button_club['state']='disabled'
    button_played['state']='disabled'
    button_players['state']='disabled'
    button_exit_sum['state']='disabled'
    button_show_all['state']='disabled'

    
###### Window for club



#### for exit button
def exit_club():
    global b_club
    global b3
    b_club.destroy()
    b3.destroy()
    b3=Frame(root,bd=3,relief=RIDGE)
    b3.place(x=10,y=570,width=760,height=220)
    button_league['state']='normal'
    button_club['state']='normal'
    button_played['state']='normal'
    button_players['state']='normal'
    button_exit_sum['state']='disabled'
    button_show_all['state']='normal'

def refresh_clubs():
    global b_club
    club_name.set("")
    estd_date.set("")
    manager_name.set("")
    home_ground.set("") 
    b_club.destroy()
    box_clubs() 


def box_clubs():
   
    global b_club
    
    global entry_club1  
        
        
        ##########      Frame for club
        
    b_club=LabelFrame(root,text="Details of club",bd=3,relief=RIDGE)
    b_club.place(x=415,y=75,width=1100,height=490)
    label_club5=Label(b_club,text="Club Name",bg="black",fg="white",font=("Ariel",25,"bold"))
    label_club5.grid(row=0,column=0,padx=15,pady=15)
    label_club1=Label(b_club,text="Manager Name",bg="black",fg="white",font=("Ariel",25,"bold"))
    label_club1.grid(row=1,column=0,padx=15,pady=15)
    label_club2=Label(b_club,text="Date Founded",bg="black",fg="white",font=("Ariel",25,"bold"))
    label_club2.grid(row=2,column=0,padx=15,pady=15)
    label_club3=Label(b_club,text="Stadium",bg="black",fg="white",font=("Ariel",25,"bold"))
    label_club3.grid(row=3,column=0,padx=15,pady=15)
    




        #########    Entry Frame for club

    entry_club1=ttk.Entry(b_club,width=25, font=('Arial 24'),textvariable=club_name)
    entry_club2=ttk.Entry(b_club,width=25, font=('Arial 24'),textvariable=estd_date)
    entry_club3=ttk.Entry(b_club,width=25, font=('Arial 24'),textvariable=manager_name)
    entry_club4=ttk.Entry(b_club,width=25, font=('Arial 24'),textvariable=home_ground)
    


    entry_club1.grid(row=0,column=1,padx=5,pady=5)
    entry_club2.grid(row=1,column=1,padx=5,pady=5)
    entry_club3.grid(row=2,column=1,padx=5,pady=5)
    entry_club4.grid(row=3,column=1,padx=5,pady=5)
    
    
    
    

    ####### ADD Record button

    b_club1=LabelFrame(b_club,bd=3,relief=RIDGE)
    b_club1.place(x=12,y=365,width=1080,height=100)
    button_add=Button(b_club1,text="ADD RECORDS",command=add_records_club,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_add.grid(row=0,column=0,padx=2,pady=2)
    button_add=Button(b_club1,text="EXIT",command=exit_club,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_add.grid(row=0,column=1,padx=2,pady=2)
    button_refresh=Button(b_club1,text="REFRESH",command=refresh_clubs,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_refresh.grid(row=0,column=2,padx=2,pady=2)
    button_showtable=Button(b_club1,text="SHOW  TABLE",command=table_club,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_showtable.grid(row=0,column=3,padx=2,pady=2)
    button_update=Button(b_club1,text="UPDATE",command=update_club,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_update.grid(row=0,column=4,padx=2,pady=2)
    button_delete=Button(b_club1,text="DELETE",command=delete_club,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_delete.grid(row=0,column=5,padx=2,pady=2)

    button_league['state']='disabled'
    button_club['state']='disabled'
    button_played['state']='disabled'
    button_players['state']='disabled'
    button_exit_sum['state']='disabled'
    button_show_all['state']='disabled'
    
    
        



###### Window for player


#### for exit button
def exit_player():
    global b_club
    global b3
    b_player.destroy()
    b3.destroy()
    b3=Frame(root,bd=3,relief=RIDGE)
    b3.place(x=10,y=570,width=760,height=220)
    button_league['state']='normal'
    button_club['state']='normal'
    button_played['state']='normal'
    button_players['state']='normal'
    button_exit_sum['state']='disabled'
    button_show_all['state']='normal'
    

def refresh_player():
    global b_player
    player_name1.set("")
    age1.set("")
    jersey_no1.set("")
    club_name1.set("")
    b_player.destroy()
    box_Players() 

def box_Players():
    
    global b_player
    global entry_player3
    
    
        
            
        ##########      Frame for player
    b_player=LabelFrame(root,text="Details",bd=3,relief=RIDGE)
    b_player.place(x=415,y=75,width=1100,height=490)   
    label_player0=Label(b_player,text="Player Name",bg="black",fg="white",font=("Ariel",25,"bold"))
    label_player0.grid(row=0,column=0,padx=15,pady=15)
    label_player1=Label(b_player,text="Age",bg="black",fg="white",font=("Ariel",25,"bold"))
    label_player1.grid(row=1,column=0,padx=15,pady=15)
    label_player2=Label(b_player,text="Jersey Number",bg="black",fg="white",font=("Ariel",25,"bold"))
    label_player2.grid(row=2,column=0,padx=15,pady=15)
    label_player3=Label(b_player,text="Club Name",bg="black",fg="white",font=("Ariel",25,"bold"))
    label_player3.grid(row=3,column=0,padx=15,pady=15)
    




        #########    Entry Frame for player
    entry_player0=ttk.Entry(b_player,width=15, font=('Arial 24'),textvariable=player_name1)
    entry_player1=ttk.Entry(b_player,width=15, font=('Arial 24'),textvariable=age1)
    entry_player2=ttk.Entry(b_player,width=15, font=('Arial 24'),textvariable=jersey_no1)
    entry_player3=ttk.Entry(b_player,width=15, font=('Arial 24'),textvariable=club_name1)
    
    

    entry_player0.grid(row=0,column=1,padx=5,pady=5)
    entry_player1.grid(row=1,column=1,padx=5,pady=5)
    entry_player2.grid(row=2,column=1,padx=5,pady=5)
    entry_player3.grid(row=3,column=1,padx=5,pady=5)
    
    
    
    

    ####### ADD Record button

    b_player1=LabelFrame(b_player,bd=3,relief=RIDGE)
    b_player1.place(x=12,y=365,width=1080,height=100)
    button_add=Button(b_player1,text="ADD RECORDS",command=add_records_player,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_add.grid(row=0,column=0,padx=2,pady=2)
    button_add=Button(b_player1,text="EXIT",command=exit_player,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_add.grid(row=0,column=1,padx=2,pady=2)
    button_refresh=Button(b_player1,text="REFRESH",command=refresh_player,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_refresh.grid(row=0,column=2,padx=2,pady=2)
    button_showtable=Button(b_player1,text="SHOW  TABLE",command=table_player,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_showtable.grid(row=0,column=3,padx=2,pady=2)
    button_update=Button(b_player1,text="UPDATE",command=update_player,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_update.grid(row=0,column=4,padx=2,pady=2)
    button_delete=Button(b_player1,text="DELETE",command=delete_player,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_delete.grid(row=0,column=5,padx=2,pady=2)
    button_league['state']='disabled'
    button_club['state']='disabled'
    button_played['state']='disabled'
    button_players['state']='disabled'
    button_exit_sum['state']='disabled'
    button_show_all['state']='disabled'
    
        

######## window for match played

##Exit for match played
def exit_matchplay():
    global b_matchplay
    global b3
    b_matchplay.destroy()
    b3.destroy()
    b3=Frame(root,bd=3,relief=RIDGE)
    b3.place(x=10,y=570,width=760,height=220)
    button_league['state']='normal'
    button_club['state']='normal'
    button_played['state']='normal'
    button_players['state']='normal'
    button_exit_sum['state']='disabled'
    button_show_all['state']='normal'
    


def refresh_matchplay():
    global b_matchplay
    match_id2.set("")
    player_name2.set("")
    goal1.set("")
    assists1.set("")
    yellow_card1.set("")
    red_card1.set("")
    b_matchplay.destroy()
    box_played() 

def box_played():
    
    global b_matchplay
    global entry14
    
    
      
        
        ##########      Frame 1 for match played
        
    b_matchplay=LabelFrame(root,text="Details Of Played",bd=3,relief=RIDGE)
    b_matchplay.place(x=415,y=75,width=1100,height=490)
    label14=Label(b_matchplay,text="Match Id",bg="black",fg="white",font=("Ariel",25,"bold"))
    label14.grid(row=0,column=0,padx=15,pady=15)
    label24=Label(b_matchplay,text="Player Name",bg="black",fg="white",font=("Ariel",25,"bold"))
    label24.grid(row=1,column=0,padx=15,pady=15)
    label34=Label(b_matchplay,text="Goal",bg="black",fg="white",font=("Ariel",25,"bold"))
    label34.grid(row=2,column=0,padx=15,pady=15)
    label44=Label(b_matchplay,text="Assists",bg="black",fg="white",font=("Ariel",25,"bold"))
    label44.grid(row=3,column=0,padx=15,pady=15)
    label54=Label(b_matchplay,text="Yellow Card",bg="black",fg="white",font=("Ariel",25,"bold"))
    label54.grid(row=4,column=0,padx=15,pady=15)
    label64=Label(b_matchplay,text="Red Card",bg="black",fg="white",font=("Ariel",25,"bold"))
    label64.grid(row=0,column=2,padx=15,pady=15)
    




        #########    Entry Frame 1 for match played

    entry14=ttk.Entry(b_matchplay,width=13, font=('Arial 24'),textvariable=match_id2)
    entry24=ttk.Entry(b_matchplay,width=13, font=('Arial 24'),textvariable=player_name2)
    entry34=ttk.Entry(b_matchplay,width=13, font=('Arial 24'),textvariable=goal1)
    entry44=ttk.Entry(b_matchplay,width=13, font=('Arial 24'),textvariable=assists1)
    entry54=ttk.Entry(b_matchplay,width=13, font=('Arial 24'),textvariable=yellow_card1)
    entry64=ttk.Entry(b_matchplay,width=13, font=('Arial 24'),textvariable=red_card1)
    


    entry14.grid(row=0,column=1,padx=5,pady=5)
    entry24.grid(row=1,column=1,padx=5,pady=5)
    entry34.grid(row=2,column=1,padx=5,pady=5)
    entry44.grid(row=3,column=1,padx=5,pady=5)
    entry54.grid(row=4,column=1,padx=5,pady=5)
    entry64.grid(row=0,column=3,padx=5,pady=5)
    
    
    

    ####### ADD button for match played

    b_matchplay1=LabelFrame(b_matchplay,bd=3,relief=RIDGE)
    b_matchplay1.place(x=12,y=365,width=1080,height=100)
    button_add=Button(b_matchplay1,text="ADD RECORDS",command=add_records_played,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_add.grid(row=0,column=0,padx=2,pady=2)
    button_add=Button(b_matchplay1,text="EXIT",command=exit_matchplay,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_add.grid(row=0,column=1,padx=2,pady=2)
    button_refresh=Button(b_matchplay1,text="REFRESH",command=refresh_matchplay,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_refresh.grid(row=0,column=2,padx=2,pady=2)
    button_showtable=Button(b_matchplay1,text="SHOW  TABLE",command=table_played,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_showtable.grid(row=0,column=3,padx=2,pady=2)
    button_update=Button(b_matchplay1,text="UPDATE",command=update_played,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_update.grid(row=0,column=4,padx=2,pady=2)
    button_delete=Button(b_matchplay1,text="DELETE",command=delete_played,bg="black",fg="gold",font=("times new roman",15,"bold"))
    button_delete.grid(row=0,column=5,padx=2,pady=2)

    button_league['state']='disabled'
    button_club['state']='disabled'
    button_played['state']='disabled'
    button_players['state']='disabled'
    button_exit_sum['state']='disabled'
    button_show_all['state']='disabled'
       
        


########    Buttons for table  ###########

frame=Frame(root,bd=3,relief=RIDGE)
frame.place(x=10,y=70,width=400,height=300)


button_league=Button(frame,text=" MATCHES ",command=box_matches,width=22,fg="gold",bg="black",font=("times new roman",20,"bold"))
button_league.grid(row=1,column=0,padx=18,pady=8)

button_club=Button(frame,text=" CLUB ",command=box_clubs,width=22,fg="gold",bg="black",font=("times new roman",20,"bold"))
button_club.grid(row=0,column=0,padx=18,pady=10)


button_players=Button(frame,text=" PLAYERS ",command=box_Players,width=22,fg="gold",bg="black",font=("times new roman",20,"bold"))
button_players.grid(row=2,column=0,padx=18,pady=10)


button_played=Button(frame,text="PLAYED",command=box_played,width=22,fg="gold",bg="black",font=("times new roman",20,"bold"))
button_played.grid(row=3,column=0,padx=18,pady=10)



button_show_all=Button(root,text="SUMMARY",command=table_summary,width=22,fg="gold",bg="black",font=("times new roman",20,"bold"))
button_show_all.place(x=10,y=400)


button_exit_sum=Button(root,text="EXIT SUMMARY",command=exit_sum,width=22,fg="gold",bg="black",font=("times new roman",20,"bold"),state='disabled')
button_exit_sum.place(x=10,y=450)




#####   to SHOW  TABLES





def table_matches():
    global match_details
    scroll_x=ttk.Scrollbar(b3,orient=HORIZONTAL)
    scroll_y=ttk.Scrollbar(b3,orient=VERTICAL)
    match_details=ttk.Treeview(b3,column=("m_id","home","away","h_t_score","a_t_score"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM,fill=X)  
    scroll_y.pack(side=RIGHT,fill=Y)
    scroll_x.config(command=match_details.xview)
    scroll_y.config(command=match_details.yview)
    match_details.heading("m_id",text="Match id")
    match_details.heading("home",text="Home Team")
    match_details.heading("away",text="Away Team")
    match_details.heading("h_t_score",text="Home Team Score")
    match_details.heading("a_t_score",text="Away Team Score")
   

    match_details["show"]="headings"
    match_details.pack(fill=BOTH,expand=1)

    fetch_matches()
    global entry1 
    entry1['state']='disabled' 

def fetch_matches():
    global match_details
    import mysql.connector
    conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
    my_cursor=conn.cursor()
    my_cursor.execute("select * from matches")
    rows=my_cursor.fetchall()
    for i in rows:
        match_details.insert('','end',values=i)
    my_cursor.close()
    conn.close

    match_details.bind("<ButtonRelease-1>",get_cursor_matches)

    match_details["show"]="headings"
    match_details.pack(fill=BOTH,expand=1)

def table_club():
    global club_details
    scroll_x=ttk.Scrollbar(b3,orient=HORIZONTAL)
    scroll_y=ttk.Scrollbar(b3,orient=VERTICAL)
    club_details=ttk.Treeview(b3,column=("c_name","m_name","date","stadium"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM,fill=X)  
    scroll_y.pack(side=RIGHT,fill=Y)
    scroll_x.config(command=club_details.xview)
    scroll_y.config(command=club_details.yview)
    club_details.heading("c_name",text="Club Name")
    club_details.heading("m_name",text="Manager Name")
    club_details.heading("date",text="Date")
    club_details.heading("stadium",text="Stadium")
    fetch_club()
    global entry_club1
    entry_club1['state']='disabled'    

def fetch_club():
    global club_details
    import mysql.connector
    conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
    my_cursor=conn.cursor()
    my_cursor.execute("select * from club")
    rows=my_cursor.fetchall()
    for i in rows:
        club_details.insert('','end',values=i)
    my_cursor.close()
    conn.close

    club_details.bind("<ButtonRelease-1>",get_cursor)

    club_details["show"]="headings"
    club_details.pack(fill=BOTH,expand=1)
    


def table_player():
    global player_details
    scroll_x=ttk.Scrollbar(b3,orient=HORIZONTAL)
    scroll_y=ttk.Scrollbar(b3,orient=VERTICAL)
    player_details=ttk.Treeview(b3,column=("p_name","age","j_num","c_name"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM,fill=X)  
    scroll_y.pack(side=RIGHT,fill=Y)
    scroll_x.config(command=player_details.xview)
    scroll_y.config(command=player_details.yview)
    player_details.heading("p_name",text="Player name")
    player_details.heading("age",text="Age")
    player_details.heading("j_num",text="Jersey Number")
    player_details.heading("c_name",text="Club Name")

    fetch_player()
    global entry_player3
    entry_player3['state']='disabled' 
    

    player_details["show"]="headings"
    player_details.pack(fill=BOTH,expand=1)

def fetch_player():
    import mysql.connector
    conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
    my_cursor1=conn.cursor()
    my_cursor1.execute("select * from player")
    rows2=my_cursor1.fetchall()
    for i in rows2:
        player_details.insert('','end',values=i)
    my_cursor.close()
    conn.close

    player_details.bind("<ButtonRelease-1>",get_cursor_player)

    player_details["show"]="headings"
    player_details.pack(fill=BOTH,expand=1)

def table_played():
    global played_details
    scroll_x=ttk.Scrollbar(b3,orient=HORIZONTAL)
    scroll_y=ttk.Scrollbar(b3,orient=VERTICAL)
    played_details=ttk.Treeview(b3,column=("m_id","p_name","goals","assists","y_card","r_card"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM,fill=X)  
    scroll_y.pack(side=RIGHT,fill=Y)
    scroll_x.config(command=played_details.xview)
    scroll_y.config(command=played_details.yview)
    played_details.heading("m_id",text="Match id")
    played_details.heading("p_name",text="Player Name")
    played_details.heading("goals",text="Goals")
    played_details.heading("assists",text="Assists")
    played_details.heading("y_card",text="Yellow Card")
    played_details.heading("r_card",text="Red Card")
    
    fetch_played()
    global entry14 
    entry14['state']='disabled'
   

    played_details["show"]="headings"
    played_details.pack(fill=BOTH,expand=1)


def fetch_played():
    import mysql.connector
    conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
    my_cursor1=conn.cursor()
    my_cursor1.execute("select * from played")
    rows2=my_cursor1.fetchall()
    for i in rows2:
        played_details.insert('','end',values=i)
    my_cursor.close()
    conn.close

    played_details.bind("<ButtonRelease-1>",get_cursor_played)

    played_details["show"]="headings"
    played_details.pack(fill=BOTH,expand=1)
####for club
def get_cursor(event=""):
    #global club_details
    cursor_row=club_details.focus()
    content=club_details.item(cursor_row)
    row=content["values"]
    club_name.set(row[0])
    estd_date.set(row[1])
    manager_name.set(row[2])
    home_ground.set(row[3])


### for players
def get_cursor_player(event1=""):
    global player_details
    cursor_row1=player_details.focus()
    content=player_details.item(cursor_row1)
    row=content["values"]
    player_name1.set(row[0])
    age1.set(row[1])
    jersey_no1.set(row[2])
    club_name1.set(row[3])

###Fetch matches
def get_cursor_matches(event2=""):
    global match_details
    cursor_row2=match_details.focus()
    content1=match_details.item(cursor_row2)
    row=content1["values"]
    match_id1.set(row[0])
    home_team1.set(row[1])
    away_team1.set(row[2])
    home_team_score1.set(row[3])
    away_team_score1.set(row[4])

###Fetch played

def get_cursor_played(event3=""):
    global played_details
    cursor_row3=played_details.focus()
    content2=played_details.item(cursor_row3)
    row=content2["values"]
    match_id2.set(row[0])
    player_name2.set(row[1])
    goal1.set(row[2])
    assists1.set(row[3])
    yellow_card1.set(row[4])
    red_card1.set(row[5])





##### update records in club
def update_club():
    from mysql.connector import Error
    global b3

    try:
        import mysql.connector
        conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
        my_cursor=conn.cursor()
        my_cursor.execute("update club set estd_date=%s,manager_name=%s,home_ground=%s where club_name=%s",(estd_date.get(),manager_name.get(),home_ground.get(),club_name.get()))
        conn.commit()
        b3.destroy()
        b3=Frame(root,bd=3,relief=RIDGE)
        b3.place(x=10,y=570,width=760,height=220)
        table_club()
        my_cursor.close()
        conn.close()
        messagebox.showinfo("Update","Data updated successfully")
    except Error as error:
        messagebox.showerror("error",error)



def delete_club():
    from mysql.connector import Error
    global b3
    try:
        import mysql.connector
        conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
        my_cursor=conn.cursor()
        my_cursor.execute("delete from club where club_name = %s",(club_name.get(),))
        conn.commit() 
        b3.destroy()
        b3=Frame(root,bd=3,relief=RIDGE)
        b3.place(x=10,y=570,width=760,height=220)
        table_club()        
        my_cursor.close()
        conn.close() 
        messagebox.showinfo("Delete","Record Deleted Successfully")
    except Error as error:
        messagebox.showerror("error",error)



def update_player():
    
    global b3
    global player_name_player
    try:
        import mysql.connector
        from mysql.connector import Error
        conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
        my_cursor=conn.cursor()
        try:
            age=int(age1.get())
            jersey_no=int(jersey_no1.get())
            player_name_player=player_name1.get()
            club_name=club_name1.get()
        except:
            response=messagebox.showerror("error","Enter Integer Values For Age And Jersey Number")
        my_cursor.execute("update player set player_name=%s,age=%s,jersey_no=%s where club_name=%s",(player_name_player,age,jersey_no,club_name))
        conn.commit()
        b3.destroy()
        b3=Frame(root,bd=3,relief=RIDGE)
        b3.place(x=10,y=570,width=760,height=220)
        table_player()
        my_cursor.close()
        conn.close()
        messagebox.showinfo("Update","Data updated successfully")
    except Error as error:
        messagebox.showerror("error",error)

def delete_player():
    from mysql.connector import Error
    global b3
    #global player_name_player
    try:
        global player_name_player
        player_name_player=player_name1.get()
        club_name=club_name1.get()
        import mysql.connector
        conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
        my_cursor=conn.cursor()
        my_cursor.execute("delete from player where club_name = %s and player_name = %s",(club_name,player_name_player,))
        conn.commit() 
        b3.destroy()
        b3=Frame(root,bd=3,relief=RIDGE)
        b3.place(x=10,y=570,width=760,height=220)
        table_player()        
        my_cursor.close()
        conn.close() 
        messagebox.showinfo("Delete","Record Deleted Successfully")
    except Error as error:
        messagebox.showerror("error",error)





def update_matches():
    global b3
    try:
        import mysql.connector
        from mysql.connector import Error
        conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
        my_cursor=conn.cursor()
        try:
            match_id=int(match_id1.get())
            home_team=home_team1.get()
            away_team=away_team1.get()
            home_team_score=int(home_team_score1.get())
            away_team_score=int(away_team_score1.get())
        except:
            response=messagebox.showerror("error","Enter Integer Values For match id , home_team_score and away_team_score")

        my_cursor.execute("update matches set home_team=%s,away_team=%s,home_team_score=%s,away_team_score=%s where match_id=%s",(home_team,away_team,home_team_score,away_team_score,match_id))
        conn.commit()
        b3.destroy()
        b3=Frame(root,bd=3,relief=RIDGE)
        b3.place(x=10,y=570,width=760,height=220)
        table_matches()
        my_cursor.close()
        conn.close()
        messagebox.showinfo("Update","Data updated successfully")
    except Error as error:
        messagebox.showerror("error",error)



def delete_matches():
    from mysql.connector import Error
    global b3
    try:
        import mysql.connector
        conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
        my_cursor=conn.cursor()
        try:
            match_id=int(match_id1.get())
        except:
            response=messagebox.showerror("error","Enter Integer Values For match id ")
        my_cursor.execute("delete from matches where match_id = %s",(match_id,))
        conn.commit() 
        b3.destroy()
        b3=Frame(root,bd=3,relief=RIDGE)
        b3.place(x=10,y=570,width=760,height=220)
        table_matches()        
        my_cursor.close()
        conn.close() 
        messagebox.showinfo("Delete","Record Deleted Successfully")
    except Error as error:
        messagebox.showerror("error",error)

def update_played():
    global b3
    global player_name_played
    import mysql.connector
    from mysql.connector import Error
    conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
    my_cursor=conn.cursor()
    
    
    try:
        try:
            match_id_played=int(match_id2.get())
            player_name_played=player_name2.get()
            goal=int(goal1.get())
            assists=int(assists1.get())
            yellow_card =int(yellow_card1.get())
            red_card =int(red_card1.get())
        except:
            response=messagebox.showerror("error","Enter Integer Values For match id ,goal,assists,yellow card and red card")
        my_cursor.execute("update played set goal=%s,assists=%s,yellow_card=%s,red_card=%s where match_id=%s and player_name=%s",(goal,assists,yellow_card,red_card,match_id_played,player_name_played))
        conn.commit()
        b3.destroy()
        b3=Frame(root,bd=3,relief=RIDGE)
        b3.place(x=10,y=570,width=760,height=220)
        table_played()
        my_cursor.close()
        conn.close()
        messagebox.showinfo("Update","Data updated successfully")
    except Error as error:
        messagebox.showerror("error",error)




def delete_played():
    from mysql.connector import Error
    global b3
    global match_id_played
    global player_name_played
    try:
        import mysql.connector
        conn=mysql.connector.connect(host="localhost",database="project_dbms",user="root",password="pas076bei041")
        my_cursor=conn.cursor()
        try:
            match_id_played=int(match_id2.get())
            player_name_played=player_name2.get()
        except:
            response=messagebox.showerror("error","Enter Integer Values For match id ")
        my_cursor.execute("delete from played where match_id = %s and player_name=%s",(match_id_played,player_name_played,))
        conn.commit() 
        b3.destroy()
        b3=Frame(root,bd=3,relief=RIDGE)
        b3.place(x=10,y=570,width=760,height=220)
        table_played()        
        my_cursor.close()
        conn.close() 
        messagebox.showinfo("Delete","Record Deleted Successfully")
    except Error as error:
        messagebox.showerror("error",error)




root.mainloop()
