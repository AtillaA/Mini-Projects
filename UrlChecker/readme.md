# URL Checker
-------------
A basic TypeScript browser application that validates URL formats on the client side and checks their existence asynchronously using a throttled mock server.


## Features:
------------
- Validates URL formats instantly as the user types.
- Throttles requests to avoid server-side request overflow.
- Handles race conditions by tracking request identifiers to ignore stale responses.
- Identifies whether the URL points to a file or a folder.


## Development Environment
--------------------------
- Node.js Version: v24.18.0
- TypeScript Version: 7.0.2


## Getting Started
------------------
1. Install dependencies (npm install)
2. Compile TypeScript (npm run build)
3. Open index.html in a web browser
