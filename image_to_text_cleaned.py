# Open the script and read its contents
with open("c:/Users/paria/OneDrive/Desktop/indiannn/lovely/image to text.py", "r", encoding="utf-8") as file:
    script_content = file.read()

# Remove all non-printable characters
cleaned_content = "".join(char for char in script_content if char.isprintable() or char in "\n\r\t ")

# Save the cleaned script as a new file
new_script_path = "c:/Users/paria/OneDrive/Desktop/indiannn/lovely/image_to_text_cleaned.py"
with open(new_script_path, "w", encoding="utf-8") as file:
    file.write(cleaned_content)

print(f"✅ Cleaned script saved as: {new_script_path}")
