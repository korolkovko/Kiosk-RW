## Entity: ItemLive  
For active items on sale.

### Fields:

- **ItemID**  
    Type: BIGSERIAL  
    Constraints: PRIMARY KEY (ItemID)  
    Cardinality: 1..1  
    Description: Unique identifier for an active menu item available for ordering.

- **NameRu**  
    Type: String   
    Cardinality: 1..1  
    Description: Display name of the item as shown on the kiosk interface.

- **NameEng**  
    Type: String   
    Cardinality: 0..1  
    Description: Display name of the item as shown on the kiosk interface.

- **DescriptionRu**  
    Type: String   
    Cardinality: 1..1  
    Description: Optional extended description of the item.

- **DescriptionEng**  
    Type: String   
    Cardinality: 0..1  
    Description: Optional extended description of the item.

- **IsActive**  
    Type: Boolean   
    Cardinality: 1..1  
    Description: Indicates whether this item is currently available for ordering.

- **UnitOfMeasureRu**  
    Type: ENUM  
    Source: One from UnitOfMeasure(NameOfMeasurementUnitRu)  
    Cardinality: 1..1  
    Description: Unit used to express the quantity of the item, such as pieces, grams, or milliliters.

- **UnitOfMeasureEng**  
    Type: ENUM  
    Source: One from UnitOfMeasure(NameOfMeasurementUnitEng)  
    Cardinality: 0..1  
    Description: Unit used to express the quantity of the item, such as pieces, grams, or milliliters.

- **ItemPriceNet**  
    Type: Decimal   
    Cardinality: 1..1  
    Description: Net price of the item before VAT is applied.

- **ItemVatRate**  
    Type: Decimal   
    Cardinality: 0..1  
    Description: Applicable VAT rate for this item, expressed as a percentage (e.g. 10.0 or 20.0).

- **ItemVatAmount**  
    Type: Decimal   
    Cardinality: 1..1  
    Description: The VAT amount calculated based on net price and tax rate.

- **ItemPriceGross**  
    Type: Decimal   
    Cardinality: 1..1  
    Description: Final item price including VAT.

- **ItemFoodCategory**  
    Type: ENUM  
    Source: One from FoodCategory(Name)  
    Cardinality: 1..1  
    Description: Represents the classification of the item, such as Drinks, Meals, Sauces, etc.

- **ItemDayCategory**  
    Type: ENUM  
    Source: One from DayCategory(Name)  
    Cardinality: 1..1  
    Description: Represents the classification of the item in accordance with time – Breakfast, Lunch, Dinner etc.

- **CreatedAt**  
    Type: DateTime   
    Cardinality: 1..1  
    Description: Timestamp of when the item was created in the system.

- **CreatedBy**  
    Type: Integer  
    Constraints: FOREIGN KEY (ChangeBy) REFERENCES User(UserID)  
    Cardinality: 1..1  
    Description: User ID or name of the person who created the item.

### Relationships:

- remains to be specified


## Entity: ItemArchive  
For archived items – were on sale.

### Fields:

- **ItemArchiveID**  
    Type: BIGSERIAL  
    Constraints: PRIMARY KEY (ItemArchiveID)  
    Cardinality: 1..1  
    Description: Just ID.

- **ItemID**  
    Type: BIGSERIAL  
    Constraints: SNAPSHOT OF ItemLive(ItemID)  
    Cardinality: 1..1  
    Description: Id for traceability – represents active ItemID for the moment when this item was on sale.

- **NameRu**  
    Type: String   
    Constraints: SNAPSHOT OF ItemLive(Name)  
    Cardinality: 1..1  
    Description: Display name of the item as shown on the kiosk interface.

- **NameEng**  
    Type: String   
    Constraints: SNAPSHOT OF ItemLive(Name)  
    Cardinality: 0..1  
    Description: Display name of the item as shown on the kiosk interface.

- **DescriptionRu**  
    Type: String   
    Constraints: SNAPSHOT OF ItemLive(Description)  
    Cardinality: 1..1  
    Description: Optional extended description of the item.

- **DescriptionEng**  
    Type: String   
    Constraints: SNAPSHOT OF ItemLive(Description)  
    Cardinality: 0..1  
    Description: Optional extended description of the item.

- **UnitOfMeasureRu**  
    Type: String   
    Constraints: SNAPSHOT OF ItemLive(UnitOfMeasureRu)  
    Cardinality: 1..1  
    Description: Unit used to express the quantity of the item, such as pieces, grams, or milliliters.

- **UnitOfMeasureEng**  
    Type: String   
    Constraints: SNAPSHOT OF ItemLive(UnitOfMeasureEng)  
    Cardinality: 0..1  
    Description: Unit used to express the quantity of the item, such as pieces, grams, or milliliters.

- **ItemPriceNet**  
    Type: Decimal  
    Constraints: SNAPSHOT OF ItemLive(ItemPriceNet)  
    Cardinality: 1..1  
    Description: Net price of the item before VAT is applied.

- **ItemVatRate**  
    Type: Decimal   
    Constraints: SNAPSHOT OF ItemLive(ItemVatRate)  
    Cardinality: 1..1  
    Description: Applicable VAT rate for this item, expressed as a percentage (e.g. 10.0 or 20.0).

- **ItemVatAmount**  
    Type: Decimal   
    Constraints: SNAPSHOT OF ItemLive(ItemVatAmount)  
    Cardinality: 1..1  
    Description: The VAT amount calculated based on net price and tax rate.

- **ItemPriceGross**  
    Type: Decimal  
    Constraints: SNAPSHOT OF ItemLive(ItemPriceGross)  
    Cardinality: 1..1  
    Description: Final item price including VAT.

- **ItemFoodCategory**  
    Type: String   
    Constraints: SNAPSHOT OF ItemLive(ItemFoodCategory)  
    Cardinality: 0..1  
    Description: Represents the classification of the item, such as Drinks, Meals, Sauces, etc.

- **ItemDayCategory**  
    Type: String   
    Constraints: SNAPSHOT OF ItemLive(ItemDayCategory)  
    Cardinality: 0..1  
    Description: Represents the classification of the item in accordance with time – Breakfast, Lunch, Dinner etc.

- **CreatedAt**  
    Type: DateTime   
    Cardinality: 1..1  
    Description: Timestamp of when the item was put into Archive in the system.

- **CreatedBy**  
    Type: Integer  
    Constraints: FOREIGN KEY (ChangeBy) REFERENCES User(UserID)  
    Cardinality: 0..1  
    Description: User ID or name of the person who archived the item.

### Relationships:

- remains to be specified


## Entity: ItemLiveAvailable  
For each active item on sale – to know available quantity.

### Fields:

- **ItemID**  
    Type: BIGSERIAL  
    Constraints: PRIMARY KEY (ItemID), FOREIGN KEY (ItemID) REFERENCES ItemLive(ItemID) ON DELETE CASCADE  
    Cardinality: 1..1  
    Description: For each active item on sale – to know available quantity.

- **NameOfMeasurementUnitRu**  
    Type: String  
    Constraints: SNAPSHOT OF ItemLive(UnitOfMeasureRu)  
    Cardinality: 1..1  
    Description: Unit of measurement for available stock quantity, such as pieces, grams, or milliliters.

- **NameOfMeasurementUnitEng**  
    Type: String  
    Constraints: SNAPSHOT OF ItemLive(UnitOfMeasureEng)  
    Cardinality: 0..1  
    Description: Unit of measurement for available stock quantity, such as pieces, grams, or milliliters.

- **StockLiveQuantity**  
    Type: Integer  
    Cardinality: 1..1  
    Description: Current available stock of the item that can be sold / available for ordering.

- **ReservedQuantity**  
    Type: Integer  
    Cardinality: 1..1  
    Description: Quantity of the item currently reserved in active sessions or unpaid orders.

### Relationships:

- remains to be specified


## Entity: ItemLiveStockReplenishment  
For each action of replenishment – to know history.

### Fields:

- **OperationID**  
    Type: BIGSERIAL  
    Constraints: PRIMARY KEY (ID)  
    Cardinality: 1..1  
    Description: ID throughout.

- **ItemID**  
    Type: BIGSERIAL  
    Constraints: FOREIGN KEY (ItemID) REFERENCES ItemLive(ItemID) ON DELETE CASCADE  
    Cardinality: 1..1  
    Description: Reference to the item being replenished.

- **NameRu**  
    Type: String  
    Constraints: SNAPSHOT OF ItemLive(NameRU)  
    Cardinality: 1..1  
    Description: Display name of the item as shown on the kiosk interface.

- **DescriptionEng**  
    Type: String  
    Constraints: SNAPSHOT OF ItemLive(DescriptionRU)  
    Cardinality: 1..1  
    Description: Optional extended description of the item.

- **UnitOfMeasureRu**  
    Type: String  
    Constraints: SNAPSHOT OF ItemLive(UnitOfMeasureRu)  
    Cardinality: 1..1  
    Description: Unit of measurement used for this stock adjustment.

- **UnitOfMeasureEng**  
    Type: String  
    Constraints: SNAPSHOT OF ItemLive(UnitOfMeasureEng)  
    Cardinality: 0..1  
    Description: Unit of measurement used for this stock adjustment.

- **ChangeQuantity**  
    Type: Integer  
    Cardinality: 1..1  
    Description: Quantity of items added to or removed from stock.

- **ChangeAt**  
    Type: DateTime `YYYYMMDDHHMMSS`  
    Cardinality: 1..1  
    Description: Timestamp of when this stock adjustment occurred.

- **ChangeBy**  
    Type: Integer  
    Constraints: FOREIGN KEY (ChangeBy) REFERENCES User(UserID)  
    Cardinality: 1..1  
    Description: User who performed the stock adjustment.

### Relationships:

- remains to be specified


## Entity: Order  
Customer's completed or active Order/transaction.

### Fields:

- **OrderID**  
    Type: BIGSERIAL  
    Constraints: PRIMARY KEY (OrderID, OrderDate)  
    Cardinality: 1..1  
    Description: Unique identifier for this order.

- **OrderDate**  
    Type: Date  
    Cardinality: 1..1  
    Description: Unique identifier for this order.  
    Note: Simplify this by using a single primary key for orders (just OrderID as a surrogate PK) and make OrderDate a regular indexed column (for partitioning or querying by date). If daily order-number resets are desired for business reasons (e.g. order #1–100 each day), that can be handled by storing a separate “order number” field or computing it based on date.

- **OrderStatus**  
    Type: ENUM (“PENDING”, “COMPLETED”, “FAILED”, “CANCELLED”)  
    Cardinality: 1..1  
    Description: Order Status.

- **OrderTime**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: Timestamp when the order was placed.

- **OrderCurrency**  
    Type: ENUM (“RUB”, “РУБ”)  
    Cardinality: 1..1  
    Description: Currency in which the order was processed and paid.

- **TotalAmountNett**  
    Type: Decimal  
    Cardinality: 1..1  
    Description: Total cost of the order excluding VAT.

- **TotalAmountVAT**  
    Type: Decimal  
    Cardinality: 1..n  
    Description: Aggregate VAT calculated from all items in the order.

- **TotalAmountGross**  
    Type: Decimal  
    Cardinality: 1..1  
    Description: Total amount the customer pays, including VAT.

- **CustomerID**  
    Type: BIGSERIAL  
    Constraints: FOREIGN KEY (CustomerID) REFERENCES KnownCustomer(CustomerID)  
    Cardinality: 0..1  
    Description: Reference to a known customer, if applicable.

- **OrderPickupNumber**  
    Type: String  
    Cardinality: 1..1  
    Description: Public-facing number assigned to the order for pickup at the counter.

- **OrderPINCode**  
    Type: String  
    Cardinality: 1..1  
    Description: PIN-code to enter and get the order.

- **SessionID**  
    Type: UUID  
    Constraints: → Session(SessionID)  
    Cardinality: 0..1  
    Description: It could be different session if we lost a connection for example.

- **KioskID**  
    Type: Integer (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Actually it is an info of a tablet.

- **KioskIP**  
    Type: String (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Actually it is an info of a tablet.

- **KioskPORT**  
    Type: String (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Actually it is an info of a tablet.

- **PosTerminalID**  
    Type: Integer (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Pick it up as a snapshot from Device table.

- **PosTerminalIP**  
    Type: String (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Pick it up as a snapshot from Device table.

- **PosTerminalPORT**  
    Type: String (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Pick it up as a snapshot from Device table.

- **FiscalMachineID**  
    Type: Integer (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Pick it up as a snapshot from Device table.

- **FiscalMachineIP**  
    Type: String (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Pick it up as a snapshot from Device table.

- **FiscalMachinePORT**  
    Type: String (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Pick it up as a snapshot from Device table.

- **FiscalPrinterID**  
    Type: Integer (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Pick it up as a snapshot from Device table.

- **FiscalPrinterIP**  
    Type: String (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Pick it up as a snapshot from Device table.

- **FiscalPrinterPORT**  
    Type: String (optional, one)  
    Constraints: SNAPSHOT FROM Device table  
    Cardinality: 0..1  
    Description: Pick it up as a snapshot from Device table.

### Relationships:

- remains to be specified


## Entity: Payment  
Details of the payment associated with an order.

### Fields:

- **PaymentID**  
    Type: BIGSERIAL  
    Constraints: PRIMARY KEY (PaymentID)  
    Cardinality: 1..1  
    Description: Unique payment identifier.

- **OrderID**  
    Type: BIGSERIAL  
    Constraints: FOREIGN KEY (OrderID) REFERENCES Order(OrderID)  
    Cardinality: 1..1  
    Description: Reference to associated order.

- **PaymentDate**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: Timestamp of payment attempt — when the payment was initiated or completed.

- **PaymentCurrency**  
    Type: ENUM (“RUB”, “РУБ”)  
    Cardinality: 0..1  
    Description: Three-letter ISO currency code (e.g., RUB, EUR).

- **TotalAmountNet**  
    Type: Decimal  
    Cardinality: 1..1  
    Description: Amount excluding VAT.

- **VatRate**  
    Type: Decimal  
    Cardinality: 1..1  
    Description: Applied VAT rate.

- **TotalAmountVAT**  
    Type: Decimal  
    Cardinality: 1..1  
    Description: Calculated from VAT rate and net amount.

- **TotalAmountGross**  
    Type: Decimal  
    Cardinality: 1..1  
    Description: Final amount charged to customer (Net amount + VAT).

- **Method**  
    Type: Integer  
    Constraints: FOREIGN KEY (Method) REFERENCES PaymentMethod(PaymentMethodID)  
    Cardinality: 0..1  
    Description: Payment method — e.g., cash, card, QR, ApplePay, online.

- **Status**  
    Type: ENUM (“AWAITING”, “DECLINED”, “ERROR”, “PAID”)  
    Cardinality: 0..1  
    Description: Payment processing result — e.g., initiated, success, failed, cancelled.

- **TransactionId**  
    Type: String  
    Cardinality: 0..1  
    Description: External transaction ID from acquirer or payment gateway.

- **PaymentDetails**  
    Type: String  
    Cardinality: 0..1  
    Description: Additional details — may include card mask, bank name, etc.

- **PosTerminalID**  
    Type: Integer  
    Constraints: SNAPSHOT OF PosTerminal(PosTerminalID)  
    Cardinality: 0..1  
    Description: POS terminal that processed the payment.

- **ResponseCode**  
    Type: String  
    Cardinality: 0..1  
    Description: Technical response code from payment system or POS — e.g., “00”, “05”, “91”.

- **ResponseMessage**  
    Type: String  
    Cardinality: 0..1  
    Description: Human-readable result from POS — e.g., “Approved”, “Declined”, “Timeout”, “Invalid card”.

- **CreatedAt**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: When record was created. Usually same as PaymentDate unless delayed.

- **CompletedAt**  
    Type: DateTime  
    Cardinality: 0..1  
    Description: When payment was finalized. Populated only if payment succeeded or definitively failed.

### Relationships:

- remains to be specified


## Entity: User  
A registered user of the system (admin, kiosk, staff, customer).

### Fields:

- **UserID**  
    Type: Integer  
    Constraints: PRIMARY KEY (UserID)  
    Cardinality: 1..1  
    Description: Unique identifier for user account.

- **Username**  
    Type: String  
    Cardinality: 1..1  
    Description: Login identifier (visible or internal).

- **PasswordHash**  
    Type: String  
    Cardinality: 0..1  
    Description: Hashed password using bcrypt or similar.

- **Email**  
    Type: String  
    Cardinality: 0..1  
    Description: Optional email contact.

- **Phone**  
    Type: String  
    Cardinality: 0..1  
    Description: Optional phone number.

- **RoleID**  
    Type: Integer  
    Constraints: FOREIGN KEY (RoleID) REFERENCES Role(RoleID)  
    Cardinality: 1..1  
    Description: Defines the user's permissions and system role.

- **AccessToken**  
    Type: String  
    Cardinality: 0..1  
    Description: JWT or session token for authenticated access.  
    ⚠️ *MAYBE IT SHOULD NOT BE HERE* (to be evaluated).

- **RefreshToken**  
    Type: String  
    Cardinality: 0..1  
    Description: For long-lived sessions, if using OAuth2.  
    ⚠️ *MAYBE IT SHOULD NOT BE HERE* (to be evaluated).

### Relationships:

- remains to be specified


## Entity: KnownCustomer  
Identified customer using the kiosk.

### Fields:

- **CustomerID**  
    Type: BIGSERIAL  
    Constraints: PRIMARY KEY (CustomerID)  
    Cardinality: 1..1  
    Description: Unique ID for the customer.

- **FirstName**  
    Type: String  
    Cardinality: 0..1  
    Description: Optional first name.

- **LastName**  
    Type: String  
    Cardinality: 0..1  
    Description: Optional last name.

- **Email**  
    Type: String  
    Cardinality: 1..1  
    Description: Optional email.

- **Phone**  
    Type: String  
    Cardinality: 0..1  
    Description: Optional phone number (e.g., used for login).

- **LoyaltyCardCode**  
    Type: String  
    Cardinality: 0..1  
    Description: Loyalty program card number.

- **AuthMethod**  
    Type: Enum ("PSW", "SMS", "QR", "NFCDevice", "Oauth2")  
    Cardinality: 0..1  
    Description: phone, qr, card, email, etc.

- **CreatedAt**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: Timestamp when customer was first seen/created.

- **LastSeenAt**  
    Type: DateTime  
    Cardinality: 0..1  
    Description: Last time this customer interacted.

- **IsAnonymousLink**  
    Type: Boolean  
    Cardinality: 0..1  
    Description: If derived from anonymous session with enrichment.

- **AccessToken**  
    Type: String  
    Cardinality: 0..1  
    Description: JWT or session token for authenticated access.  
    ⚠️ *MAYBE IT SHOULD NOT BE HERE* (to be evaluated).

- **RefreshToken**  
    Type: String  
    Cardinality: 0..1  
    Description: For long-lived sessions, if using OAuth2.  
    ⚠️ *MAYBE IT SHOULD NOT BE HERE* (to be evaluated).

### Relationships:

- remains to be specified


## Entity: Role  
User access control role.

### Fields:

- **RoleID**  
    Type: Integer  
    Constraints: PRIMARY KEY (RoleID)  
    Cardinality: 1..1  
    Description: Unique role ID.

- **Name**  
    Type: String  
    Cardinality: 1..1  
    Description: Role name (e.g., admin, superadmin, kiosk, customer).

- **Permission**  
    Type: JSONB or String  
    Cardinality: 0..1  
    Description: Optional list of permissions.

### Relationships:

- remains to be specified


## Entity: Session  
Active user or kiosk session.

### Fields:

- **SessionID**  
    Type: UUID  
    Constraints: PRIMARY KEY (SessionID)  
    Cardinality: 1..1  
    Description: Unique session identifier.

- **UserID**  
    Type: Integer  
    Snapshot of: User(UserID)  
    Cardinality: 0..1  
    Description: Null if anonymous session.

- **DeviceID**  
    Type: Integer  
    Snapshot of: Device(DeviceID)  
    Cardinality: 0..1  
    Description: Null if anonymous session.

- **KnownCustomerID**  
    Type: BIGSERIAL  
    Snapshot of: KnownCustomer(CustomerID)  
    Cardinality: 0..1  
    Description: Null if anonymous session.

- **StartedAt**  
    Type: DateTime  
    Cardinality: 0..1  
    Description: When session was initiated.

- **LastActiveAt**  
    Type: DateTime  
    Cardinality: 0..1  
    Description: Last interaction timestamp.

- **ExpiredAt**  
    Type: DateTime  
    Cardinality: 0..1  
    Description: Session expiration timestamp (if fixed).

- **SessionToken**  
    Type: String  
    Cardinality: 0..1  
    Description: Token used for authentication and validation.

### Relationships:

- remains to be specified


## Entity: Branch  
Settings for the certain Restaurant.

### Fields:

- **BranchID**  
    Type: Integer  
    Constraints: PRIMARY KEY (BranchID)  
    Cardinality: 1..1  
    Description: Represent ID of the record.

- **Name**  
    Type: String  
    Cardinality: 1..1  
    Description: Represent the name of this restaurant.

- **Address**  
    Type: JSONB  
    Cardinality: 1..1  
    Description: Represent the address of this restaurant.

- **WorkHours**  
    Type: JSONB  
    Cardinality: 1..1  
    Description: Represent work hours including pauses during the day.

- **LegalEntity**  
    Type: JSONB  
    Cardinality: 1..1  
    Description: Represent legal and tax information of the restaurant.

- **ChangeAt**  
    Type: DateTime (YYYYMMDDHHMMSS)  
    Cardinality: 1..1  
    Description: Timestamp of when changes occurred.

- **ChangeBy**  
    Type: Integer  
    Foreign Key: REFERENCES User(UserID)  
    Cardinality: 1..1  
    Description: User who changed settings.

### Relationships:

- remains to be specified


## Entity: SessionAndOrderSettings  
Settings for the Order process behavior.

### Fields:

- **ID**  
    Type: Integer  
    Constraints: PRIMARY KEY (ID)  
    Cardinality: 1..1  
    Description: Represent ID of the record.

- **Name**  
    Type: String  
    Cardinality: 1..1  
    Description: Name of parameter.

- **Description**  
    Type: String  
    Cardinality: 1..1  
    Description: Description – what for.

- **Value1**  
    Type: Integer (optional, one)  
    Cardinality: 0..1  
    Description: Could be number – depends on settings.

- **Value2**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: Could be string – depends on settings.

- **Value3**  
    Type: Boolean (optional, one)  
    Cardinality: 0..1  
    Description: Could be boolean – depends on settings.

- **ChangeAt**  
    Type: DateTime (YYYYMMDDHHMMSS)  
    Cardinality: 1..1  
    Description: Timestamp of when changes occurred.

- **ChangeBy**  
    Type: Integer  
    Foreign Key: REFERENCES User(UserID)  
    Cardinality: 1..1  
    Description: User who changed settings.

### Relationships:

- remains to be specified


## Entity: UnitOfMeasure  
Register of measurement units.

### Fields:

- **UnitOfMeasureID**  
    Type: Integer  
    Constraints: PRIMARY KEY (UnitOfMeasureID)  
    Cardinality: 1..1  
    Description: ID.

- **NameOfMeasurementUnitRu**  
    Type: String  
    Cardinality: 1..1  
    Description: Russian name.

- **NameOfMeasurementUnitEng**  
    Type: String  
    Cardinality: 1..1  
    Description: English name.

- **ChangeAt**  
    Type: DateTime (YYYYMMDDHHMMSS)  
    Cardinality: 1..1  
    Description: Timestamp of when changes occurred.

- **ChangeBy**  
    Type: Integer  
    Foreign Key: REFERENCES User(UserID)  
    Cardinality: 0..1  
    Description: User who changed settings.

### Relationships:

- remains to be specified


## Entity: PaymentMethod  
Available payment methods  
*Reserved table – not in active use now*

### Fields:

- **PaymentMethodID**  
    Type: Integer  
    Constraints: PRIMARY KEY (PaymentMethodID)  
    Cardinality: 1..1  
    Description: Unique identifier for payment method.

- **Code**  
    Type: ENUM ("Card", "NFCDevice", "QR")  
    Cardinality: 1..1  
    Description: Code representing type of payment.

- **DescriptionRu**  
    Type: String  
    Cardinality: 1..1  
    Description: Description in Russian.

- **DescriptionEn**  
    Type: String  
    Cardinality: 1..1  
    Description: Description in English.

- **IsActive**  
    Type: Boolean  
    Cardinality: 0..1  
    Description: Status if method is active.

- **ChangeAt**  
    Type: DateTime (YYYYMMDDHHMMSS)  
    Cardinality: 1..1  
    Description: Timestamp of when changes occurred.

- **ChangeBy**  
    Type: Integer  
    Foreign Key: REFERENCES User(UserID)  
    Cardinality: 1..1  
    Description: User who changed settings.

### Relationships:

- remains to be specified


## Entity: FoodCategory  
List of possible classifications of the item, such as Drinks, Meals, Sauces, etc.

### Fields:

- **FoodCategoryID**  
    Type: Integer  
    Constraints: PRIMARY KEY (FoodCategoryID)  
    Cardinality: 1..1  
    Description: Unique ID for the food category.  

- **Name**  
    Type: String  
    Cardinality: 1..1  
    Description: Name of the food category.  

- **ChangeAt**  
    Type: DateTime (YYYYMMDDHHMMSS)  
    Cardinality: 0..1  
    Description: Timestamp of when the category was created or last updated.  

- **ChangeBy**  
    Type: Integer  
    Foreign Key: REFERENCES User(UserID)  
    Cardinality: 0..1  
    Description: User who created or changed the category.  

### Relationships:

- remains to be specified


## Entity: DayCategory  
List of possible time-based classifications such as Breakfast, Dinner, Festive, etc.

### Fields:

- **DayCategoryID**  
    Type: Integer  
    Constraints: PRIMARY KEY (DayCategoryID)  
    Cardinality: 1..1  
    Description: ID of the day category.  

- **Name**  
    Type: String  
    Constraints: 
    Cardinality: 1..1  
    Description: Name of the time classification (e.g., Breakfast, Dinner).  

- **StartAt**  
    Type: DateTime (HHMMSS 24h)  
    Cardinality: 1..1  
    Description: Start time for this category.  

- **EndsAt**  
    Type: DateTime (HHMMSS 24h)  
    Cardinality: 1..1  
    Description: End time for this category.  

- **ChangeAt**  
    Type: DateTime (YYYYMMDDHHMMSS)  
    Cardinality: 0..1  
    Description: Timestamp when the record was created or updated.  

- **ChangeBy**  
    Type: Integer  
    Foreign Key: REFERENCES User(UserID)  
    Cardinality: 0..1  
    Description: User who created or updated this category.  

### Relationships:

- remains to be specified


## Entity: Device  
Registered hardware device used in the system (e.g., kiosk, POS, fiscal printer).

### Fields:

- **DeviceID**  
    Type: Integer  
    Constraints: PRIMARY KEY (DeviceID)  
    Cardinality: 1..1  
    Description: Unique identifier for any device (KIOSK, POS, KKT, etc.)  

- **DeviceType**  
    Type: Enum ['KIOSK', 'POS_TERMINAL', 'FISCAL_PRINTER', 'KKT']  
    Cardinality: 1..1  
    Description: Type of device  

- **DeviceCode**  
    Type: String (unique, required, one)  
    Cardinality: 1..1  
    Description: Code like KIOSK-001, POS-002  

- **DeviceName**  
    Type: String  
    Cardinality: 1..1  
    Description: Human-readable name  

- **BranchID**  
    Type: Integer (FK to Branch, optional)  
    Cardinality: 0..1  
    Description: Physical branch assignment  

- **IPAddress**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: Last known IP address  

- **MACAddress**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: Hardware-level ID  

- **SerialNumber**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: Manufacturer serial number  

- **FirmwareVersion**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: Device firmware build  

- **DeviceOS**  
    Type: Enum (optional, one)  
    Cardinality: 0..1  
    Description: Operating system: linux, android, custom, etc.  

- **IsManaged**  
    Type: Boolean  
    Cardinality: 0..1  
    Description: Whether managed centrally or manually  

- **IsActive**  
    Type: Boolean  
    Cardinality: 0..1  
    Description: Whether currently active/usable  

- **LastHeartbeat**  
    Type: DateTime (optional, one)  
    Cardinality: 0..1  
    Description: Last time device pinged system  

- **RegisteredAt**  
    Type: DateTime  
    Cardinality: 0..1  
    Description: When device was registered  

- **RegisteredBy**  
    Type: Integer  
    Foreign Key: REFERENCES User(UserID)  
    Cardinality: 0..1  
    Description: Who registered the device  

### Relationships:

- remains to be specified


## Entity: POSTerminal  
POS terminal device linked to a physical hardware unit.

### Fields:

- **PosTerminalID**  
    Type: Integer  
    Constraints: PRIMARY KEY (PosTerminalID), FOREIGN KEY (PosTerminalID) REFERENCES Device(DeviceID)  
    Cardinality: 1..1  
    Description: Linked hardware device  

- **TerminalID**  
    Type: String  
    Cardinality: 1..1  
    Description: Bank-side terminal ID  

- **MerchantID**  
    Type: String  
    Cardinality: 0..1  
    Description: Merchant account ID  

- **BankName**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: Issuing/acquiring bank  

- **SupportedCardTypes**  
    Type: JSONB (optional, one)  
    Cardinality: 0..1  
    Description: List of supported cards ['visa', 'mir']  

- **MinAmount**  
    Type: Decimal (optional, one)  
    Cardinality: 0..1  
    Description: Min transaction amount  

- **MaxAmount**  
    Type: Decimal (optional, one)  
    Cardinality: 0..1  
    Description: Max transaction amount  

- **CommissionRate**  
    Type: Decimal (optional, one)  
    Cardinality: 0..1  
    Description: Commission % per payment  

### Relationships:

- remains to be specified


## Entity: FiscalDevice  
Fiscal printer device linked to a physical hardware unit.

### Fields:

- **FiscalDeviceID**  
    Type: Integer  
    Constraints: PRIMARY KEY (FiscalDeviceID), FOREIGN KEY (FiscalDeviceID) REFERENCES Device(DeviceID)  
    Cardinality: 1..1  
    Description: Linked device  

- **FiscalNumber**  
    Type: String  
    Cardinality: 1..1  
    Description: FN/registration number  

- **INN**  
    Type: String  
    Cardinality: 1..1  
    Description: Taxpayer INN  

- **FiscalMode**  
    Type: Enum ['OSN', 'USN', 'ENVD']  
    Cardinality: 0..1  
    Description: Fiscal regime used  

- **OFDProvider**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: Connected fiscal data operator  

- **CertificateExpiry**  
    Type: Date (optional, one)  
    Cardinality: 0..1  
    Description: Cert expiration date  

- **LastFiscalReport**  
    Type: DateTime (optional, one)  
    Cardinality: 0..1  
    Description: Last successfully sent report  

### Relationships:

- remains to be specified

## Entity:KioskConfiguration
How different devices bonded in one Kiosk

### Fields:

- **KioskID**  
  Type: Integer  
  Constraints: FOREIGN KEY (KioskID) REFERENCES Device(DeviceID)  
  Filter: WHERE DeviceType = 'KIOSK'  
  Cardinality: 0..1  
  Description: ID of the iPad or terminal acting as kiosk

- **PosTerminalID**  
  Type: Integer  
  Constraints: FOREIGN KEY (PosTerminalID) REFERENCES Device(DeviceID)  
  Filter: WHERE DeviceType = 'POS_TERMINAL'  
  Cardinality: 0..1  
  Description: Linked POS terminal device

- **FiscalDeviceID**  
  Type: Integer  
  Constraints: FOREIGN KEY (FiscalDeviceID) REFERENCES Device(DeviceID)  
  Filter: WHERE DeviceType = 'KKT'  
  Cardinality: 0..1  
  Description: Linked fiscal registration device (KKT)

- **PrinterID**  
  Type: Integer  
  Constraints: FOREIGN KEY (PrinterID) REFERENCES Device(DeviceID)  
  Filter: WHERE DeviceType = 'FISCAL_PRINTER'  
  Cardinality: 0..1  
  Description: Linked receipt/fiscal printer

- **IsActive**  
  Type: Boolean  
  Cardinality: 0..1  
  Description: Whether this configuration is active now

- **CreatedAt**  
  Type: DateTime  
  Cardinality: 0..1  
  Description: When this configuration was created

- **CreatedBy**  
  Type: Integer  
  Constraints: FOREIGN KEY (CreatedBy) REFERENCES User(UserID)  
  Cardinality: 0..1  
  Description: User who created the binding

### Relationships:

- remains to be specified


## Entity: DeviceAuth  
Authentication profile for a hardware device.

### Fields:

- **DeviceID**  
    Type: Integer  
    Constraints: FOREIGN KEY (DeviceID) REFERENCES Device(DeviceID)  
    Cardinality: 1..1  
    Description: Authentication profile  

- **AuthType**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: Type of authentication  

- **PublicKey**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: Public key (if applicable)  

- **PrivateKeyHash**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: Hash of private secret/token  

- **TokenHash**  
    Type: String (optional, one)  
    Cardinality: 0..1  
    Description: For API key-based auth  

- **ExpiresAt**  
    Type: DateTime (optional, one)  
    Cardinality: 0..1  
    Description: When this credential expires  

- **RevokedAt**  
    Type: DateTime (optional, one)  
    Cardinality: 0..1  
    Description: If revoked, the timestamp  

- **CreatedAt**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: When this auth was registered  

- **LastUsedAt**  
    Type: DateTime (optional, one)  
    Cardinality: 0..1  
    Description: Last time used (for audit/logging)  

### Relationships:

- remains to be specified


## Entity: OrderFSMKioskRuntime  
FSMKiosk runtime for order. Reflects real order’s way from payment to being picked-up.

### Fields:

- **OrderFSMKioskRuntimeID**  
    Type: UUID  
    Constraints: PRIMARY KEY (OrderFSMKioskRuntimeID)  
    Cardinality: 1..1  
    Description: FSMKiosk runtime for order  
    Relationships: remains to be specified  

- **OrderID**  
    Type: BIGSERIAL  
    Constraints: FOREIGN KEY(OrderID) REFERENCES TO Order(OrderID)  
    Cardinality: 1..1  
    Description: Reference to the associated order  
    Relationships: remains to be specified  

- **FSMKioskState**  
    Type: Enum  
    Values: INIT, AWAITING_PAYMENT, AWAITING_FISCALISATION, AWAITING_PRINTING, AWAITING_EXECUTION_CONFIRMATION, COMPLETED, UNSUCCESSFUL_PAYMENT, CANCELLED_BY_USER, CANCELLED_BY_TIMEOUT, UNSUCCESSFUL_FISCALIZATION, UNSUCCESSFUL_PRINTING_ALTERNATIVE_RECEIPT_DECLINED, CANCELLED_BY_ZERO_CULTURE, UNKNOWN_EXECUTION_NO_RESPONSE, PRINT_FAILED  
    Cardinality: 1..1  
    Description: Current FSMKiosk state  
    Relationships: remains to be specified  

- **FSMKioskVersion**  
    Type: String  
    Cardinality: 0..1  
    Description: Version of FSMKiosk logic  
    Relationships: remains to be specified  

- **PaymentSessionID**  
    Type: String  
    Cardinality: 0..1  
    Description: Session context for the FSMKiosk  
    Relationships: remains to be specified  

- **POSTerminalID**  
    Type: Integer  
    Constraints: FOREIGN KEY REFERENCES Device(DeviceID)  
    Cardinality: 1..1  
    Description: Which POS device was used  
    Relationships: remains to be specified  

- **PaymentAttemptStartedAt**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: When attempt to pay started  
    Relationships: remains to be specified  

- **PaymentAttemptResponseAt**  
    Type: DateTime  
    Cardinality: 0..1  
    Description: When response of payment-attempt got  
    Relationships: remains to be specified  

- **PaymentAttemptResultCode**  
    Type: String  
    Cardinality: 1..1  
    Description: Code of POS-terminal/iPad response/error  
    Relationships: remains to be specified  

- **PaymentAttemptResultDescription**  
    Type: JSONB  
    Cardinality: 0..1  
    Description: Description of POS-terminal/iPad response  
    Relationships: remains to be specified  

- **PaymentIDTransaction**  
    Type: String  
    Cardinality: 0..1  
    Description: Payment ID returned by POS terminal/iPad [RESERVED]  
    Relationships: remains to be specified  

- **PaymentSlipNumberID**  
    Type: String  
    Cardinality: 0..1  
    Description: ID returned by POS terminal/iPad  
    Relationships: remains to be specified  

- **FiscalSessionID**  
    Type: String  
    Cardinality: 0..1  
    Description: Session context for the FSMKiosk  
    Relationships: remains to be specified  

- **FiscalDeviceID**  
    Type: Integer  
    Constraints: FOREIGN KEY REFERENCES Device(DeviceID)  
    Cardinality: 1..1  
    Description: Which POS device was used  
    Relationships: remains to be specified  

- **FiscalAttemptStartedAt**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: When attempt to pay started  
    Relationships: remains to be specified  

- **FiscalAttemptResponseAt**  
    Type: DateTime  
    Cardinality: 0..1  
    Description: When response of payment-attempt got  
    Relationships: remains to be specified  

- **FiscalAttemptResultCode**  
    Type: String  
    Cardinality: 1..1  
    Description: Code of POS-terminal/iPad response/error  
    Relationships: remains to be specified  

- **FiscalAttemptResultDescription**  
    Type: JSONB  
    Cardinality: 0..1  
    Description: Description of POS-terminal/iPad response  
    Relationships: remains to be specified  

- **FiscalIDTransaction**  
    Type: String  
    Cardinality: 0..1  
    Description: Fiscal internal machine ID [reserved]  
    Relationships: remains to be specified  

- **FiscalisationNumberID**  
    Type: String  
    Cardinality: 0..1  
    Description: OFD ID  
    Relationships: remains to be specified  

- **PrintingSessionID**  
    Type: String  
    Cardinality: 0..1  
    Description: Session context for the FSMKiosk  
    Relationships: remains to be specified  

- **PrintingDeviceID**  
    Type: Integer  
    Constraints: FOREIGN KEY REFERENCES Device(DeviceID)  
    Cardinality: 1..1  
    Description: Which POS device was used  
    Relationships: remains to be specified  

- **PrintingAttemptStartedAt**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: When attempt to pay started  
    Relationships: remains to be specified  

- **PrintingAttemptResponseAt**  
    Type: DateTime  
    Cardinality: 0..1  
    Description: When response of payment-attempt got  
    Relationships: remains to be specified  

- **PrintingAttemptResultCode**  
    Type: String  
    Cardinality: 1..1  
    Description: Code of POS-terminal/iPad response/error  
    Relationships: remains to be specified  

- **PrintingAttemptResultDescription**  
    Type: JSONB  
    Cardinality: 0..1  
    Description: Description of POS-terminal/iPad response  
    Relationships: remains to be specified  

- **PickupCode**  
    Type: String  
    Cardinality: 0..1  
    Description: Code for order pickup  
    Relationships: remains to be specified  

- **PinCode**  
    Type: String  
    Cardinality: 0..1  
    Description: PIN code for order pickup  
    Relationships: remains to be specified  

- **QRCode**  
    Type: String  
    Cardinality: 0..1  
    Description: QR code for pickup or emergency cases when printer or screen doesn't work on device  
    Relationships: remains to be specified 

### Relationships:

- remains to be specified


## Entity: OrderLifecycleLog  
FSMKiosk audit log for orders. Logs every state transition during the lifetime of an order.

### Fields:

- **OrderLifecycleLogID**  
    Type: UUID  
    Constraints: PRIMARY KEY (OrderLifecycleLogID)  
    Cardinality: 1..1  
    Description: Unique transition log entry ID  
    Relationships: remains to be specified  

- **OrderID**  
    Type: BIGSERIAL  
    Constraints: FOREIGN KEY(OrderID) REFERENCES TO Order(OrderID)  
    Cardinality: 1..1  
    Description: Reference to the related order  
    Relationships: remains to be specified  

- **OrderFSMKioskRuntimeID**  
    Type: UUID  
    Constraints: FOREIGN KEY REFERENCES TO OrderFSMKioskRuntime(OrderFSMKioskRuntimeID)  
    Cardinality: 0..1  
    Description: Link to the FSMKiosk runtime record  
    Relationships: remains to be specified  

- **FromState**  
    Type: Enum  
    Values:  
    - INIT  
    - AWAITING_PAYMENT  
    - AWAITING_FISCALISATION  
    - AWAITING_PRINTING  
    - AWAITING_EXECUTION_CONFIRMATION  
    - COMPLETED  
    - UNSUCCESSFUL_PAYMENT  
    - CANCELLED_BY_USER  
    - CANCELLED_BY_TIMEOUT  
    - UNSUCCESSFUL_FISCALIZATION  
    - UNSUCCESSFUL_PRINTING_ALTERNATIVE_RECEIPT_DECLINED  
    - CANCELLED_BY_ZERO_CULTURE  
    - UNKNOWN_EXECUTION_NO_RESPONSE  
    - PRINT_FAILED  
    Cardinality: 0..1  
    Description: State before the transition  
    Relationships: remains to be specified  

- **ToState**  
    Type: Enum  
    Values:  
    - INIT  
    - AWAITING_PAYMENT  
    - AWAITING_FISCALISATION  
    - AWAITING_PRINTING  
    - AWAITING_EXECUTION_CONFIRMATION  
    - COMPLETED  
    - UNSUCCESSFUL_PAYMENT  
    - CANCELLED_BY_USER  
    - CANCELLED_BY_TIMEOUT  
    - UNSUCCESSFUL_FISCALIZATION  
    - UNSUCCESSFUL_PRINTING_ALTERNATIVE_RECEIPT_DECLINED  
    - CANCELLED_BY_ZERO_CULTURE  
    - UNKNOWN_EXECUTION_NO_RESPONSE  
    - PRINT_FAILED  
    Cardinality: 1..1  
    Description: New state after the transition  
    Relationships: remains to be specified  

- **TriggerEvent**  
    Type: Enum  
    Values:  
    - FSMKiosk_STARTED  
    - PAYMENT_SUCCEEDED  
    - PAYMENT_FAILED  
    - PAYMENT_RETRY  
    - USER_CANCELLED  
    - INACTIVITY_TIMEOUT  
    - FISCALIZATION_SUCCEEDED  
    - FISCALIZATION_FAILED  
    - FISCALIZATION_RETRY  
    - PRINT_SUCCEEDED  
    - PRINTING_FAILED_ALTERNATIVE_RECEIPT_ACCEPTED_BY_USER  
    - PRINTING_FAILED_ALTERNATIVE_RECEIPT_DECLINED_BY_USER  
    - PRINTING_FAILED_OR_TIMEOUT  
    - EXECUTION_CONFIRMED_BY_EXTERNAL_REASON_TO_CANCEL_BY_ZERO_CULTURE  
    - EXECUTION_CANCELED_BY_TIMEOUT  
    Cardinality: 1..1  
    Description: Event or action that caused the transition  
    Relationships: remains to be specified  

- **ActorType**  
    Type: Enum  
    Values:  
    - Customer (from state ‘ready to pay’)  
    - PosTerminal  
    - FiscalDevice  
    - Printer (FiscalPrinter)  
    - Kitchen (when customer picked up)  
    - Customer (when pick up)  
    - System  
    Cardinality: 0..1  
    Description: Who initiated the transition  
    Relationships: remains to be specified  

- **ActorID**  
    Type: String or Integer  
    Cardinality: 0..1  
    Description: ID of actor, e.g., device ID or user ID  
    Relationships: remains to be specified  

- **Comment**  
    Type: String  
    Cardinality: 0..1  
    Description: Optional context message  
    Relationships: remains to be specified  

- **EventCreatedAt**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: When this transition was recorded  
    Relationships: remains to be specified  

### Relationships:

- remains to be specified


## Entity: SlipReceipt  
Here we have all our slip-receipts (e.g., printed or generated by POS terminal).

### Fields:

- **SlipReceiptID**  
    Type: UUID  
    Constraints: PRIMARY KEY (SlipReceiptID)  
    Cardinality: 1..1  
    Description: ID  
    Relationships: remains to be specified  

- **OrderID**  
    Type: BIGSERIAL  
    Constraints: FOREIGN KEY (OrderID) REFERENCES TO Order(OrderID)  
    Cardinality: 0..1  
    Description: Linked order (if applicable)  
    Relationships: remains to be specified  

- **ReceiptPosTerminalReturnedID**  
    Type: String  
    Cardinality: 1..1  
    Description: Returned by device ID  
    Relationships: remains to be specified  

- **ReceiptBody**  
    Type: JSONB  
    Cardinality: 1..1  
    Description: What is inside (JSON content of the slip receipt)  
    Relationships: remains to be specified  

- **CreatedAt**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: When created  
    Relationships: remains to be specified  

- **CreatedBy**  
    Type: String  
    Cardinality: 0..0  
    Description: Who created  
    Relationships: remains to be specified

### Relationships:

- remains to be specified


## Entity: FiscalReceipt  
Here we have all our fiscal-receipts (e.g., receipts printed by fiscal printer).

### Fields:

- **FiscalReceiptID**  
    Type: UUID  
    Constraints: PRIMARY KEY (FiscalReceiptID)  
    Cardinality: 1..1  
    Description: ID  
    Relationships: remains to be specified  

- **OrderID**  
    Type: BIGSERIAL  
    Constraints: FOREIGN KEY (OrderID) REFERENCES TO ORDER(OrderID)  
    Cardinality: 0..1  
    Description: Linked order (if applicable)  
    Relationships: remains to be specified  

- **ReceiptFiscalMachineReturnedID**  
    Type: String  
    Cardinality: 1..1  
    Description: Returned by device ID  
    Relationships: remains to be specified  

- **ReceiptBody**  
    Type: JSONB  
    Cardinality: 1..1  
    Description: What is inside (fiscal receipt contents as JSON)  
    Relationships: remains to be specified  

- **CreatedAt**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: When created  
    Relationships: remains to be specified  

- **CreatedBy**  
    Type: String  
    Cardinality: 0..1  
    Description: Who created  
    Relationships: remains to be specified

### Relationships:

- remains to be specified


## Entity: SummaryReceipt  
Here we have our summary check — a logical combination of slip and fiscal receipts with pickup info.

### Fields:

- **SummaryReceiptID**  
    Type: UUID  
    Constraints: PRIMARY KEY (SummaryReceiptID)  
    Cardinality: 1..1  
    Description: Unique identifier of the summary check  
    Relationships: remains to be specified  

- **OrderID**  
    Type: BIGSERIAL  
    Constraints: FOREIGN KEY (OrderID) REFERENCES TO ORDER(OrderID)  
    Cardinality: 0..1  
    Description: Linked order  
    Relationships: remains to be specified  

- **SlipReceiptID**  
    Type: UUID  
    Constraints: FOREIGN KEY (SlipReceiptID) REFERENCES SlipReceipt(SlipReceiptID)  
    Cardinality: 1..1  
    Description: Link to slip  
    Relationships: remains to be specified  

- **FiscalReceiptID**  
    Type: UUID  
    Constraints: FOREIGN KEY (FiscalReceiptID) REFERENCES FiscalReceipt(FiscalReceiptID)  
    Cardinality: 1..1  
    Description: Link to fiscal  
    Relationships: remains to be specified  

- **PickupCode**  
    Type: String  
    Cardinality: 1..1  
    Description: Pickup code for customer  
    Relationships: remains to be specified  

- **PinCode**  
    Type: String  
    Cardinality: 1..1  
    Description: PIN code for customer  
    Relationships: remains to be specified  

- **CreatedAt**  
    Type: DateTime  
    Cardinality: 1..1  
    Description: When created  
    Relationships: remains to be specified  

- **CreatedBy**  
    Type: String  
    Cardinality: 0..1  
    Description: Who created  
    Relationships: remains to be specified

### Relationships:

- remains to be specified


