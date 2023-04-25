import os
import random
import gradio as gr
from PIL import Image

# Function to get metadata of all images in the specified folder
def get_metadata(folder):
    metadata = {}
    for filename in os.listdir(folder):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            try:
                with Image.open(os.path.join(folder, filename)) as img:
                    exif_data = img._getexif()
                    if exif_data is not None:
                        metadata[filename] = exif_data
            except Exception as e:
                print(f'Error reading metadata from file {filename}: {str(e)}')
    return metadata

# Function to find lonely files in LoRA folder
def find_lonely_files(lora_folder):
    lonely_files = []
    for filename in os.listdir(lora_folder):
        if not filename.endswith('.jpg') and not filename.endswith('.jpeg') and not filename.endswith('.png'):
            continue
        file_name, file_extension = os.path.splitext(filename)
        lonely_file_path = os.path.join(lora_folder, file_name)
        if not os.path.exists(lonely_file_path):
            lonely_files.append(file_name)
    return lonely_files

# Function to pair lonely files with images in img_output folder
def pair_lonely_files_with_images(lonely_files, metadata, img_folder, lora_folder):
    for lonely_file in lonely_files:
        for image_file, image_metadata in metadata.items():
            if lonely_file in image_metadata:
                image_file_path = os.path.join(img_folder, image_file)
                new_file_name = os.path.join(lora_folder, lonely_file + '.jpg')
                os.rename(image_file_path, new_file_name)
                break

# Gradio interface
def check_lonely_lora(lora_folder_path, img_folder_path):
    metadata = get_metadata(img_folder_path)
    lonely_files = find_lonely_files(lora_folder_path)
    pair_lonely_files_with_images(lonely_files, metadata, img_folder_path, lora_folder_path)
    return f"Lonely files in {lora_folder_path}: {', '.join(lonely_files)}"

# Gradio user interface
inputs = [
    gr.inputs.Textbox(label="Path to LoRA folder"),
    gr.inputs.Textbox(label="Path to img_output folder")
]

outputs = gr.outputs.Textbox()

title = "Check Lonely LoRA"

description = "This tool finds lonely files in the specified LoRA folder and pairs them with corresponding images in the specified img_output folder."

examples = [
    ["./LoRA", "./img_output"]
]

gr.Interface(fn=check_lonely_lora, inputs=inputs, outputs=outputs, title=title, description=description, examples=examples).launch()
