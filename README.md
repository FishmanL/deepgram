# deepgram

This code defines a simple backend and API for uploading music files.


To run:  stand up a postgres instance at 127.0.0.1, placing your password in a file called config.yaml at the root level of
the code with the key of "password", then flask run from the root of the db.


The following routes exist:
POST reqs:
/post -- takes no parameters, accepts 1 file.  Nonwav files or improperly formatted wav files will return an error message.


GET reqs:  
/list -- lists all filenames with metadata fitting the below arguments.

/info -- lists metadata about all filenames with metadata fitting below arguments.

/download -- downloads *the first* file that fits the metadata query.  Search by filename recommended.


GET arguments, all integers except filename: 

nframes -- number of frames in the file

samplewidth -- number of bytes per sample in the file

numchannels -- whether the audio is mono (1) or stereo (2), 

filename -- the name of the file, supporting partial names but not regex.

seconds -- length of the file in seconds

framerate -- fps of the audio

minduration -- minimum duration of the file, in seconds

maxduration -- maximum duration of the file, in seconds


to add new query params, see dbhandler (selectsql and preprocessdict)

to add new metadata columns, see wavprocessor, tables.sql, and dbhandler.

