from tkinter import * 
import sqlite3

root = Tk()
root.title("Todo list")
root.geometry("500x500")

conn = sqlite3.connect("todo.db")
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")
conn.commit()

def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE id = ?", (id, ))
        conn.commit()
        renderTodos()
    return _remove

# Currying: retrasar la ejecución de una func
def complete(id):
    def _complete(): # para no usar el lambda y envolver la función en bucles
        todo = c.execute("SELECT * FROM todo WHERE id = ?", (id, )).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id = ?", (not todo[3], id))
        conn.commit()
        renderTodos()
    return _complete

def renderTodos():
    rows = c.execute("SELECT * FROM todo").fetchall()
    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = "red" if completed else "black"
        l = Checkbutton(frame, text=description, fg=color, width=42, anchor="w", command=complete(id))
        l.grid(row=i, column=0, sticky="w")
        btn = Button(frame, text="Eliminar", command=remove(id))
        btn.grid(row=i, column=1)
        l.select() if completed else l.deselect()

def addTodo():
    todo = e.get()
    if todo:
        c.execute("""
            INSERT INTO todo (description, completed) VALUES (?, ?)
        """, (todo, False))
        conn.commit()
        e.delete(0, END)
        renderTodos()
    else: pass

l = Label(root, text="Tarea")
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)

b = Button(root, text="Agregar", command=addTodo)
b.grid(row=0, column=3)

frame = LabelFrame(root, text="Mis tareas", padx=5, pady= 5)
frame.grid(row=1, column=0, columnspan=3, sticky="nswe", padx=5)

e.focus()
root.bind("<Return>", lambda x:addTodo())

renderTodos()

root.mainloop()