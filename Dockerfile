FROM python:3.12

# Create the parent directory first
RUN mkdir -p /rera_app/rera

# copy the .env file 
# ARG ENV_CONTENTS
# WORKDIR /rera_app
# COPY --from=type=local/src=.env /dev/null /dev/null
# RUN echo "$ENV_CONTENTS" > .env

# Create the data directories
RUN mkdir -p /rera_app/datalake/data_sources/annexes /rera_app/datalake/data_sources/recitals

# Set the working directory after creating all directories, set the work directory again 
WORKDIR /rera_app/rera

# Copy files while maintaining the directory structure
COPY ./datalake/data_sources/annexes/a*.txt /rera_app/datalake/data_sources/annexes/
COPY ./datalake/data_sources/recitals/r*.txt /rera_app/datalake/data_sources/recitals/
COPY ./datalake/data_sources/eu-ai-act-full_regulation_text_ENG.pdf /rera_app/datalake/data_sources/


COPY .env /rera_app/.env

EXPOSE 8080

# Copy application files
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["sh", "-c", "python search_api.py & streamlit run Main.py --server.port=8080 --server.address=0.0.0.0"]
