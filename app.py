from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'Ana250903.' # Cambia esto por una clave real y segura

# Configuración del correo electrónico
EMAIL_ADDRESS = 'cumpledeana22@gmail.com' # Reemplaza con tu dirección de correo
EMAIL_PASSWORD = 'itzq cgrn lbul uhdx' # Reemplaza con tu contraseña de aplicación

@app.route('/')
def index():
    return render_template('confirmacion.html')

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

@app.route('/asistencia', methods=['POST'])
def asistencia():
    if request.form.get('asistencia') == 'no':
        return redirect(url_for('gracias'))
    else:
        return render_template('nombre.html')

@app.route('/enviar_nombre', methods=['POST'])
def enviar_nombre():
    nombre = request.form.get('nombre')
    if not nombre:
        flash('El nombre no puede estar vacío.')
        return redirect(url_for('asistencia'))
    
    enviar_correo('Confirmación de Asistencia', f'El invitado {nombre} ha confirmado su asistencia.')
    
    return render_template('regalos.html', nombre=nombre)

@app.route('/enviar_regalos', methods=['POST'])
def enviar_regalos():
    regalo_seleccionado = request.form.get('regalo')
    nombre_invitado = request.form.get('nombre_invitado')
    
    mensaje = f'El invitado {nombre_invitado} ha seleccionado el siguiente regalo: {regalo_seleccionado}'
    enviar_correo('Ideas de Regalo Seleccionadas', mensaje)
    
    return render_template('final.html')

def enviar_correo(asunto, cuerpo):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        server.quit()
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

if __name__ == '__main__':
    app.run(debug=True)