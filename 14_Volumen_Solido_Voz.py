
import matplotlib.pyplot as plt
import numpy as np
import math
import speech_recognition as sr
import pyttsx3
from mpl_toolkits.mplot3d import Axes3D
import re

# ====================== CONFIGURACIÓN DE VOZ ======================
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Ajusta esto si deseas cambiar la voz
engine.setProperty('rate', 150)

def hablar(texto):
    print("Jessica:", texto)
    engine.say(texto)
    engine.runAndWait()

def escuchar_texto(prompt):
    r = sr.Recognizer()
    hablar(prompt)
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            texto = r.recognize_google(audio, language='es-ES')
            #hablar(f"Has dicho: {texto}")
            return texto
        except sr.UnknownValueError:
            hablar("No entendí, por favor escribe tu respuesta")
            return input("Escribe tu respuesta: ")
        except sr.RequestError:
            hablar("Error en el servicio de voz")
            return input("Escribe tu respuesta: ")

def obtener_entrada_numerica(prompt):
    while True:
        entrada = escuchar_texto(prompt)
        entrada = entrada.lower().replace(",", ".")  # Reemplaza coma por punto
        numeros = re.findall(r"[-+]?\d*\.\d+|\d+", entrada)  # Extrae número flotante o entero

        if numeros:
            try:
                return float(numeros[0])  # Toma el primer número reconocido
            except ValueError:
                pass

        hablar("No entendí el número, por favor repítelo o escríbelo")
        try:
            return float(input("Ingresa el número: ").replace(",", "."))
        except ValueError:
            hablar("Eso tampoco fue un número válido.")


# ====================== RECORDAR NOMBRE ======================
def obtener_nombre():
    entrada = escuchar_texto("")
    
    patrones = [
        r"me llamo (\w+)",
        r"soy (\w+)",
        r"mi nombre es (\w+)",
        r"(\w+)$"
    ]

    nombre = None
    for patron in patrones:
        coincidencia = re.search(patron, entrada.lower())
        if coincidencia:
            nombre = coincidencia.group(1).capitalize()
            break

    if not nombre:
        nombre = entrada.strip().split()[-1].capitalize()

    respuesta = escuchar_texto(f"Hola {nombre}, es un gusto conocerte. ¿Cómo puedo ayudarte?")

    if "volumen" in respuesta.lower() and "sólido" in respuesta.lower():
        hablar("Perfecto, ¿Volumen de que solido deseas calcular: cono, cilindro o esfera?")
    else:
        hablar("Perfecto, ¿Volumen de que solido deseas calcular: cono, cilindro o esfera")

    return nombre, respuesta  # ✅ devolvemos ambos


# ====================== CÁLCULOS Y GRÁFICAS ======================
def calcular_cono():
    while True:
        r = obtener_entrada_numerica("Dime el radio de la base del cono en metros")
        h = obtener_entrada_numerica("Dime la altura del cono en metros")
        hablar(f"Entonces, el radio es {r:.2f} metros y la altura es {h:.2f} metros.")
        confirmacion = escuchar_texto("¿Es correcto?")

        if "sí" in confirmacion.lower():
            break
        elif "no" in confirmacion.lower():
            hablar("Vamos a volver a ingresar los datos.")
        else:
            hablar("No entendí la respuesta, por favor responde sí o no.")

    volumen = (1/3) * math.pi * r**2 * h
    hablar(f"El volumen del cono es {volumen:.2f} metros cúbicos")
    
    ver_grafico = escuchar_texto("¿Deseas que te muestre el gráfico del sólido?")
    if "sí" in ver_grafico.lower():

        # Gráfico 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        theta = np.linspace(0, 2 * np.pi, 100)
        R = np.linspace(0, r, 50)
        T, R = np.meshgrid(theta, R)
        X = R * np.cos(T)
        Y = R * np.sin(T)
        Z = (h / r) * (r - R)
        ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.7)
        ax.set_xlabel("EJE X")
        ax.set_ylabel(" EJE Y")
        ax.set_zlabel("EJE Z")
        ax.set_title("Volumen de Cono", bbox=dict(facecolor="green", alpha=0.5, edgecolor="black", boxstyle="round,pad=0.5"),
          color="purple", fontsize=14)
        # Mostrar texto con el volumen en el gráfico
        ax.text(0, 0, h + 0.2*h, f"Volumen: {volumen:.2f} m³", fontsize=12, color='purple')
        plt.show()



def calcular_cilindro():
    while True:
        r = obtener_entrada_numerica("Dime el radio de la base del cilindro en metros")
        h = obtener_entrada_numerica("Dime la altura del cilindro en metros")
        hablar(f"Entonces, el radio es {r:.2f} metros y la altura es {h:.2f} metros.")
        confirmacion = escuchar_texto("¿Es correcto?")

        if "sí" in confirmacion.lower():
            break
        elif "no" in confirmacion.lower():
            hablar("Vamos a volver a ingresar los datos.")
        else:
            hablar("No entendí la respuesta, por favor responde sí o no.")

    volumen = math.pi * r**2 * h
    hablar(f"El volumen del cilindro es {volumen:.2f} metros cúbicos")

    ver_grafico = escuchar_texto("¿Deseas que te muestre el gráfico del sólido?")
    if "sí" in ver_grafico.lower():

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        z = np.linspace(0, h, 50)
        theta = np.linspace(0, 2 * np.pi, 50)
        Z, Theta = np.meshgrid(z, theta)
        X = r * np.cos(Theta)
        Y = r * np.sin(Theta)
        ax.plot_surface(X, Y, Z, color='orange', alpha=0.6)
        ax.set_xlabel("EJE X")
        ax.set_ylabel(" EJE Y")
        ax.set_zlabel("EJE Z")
        ax.set_zlim(0, h+3)
        ax.set_title("Volumen de Cilindro", bbox=dict(facecolor="green", alpha=0.5, edgecolor="black", boxstyle="round,pad=0.5"),
          color="purple", fontsize=14)
         # Mostrar texto con el volumen en el gráfico
        ax.text(0, 0, h + 0.2*h, f"Volumen: {volumen:.2f} m³", fontsize=12, color='purple')
        plt.show()


def calcular_esfera():
    while True:
        r = obtener_entrada_numerica("Dime el radio de la esfera en metros")
        hablar(f"Entonces, el radio es {r:.2f} metros.")
        confirmacion = escuchar_texto("¿Es correcto?")

        if "sí" in confirmacion.lower():
            break
        elif "no" in confirmacion.lower():
            hablar("Vamos a volver a ingresar el dato.")
        else:
            hablar("No entendí la respuesta, por favor responde sí o no.")

    volumen = (4/3) * math.pi * r**3
    hablar(f"El volumen de la esfera es {volumen:.2f} metros cúbicos")

    ver_grafico = escuchar_texto("¿Deseas que te muestre el gráfico del sólido?")
    if "sí" in ver_grafico.lower():

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = r * np.outer(np.cos(u), np.sin(v))
        y = r * np.outer(np.sin(u), np.sin(v))
        z = r * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z, color='green', alpha=0.5)
        ax.set_xlabel("EJE X")
        ax.set_ylabel(" EJE Y")
        ax.set_zlabel("EJE Z")
        ax.set_zlim(0, 2*r+3)
        ax.set_title("Volumen de Esfera", bbox=dict(facecolor="green", alpha=0.5, edgecolor="black", boxstyle="round,pad=0.5"),
          color="purple", fontsize=14)
        # Mostrar texto con el volumen en el gráfico
        ax.text(0, 0, r + 0.5*r, f"Volumen: {volumen:.2f} m³", fontsize=12, color='purple')
        plt.show()


# ====================== FLUJO PRINCIPAL ======================
def asistente_virtual():
    hablar("Hola soy Jessica tu asistente virtual")
    nombre, respuesta = obtener_nombre()

    if any(figura in respuesta.lower() for figura in ["cono", "cilindro", "esfera"]):
        opcion = respuesta
    else:
        # Ya se preguntó dentro de obtener_nombre(), así que aquí solo esperamos respuesta
        opcion = escuchar_texto("")  # ← No repetir el mensaje, solo escuchar

    while True:
        if "cono" in opcion.lower():
            calcular_cono()
        elif "cilindro" in opcion.lower():
            calcular_cilindro()
        elif "esfera" in opcion.lower():
            calcular_esfera()
        else:
            hablar("Lo siento, no entendí la figura. Intenta de nuevo.")
            opcion = escuchar_texto("¿Volumen de que solido desea calcular: cono, cilindro o esfera?")
            continue

        continuar = escuchar_texto("¿Deseas calcular otra figura?")
        if "no" in continuar.lower() or "gracias" in continuar.lower():
            hablar(f"Encantada de ayudarte, {nombre}. Hasta pronto.")
            break
        else:
            opcion = escuchar_texto("¿Volumen de que solido desea calcular: cono, cilindro o esfera?")


# Ejecutar
asistente_virtual()
