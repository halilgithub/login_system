# login_system
I developed a sample **Login System** with Python and PyQt5 library.

## introduction and status

Everything is kept in txt files, no database is used.
Tested in Ubuntu 20.4 and Windows 10 successfully.
It functions well however I am improving it day by day.
I am adding new features and resolving potential defects continuously.
I am trying to enhance not only implementation but also design at the same time.
Reaching out a more object-oriented and pythonic design.
I am not done yet...

## features

Basically, as admin you can login and do some stuff:
  + see user list with their profil data and last-seen time
  + add user
  + update/delete user

You can also login as normal user and take these actions:
  + see your last-seen date and time
  + change your password

## usage

Execute the program from command line:

```console
foo@bar:~$ python main.py
```

| **Main Login Panel:** |
|:----:|
| ![Login Panel](https://github.com/halilgithub/login_system/blob/master/screen_shots/main_window.png "Main Login Panel") |

<pre>
This is the credentials for admin:
    email:     admin
    password:  admin
</pre>

| **Admin Panel:** |
|:----:|
| ![Admin panel](https://github.com/halilgithub/login_system/blob/master/screen_shots/admin_panel.png "Admin Panel") |

<pre>
These are some credentials for normal users:
    email: Leighann@Spainhour.com    password: 1234
    email: Jonathon@Hatcher.com      password: 1234
    email: Granville@Lehman.com      password: 1234
</pre>

| **User Panel:** |
|:----:|
| ![User panel](https://github.com/halilgithub/login_system/blob/master/screen_shots/user_panel.png "User Panel") |


## copyright and license
This project is under the MIT License.

