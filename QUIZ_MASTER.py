import pymysql 
import prettytable as prt
import sys 
import time

#==============================================================================================================================================================================

def chk_connection():
    
    mycon=None
    try:
        mycon=pymysql.connect(user='root',host='localhost',password='abhay@2611',database='QUIZ_MNGT_SYSTEM')
    except:
        pass
    if mycon!=None:
        con=True
        #print('CONNECTION ESTABLISHED SUCCESSFULL')
        mycon.close()
        return con
        #print('Version:',mycon.version_info)
    else:
        print('\n\n\n')
        print('=================================CONNECTION FAILED WITH DATABASE !  WE ARE SORRY FOR THE INCONVINIENCE===================\n\n')
        return False
            
    
    

#chk_connection()




#==============================================================================================================================================================================

def get_subject_nm(typ):
    print("\n\n"+'='*20+"SUBJECT AVAILABLE WITH THIER CODE"+"="*20)
    
    subject=["CS","PHYSICS","CHEMISTRY","MATHS","ENGLISH"]
    i=0
    x=prt.PrettyTable(["CODE","SUBJECT"])
    for sub in subject:
        x.add_row((i,sub))
        i+=1

    print(x)


    while True:
        print('\nENTER SUBJECT CODE TO '+typ+'OF: ',end='')
        try:
            
            sub_code=int(input())
            if sub_code<i and sub_code>-1:
                    break
            else:
                    print('\t\tENTER CORRECT SUBJECT CODE !\n')
        except ValueError:
            print('\tONLY NUMBERS EXPECTED!')

    return subject[sub_code]



    

#==============================================================================================================================================================================
def insert_many_ques():
    cur=None

    try:
        
        mycon=pymysql.connect(user='root',host='localhost',password='abhay@2611',database='QUIZ_MNGT_SYSTEM')
        cur=mycon.cursor()

        #TO FETCH MAX QID-------------------------
        qry='SELECT MAX(QID) FROM QUIZ_MST'     
        cur.execute(qry)

        row=cur.fetchone()
        max_qid=int(row[0])
        if max_qid:  #IF ANY RECORD EXIST IN TABLE
            new_qid=max_qid+1
        else:
            new_qid=1

        #QUESTION ADDING  TO DATABASE ------------------------------
        print('\t\t\t\t\t\t===================================')
        subject=get_subject_nm("ADD QUESTION ")

        questions=list()
        print('\t\t\t\tMAXIMUM CHARACTER LENGTH FOR QUESTION IS = 600 \n')
        
        while True:
            
            ques=input('ENTER QUESTION:  ')
            if len(ques)>600:
                print('\tQUESTION LENGTH IS GREATER THAN 600! REDUCE YOUR QUESTION SIZE AND RE-ENTER QUESTION')
                continue
            op1=input('ENTER OPTION 1:  ')
            op2=input('ENTER OPTION 2:  ')
            op3=input('ENTER OPTION 3:  ')
            correct=input('ENTER CORRECT OPTION NUMBER[A-C]:  ')
            

            
            

            questions.append((new_qid,ques,op1,op2,op3,correct,subject))

            print('\n\t====WISH TO ADD MORE QUESTION ? \n====PRESS [Y/y] TO ADD:',end='')
            choice=input()

            if choice.lower()=='y':
                new_qid+=1

            else:
                break


        qry='INSERT INTO QUIZ_MST VALUES(%s,%s,%s,%s,%s,%s,%s)'
        cur.executemany(qry,tuple(questions))
        mycon.commit()
        print('\t\t\t\t\t\t\t\t                 ===============================')
        print('\t\t\t\t\t\t\t\t=================!QUESTION ADDITION SUCCESSFULL!=================')


    except pymysql.DatabaseError as e:
        if mycon:
            mycon.rollback()
            print('\t\t\t\t\t\t=====!QUESTION ADDITION FAILED!======')
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()


#insert_many_ques()


#==============================================================================================================================================================================

def show_all():
    cur=None

    try:
        print('\n\t\t\t\t\t\t\t\t\t      =====================')
        print('=============================================================================  SHOWING ALL RECORDS  ==========================================================='+'='*30)
        print('\t\t\t\t\t\t\t\t\t      =====================\n\n')
        
        mycon=pymysql.connect(user='root',host='localhost',password='abhay@2611',database='QUIZ_MNGT_SYSTEM')
        cur=mycon.cursor()
        qry="SELECT * FROM QUIZ_MST "

        tble=prt.PrettyTable(["QUESTION ID","QUESTION","OPTION A","OPTION B","OPTION C","CORRECT ANSWER","SUBJECT"])

        count=0
        cur.execute(qry)
        for row in cur.fetchall():
            tble.add_row(row)
            count+=1
        
        print(tble)
        print('\n\n\t\t\t\t\t\t\t\t\t\t>>>TOTAL  {}  RECORDS FETCHED<<<'.format(count))



    except pymysql.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()





#show_all()




#==============================================================================================================================================================================
def search_ques():
    cur=None
    
    try:
        print('\n\n==================================================================  SEARCH CONSOLE   ================================================================================')
        mycon=pymysql.connect(user='root',host='localhost',password='abhay@2611',database='QUIZ_MNGT_SYSTEM')
        cur=mycon.cursor()
        try:
            qid=int(input('ENTER QID OF THE QUESTION TO BE SEARCHED: '))
        except ValueError:
            print("\n\t\t=====!  INVALID QID  !  NUMBERS ONLY EXPECTED  !=====")
            return
        
        qry="SELECT * FROM QUIZ_MST WHERE qid=%s"
        cur.execute(qry,qid)

        row_det=cur.fetchall()
        
        if not row_det:
            print('\n====================!NO SUCH QUESTION WITH GIVEN QID EXIST!====================')

        else:
            row=row_det[0]
            print('\t\t\t\t\t\t\t=========================== ')
            print('\t\t\t\t\t\t\t!REQUIRED QUESTION DETAILS!\t')
            print('\t\t\t\t\t\t\t=========================== ')
            print('\nQID: {}\nQUESTION: {}\nOPTION 1: {}\nOPTION 2:{} \nOPTION 3: {}\nCORRECT OPTION: {}\nSUBJECT: {}'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            print('\t\t\t\t\t\t========================================== ')

                
    
    except pymysql.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()



#==============================================================================================================================================================================

def update_ques():
    cur=None
    
    try:
        print('==================================================================  UPDATE FORM   ================================================================================')
        mycon=pymysql.connect(user='root',host='localhost',password='abhay@2611',database='QUIZ_MNGT_SYSTEM')
        cur=mycon.cursor()
        try:
            qid=int(input('ENTER QID OF THE QUESTION TO BE EDITED: '))
        except ValueError:
            print("\n\t\t=====!  INVALID QID  !  NUMBERS ONLY EXPECTED  !=====")
            return
        
        qry="SELECT * FROM QUIZ_MST WHERE qid=%s"
        cur.execute(qry,qid)

        row_det=cur.fetchall()
        
        if not row_det:
            print('NO SUCH QUESTION WITH GIVEN QID EXIST')

        else:
            row=row_det[0]
            print('\t\t\t\t\t\t\t=========================== ')
            print('\t\t\t\t\t\t\t!CURRENT QUESTION DETAILS!\t')
            print('\t\t\t\t\t\t\t=========================== ')
            print('\nQID: {}\nQUESTION: {}\nOPTION 1: {}\nOPTION 2:{} \nOPTION 3: {}\nCORRECT OPTION: {}\nSUBJECT: {}'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            print('\t\t\t\t\t\t========================================== ')

            print('\t\t\t\t\t\t!PLEASE ENTER NEW DETAILS OF THIS QUESTION!')
            print('\t\t\t\t\t\t========================================== ')

            while True:
            
                n_ques=input('ENTER NEW QUESTION:  ')
                if len(n_ques)>600:
                    print('\tQUESTION LENGTH IS GREATER THAN 600! REDUCE YOUR QUESTION SIZE AND RE-ENTER QUESTION')
                    continue
                n_op1=input('ENTER OPTION 1:  ')
                n_op2=input('ENTER OPTION 2:  ')
                n_op3=input('ENTER OPTION 3:  ')
                n_correct=input('ENTER CORRECT OPTION NUMBER[A-C]:  ')
                n_subject=input('ENTER NEW SUBJECT NAME: ')
                break

            qry='''UPDATE  QUIZ_MST 
                SET
                QNAME=%s,
                op1=%s,
                op2=%s,
                op3=%s,
                correct_op=%s,
                subject=%s
                WHERE QID=%s
                '''
            cur.execute(qry,(n_ques,n_op1,n_op2,n_op3,n_correct,n_subject,qid))
            mycon.commit()
            print('\n\n===============!QUESTION EDITED SUCCESSFULLY!===========================')
    

    except pymysql.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()


#update_ques()
#==============================================================================================================================================================================
def delete_ques():
    cur=None

    print('='*188)
    print('\t\t\t\t\t\t\t\t\t\tDELETE FORM')
    print('\t\t\t\t\t\t\t\t\t\t===========')

    ch=True
    print()
    while ch:
        try:
            qid=int(input('\n>>>ENTER QID OF THE QUESTION TO BE DELETED:'))
            ch=False

        except ValueError:
            print('\n\t\t\t\t\t\t\t\t\t!PLEASE ENTER ONLY A VALID QUESTION ID!\n\t\t\t\t\t\t\t\t\t       !ONLY NUMBERS EXCEPTED!')

    try:
        mycon=pymysql.connect(user='root',host='localhost',password='abhay@2611',database='QUIZ_MNGT_SYSTEM')
        cur=mycon.cursor()

        #CHECKING WETHER QID IS PRESENT OR NOT IN DATABASE
        qry="SELECT * FROM QUIZ_MST WHERE QID=%s"
        cur.execute(qry,qid)

        row_det=cur.fetchall()
        

        if not row_det:  #IF QID IS NOT PRESENT IN THE DB THEN GOES IN THIS BLOCK

            print('\n\n\t\t\t\t\t\t\t\t\t=================================')
            print('\t\t\t\t\t\t\t\t\tNO SUCH RECORD EXIST WITH QID=',qid)
            print('\t\t\t\t\t\t\t\t\t=================================')
            
        else:            #IF QID DOES EXIST
            
            row=row_det[0]
            print('\n\n\t\t\t\t\t\t\t\t\t==========!CURRENT QUESTION RECORD!==========')
            print('QID:  ',qid)
            print('QUESTION:  ',row[1])
            print('OPTION 1:  ',row[2])
            print('OPTION 2:  ',row[3])
            print('OPTION 3:  ',row[4])
            print('CORRECT OPTION:  ',row[5])
            print('SUBJECT:  ',row[6])

            time.sleep(2)

            print('\n\n!DO YOU REALLY WANT TO DELETE THIS RECORD!\nPRESS Y\y:  ',end='')
            choice=input()
            if choice.lower()=='y':
                qry='DELETE FROM QUIZ_MST WHERE QID=%s'
                cur.execute(qry,qid)
                mycon.commit()
                print('\n\n\t\t\t\t\t\t\t\t\t===============================')
                print('\t\t\t\t\t\t\t\t\t!QUESTION DELETED SUCCESSFULLY!')
                print('\t\t\t\t\t\t\t\t\t===============================')
                
            else:
                print('\n\n\t\t\t\t\t\t\t\t\t=======================')
                print('\t\t\t\t\t\t\t\t\t!QUESTION NOT DELETED !')
                print('\t\t\t\t\t\t\t\t\t=======================')
                pass




    except pymysql.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()


#delete_ques()


#==============================================================================================================================================================================

def play():
    cur=None
    
    print('==========================================================================  PLAY  QUIZ  ================================================================================')

    # vALUES NEEDED  TO BE INSERTED AFTER TEST IN "STUDENT_MST" --------
    name=input("\n\nENTER YOUR NAME:  ")
    total_marks=0
    cans=0
    wans=0
    subject_name=''
    new_sid=1
    #--------------------------------------------

    try:

        
        mycon=pymysql.connect(user='root',host='localhost',password='abhay@2611',database='QUIZ_MNGT_SYSTEM')
        cur=mycon.cursor()

        query="SELECT * FROM QUIZ_MST WHERE SUBJECT=%s"
        subject_name=get_subject_nm("TAKE TEST ")
        cur.execute(query,(subject_name,))

        row_det=cur.fetchall()
        if not row_det:
            print("\n\n\t\t\t\t=============="'!NO QUESTIONS EXIST FOR THHIS SUBJECT!'+"==============")
        else:
            
            print('\n\t\t\t=================!TEST READY!=================')
            for qid,ques,op1,op2,op3,crt,sub in row_det:

                print('\n QUESTION: {}\n OPTION A: {}\n OPTION B: {}\n OPTION C: {}\n'.format(ques,op1,op2,op3))

                print('\t\tENTER YOUR ANSWER[A-C]:  ',end='')
                choice=input()

                if choice.lower()==crt.lower():
                    total_marks+=5
                    cans+=1
                else:
                    total_marks-=2
                    wans+=1

            print('\tYOUR SCORE FOR THIS TEST IS :',total_marks)

            
            
            query="SELECT MAX(SID) FROM STUDENT_MST"
            cur.execute(query)
            row=cur.fetchall()
            max_sid=row[0][0]
            
            if max_sid:
                new_sid=max_sid+1
                #print(new_sid)

            
            
            row_student=(int(new_sid),name,int(cans),int(wans),subject_name,int(total_marks))
            query="INSERT INTO STUDENT_MST VALUES(%s,%s,%s,%s,%s,%s)"
            cur.execute(query,row_student)


            mycon.commit()




    except pymysql.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()



#play()

#==============================================================================================================================================================================
def scoreboard():
    cur=None
    
    try:
        mycon=pymysql.connect(user='root',host='localhost',password='abhay@2611',database='QUIZ_MNGT_SYSTEM')
        cur=mycon.cursor()

        qry="SELECT * FROM STUDENT_MST"
        cur.execute(qry)
        row_det=cur.fetchall()

        
        
        if row_det:
            x=prt.PrettyTable(["SID","STUDENT NAME","CRT ANS","WRNG ANS","SUBJECT","TOTAL MARKS"])
            print(' '*75+"!FETCHING STUDENTS RECORD!"+'\n'+" "*75+"========================="+"\n\n")
            time.sleep(2)
            for row in row_det:
                x.add_row(row)
            print(x)

        else:
            print(end='\n\n')
            print(' '*75+"==========================")
            print(" "*75+'!NO RECORD EXIST TILL NOW!')
            print(' '*75+"==========================")
    
    except pymysql.DatabaseError as e:
        if mycon:
            mycon.rollback()
            
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()


#scoreboard()
#==============================================================================================================================================================================
def score_arrange():
    cur=None
    
    print('\n\n'+"="*188)
    try:
        mycon=pymysql.connect(user='root',host='localhost',password='abhay@2611',database='QUIZ_MNGT_SYSTEM')
        cur=mycon.cursor()

        sub=get_subject_nm("SEARCH TOP 3 ")
        qry="SELECT * FROM STUDENT_MST WHERE SUBJECT=%s ORDER BY TOTAL_MARKS DESC"
        cur.execute(qry,sub)

        row_det=cur.fetchall()
        num=[]
        x=prt.PrettyTable(["SID","STUDENT NAME","CRT ANS","WRNG ANS","SUBJECT","TOTAL MARKS","RANK"])
        print(' '*75+"!FETCHING STUDENTS RECORD!"+'\n'+" "*75+"========================="+"\n\n")
        time.sleep(2)
        
        for row in row_det:

            if len(num)<3:
                if row[5] not in num:
                    num.append(row[5])
                rank=(len(num),)
                x.add_row(row+rank)
            elif len(num)==3:
                if row[5] in num:
                    x.add_row(row)
            elif len(num)>3:
                break
                
        if row_det:
            print('='*20+"TOP 3 STUDENTS DETAILS OF "+sub+"="*20)
            print(x)
        
        else:
            print(end='\n\n')
            print(' '*75+"==========================")
            print(" "*75+'!NO RECORD EXIST TILL NOW!')
            print(' '*75+"==========================")

            
    
    except pymysql.DatabaseError as e:
        if mycon:
            mycon.rollback()
            print('abhay')
            
        print('Database Error : ',e)
                    
    finally:
        if cur:
            cur.close()
        if mycon:
            mycon.close()

#score_arrange()

#==============================================================================================================================================================================


def admin():
    while True:

        time.sleep(2)
        print('\n\n\n\n','='*188,sep='')
        print(' '*85,'ADMIN SECTION')
        print(' '*85,'=============\n')
        print(' '*75,'ENTER 1 - TO ADD QUESTION')
        print(' '*75,'ENTER 2 - TO UPDATE QUESTION')
        print(' '*75,'ENTER 3 - TO SHOW ALL QUESTION')
        print(' '*75,'ENTER 4 - TO SEARCH QUESTION RECORD')
        print(' '*75,'ENTER 5 - TO TO DELETE QUESTION')
        print(' '*75,'ENTER 6 - TO RETURN TO HOME MENU')

        ch=None
        
        while True:
            try:
                ch=int(input(' '*75+'ENTER YOUR CHOICE: '))
                break
            except ValueError:
                print('\n\t\t\t\t\t\t\t\t\t\t======================\n\t\t\t\t\t\t\t\t\t\t!NUMBERS ONLY EXPECTED!\n\t\t\t\t\t\t\t\t\t\t======================')

        if ch==None:
            pass
        elif ch==1:
            insert_many_ques()
        elif ch==2:
            update_ques()
        elif ch==3:
            show_all()
        elif ch==4:
            search_ques()
        elif ch==5:
            delete_ques()
        elif ch==6:
            print('='*188)
            print('\n'+' '*75+'RETURNING TO HOME MENU.....\n')
            time.sleep(2)
            return 
        else:
            print('\n\t\t\t\t\t\t\t\t\t\t\t!NUMBER OUT OF RANGE!')
        
            
        






#==============================================================================================================================================================================

#DRIVER CODE
#MAIN MENU

if chk_connection():            

    while True:
        
            
        print('\n\n'+'='*188)
        print(' '*85+"MAIN MENU"+"\n"+" "*85+"=========\n")
        print(' '*75,'ENTER 1 -  ADMIN SECTION')
        print(' '*75,'ENTER 2 -  PLAY SECTION')
        print(' '*75,'ENTER 3 -  VIEW SCOREBOARD')
        print(' '*75,'ENTER 4 -  VIEW TOP 3 STUDENT OF A SUBJECT')
        print(' '*75,'ENTER 5 -  EXIT THE SOFTWARE')
        #print(' '*75,'ENTER YOUR CHOICE: ',end='')

        ch=None
        while True:
            try:
                ch=int(input(' '*75+'ENTER YOUR CHOICE: '))
                print('='*188)
                break
            except ValueError:
                print('\n',' '*75,'!NUMBERS ONLY EXCEPTED!\n\n')

        if ch==None:
            continue
        elif ch==1:
            print('\n'+' '*75+'REDIRECTING TO ADMIN SECTION...')
            admin()
        elif ch==2:
            play()
        elif ch==3:
            scoreboard()
        
        elif ch==4:
            score_arrange()
        elif ch==5:
            print()
            print('='*188)
            print('\n'+' '*75+'THANK YOU FOR USING THIS SOFTWARE')
            print('='*188)
            time.sleep(5)
            sys.exit()
        else:
            print(' '*75+'!CHOICE OUT OF RANGE!')
            

 
else:
    print('\n\n\n\n==================================PLEASE VISIT HERE AGAIN!==========================================')
    input()


    
