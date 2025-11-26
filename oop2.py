class Task:
    def __init__(self, name):
        self.__name = name
        self.__status = "todo"
        self.__assigned = None

    def get_name(self):
        return self.__name

    def get_status(self):
        return self.__status

    def get_assigned(self):
        return self.__assigned

    def set_status(self, new_status, user):
        if (new_status == "todo") or (new_status == "in_progress") or (new_status == "done"):
            self.__status = new_status
        else:
            print("Нет такого статуса")

    def set_assigned(self, assigned):
        self.__assigned = assigned

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def get_name(self):
        return self.name

    def get_role(self):
        return self.role

    def can_edit_task(self, task):
        return False

class Admin(User):
    def __init__(self, name):
        super().__init__(name, "Admin")

    def can_edit_task(self, task):
        return True

class Manager(User):
    def __init__(self, name):
        super().__init__(name, "Manager")

    def can_edit_task(self, task):
        return True


class Employee(User):
    def __init__(self, name):
        super().__init__(name, "Employee")

    def can_edit_task(self, task):
        if task and task.get_assigned() == self:
            return True
        else:
            return False

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.users = []

    def create_task(self, name):
        task = Task(name)
        self.tasks.append(task)
        return task

    def add_user(self, user):
        self.users.append(user)

    def assign_task(self, task, assigned, user):
        if not user.can_edit_task(task):
            print(f"Пользователю {user.get_name()} нельзя назначать задачи")
            return False
        
        task.set_assigned(assigned)
        print(f'Задача "{task.get_name()}" назначена {assigned.get_name()} пользователем {user.get_name()}')
        return True

    def change_status(self, task, new_status, user):
        if not user.can_edit_task(task):
            print(f"Пользователю {user.get_name()} нельзя менять статус этой задачи")
            return False
        
        # проверка что менеджер не меняет исполнителя
        if isinstance(user, Manager) and task.get_assigned():
            pass

        if task.set_status(new_status, user):
            print(f'Статус задачи "{task.get_name()}" изменен на "{new_status}" пользователем{user.get_name()}')
            return True
        else:
            print(f'Ошибка: неверный статус "{new_status}" для задачи "{task.get_name()}"')
            return False

    def print_all_tasks(self):
        print("All Tasks:")
        for task in self.tasks:
            print(task)

def main():
    task_manager = TaskManager()

    admin = Admin("Админ Андрей")
    manager = Manager("Менеджер Матвей")
    employee1 = Employee("Сотрудник Степан")
    employee2 = Employee("Сотрудник Стас")
    task_manager.add_user(admin)
    task_manager.add_user(manager)
    task_manager.add_user(employee1)
    task_manager.add_user(employee2)

    task1 = task_manager.create_task("Сделать картину")
    task2 = task_manager.create_task("Купить доски")
    task3 = task_manager.create_task("Заказать пилы")

    task_manager.print_all_tasks()


    # Админ может назначать задачи
    task_manager.assign_task(task1, employee1, admin)
    task_manager.assign_task(task2, employee2, admin)
    task_manager.assign_task(task3, employee1, admin)

    # Менеджер может назначать задачи
    task_manager.assign_task(task1, employee2, manager)

    # Сотрудник не может назначать задачи
    task_manager.assign_task(task2, employee1, employee1)

    # Сотрудник может менять статус своей задачи
    task_manager.change_status(task1, "in_progress", employee1)
    
    # Сотрудник не может менять статус чужой задачи
    task_manager.change_status(task2, "in_progress", employee1)
    
    # Менеджер может менять статус любой задачи
    task_manager.change_status(task2, "in_progress", manager)
    task_manager.change_status(task3, "done", manager)
    
    # Админ может менять статус любой задачи
    task_manager.change_status(task1, "done", admin)
    
    # Попытка установить неверный статус
    task_manager.change_status(task2, "7557893957776568", admin)

    task_manager.print_all_tasks()

    tasks = [task1, task2, task3]
    users = [admin, manager, employee1, employee2]
    
#    for user in users:
 #       print(f"\n{user.get_name()} ({user.get_role()}) permissions:")
  #     for task in tasks:
   #         can_edit = user.can_edit_task(task)
    #        assignee_name = task.get_assignee().get_name() if task.get_assignee() else "None"
     #       print(f"  - Task '{task.get_name()}'(assignee: {assignee_name}): can_edit = {can_edit}")
main()