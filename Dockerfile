#FROM rasa/rasa:latest
FROM python:3.8

ADD app/echobot.py .
COPY ./app ./app
#COPY server.sh /app/server.sh
#
#USER root
#RUN chmod -R 777 /app

#RUN pip install --user virtualenv
#RUN virtualenv myenv
#RUN source myenv/bin/activate
#RUN sudo pip install google-api-python-client
#RUN sudo pip install google-cloud
#RUN sudo pip install google-cloud-vision
#RUN sudo pip install google-cloud-storage
#RUN pip install python_jwt
#COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install python-telegram-bot
RUN pip install schedule

#RUN pip install requests
#RUN pip install python-firebase

#RUN pip install deepspeech
#RUN pip install firebase
#RUN pip install youtube-search
#USER 1001
#ENTRYPOINT ["/app/server.sh"]
CMD ["python3","./app/eechobot.py"]