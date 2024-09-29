# Updated Web Pages

## Config page

- Email (TextBox)
- Password (TextBox)
- Confirm Password (TextBox)
- Submit (Button)

## Login Page

    - UserName (TextBox)
        - Forgot Username (Button)
    - Password (TextBox)
        - Forgot Password (Button)
    - Login (Button)

### Forgot Username/Password

    - Enter Email (TextBox)
    - Submit (Button)

## Admin Dashboard

    - Add Educator (View card)
    - Add Secretery (View card)
    - Manage Profile (View card)

### Add Educator

    - First Name (Textbox)
    - Last Name (Textbox)
    - ID Number (Textbox)
    - Email (Textbox)
    - Mobile Number (Textbox)
    - Add Educator (Button)

### Add Secretery

    - First Name (Textbox)
    - Last Name (Textbox)
    - ID Number (Textbox)
    - Email (Textbox)
    - Mobile Number (Textbox)
    - Add Secretery (Button)

### Manage Profile

    - Username (InActive Textbox)
    - Email (InActive Textbox)
    - Change Password (Button)

#### Change Password

    - New password (TextBox)
    - Confirm Password (Textbox)
    - Update Password (Button)

## Secretery Dashboard

    - Add Parent/Guadian (View card)
    - Add Student (View card)
    - Update Attendance (View card)
    - Add Attendance exemption (View card)
    - Manage Profile (View card)

### Add Parent/Guadian

    - First Name (Textbox)
    - Last Name (Textbox)
    - ID Number (Textbox)
    - Email (Textbox)
    - Mobile Number (Textbox)
    - Address (Display Name)
    - Street address (Textbox)
    - Suburb (Textbox)
    - City (Textbox)
    - Province (DropDown)
    - Add Parent/Guadian (Button)

### Add Student

    - First Name (Textbox)
    - Last Name (Textbox)
    - ID Number (Textbox)
    - Guardian (SearchBox) - dropdown with textbox
    - Grade (SearchBox) - dropdown with textbox
    - Division (SearchBox) - dropdown with textbox
    - Add Student (Button)

### Update Attendance

    - Date
    - Grade (SearchBox) - dropdown with textbox
    - Division (SearchBox) - dropdown with textbox
    - StudentID (SearchBox) - dropdown with textbox
    - Attendance Status (Dropdown List)
    - Update Attendance (Button)

### Add Attendance exemption

    - Start Date
    - End Date
    - Grade (SearchBox) - dropdown with textbox
    - Division (SearchBox) - dropdown with textbox
    - StudentID (SearchBox) - dropdown with textbox
    - Attendance Status (Dropdown List)
    - Update Attendance (Button)

### Manage Profile

    - First Name (Inactive Textbox)
    - Last Name (Inactive Textbox)
    - Username (Inactive Textbox)
    - Email (Inactive Textbox)
    - Mobile Number (Textbox)
    - Update mobile Number (Button)
    - Change Password (Button)

## Educator Dashboard

    - Generate Class List (View card)
    - Manage Profile (View card)

### Generate Class List

    - Date
    - Grade (SearchBox) - dropdown with textbox
    - Division (SearchBox) - dropdown with textbox
    - Generate List (Button)

### Class List Generated

    - Date
    - Grade & Division (Inactive Textbox)
    - Form Educator (Inactive Textbox)
    - StudentID (Disp), First Name (Disp), Last Name (Disp), Leave Status(Disp), Attendance Status (Checkbox)
    - Submit Register (Button)

## Parent Dashboard

    - Add Attendance exemption (View card)
    - Manage Profile (View card)

#### Return Lists **

- Educator (UserName, First Name, Last Name, Form Class) -> Add Educator Page -> Edit and Delete Buttons
- Secretery (UserName, First Name, Last Name) -> Add Secretery Page -> Edit and Delete Buttons
- Guardian (UserName, First Name, Last Name) -> Add Guardian Page -> Edit and Delete Buttons
- Class (Grade & Division, Form Educator) -> Manage Grade & Division -> Edit and Delete Buttons
- Attendance (Date, Class, Form Educator) -> Class List Generated Page -> Edit and Delete Buttons -> Add Student page -> Edit and Delete Buttons

### Manage Grade & Division

    - Grade (SearchBox)
    - Division (SearchBox)
    - Form Educator (SearchBox)
