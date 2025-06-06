import os
import shutil
import fnmatch
import streamlit as st

def copy_files(file_list, source_dir, destination_dir):
    log = []

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for pattern in file_list:
        pattern = pattern.strip()
        if not pattern:
            continue

        pattern_lower = pattern.lower()
        found = False

        for root, dirs, files in os.walk(source_dir):
            for file_name in files:
                file_name_lower = file_name.lower()

                if fnmatch.fnmatch(file_name_lower, f"*{pattern_lower}*.pdf") or fnmatch.fnmatch(file_name_lower, f"*{pattern_lower}*.dwg"):
                    found = True
                    relative_path = os.path.relpath(root, source_dir)
                    destination_folder = os.path.join(destination_dir, relative_path)
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)

                    source_file_path = os.path.join(root, file_name)
                    destination_file_path = os.path.join(destination_folder, file_name)

                    shutil.copy(source_file_path, destination_folder)
                    log.append(f"✅ Copied: `{file_name}` to `{destination_folder}`")

        if not found:
            log.append(f"❌ File not found for pattern: `{pattern}`")

    return log


# --- Streamlit UI ---

st.set_page_config(page_title="File Copier App", layout="centered")
st.title("📁 PDF/DWG File Sorter & Copier Tool")
st.markdown("Enter file name patterns to search and copy matching files (.pdf / .dwg) from a source to a destination folder.")

file_input = st.text_area("🔍 File name patterns (one per line):", height=150)
file_patterns = [p.strip() for p in file_input.splitlines() if p.strip()]

source_dir = st.text_input("📂 Source Folder Path", value=r"\\192.168.10.2\rbi\...")
destination_dir = st.text_input("📥 Destination Folder Path", value=r"\\192.168.10.2\rbi\...")

if st.button("🚀 Run File Copy"):
    if not file_patterns or not source_dir or not destination_dir:
        st.warning("⚠️ Please fill in all fields before running.")
    else:
        with st.spinner("🔄 Copying files..."):
            result_log = copy_files(file_patterns, source_dir, destination_dir)
            st.success("✅ Copy process completed.")
            st.write("### 🧾 Results Log:")
            for log in result_log:
                st.write(log)
