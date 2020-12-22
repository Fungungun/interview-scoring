
#房间号：人数
room_person = {
    "1": 10,
    "2": 10,
    "3": 10,
    "4": 10,
    "5": 10,
    "6": 10,
    "7": 10,
    "8": 10,
}


draw_id = []
for r in room_person:
    for j in range(1, room_person[r] + 1):
        draw_id.append(f"{r}-{j}")

# print(draw_id)

# 考官号
examiner_id = [
    1, 2, 3, 4, 5, 6, 7
]

scoring_items = [
    {
        "id": 1,
        "name":"职位及自我认知能力",
        "maximum_score": 35,
        "good":"30-35",
        "ok":"21-29",
        "normal":"1-20",
    },
    {
        "id": 2,
        "name":"综合分析能力",
        "maximum_score": 30,
        "good":"25-30",
        "ok":"16-24",
        "normal":"1-15",
    },
    {
        "id": 3,
        "name":"应急应变能力",
        "maximum_score": 25,
        "good":"20-25",
        "ok":"11-19",
        "normal":"1-10",
    },
    {
        "id": 4,
        "name":"言语表达及仪表",
        "maximum_score": 10,
        "good":"9-10",
        "ok":"6-8",
        "normal":"1-5",
    },
    # {
    #     "id": 5,
    #     "name":"新考察项目1",
    #     "maximum_score": 123,
    #     "good":"123",
    #     "ok":"123",
    #     "normal":"123",
    # },
    # {
    #     "id": 6,
    #     "name":"新考察项目2",
    #     "maximum_score": 123,
    #     "good":"123",
    #     "ok":"123",
    #     "normal":"123",
    # },
    # {
    #     "id": 7,
    #     "name":"新考察项目3",
    #     "maximum_score": 123,
    #     "good":"123",
    #     "ok":"123",
    #     "normal":"123",
    # },
    ]