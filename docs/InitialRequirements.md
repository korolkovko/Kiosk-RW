# Functional Requirements

## Menu Management

- Load information for menu formation: via CSV/tables, with timestamp and comment (what and why was updated)
- Form "menu" object per shift
- Track quantity of available items per shift
- Hold items during order processing (when customer in cart proceeds to payment)
- Deduct inventory after successful order payment
- Menu updates: price changes, availability, stop-list
- Form "order cart" object

## Client (Frontend on iPad)

- Touch interface support (up to 3 fingers, 1 for selection and up to 3 for navigation)
- Browse menu
- Select item, quantity, options (sauces, flavors, etc.)
- Add to cart
- View and edit cart
- Cancel cart
- Return to menu
- Proceed to payment
- Auto-update menu (if changed on server)
- Auto-update cart (if any dish went to stop-list or ran out while customer hasn't paid yet) = notification about this
- Interface language switching at any step: RU, EN

## Administrator (Admin Panel)

- Upload and edit menu
- Set/remove items from stop-list
- View orders (all statuses)

## Super Administrator

- View logs
- View orders (all statuses)
- View critical errors/notifications
- User management
- System state monitoring (alive/profiling/alerts)
- System restart
- System stop

## Orchestrator (Business Logic and Integrations)

- Check inventory and reserve before payment
- Send payment task (POS)
- Send fiscalization task (KKT)
- Order timeout: return to main menu after 20 sec of inactivity
- Error handling, cancellations and non-standard scenarios (see separate document)
- Print slip receipt
- Print fiscal receipt
- Generate and send order number to customer
- Send order to kitchen (external service or separate module)
- Update inventory - notify Menu Management
- Log and save all order stages in DB

## System (Technical Aspects)

- Role model support
- Use ORM for separation of logic and storage
- JWT or OAuth2 authorization
- Health-check endpoints
- Centralized event logging

## Roles

- **No-name client**: browse and select menu, cart, payment, receive order number
- **Named client**: all the same + personalized offers, visual elements, order customization
- **Super Administrator**: menu management, logs, users, monitoring, restarts
- **Administrator**: menu management
- **POS terminal**: receive payment commands, return ID and status, send slip receipt
- **KKT**: receive fiscalization command, return ID/status, receive slip receipt copy

## Non-Functional Requirements

- Operation mode: 24/7
- UI response: <= 150 ms
- Inactivity time - reset everything and show menu from start: >= 20 sec
- Support up to 15 parallel orders without degradation
- Limit on items per order: 10 (configurable in settings)
- Load monitoring, alerts
- Manual restart of frontend/backend through admin panel
- DB backup: daily
- Log backup: daily, rotation by days
- Launch via Docker, Kubernetes
- Configuration via .env/YAML
- requirements.txt and complete dependency description
- Multithreading support (async or worker-based)
- Error handling

## Integrations

- Dedicated integration layer
- REST API and SDK support
- Synchronous and asynchronous call support
- Future integration capability with enterprise accounting/POS systems

## Privacy and Security

- Personal data storage (for named clients)
- Anonymization or deletion of old orders
- Sensitive information filtering from logs

## Updates and Settings (Deployment & Configuration)

- **Application settings changes** (UI, menu, language, etc.): through admin panel, without restart, hot reload
- **System settings changes** (.env, environment variables): requires backend restart through admin panel or manually
- **Frontend changes**:
  - Frontend builds as SPA, deployed to CDN or local server
  - Update via hot-swap or polling for iPad
  - Preferably implement resource versioning (hash files)
- **New version/bugfix deployment**:
  - Backend — rolling update via docker-compose/k8s
  - Frontend — resource replacement and cache busting (via service worker or cache disabling)
  - Minimize downtime: blue-green or staged deployment
- **Database changes**:
  - Migrations using Alembic or Django ORM
  - DB version should be tracked (semver)
  - Provide backups before migration