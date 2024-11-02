from query import Query
from teacher_crud import TeacherCRUD

from pprint import pprint
from database import Neo4jDriver

driver = Neo4jDriver.get_driver()
session = driver.session()
query = Query(session)

print('\n', '-' * 20)
print('\nQuestão 1 - A')
renzo = query.get_teacher("Renzo")
pprint(renzo)

print('\nQuestão 1 - B')
starts_with_m = query.get_teacher_starts("M")
pprint(starts_with_m)

print('\nQuestão 1 - C')
all_city_names = query.get_all_city_names()
pprint(all_city_names)

print('\nQuestão 1 - D')
schools_between = query.get_schools_between(150, 550)
pprint(schools_between)

print('\n', '-' * 20)
print('\nQuestão 2 - A')
oldes_teacher = query.get_oldest_teacher()
youngest_teacher = query.get_youngest_teacher()
pprint({"oldest": oldes_teacher, "youngest": youngest_teacher})

print('\nQuestão 2 - B')
avg_population = query.get_avg_population()
pprint(avg_population)

print('\nQuestão 2 - C')
city_sub_a = query.get_city_sub_a("37540-000")
pprint(city_sub_a)

print('\nQuestão 2 - D')
teacher_substring = query.get_teacher_substring()
pprint(teacher_substring)

print('\n', '-' * 20)
print('\nQuestão 3 - B')
teacher_crud = TeacherCRUD(session)
teacher_crud.create('Chris Lima', 1956, '189.052.396-66')
pprint('Created Teacher Chris Lima')
pprint(teacher_crud.read('Chris Lima'))

print('\nQuestão 3 - C')
chris = teacher_crud.read('Chris Lima')
pprint('Teacher Chris Lima')
pprint(chris)

print('\nQuestão 3 - D')
teacher_crud.update('Chris Lima', '162.052.777-77')
pprint('Updated Teacher Chris Lima')
pprint(teacher_crud.read('Chris Lima'))


print('\n', '-' * 20)
