# Ramyeon Site

A Vue.js web application for a ramyeon (Korean instant noodle) restaurant website.

## Project Description

This is a modern web application built with Vue.js 3 that provides an online platform for a ramyeon restaurant. Features include menu browsing, user authentication, cart functionality, promotions, and more.

## Tech Stack

- **Frontend Framework:** Vue.js 3
- **Styling:** Tailwind CSS
- **Build Tool:** Vue CLI
- **QR Code Generation:** qrcode library
- **AI Integration:** Anthropic AI SDK

## Prerequisites

Before running this project, make sure you have the following installed:

- **Node.js** (version 14 or higher) - [Download here](https://nodejs.org/)
- **npm** (comes with Node.js) or **yarn**

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ramyeonsite
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Environment Setup (if needed):**
   - Copy `.env.example` to `.env` if it exists
   - Configure any required environment variables (API keys, etc.)

## Development

### Start Development Server
```bash
npm run serve
```
This will start the development server at `http://localhost:8080` with hot-reload enabled.

### Build for Production
```bash
npm run build
```
This creates a `dist` folder with optimized production files.

### Lint and Fix Files
```bash
npm run lint
```
This will lint your code and automatically fix any fixable issues.

## Project Structure

```
ramyeonsite/
├── public/                 # Static assets
├── src/
│   ├── assets/            # Images, styles, etc.
│   ├── components/        # Vue components
│   ├── App.vue           # Root component
│   └── main.js           # Application entry point
├── scripts/               # Utility scripts
├── package.json          # Dependencies and scripts
├── vue.config.js         # Vue CLI configuration
├── tailwind.config.js    # Tailwind CSS configuration
└── README.md             # This file
```

## Key Features

- User authentication (Login/Signup)
- Menu browsing with food items
- Shopping cart functionality
- Promotions and vouchers
- QR code generation
- Responsive design with Tailwind CSS
- Contact and about pages

## Scripts

- `npm run serve` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Lint and fix code
- `npm run claude` - Run Claude AI script

## Configuration

For detailed Vue CLI configuration options, see the [Configuration Reference](https://cli.vuejs.org/config/).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is private and proprietary.
