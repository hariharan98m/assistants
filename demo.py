# import gradio as gr

# def terminal_command(command):
#     """
#     Dummy function to simulate terminal command execution.
#     It returns a default response for any command.
#     """
#     return f"Executed: {command}\nOutput: This is a dummy response."

# def chatbot_response(message):
#     """
#     Dummy function for chatbot response.
#     It returns a default reply for any message.
#     """
#     return f"You said: {message}. Here's a default reply."

# # Create the Gradio blocks interface
# with gr.Blocks() as app:
#     gr.Markdown("# Shadow")
#     with gr.Row():
#         with gr.Column(scale=2):
#             terminal_input = gr.Textbox(lines=2, placeholder="Enter Command", label="Terminal")
#             terminal_output = gr.Textbox(lines=10, interactive=False)
#             terminal_button = gr.Button("Execute")
#         with gr.Column(scale=1):
#             chat_input = gr.Textbox(lines=2, placeholder="Type your message", label="Chatbot")
#             chat_output = gr.Textbox(lines=10, interactive=False)
#             chat_button = gr.Button("Send")

#     terminal_button.click(terminal_command, inputs=terminal_input, outputs=terminal_output)
#     chat_button.click(chatbot_response, inputs=chat_input, outputs=chat_output)

# # Launch the interface
# app.launch()

import gradio as gr

def my_app():
    tabs = gr.Tabs()
    code_tab = tabs.new("Code")
    output_tab = tabs.new("Output")

    code = gr.Textbox(label="Code", visible=True, tab=code_tab)
    output = gr.Execute(code, label="Output", visible=True, tab=output_tab)

    return tabs

if __name__ == "__main__":
    gr.Interface(my_app).launch()