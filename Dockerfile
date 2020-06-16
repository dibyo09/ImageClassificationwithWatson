FROM python:3.6.1-alpine
EXPOSE 80
RUN mkdir -p /src
ENV PYTHONPATH /
WORKDIR /src

RUN mkdir -p /src/kaplptreeimages/uploads

RUN mkdir -p /src/templates
ADD src/templates/*.* /src/templates/
COPY ["src/templates/*.*", "templates/"]

ADD src/FileUploadDownload.py /src/FileUploadDownload.py
COPY ["src/FileUploadDownload.py", "FileUploadDownload.py"]

ADD src/imageclassify.py /src/imageclassify.py
COPY ["src/imageclassify.py", "imageclassify.py"]

COPY ["src/requirements.txt", "requirements.txt"]
COPY ["src/api_keys.json", "api_keys.json"]

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
LABEL io.openshift.expose-services 5000:http
USER 1001
CMD ["python","FileUploadDownload.py"]


