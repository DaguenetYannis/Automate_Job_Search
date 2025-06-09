import os
from striprtf.striprtf import rtf_to_text

def convert_rtf_folder(input_folder: str, output_folder: str):
    """
    Converts all .rtf files in the input_folder to .txt files in the output_folder.
    """
    converted_files = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".rtf"):
            rtf_path = os.path.join(input_folder, filename)

            try:
                with open(rtf_path, "r", encoding="utf-8", errors="ignore") as f:
                    rtf_content = f.read()

                plain_text = rtf_to_text(rtf_content)

                new_filename = filename.replace(".rtf", ".txt")
                output_path = os.path.join(output_folder, new_filename)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(plain_text)

                print(f"✅ Converted: {filename} → {new_filename}")
                converted_files += 1

            except Exception as e:
                print(f"❌ Failed to convert {filename}: {e}")

    print(f"\n🔁 Total converted files: {converted_files}")

# Example usage
if __name__ == "__main__":
    convert_rtf_folder("Jobs_database/rtf", "Jobs_database/txt")
