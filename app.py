from flask import Flask, request, render_template, redirect
import boto3
import uuid
import json
import os

app = Flask(__name__)
s3_bucket = 'cloud-computing-final-project21'
pets_file = 'pets.json'
s3 = boto3.client('s3')


# Load existing pets
def load_pets():
    if os.path.exists(pets_file):
        with open(pets_file) as f:
            return json.load(f)
    return []


# Save pet metadata
def save_pets(pets):
    with open(pets_file, 'w') as f:
        json.dump(pets, f)


@app.route('/', methods=['GET', 'POST'])
def index():
    pets = load_pets()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        breed = request.form['breed']
        image = request.files['image']

        # Upload image to S3
        image_filename = f"{uuid.uuid4()}_{image.filename}"
        s3.upload_fileobj(image, s3_bucket, image_filename)
        image_url = f"https://{s3_bucket}.s3.amazonaws.com/{image_filename}"

        # Add pet
        pet = {'name': name, 'age': age, 'breed': breed, 'image': image_url}
        pets.append(pet)
        save_pets(pets)

        return redirect('/')

    return render_template('index.html', pets=pets)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
