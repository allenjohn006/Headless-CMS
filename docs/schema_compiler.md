# Dynamic Schema Compiler & Validation

This document describes how the dynamic schema validation engine works under the hood inside `backend/app/services/schema_compiler.py`.

---

## 🧐 The Challenge
In a typical web application, database columns and validation models (like Pydantic) are hardcoded at compile time. In a **Headless CMS**, users expect to change fields (e.g. adding a new field like `"price"` of type `"Number"`, setting it as `is_required=True` or defining `min_value: 0`) at runtime.

The CMS needs a **Schema Compiler** capable of looking up dynamically defined structure mappings in the database and executing strict type and validation checking on any incoming JSON payloads before saving them.

---

## ⚙️ How it Works

```
 1. Editor issues POST /api/v1/content/products
               |
               v
 2. Look up the Collection "products" ID in DB
               |
               v
 3. Query all Field records belonging to Collection ID
               |
               v
 4. Run `validate_content_schema(db, collection_id, payload)`
               |
       +-------+-------+
       |               |
       v               v
 [Errors Found?]  [Valid Payload]
       |               |
       v               v
  Reject with 400   Save JSON inside `contents`
  and list errors   table & return 201 Created
```

---

## 🛠️ The Validation Rules

The compiler validates incoming JSON dynamically against these constraints:

### 1. Missing Required Fields
- Checks if a field with `is_required=True` is missing (`None` or omitted completely) from the payload.
- **Action**: Appends a specific required field validation error.

### 2. DataType Checking
Checks if the passed datatype matches the stored validation schema rules.

| Dynamic Field Type | Expected JSON/Python Type | Rejected Types |
| :--- | :--- | :--- |
| **Text** | `str` | `int`, `float`, `bool`, `dict` |
| **Number** | `int` or `float` | `str`, `bool`, `dict` |
| **Boolean** | `bool` | `str` (even `"true"`), `int` (even `1`) |

### 3. Custom Schema Validation Dicts
Within each `fields` table, there is a `validations` dynamic JSON column that stores advanced constraints. The compiler evaluates:

#### A. Strings (`min_length` & `max_length`)
- Checks if `len(str_value) < validations["min_length"]`
- Checks if `len(str_value) > validations["max_length"]`

#### B. Extra Keys Control
- Any keys in the client's payload that do not correspond to the collection's registered fields are immediately flagged and rejected with the error message `"Field is not defined in the schema."`
- This prevents editors from polluting dynamic database records with garbage JSON properties.

---

## 📊 Error Output Format
If validation fails, the API returns a structured `400 Bad Request` payload outlining exactly which fields failed validation and why:

```json
{
  "detail": {
    "errors": [
      {
        "field": "title",
        "message": "This field is required."
      },
      {
        "field": "price",
        "message": "Must be a number."
      },
      {
        "field": "secret_field",
        "message": "Field is not defined in the schema."
      }
    ]
  }
}
```
This precise payload enables the **Content Studio UI** to dynamically highlight the form inputs on the UI screen and display real-time validation error alerts to editors!
