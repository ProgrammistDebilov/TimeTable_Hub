import flet as ft
import json 

with open('data.json', 'r') as data_file:
    data = json.load(data_file)

day_number = 1

week_days = {
    "1":"Понедельник",
    "2":"Вторник",
    "3":"Среда",
    "4":"Четверг",
    "5":"Пятница",
    "6":"Суббота"
}

addresses = {
    '0':'/',
    '1':'/teachers',
    '2':'/settings'
}


def main(page):

    page.title = "TimeTable Hub"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horisontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#121212"

    page.fonts = {"Roboto":"Roboto-Regular.ttf"}
    page.theme = ft.Theme(font_family="Roboto")

    def keyboard(e: ft.KeyboardEvent):
        match e.key:
            case "Arrow Left":
                back(e)
            case "Arrow Right":
                forward(e)
                
    page.on_keyboard_event = keyboard

    

    def back(e):
        global day_number
        global week_days

        if day_number == 1:
            day_number = 6
        else:
            day_number-=1

        day.value =  week_days[str(day_number)]

        row.clear()
        for i in data[week_days[str(day_number)]]:
            row.append(ft.DataRow([ft.DataCell(ft.Text(i['Предмет'])), ft.DataCell(ft.Text(i['Преподаватель'])), ft.DataCell(ft.Text(i['Аудитория/Кабинет']))]))


        page.update()

    def forward(e):
        global day_number

        if day_number == 6:
            day_number = 1
        else:
            day_number+=1

        day.value = week_days[str(day_number)]

        row.clear()
        for i in data[week_days[str(day_number)]]:
            row.append(ft.DataRow([ft.DataCell(ft.Text(i['Предмет'])), ft.DataCell(ft.Text(i['Преподаватель'])), ft.DataCell(ft.Text(i['Аудитория/Кабинет']))]))

        page.update()
    
    def route_change(e):
        page.views.pop()
        page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.EDIT, bgcolor="#6200EE")
        page.views.append(
            pages[page.route]
        )

    def close_dlg(e):
        edit_dialog.open = False
        page.update()
    
    
    def open_dlg_modal(e):
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()

    
    day = ft.Text(week_days[str(day_number)], size=25)

    group = ft.Text("Группа №"+ data['Группа'], size = 15)

    column = [ft.DataColumn(ft.Text("Предмет")), ft.DataColumn(ft.Text("Учитель")), ft.DataColumn(ft.Text("№ Каб."),numeric=True)]
    row = []
    teachers = []

    for i in data[week_days[str(day_number)]]:
        row.append(ft.DataRow([ft.DataCell(ft.Text(i['Предмет'])), ft.DataCell(ft.Text(i['Преподаватель'])), ft.DataCell(ft.Text(i['Аудитория/Кабинет']))]))

    for i in data['Учителя']:
        teachers.append(ft.ListTile(leading=ft.Icon(ft.icons.PERSON),title=ft.Text(i['Имя']+' '+ i['Фамилия']+' '+i['Отчество']),subtitle=ft.Text(i['Профессия'])))


    table = ft.DataTable(
        bgcolor = "#424242",
        border=ft.border.all(1, "#6200EE"),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, "424242"),
        horizontal_lines=ft.border.BorderSide(1, "03DAC6"),
        columns=column,
        rows=row
    )

    edit_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Что вы хотите поменять?"),
        content=ft.TextField(label="Standard"),
        actions=[
            ft.TextButton("ОК", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    pages = {
        '/login':ft.View(
        '/login',[]
        ),
        '/':ft.View(
        '/schedule',[
            ft.Row([group], alignment=ft.MainAxisAlignment.START),
            ft.Row([day], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.IconButton(ft.icons.ARROW_BACK_IOS, on_click=back),table,ft.IconButton(ft.icons.ARROW_FORWARD_IOS, on_click=forward)], alignment=ft.MainAxisAlignment.CENTER),
            ft.FloatingActionButton(icon=ft.icons.EDIT, bgcolor="#6200EE", on_click=open_dlg_modal),
            ft.NavigationBar(
                destinations=[
                    ft.NavigationDestination(icon=ft.icons.VIEW_TIMELINE_OUTLINED,selected_icon=ft.icons.VIEW_TIMELINE,label="Расписание"),
                    ft.NavigationDestination(icon=ft.icons.PEOPLE_ALT_OUTLINED,selected_icon=ft.icons.PEOPLE_ALT,label="Учителя"),
                    ft.NavigationDestination(icon=ft.icons.SETTINGS_OUTLINED,selected_icon=ft.icons.SETTINGS,label="Настройки")
        ],on_change=lambda e: page.go(addresses[str(e.control.selected_index)])
    )
            ]
        ),
        '/teachers':ft.View(
        '/teachers',[ft.Row([ft.Card(content=ft.Container(content=ft.Column(teachers),width=400,padding=10))],alignment=ft.MainAxisAlignment.CENTER),
                     ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VIEW_TIMELINE_OUTLINED,selected_icon=ft.icons.VIEW_TIMELINE,label="Расписание"),
            ft.NavigationDestination(icon=ft.icons.PEOPLE_ALT_OUTLINED,selected_icon=ft.icons.PEOPLE_ALT,label="Учителя"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS_OUTLINED,selected_icon=ft.icons.SETTINGS,label="Настройки")
        ],on_change=lambda e: page.go(addresses[str(e.control.selected_index)])
    )]
        ,scroll="adaptive"),
        '/settings':ft.View(
        '/settings',[ft.Row([ft.Text("Тут будут настройки")], alignment=ft.MainAxisAlignment.CENTER),
                     ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VIEW_TIMELINE_OUTLINED,selected_icon=ft.icons.VIEW_TIMELINE,label="Расписание"),
            ft.NavigationDestination(icon=ft.icons.PEOPLE_ALT_OUTLINED,selected_icon=ft.icons.PEOPLE_ALT,label="Учителя"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS_OUTLINED,selected_icon=ft.icons.SETTINGS,label="Настройки")
        ],on_change=lambda e: page.go(addresses[str(e.control.selected_index)])
    )]
        )
    }


    page.on_route_change = route_change
    page.go(page.route)


ft.app(target=main)