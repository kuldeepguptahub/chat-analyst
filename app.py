import streamlit as st

with st.sidebar:
    st.title('Upload a chat')
    st.write('Multi-file upload is not supported at the moment. Upload one file only.')

    input_text = st.text_area(label='paste your chat here...')
    
    st.subheader('Or')

    text_file = st.file_uploader(label='Upload a file here',
                     accept_multiple_files=False,
                     type='txt',
                     )

col1, col2 = st.columns(2, gap = 'small', border=True)

with col1:
    if input_text:
        st.write(input_text)

with col2:
    if text_file:
        st.write(text_file.read())
        