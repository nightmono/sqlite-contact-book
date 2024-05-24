import guizero
import sql

def create_padding(master: guizero.App, width="fill", height="fill", align=None):
    guizero.Box(master, width=width, height=height, align=align)

def create_options_box() -> guizero.Box:
    options_box = guizero.Box(app, height="fill", align="right", border=True)

    create_padding(options_box, height=20)
    create_padding(options_box, width=20, align="left")
    create_padding(options_box, width=20, align="right")

    guizero.PushButton(options_box, text="New", width="fill", command=new_contact)
    create_padding(options_box, height=10)

    guizero.PushButton(options_box, text="View", width="fill")
    create_padding(options_box, height=10)

    guizero.PushButton(options_box, text="Edit", width="fill")
    create_padding(options_box, height=10)

    guizero.PushButton(options_box, text="Delete", width="fill")
    create_padding(options_box, height=10)

    guizero.PushButton(options_box, text="Refresh", width="fill", command=update_content_box)

    return options_box

def create_content_box() -> guizero.App:
    content_box = guizero.Box(app, align="top", height="fill", width="fill", border=True)
    guizero.Box(content_box, width="fill")
    return content_box

def display_contact(contact_id):
    contact_id, first_name, last_name, phone_number, notes = sql.get_contact(contact_id)
    full_name = f"{first_name} {last_name}".strip()

    window = guizero.Window(app, title=full_name, layout="grid", width=280, height=200)

    guizero.Box(window, height=20, width="fill", grid=[0, 0])
    guizero.Box(window, height="fill", width=20, grid=[0, 0])
    guizero.Box(window, height="fill", width=20, grid=[3, 0])

    guizero.Text(window, text="First Name ", grid=[1, 1], align="right")
    first_name = guizero.TextBox(window, text=first_name, grid=[2, 1], width=20, enabled=False)
    guizero.Text(window, text="Last Name ", grid=[1, 2], align="right")
    last_name = guizero.TextBox(window, text=last_name, grid=[2, 2], width=20, enabled=False)
    guizero.Text(window, text="Phone Number ", grid=[1, 3], align="right")
    phone_number = guizero.TextBox(window, text=phone_number, grid=[2, 3], width=20, enabled=False)
    guizero.Text(window, text="Notes ", grid=[1, 4], align="right")
    notes = guizero.TextBox(window, text=notes, grid=[2, 4], width=20, enabled=False)

    def action():
        action_status = action_button.text
        if action_status == "Edit":
            action_button.text = "Save"

            first_name.enable()
            last_name.enable()
            phone_number.enable()
            notes.enable()

        else:
            action_button.text = "Edit"

            first_name.disable()
            last_name.disable()
            phone_number.disable()
            notes.disable()

    options_box = guizero.Box(window, grid=[0, 5, 4, 1], layout="grid")
    guizero.Box(options_box, height=20, width="fill", grid=[1, 0])
    guizero.PushButton(options_box, width=5, text="Back", grid=[0, 1],
                       command=window.destroy)
    guizero.Box(options_box, height="fill", width=30, grid=[1, 1])
    action_button = guizero.PushButton(options_box, width=5, text="Edit", grid=[2, 1], command=action)

def create_contact_button(master, contact) -> guizero.PushButton:
    contact_id, first_name, last_name, *_ = contact
    full_name = f"{first_name} {last_name}".strip()
    contact_button = guizero.PushButton(master, text=full_name, width="fill",
                                        command=display_contact, args=(contact_id,))
    return contact_button

def update_content_box():
    contacts = sql.get_contacts()

    content_box.children[0].destroy()

    if not contacts:
        guizero.Text(content_box, "No contacts to show.", height="fill")
        return

    contact_button_box = guizero.Box(content_box, width="fill")

    for i in range(len(contacts)):
        create_contact_button(contact_button_box, contacts[i])

def new_contact():
    window = guizero.Window(app, title="New Contact", layout="grid", width=280, height=200)

    guizero.Box(window, height=20, width="fill", grid=[0, 0])
    guizero.Box(window, height="fill", width=20, grid=[0, 0])
    guizero.Box(window, height="fill", width=20, grid=[3, 0])

    guizero.Text(window, text="First Name ", grid=[1, 1], align="right")
    first_name = guizero.TextBox(window, grid=[2, 1], width=20)
    guizero.Text(window, text="Last Name ", grid=[1, 2], align="right")
    last_name = guizero.TextBox(window, grid=[2, 2], width=20)
    guizero.Text(window, text="Phone Number ", grid=[1, 3], align="right")
    phone_number = guizero.TextBox(window, grid=[2, 3], width=20)
    guizero.Text(window, text="Notes ", grid=[1, 4], align="right")
    notes = guizero.TextBox(window, grid=[2, 4], width=20)

    def confirm():
        if not first_name.value:
            window.error("Missing First Name", "First name is missing")
            return

        sql.add_contact(first_name.value, last_name.value, phone_number.value,
                        notes.value)

        first_name.value = ""
        last_name.value = ""
        phone_number.value = ""
        notes.value = ""
        update_content_box()

        window.info("Contact Added", "Contact successfully added")

    options_box = guizero.Box(window, grid=[0, 5, 4, 1], layout="grid")
    guizero.Box(options_box, height=20, width="fill", grid=[1, 0])
    guizero.PushButton(options_box, width=5, text="Back", grid=[0, 1],
                       command=window.destroy)
    guizero.Box(options_box, height="fill", width=30, grid=[1, 1])
    guizero.PushButton(options_box, width=5, text="Add", grid=[2, 1],
                       command=confirm)

app = guizero.App(title="SQLite Contact Book")

options_box = create_options_box()
content_box = create_content_box()

update_content_box()

app.display()
