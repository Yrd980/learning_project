import gradio as gr
from inference import SentimentAnalyzer
import logging


def create_interface():
    analyzer = SentimentAnalyzer("checkpoint/best_model.pth")

    custom_css = """
    .gradio-container {
        font-family: "Microsoft YaHei", sans-serif !important;
    }
    .markdown-text {
        font-size: 16px !important;
        line-height: 1.5 !important;
    }
    .tab-selected {
        background-color: #2196F3 !important;
        color: white !important;
    }
 
    """
    with gr.Blocks(title="medicine sentiment analyzer ", css=custom_css) as interface:
        gr.Markdown(
            """
        # 🏥 medicine sentiment analyzer system
        """
        )

        with gr.Tabs():
            with gr.TabItem("✍️ sigle comment analyze"):
                with gr.Column():
                    text_input = gr.Textbox(
                        label="please input comment",
                        placeholder="please input comment...",
                        lines=4,
                    )
                    text_button = gr.Button("start analyze", variant="primary")
                    text_output = gr.Textbox(label="analysis result", lines=6)

                gr.Markdown(
                    """
                 ### 💡 Usage Instructions
                1. Enter the drug reviews you want to analyze in the text box
                2. Click the "Start Analysis" button
                3. The system will display the sentiment analysis results and probability distribution
                """
                )

                # File Analysis Tab
            with gr.TabItem("📁 Batch Review Analysis"):
                with gr.Column():
                    file_input = gr.File(label="Upload CSV File", file_types=[".csv"])
                    file_button = gr.Button("Start Analysis", variant="primary")
                    file_output = gr.Textbox(label="Processing Results", lines=6)

                gr.Markdown(
                    """
                ### 💡 Usage Instructions
                1. Prepare a CSV file containing a 'review' column
                2. Upload the file and click "Start Analysis"
                3. The system will generate an analysis report and save the results
                
                ### 📋 File Format Requirements
                - File format: CSV
                - Required column: review (review content)
                - Encoding: UTF-8
                """
                )

            gr.Markdown(
                """
            ### 🔍 About Sentiment Classification
            - 🟢 Positive: Indicates that the user has a positive evaluation of the drug
            - ⚪ Neutral: Indicates that the user's evaluation is relatively neutral
            - 🔴 Negative: Indicates that the user has a negative evaluation of the drug

            ### 👨‍💻 Technical Support
            If you have any issues, please contact the technical support team
            """
            )
            text_button.click(
                fn=analyzer.predict_text, inputs=text_input, outputs=text_output
            )

        file_button.click(
            fn=analyzer.predict_file, inputs=file_input, outputs=file_output
        )

    return interface


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    interface = create_interface()
    interface.launch(
        share=True, server_name="0.0.0.0", server_port=7860, favicon_path="favicon.ico"
    )
