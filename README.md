## Install python requirements
```bash
pip install -r requirements.txt
```

## Create the `.env` file in the root of the project with the following content.
```
ES_PASSWORD=<enter the password after running the docker run.. command>
```

## Upload the data to the elasticsearch container
```bash
python upload.py
```

## Run the flask application
```bash
python app.ppy
```

Now you can visit the site on `http://localhost:5000`.
