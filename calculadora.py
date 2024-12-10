import tkinter as tk
from tkinter import messagebox, ttk
import sympy as sp
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EcuacionDiferencialSolver:
    def init(self):
        self.ventana = tk.Tk()
        self.ventana.title("CALCULADORA DE ECUACIONES DIFERENCIALES")
        self.ventana.geometry("800x600")
        self.ventana.configure(bg='#f0f0f0')

        self.crear_interfaz()

    def crear_interfaz(self):
        # Marco principal
        marco_principal = tk.Frame(self.ventana, bg='#060505')
        marco_principal.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Título
        titulo = tk.Label(
            marco_principal, 
            text="ECUACIONES DIFERENCIALES", 
            font=("Arial", 18, "bold"),
            bg='#060505',
            fg='#f8f4f5'
        )
        titulo.pack(pady=10)

        # Subtítulo explicativo
        subtitulo = tk.Label(
            marco_principal, 
            text="INGRESA LA ECUACION DIFERENCIAL A RESOLVER",
            font=("Arial", 12),
            bg='#080808',
            fg='#f1eaf3'
        )
        subtitulo.pack(pady=5)

        # Entrada de ecuación
        marco_entrada = tk.Frame(marco_principal, bg='#f0f0f0')
        marco_entrada.pack(pady=10, fill=tk.X)

        tk.Label(
            marco_entrada, 
            text="Ecuación:", 
            font=("Arial", 12),
            bg='#9726c5'
        ).pack(side=tk.LEFT, padx=5)

        self.entrada_ecuacion = tk.Entry(
            marco_entrada, 
            width=50, 
            font=("Courier", 14),
            bd=2,
            relief=tk.GROOVE
        )
        self.entrada_ecuacion.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # Teclado virtual
        self.crear_teclado_virtual(marco_principal)

        # Botón de resolver
        boton_resolver = tk.Button(
            marco_principal, 
            text="Resolver Ecuación", 
            command=self.resolver_ecuacion,
            font=("Arial", 12, "bold"),
            bg='#9726c5',
            fg='white',
            activebackground='#45a049'
        )
        boton_resolver.pack(pady=10)

        # Área de resultados
        tk.Label(
            marco_principal, 
            text="Resultado:", 
            font=("Arial", 12),
            bg='#9726c5'
        ).pack()

        self.resultado_texto = tk.Text(
            marco_principal, 
            height=10, 
            width=70, 
            font=("Courier", 12),
            bd=2,
            relief=tk.GROOVE
        )
        self.resultado_texto.pack(pady=10)

        # Marco para el gráfico
        self.frame_grafico = tk.Frame(marco_principal, bg='#f0f0f0')
        self.frame_grafico.pack(pady=20)

    def crear_teclado_virtual(self, marco_padre):
        # Marco para el teclado
        marco_teclado = tk.Frame(marco_padre, bg='#f0f0f0')
        marco_teclado.pack(pady=10)

        # Definición de botones
        botones = [
            ['sin', 'cos','pi','(', ')', 'C'],
            ['log', 'tan','y', "y'", "y''", "y'''"],
            ['exp', 'sqrt', '7', '8','9','/'],
            ['x', '^', '4', '5','6','*'],
            ['', '', '1', '2','3','-'],
            ['', '', '0', '.','=','+'],
        ]

        # Crear botones
        for fila in botones:
            marco_fila = tk.Frame(marco_teclado, bg='#9726c5')
            marco_fila.pack(fill=tk.X)
            
            for boton in fila:
                btn = tk.Button(
                    marco_fila, 
                    text=boton, 
                    width=5,
                    font=("Arial", 10),
                    command=lambda x=boton: self.agregar_caracter(x),
                    bg='white',
                    activebackground='#e0e0e0'
                )
                btn.pack(side=tk.LEFT, padx=2, pady=2)

    def agregar_caracter(self, caracter):
        if caracter == 'C':
            # Limpiar entrada
            self.entrada_ecuacion.delete(0, tk.END)
            self.resultado_texto.delete('1.0', tk.END)
        else:
            # Agregar caracter a la entrada
            posicion_actual = self.entrada_ecuacion.index(tk.INSERT)
            self.entrada_ecuacion.insert(posicion_actual, caracter)

    def resolver_ecuacion(self):
        try:
            # Limpiar resultados previos
            self.resultado_texto.delete('1.0', tk.END)
            
            # Obtener ecuación
            ecuacion_str = self.entrada_ecuacion.get()
            
            # Normalizar la ecuación
            ecuacion_str = self.normalizar_ecuacion(ecuacion_str)
            
            # Definir símbolos
            x = sp.Symbol('x')
            y = sp.Function('y')(x)
            
            # Preparar ecuación para sympy
            ecuacion = self.parsear_ecuacion(ecuacion_str, x, y)
            
            # Resolver ecuación diferencial
            solucion = sp.dsolve(ecuacion, y)
            
            # Mostrar solución
            self.resultado_texto.insert(
                tk.END, 
                f"Solución general:\n{solucion}\n\n"
                "Interpretación:\n"
                "- C1, C2, etc. son constantes arbitrarias\n"
                "- La solución representa todas las funciones\n"
                "  que satisfacen la ecuación diferencial"
            )
        
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"No se pudo resolver la ecuación:\n{str(e)}"
            )

    def normalizar_ecuacion(self, ecuacion_str):
        # Eliminar espacios
        ecuacion_str = ecuacion_str.replace(' ', '')
        
        # Reemplazar símbolos problemáticos
        ecuacion_str = ecuacion_str.replace('−', '-')
        
        # Asegurar multiplicación explícita
        ecuacion_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', ecuacion_str)
        ecuacion_str = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', ecuacion_str)
        
        return ecuacion_str

    def parsear_ecuacion(self, ecuacion_str, x, y):
        # Reemplazar derivadas
        ecuacion_str = self.normalizar_derivadas(ecuacion_str)
        
        # Separar lados de la ecuación
        partes = ecuacion_str.split('=')
        
        # Definir símbolos locales
        simbolos_locales = {
            'x': x, 
            'y': y,
            'Dy': sp.diff(y, x),     # Primera derivada
            'D2y': sp.diff(y, x, 2),  # Segunda derivada
            'D3y': sp.diff(y, x, 3),  # Tercera derivada
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'log': sp.log,
            'exp': sp.exp,
            'sqrt': sp.sqrt,
            'pi': sp.pi
        }
        
        try:
            # Parsear ecuación
            if len(partes) == 2:
                lado_izq = sp.sympify(partes[0], locals=simbolos_locales)
                lado_der = sp.sympify(partes[1], locals=simbolos_locales)
                ecuacion = sp.Eq(lado_izq, lado_der)
            else:
                ecuacion = sp.sympify(partes[0], locals=simbolos_locales)
            
            return ecuacion
        
        except Exception as e:
            raise ValueError(f"Error al parsear ecuación: {e}")

    def normalizar_derivadas(self, ecuacion_str):
        # Reemplazar notaciones de derivadas
        derivadas_map = {
            "y'''": "D3y",
            "y''": "D2y", 
            "y'": "Dy"
        }
        
        for derivada, reemplazo in derivadas_map.items():
            ecuacion_str = ecuacion_str.replace(derivada, reemplazo)
        
        return ecuacion_str

    def iniciar(self):
        self.ventana.mainloop()

# Ejecutar aplicación
if _name_ == "main":
    app = EcuacionDiferencialSolver()
    app.iniciar()