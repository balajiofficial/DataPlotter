from tkinter import OptionMenu, StringVar, Tk, Entry, Button, Label, Text, END, Y
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from matplotlib import pyplot as plt
from pandas import read_csv, read_excel
from os.path import basename

plt.style.use('bmh')

# Main Window
root = Tk()
root.configure(background='#070091')
root.title("Data Plotter")
root.iconbitmap("./icon.ico")
root.geometry('1200x650')
root.minsize(900, 600)
root.state('zoomed')

# Files
file = ""
column1 = []
column2 = []
data_file = ""

# Text Fields
column1Text = Entry(root, font=('Arial', '16'))
column1Text.place(x=500, y=230)
column2Text = Entry(root, font=('Arial', '16'))
column2Text.place(x=500, y=275)

# Preview
preview = Text(root, wrap="none", font=('Arial', '14'), height=864, background='#8c03fc', foreground='white')
preview.pack(expand=True, fill=Y)
preview.place(x=900, y=0)

# Labels
text1 = Label(root, text="Column Name for X Axis/Primary Value : ", font=('Arial', '16'), bg='#070091', fg='white')
text1.place(x=60, y=230)
text2 = Label(root, text="Column Name for Y Axis/Secondary Value : ", font=('Arial', '16'), bg='#070091', fg='white')
text2.place(x=30, y=275)
text3 = Label(root, text="File :          Not selected", font=('Arial', '16'), bg='#070091', fg='white')
text3.place(x=390, y=320)
text4 = Label(root, text=" Graph : ", font=('Arial', '16'), bg='#070091', fg='white')
text4.place(x=360, y=190)

# Dropdown Menu
graph_label = StringVar(root, "Select Graph")
graphs = OptionMenu(root, graph_label, *["Line Graph", "Bar Graph", "Horizontal Bar Graph", "Pie Chart", "Scatter Plot", "Area Chart"])
graphs.place(x=500, y=190)

theme_label = StringVar(root, "Graph Theme")
graphs = OptionMenu(root, theme_label, *[style for style in plt.style.available])
graphs.place(x=720, y=10)

def getColumnData() -> bool:
    global column1
    global column2

    try:
        column1 = list(data_file[str(column1Text.get())])
        column2 = list(data_file[str(column2Text.get())])
        return True
    except:
        showinfo("Data Plotter", "One or both columns doesn't exist")
        return False

def graphWindow():
    title = basename(file).replace(".csv", "")
    plt.get_current_fig_manager().window.wm_iconbitmap("./icon.ico")
    plt.get_current_fig_manager().set_window_title(f"Data Plotter {graph_label.get()} - {title}")
    if theme_label.get() == "Graph Theme":
        plt.style.use('bmh')
    else:
        plt.style.use(theme_label.get())

def plotGraph():
    if not getColumnData():
        return

    if graph_label.get() == "Select Graph":
        showinfo("Data Plotter", "Please select type of graph")
        return

    elif graph_label.get() == "Line Graph":
        title = basename(file).replace(".csv", "")

        graphWindow()
        plt.plot(column1, column2)
        plt.xlim([min(column1), max(column1)])
        plt.ylim([min(column2), max(column2)])
        plt.title(f"Line Graph - {title}")
        plt.xlabel(str(column1Text.get()).title())
        plt.ylabel(str(column2Text.get()).title())
        plt.show()

    elif graph_label.get() == "Bar Graph":
        title = basename(file).replace(".csv", "")

        graphWindow()
        plt.bar(column1, column2)
        plt.title(f"Bar Graph - {title}")
        plt.xlabel(str(column1Text.get()).title())
        plt.ylabel(str(column2Text.get()).title())
        plt.show()

    elif graph_label.get() == "Horizontal Bar Graph":
        title = basename(file).replace(".csv", "")

        graphWindow()
        plt.barh(column2, column1)
        plt.title(f"Horizontal Bar Graph - {title}")
        plt.xlabel(str(column1Text.get()).title())
        plt.ylabel(str(column2Text.get()).title())
        plt.show()

    elif graph_label.get() == "Pie Chart":
        title = basename(file).replace(".csv", "")

        graphWindow()
        plt.pie(column1, labels=column2)
        plt.title(f"Pie Chart - {title}")
        plt.show()
    
    elif graph_label.get() == "Scatter Plot":
        title = basename(file).replace(".csv", "")

        graphWindow()
        plt.scatter(column1, column2)
        plt.title(f"Scatter Plot - {title}")
        plt.xlabel(str(column1Text.get()).title())
        plt.ylabel(str(column2Text.get()).title())
        plt.show()

    elif graph_label.get() == "Area Chart":
        title = basename(file).replace(".csv", "")

        graphWindow()
        plt.stackplot(column1, column2)
        plt.title(f"Area Chart - {title}")
        plt.xlabel(str(column1Text.get()).title())
        plt.ylabel(str(column2Text.get()).title())
        plt.show()

    else:
        raise Exception("Graph Value not recognized")


def openFile():
    global file
    global data_file

    file = askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Sheets", "*.xlsx")])
    if file == "":
        return
    else:
        try:
            if file.endswith(".csv"):
                data_file = read_csv(file)
            elif file.endswith(".xlsx"):
                data_file = read_excel(file)
            else:
                showinfo("Data Plotter", "Improper File Extension")

        except:
            showinfo("Data Plotter", "Error Parsing File")
            return

    if len(data_file) > 2500:
        showinfo("Data Plotter", "Number of rows greater than 2500. Please reduce the number of rows to avoid "
                                 "performance issues")
        return

    text3.config(text=f"File :          {basename(file)}")
    preview.delete(1.0, END)
    preview.insert(1.0, data_file)


# Buttons
fileButton = Button(root, text="Open File", relief="groove", activebackground="black", activeforeground="white",
                    font=('Arial', '16'), command=openFile)
fileButton.place(x=500, y=370)
plotButton = Button(root, text="Plot", relief="groove", activebackground="black", activeforeground="white",
                    font=('Arial', '16'), command=plotGraph)
plotButton.place(x=600, y=470)

root.mainloop()
