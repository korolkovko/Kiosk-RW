# FSMKiosk State Transitions Documentation

**Source:** 
**Format:** State-Centric (organized by FROM_STATE)  
**Total Transitions:** 16

---

## STATE: INIT

**STATE DESCRIPTION:** Starting state of the FSM

**OUTGOING TRANSITIONS FROM THIS STATE:**

### TRANSITION 1: INIT → AWAITING_PAYMENT
- **ON_EVENT:** FSM_STARTED
- **WHO (Trigger):** User/Client
- **TIMEOUT:** (none)
- **TERMINAL STATE:** No
- **COMMENT KIOSK:** System initiated FSM when User pushes Pay button
- **COMMENT WEB-SITE AND APP:** Same

---

## STATE: AWAITING_PAYMENT

**STATE DESCRIPTION:** Waiting for payment completion via POS terminal

**OUTGOING TRANSITIONS FROM THIS STATE:**

### TRANSITION 2: AWAITING_PAYMENT → AWAITING_FISCALIZATION
- **ON_EVENT:** PAYMENT_SUCCEEDED
- **WHO (Trigger):** ExternalDevice (POS/System
- **TIMEOUT:** (none)
- **TERMINAL STATE:** No
- **COMMENT KIOSK:** User completed payment on POS. Pos terminal has sent success confirmation. System moves FSM record to the next State
- **COMMENT WEB-SITE AND APP:** Same

### TRANSITION 3: AWAITING_PAYMENT → UNSUCCESSFUL_PAYMENT
- **ON_EVENT:** PAYMENT_FAILED
- **WHO (Trigger):** ExternalDevice (POS/System
- **TIMEOUT:** 30s
- **TERMINAL STATE:** Terminal
- **COMMENT KIOSK:** User tried to pay, system failed or no response 30 sec. E.g. pos terminal has sent an error or hast responded more than 30sec  
ATTENTION WE HAVE TO CHECK POS TERMINAL TIMEOUT FOR USER TO PAY
- **COMMENT WEB-SITE AND APP:** Same

### TRANSITION 4: AWAITING_PAYMENT → CANCELLED_BY_USER
- **ON_EVENT:** USER_CANCELLED
- **WHO (Trigger):** User
- **TIMEOUT:** (none)
- **TERMINAL STATE:** Terminal
- **COMMENT KIOSK:** User pressed cancel button
- **COMMENT WEB-SITE AND APP:** Same

### TRANSITION 5: AWAITING_PAYMENT → CANCELLED_BY_TIMEOUT
- **ON_EVENT:** INACTIVITY_TIMEOUT
- **WHO (Trigger):** System
- **TIMEOUT:** 30s
- **TERMINAL STATE:** Terminal
- **COMMENT KIOSK:** User left, no action taken
- **COMMENT WEB-SITE AND APP:** Same

### TRANSITION 6: AWAITING_PAYMENT → AWAITING_PAYMENT (self-loop)
- **ON_EVENT:** PAYMENT_RETRY
- **WHO (Trigger):** ExternalDevice (POS/System
- **TIMEOUT:** (none)
- **TERMINAL STATE:** No
- **COMMENT KIOSK:** System retries POS on recoverable failure  
ONLY If first Attempt returns an error kinda "no-connection" (means with Bank-host) or "unknown error" then System proceeds and offers the second attempt to User/Client. If we have the same result after the second attempt then FMS record gets moved to UNSUCCESSFUL_PAYMENT state by System
- **COMMENT WEB-SITE AND APP:** By this time the Order is created - we can show it to user/client at any moment

---

## STATE: AWAITING_FISCALIZATION

**STATE DESCRIPTION:** Waiting for fiscal receipt generation via KKT device

**OUTGOING TRANSITIONS FROM THIS STATE:**

### TRANSITION 7: AWAITING_FISCALIZATION → AWAITING_PRINTING
- **ON_EVENT:** FISCALIZATION_SUCCEEDED
- **WHO (Trigger):** ExternalDevice (KKT)
- **TIMEOUT:** (none)
- **TERMINAL STATE:** No
- **COMMENT KIOSK:** KKT completed fiscal receipt
- **COMMENT WEB-SITE AND APP:** Same

### TRANSITION 8: AWAITING_FISCALIZATION → UNSUCCESSFUL_FISCALIZATION
- **ON_EVENT:** FISCALIZATION_FAILED
- **WHO (Trigger):** ExternalDevice (KKT)
- **TIMEOUT:** (none)
- **TERMINAL STATE:** Terminal
- **COMMENT KIOSK:** System failed to fiscalize, admin intervention may be required
- **COMMENT WEB-SITE AND APP:** Same

### TRANSITION 9: AWAITING_FISCALIZATION → AWAITING_FISCALIZATION (self-loop)
- **ON_EVENT:** FISCALIZATION_RETRY
- **WHO (Trigger):** System
- **TIMEOUT:** 20s
- **TERMINAL STATE:** No
- **COMMENT KIOSK:** System retries fiscalization on recoverable failure (we don't know such recoverable Failures yet)
- **COMMENT WEB-SITE AND APP:** Same

---

## STATE: AWAITING_PRINTING

**STATE DESCRIPTION:** Waiting for receipt printing completion

**OUTGOING TRANSITIONS FROM THIS STATE:**

### TRANSITION 10: AWAITING_PRINTING → AWAITING_EXECUTION_CONFIRMATION
- **ON_EVENT:** PRINT_SUCCEEDED
- **WHO (Trigger):** ExternalDevice (Printer)
- **TIMEOUT:** (none)
- **TERMINAL STATE:** No
- **COMMENT KIOSK:** Receipt printed successfully
- **COMMENT WEB-SITE AND APP:** Receipt sent successfully  
Will be other flow

### TRANSITION 13: AWAITING_PRINTING → PRINT_FAILED
- **ON_EVENT:** PRINTING_FAILED_OR_TIMEOUT
- **WHO (Trigger):** ExternalDevice (Printer)/Sustem
- **TIMEOUT:** 20s
- **TERMINAL STATE:** No
- **COMMENT KIOSK:** Printer returned error or no messages from printer 20 sec - in this case we offer alternative way to get all info to client - QR code on screen and all info on screen - if yes accepted - we proceed, otherwise - FSM gets moved to UNSUCCESSFUL_PRINTING_ALTERNATIVE_RECEIPT_DECLINED state
- **COMMENT WEB-SITE AND APP:** Will be other flow

---

## STATE: PRINT_FAILED

**STATE DESCRIPTION:** Printer failed, awaiting user decision on alternative receipt

**OUTGOING TRANSITIONS FROM THIS STATE:**

### TRANSITION 11: PRINT_FAILED → AWAITING_EXECUTION_CONFIRMATION
- **ON_EVENT:** PRINTING_FAILED_ALTERNATIVE_RECEIPT_ACCEPTED_BY_USER
- **WHO (Trigger):** User
- **TIMEOUT:** (none)
- **TERMINAL STATE:** No
- **COMMENT KIOSK:** User confirmed receiving code on screen instead of paper receipt
- **COMMENT WEB-SITE AND APP:** Will be other flow

### TRANSITION 12: PRINT_FAILED → UNSUCCESSFUL_PRINTING_ALTERNATIVE_RECEIPT_DECLINED
- **ON_EVENT:** PRINTING_FAILED_ALTERNATIVE_RECEIPT_DECLINED_BY_USER
- **WHO (Trigger):** User
- **TIMEOUT:** 20s
- **TERMINAL STATE:** Terminal
- **COMMENT KIOSK:** User declined fallback after printer failure or User didn't react 20 sec. admin needed or we have no message from Frontend more than 20 sec
- **COMMENT WEB-SITE AND APP:** Will be other flow

---

## STATE: AWAITING_EXECUTION_CONFIRMATION

**STATE DESCRIPTION:** Waiting for kitchen/staff confirmation of order completion

**OUTGOING TRANSITIONS FROM THIS STATE:**

### TRANSITION 14: AWAITING_EXECUTION_CONFIRMATION → COMPLETED
- **ON_EVENT:** EXECUTION_CONFIRMED_BY_EXTERNAL
- **WHO (Trigger):** ExternalSystem
- **TIMEOUT:** (none)
- **TERMINAL STATE:** Terminal
- **COMMENT KIOSK:** Kitchen or staff system confirmed completion
- **COMMENT WEB-SITE AND APP:** Will be other flow

### TRANSITION 15: AWAITING_EXECUTION_CONFIRMATION → CANCELLED_BY_ZERO_CULTURE
- **ON_EVENT:** REASON_TO_CANCEL_BY_ZERO_CULTURE
- **WHO (Trigger):** System/Admin
- **TIMEOUT:** (none)
- **TERMINAL STATE:** Terminal
- **COMMENT KIOSK:** Forced stop of execution by business rule/needs
- **COMMENT WEB-SITE AND APP:** Will be other flow

### TRANSITION 16: AWAITING_EXECUTION_CONFIRMATION → UNKNOWN_EXECUTION_NO_RESPONSE
- **ON_EVENT:** EXECUTION_CANCELED_BY_TIMEOUT
- **WHO (Trigger):** System
- **TIMEOUT:** 3h
- **TERMINAL STATE:** Terminal
- **COMMENT KIOSK:** No response from kitchen, Kitchen did not respond within 3h, fallback notification sent to admin (optional), system closes order automatically
- **COMMENT WEB-SITE AND APP:** Will be other flow

---

## TERMINAL STATES LIST

The following states are marked as "Terminal" - FSM execution ends at these states:

- UNSUCCESSFUL_PAYMENT
- CANCELLED_BY_USER
- CANCELLED_BY_TIMEOUT
- UNSUCCESSFUL_FISCALIZATION
- UNSUCCESSFUL_PRINTING_ALTERNATIVE_RECEIPT_DECLINED
- COMPLETED
- CANCELLED_BY_ZERO_CULTURE
- UNKNOWN_EXECUTION_NO_RESPONSE

---

## STATES WITH TIMEOUTS

States that have timeout-driven transitions:

- AWAITING_PAYMENT: 30s timeout for PAYMENT_FAILED and INACTIVITY_TIMEOUT
- AWAITING_FISCALIZATION: 20s timeout for FISCALIZATION_RETRY
- AWAITING_PRINTING: 20s timeout for PRINTING_FAILED_OR_TIMEOUT
- PRINT_FAILED: 20s timeout for alternative receipt declined
- AWAITING_EXECUTION_CONFIRMATION: 3h timeout for EXECUTION_CANCELED_BY_TIMEOUT

---

## SELF-LOOP TRANSITIONS (RETRY MECHANISMS)

States that can transition to themselves:

- AWAITING_PAYMENT → AWAITING_PAYMENT (PAYMENT_RETRY event)
- AWAITING_FISCALIZATION → AWAITING_FISCALIZATION (FISCALIZATION_RETRY event)

---

**NOTE:** All data in this document corresponds exactly to FSM_Transition_Table.xlsx with no additions or modifications.