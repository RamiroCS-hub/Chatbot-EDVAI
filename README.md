# Chatbot for Technical Test at EDVAI

## Steps to Follow Before Running the Code:

1. Open an integrated terminal from Visual Studio Code.
2. Run the commands:
    ```sh
    pip install requests
    pip install gradio
    ```
3. Use the `cd` command to navigate to the same folder where the `main.py` file is located and run the `main.py` file with the command:
    ```sh
    python main.py
    ```
4. When executed, a tab will open in your default browser, that is the chatbot.
5. Enjoy the chatbot, try the command: "what's the weather?"

## Core Explanation of the Code:

**Chatbot Class:** For all the functionalities of the chatbot, I decided to create a class and instantiate an object of this class. This is because having all functionalities within a class allows you to avoid some scope issues with variables thanks to `self`.

I used a lambda function because it takes up less space than a normal function, and the `submit` method must receive a function that returns something.

There are 2 `submit` methods: one processes the inputs and returns the corresponding output, and the other, which runs after processing the inputs, checks if the user entered "goodbye" to close the Gradio interface.

When calling the API to get the temperature, I do it within a `try-except` statement because if for some reason the API doesn't work, an error will occur when converting the data to JSON, which will stop the code execution.

When the user says goodbye with the command "goodbye," the port on which the Gradio interface is running is closed. To restart it, you need to open another PowerShell located where the `main.py` file is and run the command:
```sh
python main.py
