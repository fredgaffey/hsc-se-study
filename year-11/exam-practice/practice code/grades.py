import random
# students = []
# for i in range(100):
#     students.append(dic := {"effort":random.randint(0,10),"score":random.randint(0,100)})
#     print(dic)
    
students = [
{"name": "Student 1", "effort": 8, "score": 95},
{"name": "Student 2", "effort": 7, "score": 85},
{"name": "Student 3", "effort": 5, "score": 72},
{"name": "Student 4", "effort": 9, "score": 94},
{"name": "Student 5", "effort": 8, "score": 89},
{"name": "Student 6", "effort": 7, "score": 83},
{"name": "Student 7", "effort": 4, "score": 74},
{"name": "Student 8", "effort": 10, "score": 98},
{"name": "Student 9", "effort": 5, "score": 79},
{"name": "Student 10", "effort": 8, "score": 87}
]    
def get_band(score):
    if score == 100:
        return 6
    elif score <= 50:
        return 1
    n = (str(score))
    n = n[0]
    n = int(n)
    print(n -3 ,score)
    return n -3


band_sum = 0
ave_effort = 0
student_count = 0
for i in students:
    student_count += 1
    band_sum += get_band(i["score"])
    ave_effort += i["effort"]

print("Average Band", int(band_sum/student_count))
print("Average Effort", round(ave_effort/student_count,2))

