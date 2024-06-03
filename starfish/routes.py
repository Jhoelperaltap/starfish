

from starfish.forms import LoginForm
from starfish.core.router import add_route, render_template

def login(request, *args):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.validate():
            # Manejo de login
            return "Login successful"
        else:
            return render_template('login.html', {'form': form})
    else:
        form = LoginForm()
        return render_template('login.html', {'form': form})

# Agregar la ruta de login al enrutador
add_route("/login", login)
