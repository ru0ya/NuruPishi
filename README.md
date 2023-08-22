# NuruPishi

This is a recipe app that fetches recipes according to user needs, 
saves favorites and bookmarks for users ease of access in future.

## Table of Contents

- [Project Description](#project-description)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Description

This recipe app is designed to help users find recipes based on the ingredients they have on hand. It utilizes the EdamamAPI to fetch food recipes and provides users with a platform to create accounts, allowing them to like and bookmark their favorite recipes.

The app uses Flask libraries for authentication and backend functionality, while the database management system employed is PostgreSQL. With this app, users can easily search for recipes, explore various cooking options, and save their preferred recipes for future reference.

## Installation

1. Clone the repository
`git clone git@github.com:ru0ya/NuruPishi.git`

2. Navigate to project directory
`cd NuruPishi`

3. Create a virtual environment
`python -m venv venv`

4. Activate virtual environment
	-On macOS and Linux:
	`source venv/bin/activate`
	- On Windows:
	`.\venv\Scripts\activate`
5. Install required dependencies
`pip install -r requirements.txt`

6. Set up the database:
	-Create a PostgreSQL database for the app.
	-Update the database configuration in the config.py file with your PostgreSQL credentials.
7. Run the database migrations:
	`flask db upgrade`
8. Start the development server:
	`flask run`
9. Access the app in your web browser at http://localhost:5000


## Usage

Once the app is up and running, you can use the following steps to search for and save recipes:

   Create an account or log in if you already have one.

   Enter the ingredients you have in the search bar and click "Search Recipes".

   Browse through the list of recipes that match your ingredients.

   Click on a recipe to view more details, including ingredients, instructions, and nutritional information.

   Like or bookmark recipes that you enjoy to save them for future reference

## Contributing

We welcome contributions to improve and enhance the recipe app. If you would like to contribute, please follow these guidelines:

   Fork the repository and create a new branch for your contribution.

   Make your changes and ensure that the app is functioning correctly.

   Submit a pull request with a clear description of your changes and the problem they solve.

We appreciate your contributions and efforts to make the recipe app better for everyone.

## Article
[Lessons learnt, failures and
wins](https://www.linkedin.com/pulse/road-nurupishi-web-app-challenges-triumps-lessons-learned-mwangi/?trackingId=gwVdpIiYTeGuoSe5ukYfZw%3D%3D)

## License

MIT License
