""" IMPORTACIONES DE BIBLIOTECAS """
import requests  # Importo la bibilioteca para poder llamar a la API
import gradio as gr  # Biblioteca de interfaz gráfica para chabots

""" DEFINO LA CLASE DEL CHATBOT """


class ChatBot:
    def __init__(self):
        # Defino el link para la API de clima y la ubico en Buenos Aires
        self.url = 'http://api.openweathermap.org/data/2.5/weather?q=Buenos Aires&lang=es&APPID=3186452c83844720bee6854d55abe5a3&units=metric'
        self.uName = ''  # Creo una variable llamada uName para guardar el nombre del usuario
        # Variables que se usan para verificar si se le preguntó y asignó un nombre al usuario
        self.haveName = False

    # Método para responder al input del usuario
    def respondMessage(self, message, chat_history):
        self.inp = message  # Defino una variable que guardará los inputs que reciba
        self.chatHistory = chat_history  # Variable para guardar el historial de chat

        # Cierro el servidor si se ingresa adios
        if (message == 'adios'):
            # Siempre que hago esto lo que estoy haciendo es al historial del chatbot añadirle lo que ingreso el usuario y la respuesta del chatbot
            self.chatHistory.append(
                (self.inp, 'Ya no podrá ingresar mas comandos. Hasta la proxima!'))
            return '', self.chatHistory

        # Verífico si el usuario tiene nombre o hay que asignarle uno
        self.haveName = self.verifyName()

        if (self.haveName == True):
            # Verifico si el para el input ingresado hay una respuesta predefinida
            if (self.pAns.get(self.inp)):
                # Llamo a lo función que se encarga de devolverme el mensaje para el input ingresado
                returnData = self.getOutput()
                return '', returnData

            self.chatHistory.append(
                (self.inp, 'Lo siento, no entiendo ese comando. Por favor, pruebe otra vez.'))
            print(self.inp)
            return '', self.chatHistory

        # Si el usuario no tiene nombre se le asigna uno
        self.uName = self.inp
        self.haveName = True

        # Defino las posibles respuestas una vez que tengo el nombre del usuario
        self.pAns = {'Hola': 'Hola, ' + self.uName + ' ¿Cómo puedo ayudarte hoy?',
                     '¿Cómo estás?': 'Hoy estoy bien, muchas gracias!',
                     'cual es el clima?': self.getTemp()
                     }  # Diccionario de respuestas a posibles preguntas

        # Se saluda y se espera a que el usuario ingrese algún comando
        message = 'Hola ' + self.uName + ', preguntáme lo que quieras'
        self.chatHistory.append((self.inp, message))

        return '', self.chatHistory  # Devuelvo primero el texto del Textbox y luego el nuevo historial, siempre como lo último que voy a devolver para cada input va a ser en este formato

    def getOutput(self):  # Método para devolver la respuesta predefinida si se recibe alguno de los inputs predefinidos
        self.chatHistory.append((self.inp, self.pAns[self.inp]))
        # Printeo en la consola lo que se tendría que ver en la interfaz de gradio
        print('La respuesta a ' + self.inp + ' es: ' + self.pAns[self.inp])
        return self.chatHistory  # Devuelvo el historial con la respuesta nueva

    def getTemp(self):  # Método para devolver la temperatura de Buenos Aires
        # Manejo si hay un error con la llamada a la API
        try:
            response = requests.get(self.url)
            data = response.json()  # Formateo la respuesta de la API para poder leerla
            # Devuelvo la temperatura
            return self.uName + ', la temperatura en Buenos Aires es: ' + str(data['main']['temp']) + '°C'
        except:
            return 'Ocurrió un error buscando la temperatura'

        # Verifico si el usuario tiene nombre o no
    def verifyName(self):
        if (len(self.uName) != 0):
            return True
        return False


""" INTERFAZ DE GRADIO QUE FUNCIONARA HASTA QUE EL USUARIO INGRESE ADIÓS """

with gr.Blocks() as demo:
    # Defino todos los objetos necesarios para la interfaz de mi chat
    chatbot = gr.Chatbot()
    msg = gr.Textbox()

    def exitFunction(msg):
        print(msg)
        if (msg == 'adios'):
            print('Cerrando el servidor que estaba corriendo en el puerto:',
                  demo.server_port)
            demo.close()

    botObj = ChatBot()  # Creo una instacia de la clase, esta va a ser mi chat bot

    # Creo una función que se ejecutará cada vez que el chatbot cargue
    # La clase Textbox recibe de parametro una lista de tuplas o de listas en la cual la pos 0 es mensaje del lado del usuario y la 1 del ladio del bot - si o si la lista tiene que ser de longitud 2
    demo.load(lambda: [['BIENVENIDO A EL CHATBOT ETRR',
              'Cuál es su nombre?']], inputs=None, outputs=chatbot)

    # Cada vez que el usuario mande un mensaje se llamará a la función para que lo maneje, respondMessage siempre va a devolver un string
    # con el texto de Textbox y el nuevo historial de Chatbot
    msg.submit(botObj.respondMessage, [msg, chatbot], [msg, chatbot])

    # Función que se ejecuta cada vez que se manda un mensaje y verifica si hay que detener el código o no
    msg.submit(exitFunction, msg, None)

demo.launch(inbrowser=True)
