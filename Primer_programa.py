import json
#Estructuras Dicretas
#2012-1
#Jose Luis Dupinet Diosdado
#Luis Antonio Sanchez Romero
import math
#tokens = '(',')','>','='
cadena = "(S>(P^R'))^((P>(Q|R))^S)"
numVariables  = 0;
resultito = []
#cosa que regresa las listas

def atributos(lista):
	#lista.sort
	
	
	resultados = []
	empiaza = 1
	numero = len(lista)
	print(lista.count("F"))
	print(lista.count("T"))
	longi=(2**(len(lista)))
	nyancat = longi
	while numero > 0:
		nyancat = nyancat /2
		nyan = []
		while len(nyan) < longi:
			aux = 0
			while aux < nyancat:
				nyan.append('1')
				aux+=1
			aux = 0
			while aux < nyancat:
				nyan.append('0')
				aux+=1
	   
		resultados.append(nyan)
		numero-=1	
	return resultados
		


def convertirRPN(cadena):
	#while hay tokens:
	output = []
	stack = []
	for token in cadena:
		actual = ""
		
		#leer una token
		#if estoken letra: -> meter a output
		if(token >= "A" and token <= "Z"):
			output.append(token)
			
		if(token == "("):
			stack.append(token) 
			
		if(token =="'"):
			stack.append("'")
				
		#if es operador ->push a stack
		if(token == "^" or token == "|" or token == ">" or token == "="):
			#si ya hay operadores en la stack:
			 #si token es de menos precedencia -> pop y push token
			if(len(stack)!=0):
				actual = stack[-1]
				while(actual == "^" or actual == "|"):
					output.append(stack.pop())
					if(len(stack)!=0):
						actual = stack[-1]
			stack.append(token) 
	
		#if es parentesis -> popear stack
		if(token == ")"):
			#print("Parentesis")
			while actual != "(":
				
				actual = stack.pop()
				
				output.append(actual)
				
			output.pop()
			
		#print("Output: "+str(output))
		#print("Stack: "+str(stack))
		#print("")
	for token in stack:
		output.append(stack.pop())			
	
	return output	

	
def operarConjuncion(dos, uno, valores):
	
	#1.-recorrer la tabla de valores (dependiendo de uno y dos)
	#2.-operar valor con valor
	#3.-guardar resultado en seccion nueva de la tabla
	res = []
	
	for element in range(len(valores[uno])):
		valor1 = valores[uno][element]
		valor2 = valores[dos][element]
		res.append(str(int(valor1) and int(valor2)))
		
	valores[str(uno)+"^"+str(dos)] = res
	return valores


def operarDisyuncion(dos, uno, valores):
	res = []
	
	for element in range(numVariables):
		valor1 = valores[uno][element]
		valor2 = valores[dos][element]
		res.append(str(int(valor1) or int(valor2)))
		
	valores[str(uno)+"|"+str(dos)] = res	
	return valores


def operarImplicacion(dos, uno, valores):
	res = []
	#print(numVariables)
	for element in range(numVariables):
		valor1 = valores[uno][element]
		valor2 = valores[dos][element]
		#print(type(valor1))
		#print(type(valor2))
		#print(str(int(not int(valor1) or int(valor2))))
		res.append(str(int(not int(valor1) or int(valor2))))
	#print(res) 
	valores[str(uno)+">"+str(dos)] = res
	#print(valores[str(uno)+">"+str(dos)])	
	return valores


def operarIgualdad(dos, uno, valores):
	res = []
	
	for element in range(numVariables):
		valor1 = valores[uno][element]
		valor2 = valores[dos][element]
		res.append(str(int(int(valor1) == int(valor2))))
		
	valores[str(uno)+"="+str(dos)] = res	
	return valores


def operarNeg(uno, valores):
	
	res = []
	
	for element in range(numVariables):
		valor1 = valores[uno][element]
		#print(not int(valor1))
		#print(type(valor1))
		if(int(valor1) == 0):
			valor1 = str(1)
		else:
			valor1 = str(0) 
		#res.append(str(int(valor1)))
		res.append(valor1)
		
	valores["'"+str(uno)] = res 
	return valores

	
def operarRPN(stack, valores):
	resultado = []
	
	for token in stack:
		#vamos a checar que diablos es token, buscar su valor en el dicc
		#y llamar a la operacion correcta
		#print(valores)
		#casos:
		#print(i)
		#print(token)
		tablaDeResultados = []
		if(token >="A" and token <= "Z"):
			resultado.append(token)
		
		elif(token == "^"):
			#operando 2
			op2 = resultado.pop()
			#operando 1
			op1 = resultado.pop()
			tablaDeResultados.append(operarConjuncion(op2, op1, valores))
			resultado.append(str(op1+token+op2))
			resultito.append(str(op1+token+op2))
		
		elif(token == "'"):
			op1 = resultado.pop()
			tablaDeResultados.append(operarNeg(op1,valores))
			resultado.append(str("'"+op1))
			resultito.append(str("'"+op1))
			
		elif(token == "|"):
			#operando 2
			op2 = resultado.pop()
			#operando 1
			op1 = resultado.pop()
			tablaDeResultados.append(operarDisyuncion(op2, op1, valores))
			resultado.append(str(op1+token+op2))
			resultito.append(str(op1+token+op2))
		
		elif(token == "="):
			#print("igual!")
			op2 = resultado.pop()
			op1 = resultado.pop()
			tablaDeResultados.append(operarIgualdad(op2, op1, valores))
			resultado.append(str(op1+"="+op2))
			resultito.append(str(op1+"="+op2))
			
		elif(token == ">"):
			#print(">")
			op2 = resultado.pop()
			op1 = resultado.pop()
			tablaDeResultados.append(operarImplicacion(op2, op1, valores))
			resultado.append(str(op1+">"+op2))
			resultito.append(str(op1+">"+op2))
		
		
	return tablaDeResultados		
			

	
def generarDiccionario(variables, valores):
	#genera un diccionario con el nombre de las variables
	#como keys y sus listas como values
	numVariables = len(variables)
	diccionario = []
	#print(variables)
	#print(valores)
	#diccionario =dict([(variables[0],valores[0]),(variables[1],valores[1]),(variables[2],valores[2])])
	for i in range(numVariables):
		#diccionario[key] = valores[i] 
		diccionario.append(((variables[i],valores[i])))
	#print(diccionario)
	return dict(diccionario)
		
	


def identificarVars(cadena):
	#cuenta el numero de variables y las mete en un stack
	variables = []
	for element in cadena:
		if(element >= "A" and element <= "Z"):
			if(variables.count(element)==0):
				variables.append(element)
				resultito.append(element)
	
	#print(numVariables)	
	return variables	


def imprimirTabla(tabla):
	#imprimir toda la tabla, renglon por renglon
	#print(resultito)
	cadena = ""
	lista = []
	tab = dict(tabla[0])
	grr = 0
	ind = 0
	#print("")
	#print(resultito)
	for i in range(len(resultito)):
		cadena += str(resultito[i]+"	")
	print(cadena)
	cadena = ""
	for la in range(numVariables):
		
		for el in resultito:
			
			lista = tab[resultito[grr]]
			#print(grr )
			#print(resultito[grr])
			cadena+=(str(lista[ind])+"	")
			grr+=1
		grr =0		
		ind+=1
		print(cadena)
		cadena = ""

			
print(cadena)
#variables guarda la lista de variables identificadas (Q,P,R,S,...)
variables = identificarVars(cadena)
numVariables =pow(2,len(variables))
#valores guarda las listas de 1s y 0s
valores = atributos(variables)
#genera el diccionario de operacion que relaciona
#los nombres de las variables y sus valores
tablaDeValores = generarDiccionario(variables,valores)
rpn = convertirRPN(cadena)
#print("rpn "+str(rpn))
tabla = operarRPN(rpn, tablaDeValores)
imprimirTabla(tabla)
