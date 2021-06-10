'''

■발생한문제
작동한 코드의 오류줄번호없이 오류가 발생하여 어디서 난 오류인지 짐작이안됨.
print두개로 감싸보며 오류난 영역을 확인해보려했으나 실패함.

■코드목적
지정한 사람의 수만큼 반복문을 돌려 점을찍고, 계속 반복해서 그 점에 대한 정보를 바꿔가며
그래프 위에서 움직이도록 하고싶음.
오류가 해결이 된다면 욕심을 부려서 전염병 감염처리(단순하게나마)도 해보고싶음.

■함수설명
update(): FuncAnimation(fig, update(population), interval = 2, blit = True)을 통해 호출되는 함수이며
          점의 위치를 실질적으로 적용해주는 역할을 해줌.

position(): update()가 돌아가면서 계속 위치를 적용해주는동안에 이 함수는 2초마다 한번씩 호출되며
            점이 이동할 방향을 바꿔줌.

updatePower_Checking(): FuncAnimation(fig, update(population), interval = 2, blit = True)를 실행할지 말지
                        판단해주는 함수인데, 1초마다 한번씩 updatePower변수(밑에 변수설명 있음)와
                        update_insertDone_called(밑에 변수설명 있음)을 확인해서 최초실행 시에 사람의 정보가
                        다 채워졌을때 아까 저것(FuncAnimation)을 실행시켜줌.


■변수설명
updatePower: update()함수를 호출하는것을 허락해주는 전원.

person: [{사람정보1}, {사람정보2}, {사람정보3}] 이런형태로 점의 위치및 상태에 대한 정보가 들어있는곳

posX_Array: 여러개의 점을 좌표에 찍을때 배열로 해야하기때문에 만들어둔 X위치들

posY_Array: 여러개의 점을 좌표에 찍을때 배열로 해야하기때문에 만들어둔 Y위치들

personform: 점 모양

update_insertDone_called: update()함수 안에 for문을 돌다가 모든 사람의 정보가 다 기록이 되었으면
                          True로 바꾸어서 ' FuncAnimation(fig, update(population), interval = 2, blit = True) '를
                          두번이상 호출하지 못하도록 해주는역할. (어차피 한번만 불러도 반복해주니까.)

posX: 사람의 X좌표

posY: 사람의 Y좌표

posX_var: 사람의 X방향 변화랑(update()함수가 호출될때마다 이동되는 변화량)

posY_var: 사람의 Y방향 변화량(update()함수가 호출될때마다 이동되는 변화량)

population: 사람수, 곧 점의 수임.



'''


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import time
import threading
import schedule

updatePower = False

fig, ax = plt.subplots()
ax.set_xlim(1, 1000)
ax.set_ylim(1, 1000)

person = [] # person info ex: [{posX:1,posY:2}]
posX_Array = [] # person X position
posY_Array = [] # person Y position

personForm = "bo"

line, = plt.plot(500, 500, personForm)
population = 3 # number of person

update_insertDone_called = False

def update(people):
    print("[update] was called!")
    global person
    global posX_Array
    global posY_Array
    global update_insertDone_called
    
    posX_Array = []
    posY_Array = []

    for t in range(people):
        if person != []:
            posX_Array = []
            posY_Array = []
            print()
            print("update->person was called!")
            
            for k in range(population):
                if person[k]["posX"] >= 1000 or person[k]["posX"] < 0: # posX constraint
                    person[k]["posX_var"] = person[k]["posX_var"] * -1 # reverse direction
                if person[k]["posY"] >= 1000 or person[k]["posY"] < 0: # posY constraint
                    person[k]["posY_var"] = person[k]["posY_var"] * -1 # reverse direction
                person[k]["posX"] = int(person[k]["posX"]) + person[k]["posX_var"]
                posX_Array.insert(k, person[k]["posX"])
                person[k]["posY"] = int(person[k]["posY"]) + person[k]["posY_var"]
                posY_Array.insert(k, person[k]["posY"])
                if k+1 == population:
                    update_insertDone_called = True
                    print("update_insertDone_called : " + str(update_insertDone_called))
                    line.set_data(posX_Array, posY_Array) # Apply location
                    return line,

def position():
    global person
    global population
    global updatePower
    
    while True:
        print("[position] was Called!")
        time.sleep(2)
        
        if person == []: # Default value when there is nothing in the array.
            for t in range(population):
                person.insert(t, {"posX": int(random.randint(100,500)), "posY": 500, "posX_var": 2, "posY_var": 2})
                posX_Array.insert(t, person[t]["posX"])
                posY_Array.insert(t, person[t]["posY"])
                print(str(t+1) + "st Input")
                print("person Var: " + str(person))
                print("최초 점 적용 시작.")
                line.set_data(posX_Array, posY_Array) # Apply location
                print("완료! (위치:position->person==[])")
                if len(person) == population:
                    updatePower = True
                    print("=======================")
                    print("posX_Array insert done.")
                    print("Array Print")
                    print("=======================")
                    print(str(posX_Array))

        if len(person) == population:
            for t in range(population):
                i = random.randint(0,1)
                if i == 0:
                    person[t]["posX_var"] = 2
                else:
                    person[t]["posX_var"] = -2

                i = random.randint(0,1)

                if i == 0:
                    person[t]["posY_var"] = 2
                else:
                    person[t]["posY_var"] = -2
                
                
                print(str(t) +"번째 posX_var값: " + str(person[t]["posX_var"]))
                print(str(t) +"번째 posY_var값: " + str(person[t]["posY_var"]))

posThread = threading.Thread(target = position)
posThread.start()

def updatePower_Checking():
    global updatePower
    global population
    print("updatePower_Checking Function Called.")
    print("updatePower_Check: " + str(updatePower))
    if updatePower == True and update_insertDone_called == False:
        ani = FuncAnimation(fig, update(population), interval = 2, blit = True)
        plt.show()
        print("updatePower_Check: " + str(updatePower))
        time.sleep(1)

schedule.every(1).second.do(updatePower_Checking)

while True:
    schedule.run_pending()
    time.sleep(1)
