import os
import shutil
import fnmatch
import streamlit as st

def copy_files(file_list, source_dir, destination_dir):
    log = []
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for pattern in file_list:
        found = False
        for root, dirs, files in os.walk(source_dir):
            for file_name in files:
                if fnmatch.fnmatch(file_name, f"*{pattern}*.pdf") or fnmatch.fnmatch(file_name, f"*{pattern}*.dwg"):
                    found = True
                    relative_path = os.path.relpath(root, source_dir)
                    destination_folder = os.path.join(destination_dir, relative_path)
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)
                    shutil.copy(os.path.join(root, file_name), destination_folder)
                    log.append(f"✅ Copied: {file_name} to {destination_folder}")
        if not found:
            log.append(f"❌ File not found for pattern: {pattern}")
    return log

st.title("📁 PDF/DWG File Sorter & Copier Tool")

file_patterns = st.text_area("Enter file name patterns (one per line):").splitlines()
source_dir = st.text_input("Source Folder Path", value=r"\\192.168.10.2\rbi\...")
destination_dir = st.text_input("Destination Folder Path", value=r"\\192.168.10.2\rbi\...")

if st.button("Run File Copy"):
    if not file_patterns or not source_dir or not destination_dir:
        st.warning("Please fill in all fields before running.")
    else:
        with st.spinner("Copying files..."):
            result_log = copy_files(file_patterns, source_dir, destination_dir)
            st.success("Process completed.")
            st.write("### Results:")
            for log in result_log:
                st.write(log)
