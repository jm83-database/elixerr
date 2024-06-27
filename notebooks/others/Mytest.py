## 클래스 선언 부분 ##
class Car :
    color = ''
    speed = 0

    def upSpeed(self, value):
        self.speed += value

    def downSpeed(self, value):
        self.speed -= value

## 메인 코드 부분 ##
myCar1 = Car()
myCar1.color = '빨강'
myCar1.speed = 0

myCar2 = Car()
myCar2.color = '파랑'
myCar2.speed = 0

myCar3 = Car()
myCar3.color = '노랑'
myCar3.speed = 0

myCar1.upSpeed(30)
print("자동차1의 색상은 %s이며, 현재 속도는 %d입니다." %(myCar1.color, myCar1.speed))

myCar2.upSpeed(60)
print("자동차2의 색상은 %s이며, 현재 속도는 %d입니다." %(myCar2.color, myCar2.speed))

myCar3.upSpeed(0)
print("자동차3의 색상은 %s이며, 현재 속도는 %d입니다." %(myCar3.color, myCar3.speed))

class Car2 :
    color = ''
    
    speed = 0
    def __init__(self):
        self.color = '빨강'
        self.speed = 0

    def upSpeed(self, value):
        self.speed += value

    def downSpeed(self, value):
        self.speed -= value
    

myCar4 = Car2()
myCar5 = Car2()

print("자동차4의 색상은 %s이며, 현재 속도는 %d입니다." %(myCar4.color, myCar4.speed))
print("자동차5의 색상은 %s이며, 현재 속도는 %d입니다." %(myCar5.color, myCar5.speed))

## 매개변수가 있는 생성자 ##
class Car3 :
    color = ''
    speed = 0

    def __init__(self, value1, value2):
        self.color = value1
        self.speed = value2

    def upSpeed(self, value):
        self.speed += value

    def downSpeed(self, value):
        self.speed -= value

myCar6 = Car3('빨강', 30)
myCar7 = Car3('파랑', 60)

print("자동차6의 색상은 %s이며, 현재 속도는 %d입니다." %(myCar6.color, myCar6.speed))
print("자동차7의 색상은 %s이며, 현재 속도는 %d입니다." %(myCar7.color, myCar7.speed))

## 자동차 생산 대수를 세는 클래스 ##
class Car4 :
    color = '' # 인스턴스 변수
    speed = 0 # 인스턴스 변수
    count = 0 # 인스턴스 변수

    def printMessage():
        print('시험 출력입니다.')

    def __init__(self):
        self.speed = 0
        Car4.count += 1

# 변수 선언
myCar8, myCar9 = None, None # 안 해도 무

# 메인 코드 부분

myCar8 = Car4()
myCar8.speed = 30
print("자동차8의 현재 속도는 %dkm, 생산된 자동차는 총 %d대입니다." %(myCar8.speed, myCar8.count))

myCar9 = Car4()
myCar9.speed = 60
print("자동차9의 현재 속도는 %dkm, 생산된 자동차는 총 %d대입니다." %(myCar9.speed, myCar9.count))


## 매서드 오버라이딩(상속) ##

class Car5 :
    speed = 0

    def upSpeed(self, value):
        self.speed += value
        print('현재 속도(슈퍼 클래스) : %d' %self.speed)

class Sedan(Car5):
    def upSpeed(self, value):
        self.speed += value

        if self.speed > 150:
            self.speed = 150

        print('현재 속도(서브 클래스) : %d' %self.speed)

class Truck(Car5):
    pass

## 변수 선언

sedan1, truck1 = None, None

## 메인 코드
sedan1 = Sedan()
truck1 = Truck()

print('트럭 --> ', end = '')
truck1.upSpeed(200)

print('승용차 -->', end = "")
sedan1.upSpeed(200)

sonata = Sedan()
print('소나타 -->', end = '')
sonata.upSpeed(200)

## 클래스의 특별한 메서드 ##
class Line :
    length = 0
    def __init__(self, length):
        self.length = length
        print(self.length, '길이의 선이 생성되었습니다.')
    
    def __del__(self):
        print(self.length, '길이의 선이 삭제되었습니다.')
    
    def __repr__(self):
        return '선의 길이 :' + str(self.length)
    
    def __add__(self, other):
        return self.length + other.length
    
    def __lt__(self, other):
        return self.length < other.length
    
    def __eq__(self, other):
        return self.length == other.length
    
## 메인 코드 ##
myLine1 = Line(100)
myLine2 = Line(200)

print(myLine1)

print('두 선의 길이 합 :', myLine1 + myLine2)

if myLine1 < myLine2 :
    print('선분 2가 더 기네요.')
elif myLine1 == myLine2 :
    print('두 선분이 같네요.')
else :
    print('모르겠네요')

del(myLine1)