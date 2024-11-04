import random as rd
class Cifrado():
    def __init__(self, secuencia_bases:str,emisor_medicion:str, receptor_medicion:str,intercepcion:bool,intercepcion_medicion:str=""):
        self.secuencia_bases = secuencia_bases
        self.emisor_medicion = emisor_medicion.upper()
        self.receptor_medicion = receptor_medicion.upper()
        self.intercepcion = intercepcion
        self.intercepcion_medicion = intercepcion_medicion.upper()
    def generar_semilla(self):
        semilla = rd.randint(0,1000)
        if semilla <= 500:
            return 0
        else:
            return 1
    def medir_base(self, medicion, base, bitabase):
        resultado = ''
        semilla_random = self.generar_semilla()
        if medicion == 'C':
            if base == '0' or base == '1':
                resultado = base
            else:
                resultado = semilla_random
        else:
            if base == '+' or base == '-':
                resultado = base
            elif bitabase:
                if base == '0':
                    resultado = '+'
                else:
                    resultado = '-'
            else:
                if semilla_random == 0:
                    resultado = '+'
                else:
                    resultado = '-'
        return str(resultado)
    def medir_cadenas(self, bases, mediciones,bitabase=False):
        nueva_base = ''
        if len(bases) == len (mediciones):
            for medicion, base in zip(mediciones, bases):
                nueva_base += self.medir_base(medicion,base,bitabase)
            return nueva_base
        else:
            return None
    def comparar_cadenas(self, cadena1, cadena2):
        indices_coincidencias = []
        indice = 0
        for cad1, cad2 in zip(cadena1, cadena2):
            if (cad1 == cad2):
                indices_coincidencias.append(indice)
            indice += 1
        return indices_coincidencias
    def bases_a_bits(self, bases):
        cadena = ""
        for base in bases:
            if base == '0' or base == '1':
                cadena += base
            elif base == '+':
                cadena += '0'
            else:
                cadena += '1'
        return cadena
    def verificar_datos(self, enviados, recibidos, coincidencias):
        llave_privada = ''
        for coincidencia in coincidencias:
            if not (enviados[coincidencia] == recibidos[coincidencia]):
                return "El mensaje fue interceptado"
            else:
                llave_privada += recibidos[coincidencia]
        print("Mensaje recibido de forma segura")
        return llave_privada

    def iniciar_encriptacion(self):
        print("Base de bits inicial: ",self.secuencia_bases)
        #Paso 1 Indicar el estado de la primera secuencia de bases que manda el emisor
        cadena_enviada = self.medir_cadenas(self.secuencia_bases,self.emisor_medicion,True)
        print("Estados mandados por el emisor: ",cadena_enviada)
        #Paso 2 Verificar si hay interceptor
        if self.intercepcion:
            #Si hay interceptor se lee la cadena de mediciones del interceptor y se mide en la cadena enviada
            cadena_enviada = self.medir_cadenas(cadena_enviada,self.intercepcion_medicion)
            print("Estados alterados por el interceptor:",cadena_enviada)
        #Paso 3 El receptor elige su secuencia de mediciones
        cadena_enviada = self.medir_cadenas(cadena_enviada,self.receptor_medicion)
        print("Estados medidos por el receptor:",cadena_enviada)
        #Paso 4 Verificar cuales son las mediciones que coinciden
        coincidencias_mediciones = self.comparar_cadenas(self.emisor_medicion, self.receptor_medicion)
        print("Coincidencias receptor y emisor:",coincidencias_mediciones)
        #Paso 5 Obtener nuevamente una secuencia de bits
        secuencia_receptor = self.bases_a_bits(cadena_enviada)
        print("Base de bits del receptor:",secuencia_receptor)
        #Paso 6 Comparar los bits resultantes
        verificacion = self.verificar_datos(self.secuencia_bases,secuencia_receptor,coincidencias_mediciones)
        print("Resultado final:",verificacion)
"""
base = input("Escribe la secuencia de bases que deseas: ".strip() or 1001100010)
emisor_medicion = input("Escribe la secuencia de medicion a realizar (H para hadaman y C para computacional): ".strip() or "hchchchchh")
receptor_medicion = input("Escribe la secuencia de medicion a realizar (H para hadaman y C para computacional): ".strip() or "hchhhchhhc")
interceptor_medicion = input("Escribe la secuencia de medicion a realizar (H para hadaman y C para computacional): ".strip() or "hchccchhhc")
"""
base = "1001100010"
emisor_medicion = "hchchchchh"
receptor_medicion = "hchhhchhhc"
interceptor_medicion = "hchccchhhc"
cifrado = Cifrado(base, emisor_medicion, receptor_medicion,True,interceptor_medicion)
cifrado.iniciar_encriptacion()
