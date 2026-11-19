from datetime import datetime
import json
import os
VALID_STATUSES = ("todo", "in-progress", "done")

class User:
    def __init__(self,id,name):
        self.name=name
        self.id=id
        self.tasks=ListTask()

class Task:
    def __init__(self,id,description):
        self.id=id
        self.description=description
        self.status="todo"
        self.created_at=datetime.now()
        self.updateat=self.created_at
    def set_status(self,status):
        self.status=status
        self.updateat=datetime.now()
    def __str__(self):
        return f"Task:{self.id} Description: {self.description} - status: {self.status}"
    def to_dict(self):
        return{
            "ID":self.id,
            "Description":self.description,
            "Status":self.status,
            "Created At":self.created_at.isoformat(),
            "Updated At":self.updateat.isoformat(),
        }
    @classmethod
    def from_dict (cls,data):
        task=cls(data["ID"], data["Description"])
        task.status=data["Status"]
        task.created_at=datetime.fromisoformat(data["Created At"])
        task.updateat=datetime.fromisoformat(data["Updated At"])
        return task

class ListTask:
    def __init__(self):
        self.tasks={}
        self.next_id=1
    def add (self,description):
        task=Task(self.next_id,description)
        self.tasks[task.id]=task
        self.next_id+=1
        return task
    def update(self,task_id,status):
        task=self.tasks.get(task_id)
        if task is None:
            return False
        task.set_status(status)
        return True
    def Delete (self,task_id):
        return self.tasks.pop(task_id,None) is not None
    def show (self):
        if not self.tasks:
            return("no tasks yet")
        if self.tasks:
            for task in self.tasks.values():
                print(task)
    def save(self,filename="test.json"):
        data={
            "next_id":self.next_id,
            "tasks":[t.to_dict() for t in self.tasks.values() ],
        }
        with open("test.json","w+") as f:
            json.dump(data,f,indent=2)
    def load(self,filename="test.json"):
        if not os.path.exists(filename):
            return
        with open(filename)as f:
            data=json.load(f)
        self.next_id=data["next_id"]
        self.task={}
        for item in data["tasks"]:
            task=Task.from_dict(item)
            self.tasks[task.id]=task

def main():
    name=input("what is your name:")
    user=User(1,name)
    user.tasks.load()

    while True:
        print("\n1) Add  2) Update  3) Delete  4) Show  5) Quit")
        choice=input("choose number")
        if choice=="1":
            desc=input("Description:")
            task=user.tasks.add(desc)
            user.tasks.save()
            print("Added:",task)
        elif choice=="2":
            try:
                task_id=int(input("Enter id number"))
            except ValueError:
                print("Enter a Number")
                continue
            status=input("New status (todo/in-progress/done): ").strip().lower()
            if status not in VALID_STATUSES:
                print("Invalid status. Use: todo, in-progress, or done.")
                continue



            if user.tasks.update(task_id,status):
                user.tasks.save()
                task = user.tasks.show()
                print("New Update", task)
            else:
                print("task is not found")
        elif choice=="3":
            try:
                task_id=int(input("Enter id number:"))
            except ValueError:
                print("Enter a number")
                continue
            if user.tasks.Delete(task_id):
                user.tasks.save()
            else:
                print("task not found")
        elif choice=="4":
            user.tasks.show()
        elif choice=="5":
            print("bye bye")

            break
        else:
            print("invalid choices")
if __name__=="__main__":
    main()
