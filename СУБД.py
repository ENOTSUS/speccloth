from graphviz import Digraph

# Создаем объект диаграммы
dot = Digraph(comment='BPMN Diagram for Special Clothing Production Information System')

# Определяем роли
dot.node('Admin', 'Администратор', shape='rect', style='filled', fillcolor='lightgrey')
dot.node('Employee', 'Сотрудник', shape='rect', style='filled', fillcolor='lightgrey')
dot.node('DB', 'База данных', shape='cylinder')

# Определяем процессы для администратора
dot.node('Admin_Start', '', shape='circle', style='filled', fillcolor='lightgreen')
dot.node('Admin_Authorize', 'Авторизация', shape='rect')
dot.node('Admin_Decision', '', shape='diamond')
dot.node('Admin_ManageAccounts', 'Управление аккаунтами сотрудников', shape='rect')
dot.node('Admin_DeleteData', 'Удаление данных', shape='rect')
dot.node('Admin_Confirm', 'Подтвердить изменения', shape='rect')
dot.node('Admin_Record', 'Запись', shape='rect')
dot.node('Admin_End', '', shape='circle', style='filled', fillcolor='red')

# Определяем процессы для сотрудника
dot.node('Employee_Start', '', shape='circle', style='filled', fillcolor='lightgreen')
dot.node('Employee_Authorize', 'Авторизация', shape='rect')
dot.node('Employee_Decision', '', shape='diamond')
dot.node('Employee_AddData', 'Добавление данных', shape='rect')
dot.node('Employee_Report', 'Составление отчетов по продажам', shape='rect')
dot.node('Employee_Order', 'Составление заказа', shape='rect')
dot.node('Employee_End', '', shape='circle', style='filled', fillcolor='red')

# Связи для администратора
dot.edge('Admin_Start', 'Admin_Authorize')
dot.edge('Admin_Authorize', 'Admin_Decision')
dot.edge('Admin_Decision', 'Admin_ManageAccounts', label='Управление аккаунтами')
dot.edge('Admin_Decision', 'Admin_DeleteData', label='Удаление данных')
dot.edge('Admin_ManageAccounts', 'Admin_Confirm')
dot.edge('Admin_DeleteData', 'Admin_Confirm')
dot.edge('Admin_Confirm', 'Admin_Record')
dot.edge('Admin_Record', 'Admin_End')

# Связи для сотрудника
dot.edge('Employee_Start', 'Employee_Authorize')
dot.edge('Employee_Authorize', 'Employee_Decision')
dot.edge('Employee_Decision', 'Employee_AddData', label='Добавление данных')
dot.edge('Employee_Decision', 'Employee_Report', label='Составление отчетов')
dot.edge('Employee_Decision', 'Employee_Order', label='Составление заказа')
dot.edge('Employee_AddData', 'Employee_End')
dot.edge('Employee_Report', 'Employee_End')
dot.edge('Employee_Order', 'Employee_End')

# Связи с базой данных
dot.edge('Admin_Authorize', 'DB')
dot.edge('Employee_Authorize', 'DB')
dot.edge('Admin_Record', 'DB')
dot.edge('Employee_AddData', 'DB')
dot.edge('Employee_Report', 'DB')
dot.edge('Employee_Order', 'DB')

# Вывод диаграммы
dot.render('/mnt/data/BPMN_Business_Model_Updated', format='png', cleanup=False)
'/mnt/data/BPMN_Business_Model_Updated.png'
