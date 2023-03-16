NuruPishi

This is a recipe app that fetches recipes according to user needs, saves favorites and bookmarks for users ease of access in future.
## API Reference

#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.
## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run start
```
## Deployment

To deploy this project run

```bash
  npm run deploy
```
## Features

- Light/dark mode toggle
- Live previews
- Fullscreen mode
- Cross platform
## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)
## Installation 

Install my-project with npm

```bash
npm install my-project
cd my-project
```
## Authors

- [@ru0ya](https://github.com/ru0ya)
## License

[MIT](https://choosealicense.com/licenses/mit/)

